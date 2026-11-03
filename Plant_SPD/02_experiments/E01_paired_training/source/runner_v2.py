"""Finite paired raw-versus-log SPD prototype training, version 2.

One shared official ResNet18 layer3 encoder processes two fixed RGB views.
The only paired-method differences are the covariance distance map and its
precomputed TRAIN-only units scale. All state tensors, samples, horizontal flips,
optimization budgets and checkpoint selection are otherwise common.
No mask, old VAL/test/final access, adaptive retry, early stopping or best-epoch
selection is implemented. External ImageNet pretraining is not zero cost.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import random
import threading
import time
import datetime

# Must be configured before any CUDA context is created.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

EPS = 1e-4
SHRINKAGE = .05
PROJECTION_SEED = 3407
OFFICIAL_WEIGHTS_SHA256 = "f37072fd47e89c5e827621c5baffa7500819f7896bbacec160b1a16c560e07ec"
CHECKPOINT_SELECTION = "FINAL_FIXED_EPOCH_20_NOT_HELD_BEST"


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(8 << 20), b""):
            h.update(b)
    return h.hexdigest()


def array_sha(a):
    a = np.ascontiguousarray(a)
    return hashlib.sha256(str(a.dtype).encode() + str(a.shape).encode() + a.tobytes()).hexdigest()


def state_digest(model):
    h = hashlib.sha256()
    for name, value in sorted(model.state_dict().items()):
        a = value.detach().cpu().contiguous().numpy()
        h.update(name.encode()); h.update(str(a.dtype).encode())
        h.update(str(a.shape).encode()); h.update(a.tobytes())
    return h.hexdigest()


def json_write(path, value, exclusive=False):
    path = Path(path)
    mode = "x" if exclusive else "w"
    # Updating progress is atomic. Immutable scientific outputs use exclusive=True.
    if exclusive:
        with open(path, mode, encoding="utf8") as f:
            json.dump(value, f, indent=2, allow_nan=False)
    else:
        tmp = path.with_name(path.name + ".tmp")
        with open(tmp, "w", encoding="utf8") as f:
            json.dump(value, f, indent=2, allow_nan=False)
        os.replace(tmp, path)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def projection_qr(seed=PROJECTION_SEED):
    q, r = np.linalg.qr(np.random.default_rng(int(seed)).standard_normal((256, 32)), mode="reduced")
    q = q * np.where(np.diag(r) >= 0, 1., -1.)[None, :]
    if np.max(abs(q.T @ q - np.eye(32))) > 1e-12:
        raise AssertionError("Fixed QR projection is not orthonormal")
    return q.astype(np.float32)


class _StableLogm(torch.autograd.Function):
    """Symmetric matrix log with exact repeated-spectrum Loewner limit.

    Float64 eigendecomposition and analytic symmetric Frechet derivative.
    No adaptive jitter, eigenvalue clipping, detach-through-eigensolver or
    eigenvector-gradient denominator is used.
    """
    @staticmethod
    def forward(ctx, a):
        if a.shape[-1] != a.shape[-2]:
            raise ValueError("Square SPD matrices required")
        aa = (a.double() + a.double().transpose(-1, -2)) * .5
        w, q = torch.linalg.eigh(aa)
        if not bool(torch.isfinite(w).all()) or not bool((w > 0).all()):
            raise FloatingPointError("Matrix log requires finite strictly-positive eigenvalues")
        ctx.save_for_backward(w, q)
        ctx.input_dtype = a.dtype
        return ((q * torch.log(w).unsqueeze(-2)) @ q.transpose(-1, -2)).to(a.dtype)

    @staticmethod
    def backward(ctx, grad_output):
        w, q = ctx.saved_tensors
        grad = (grad_output.double() + grad_output.double().transpose(-1, -2)) * .5
        wi, wj = w.unsqueeze(-1), w.unsqueeze(-2)
        delta = wi - wj
        near = delta.abs() <= 1e-6 * torch.maximum(wi, wj)
        safe_delta = torch.where(near, torch.ones_like(delta), delta)
        # log1p is stable for nearby values; repeated/near-repeated eigenvalues
        # use the analytic reciprocal-mean limit (relative truncation O(1e-12)).
        ratio = torch.log1p(delta / wj) / safe_delta
        loewner = torch.where(near, 2. / (wi + wj), ratio)
        rotated = q.transpose(-1, -2) @ grad @ q
        result = q @ (loewner * rotated) @ q.transpose(-1, -2)
        result = (result + result.transpose(-1, -2)) * .5
        return result.to(ctx.input_dtype)


def stable_logm(a):
    return _StableLogm.apply(a)


def set_train_frozen_bn(model):
    """Train affine/encoder parameters while freezing pretrained BN statistics."""
    model.train()
    for module in model.modules():
        if isinstance(module, nn.modules.batchnorm._BatchNorm):
            module.eval()
    return model


class Layer3Encoder(nn.Module):
    def __init__(self, official):
        super().__init__()
        # Only modules on the actual feature path are retained. No unused layer4/fc.
        for name in ("conv1", "bn1", "relu", "maxpool", "layer1", "layer2", "layer3"):
            setattr(self, name, getattr(official, name))

    def forward_features(self, x):
        x = self.maxpool(self.relu(self.bn1(self.conv1(x))))
        x = self.layer1(x)
        x = self.layer2(x)
        return self.layer3(x)

    def forward(self, x):
        return self.forward_features(x)


class PairedGeometryModel(nn.Module):
    def __init__(self, encoder, prototype_factors, scales_raw, scales_log,
                 method="raw", projection=None):
        super().__init__()
        if method not in ("raw", "log"):
            raise ValueError("Only the preregistered raw/log paired methods exist")
        pf = torch.as_tensor(prototype_factors, dtype=torch.float32)
        if pf.ndim != 4 or pf.shape[0] != 2 or tuple(pf.shape[-2:]) != (32, 32):
            raise ValueError("prototype_factors must be [2view,C,32,32]")
        scales = torch.stack([torch.as_tensor(scales_raw, dtype=torch.float32),
                              torch.as_tensor(scales_log, dtype=torch.float32)])
        if scales.shape != (2, 2) or not bool(torch.isfinite(scales).all()) or not bool((scales > 0).all()):
            raise ValueError("Positive finite fixed TRAIN raw/log scale per view required")
        self.encoder = encoder
        self.prototype_factors = nn.Parameter(pf.clone())
        self.log_temperature = nn.Parameter(torch.zeros((), dtype=torch.float32))

        # Both methods store BOTH unit scales so their complete initial state_dict
        # can be byte-identical. The method selector is a plain non-state attribute.
        self.register_buffer("distance_scales", scales.clone())
        qq = projection_qr() if projection is None else projection
        qq = torch.as_tensor(qq, dtype=torch.float32)
        if qq.shape != (256, 32):
            raise ValueError("Projection must be [256,32]")
        self.register_buffer("projection", qq.clone())
        self.register_buffer("identity", torch.eye(32, dtype=torch.float32))
        self.method = method
        self.n_classes = int(pf.shape[1])

    def forward(self, x):
        if x.ndim != 5 or x.shape[1:3] != (2, 3):
            raise ValueError("Input requires [B,2view,3,H,W] normalized RGB")
        b = len(x)
        fmap = self.encoder.forward_features(x.reshape(b * 2, 3, *x.shape[-2:]))
        if fmap.ndim != 4 or fmap.shape[1] != 256:
            raise ValueError("Shared encoder must produce [B*2,256,Hf,Wf]")
        tokens = fmap.flatten(2).transpose(1, 2) @ self.projection
        n = tokens.shape[1]
        if n < 2:
            raise ValueError("At least two spatial tokens required")
        centered = tokens - tokens.mean(1, keepdim=True)
        sample_cov = centered.transpose(-1, -2) @ centered / (n - 1)
        trace = sample_cov.diagonal(dim1=-2, dim2=-1).sum(-1) / 32
        covariance = ((1. - SHRINKAGE) * sample_cov +
                      SHRINKAGE * trace[:, None, None] * self.identity +
                      EPS * self.identity).reshape(b, 2, 32, 32)
        prototype_cov = self.prototype_factors @ self.prototype_factors.transpose(-1, -2) + EPS * self.identity
        if self.method == "log":
            mapped_cov, mapped_proto = stable_logm(covariance), stable_logm(prototype_cov)
            scale = self.distance_scales[1]
        else:
            mapped_cov, mapped_proto = covariance, prototype_cov
            scale = self.distance_scales[0]
        # Direct squared differences avoid cancellation in norm-dot expansion.
        distances = ((mapped_cov[:, :, None] - mapped_proto[None]) ** 2).sum((-2, -1))
        branch_logits = -distances / scale[None, :, None] / self.log_temperature.exp()
        dual_logits = branch_logits.mean(1)
        return {"dual_logits": dual_logits, "branch_logits": branch_logits,
                "covariance": covariance, "prototype_covariance": prototype_cov,
                "distances": distances}


def model_loss(output, labels):
    dual = F.cross_entropy(output["dual_logits"], labels)
    view0 = F.cross_entropy(output["branch_logits"][:, 0], labels)
    view1 = F.cross_entropy(output["branch_logits"][:, 1], labels)
    total = dual + .25 * (view0 + view1)
    return total, {"ce_dual": dual, "ce_view0": view0, "ce_view1": view1, "total": total}


def build_model(backbone_source_path, weights_path, expected_source_sha256,
                expected_weights_sha256, prototype_factors, scales_raw, scales_log,
                method="raw", seed=3407):
    if sha_file(backbone_source_path) != expected_source_sha256:
        raise ValueError("Official adapter source hash mismatch")
    if sha_file(weights_path) != expected_weights_sha256:
        raise ValueError("Official pretrained checkpoint hash mismatch")
    torch.manual_seed(int(seed))
    spec = importlib.util.spec_from_file_location("paired_official_resnet18", backbone_source_path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    official = module.build_resnet18(weights_path, expected_sha256=expected_weights_sha256, frozen=False)
    return PairedGeometryModel(Layer3Encoder(official), prototype_factors, scales_raw,
                               scales_log, method=method)


def classification_metrics(y, pred, n_classes=69):
    y, pred = np.asarray(y, np.int64), np.asarray(pred, np.int64)
    if y.shape != pred.shape or not len(y):
        raise ValueError("Aligned nonempty labels/predictions required")
    if np.any((y < 0) | (y >= n_classes) | (pred < 0) | (pred >= n_classes)):
        raise ValueError("Class outside the original mapping")
    cm = np.bincount(y*n_classes + pred, minlength=n_classes*n_classes).reshape(n_classes, n_classes)
    tp = np.diag(cm).astype(np.float64)
    denom = cm.sum(0) + cm.sum(1)
    f1 = np.divide(2*tp, denom, out=np.zeros(n_classes), where=denom > 0)
    support = cm.sum(1)
    recall = np.divide(tp, support, out=np.zeros(n_classes), where=support > 0)
    return {"accuracy": float(np.mean(y == pred)), "macro_f1_fixed": float(f1.mean()),
            "balanced_accuracy_present": float(recall[support > 0].mean()),
            "n": int(len(y)), "n_classes_present": int(np.count_nonzero(support)),
            "class_support": support.tolist()}


def normalized_batch(x_uint8, indices, device, flips=None):
    xx = torch.from_numpy(np.array(x_uint8[np.asarray(indices)], dtype=np.uint8, copy=True)).to(device=device, dtype=torch.float32)
    if flips is not None:
        flags = torch.as_tensor(np.asarray(flips), dtype=torch.bool, device=device)
        if flags.shape != (len(xx),):
            raise ValueError("One same-view horizontal flip flag per pair required")
        if bool(flags.any()):
            xx[flags] = torch.flip(xx[flags], dims=(-1,))
    xx = xx / 255.
    mean = xx.new_tensor((.485, .456, .406)).view(1, 1, 3, 1, 1)
    std = xx.new_tensor((.229, .224, .225)).view(1, 1, 3, 1, 1)
    return (xx - mean) / std


@torch.no_grad()
def evaluate(model, x_uint8, labels, indices, device="cpu", batch_size=32, deadline=None):
    modes = [(m, m.training) for m in model.modules()]
    model.eval()
    indices = np.asarray(indices, np.int64)
    probs = np.empty((len(indices), model.n_classes), np.float32)
    losses = np.zeros(4, np.float64); logits_moments = []
    try:
        for start in range(0, len(indices), batch_size):
            if deadline is not None and time.monotonic() >= deadline:
                raise TimeoutError("Fixed run deadline during evaluation")
            ii = indices[start:start+batch_size]
            out = model(normalized_batch(x_uint8, ii, device))
            yy = torch.as_tensor(np.asarray(labels)[ii], dtype=torch.long, device=device)
            _, ll = model_loss(out, yy)
            losses += np.array([float(ll[k]) for k in ("ce_dual", "ce_view0", "ce_view1", "total")]) * len(ii)

            probs[start:start+len(ii)] = out["dual_logits"].softmax(-1).cpu().numpy()
            z = out["branch_logits"]
            ent = -(z.softmax(-1) * z.log_softmax(-1)).sum(-1)
            logits_moments.append([float(z.std(unbiased=False)), float(z.min()), float(z.max()), float(ent.mean())])
        metrics = classification_metrics(np.asarray(labels)[indices], probs.argmax(-1), model.n_classes)
        metrics.update(dict(zip(("ce_dual", "ce_view0", "ce_view1", "total_loss"), (losses/len(indices)).tolist())))
        metrics["logit_batch_stats_mean_std_min_max_entropy"] = np.mean(logits_moments, axis=0).tolist()
        return {"metrics": metrics, "probabilities": probs, "indices": indices.copy()}
    finally:
        # Preserve each submodule's state, including independently frozen BN flags.
        for module, mode in modes:
            module.training = mode


def gradient_summary(model):
    groups = {"encoder": [], "prototype": [], "temperature": []}
    missing = []
    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        if param.grad is None:
            missing.append(name); continue
        grad = param.grad.detach()
        if not bool(torch.isfinite(grad).all()):
            raise FloatingPointError("Nonfinite gradient: " + name)
        group = "encoder" if name.startswith("encoder.") else "prototype" if name == "prototype_factors" else "temperature"
        groups[group].append(float(torch.sum(grad.double() ** 2)))
    if missing:
        raise FloatingPointError("Missing trainable-parameter gradients: " + ",".join(missing))
    return {key+"_grad_norm": math.sqrt(sum(values)) for key, values in groups.items()}


def make_optimizer(model):
    encoder = list(model.encoder.parameters())
    heads = [model.prototype_factors, model.log_temperature]
    return torch.optim.AdamW([{"params": encoder, "lr": 1e-4, "name": "encoder"},
                              {"params": heads, "lr": 1e-3, "name": "head"}],
                             weight_decay=1e-4)


def configure_runtime(seed, threads=4):
    torch.set_num_threads(int(threads))
    random.seed(int(seed)); np.random.seed(int(seed)); torch.manual_seed(int(seed))
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(int(seed))
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.use_deterministic_algorithms(True)



def initialize_cuda_device():
    """Create the selected CUDA context before touching its allocator statistics."""
    torch.cuda.init()
    torch.cuda.set_device(0)
    torch.cuda.reset_peak_memory_stats(0)
    return torch.device("cuda:0")


def load_bound_inputs(p):
    for key in ("input_x", "input_meta", "splits", "streams", "init", "backbone_source", "weights"):
        if sha_file(p[key+"_path"]) != p[key+"_sha256"]:
            raise ValueError("Bound input hash mismatch: " + key)
    x = np.load(p["input_x_path"], allow_pickle=False, mmap_mode="r")
    if x.shape != (5230, 2, 3, 224, 224) or x.dtype != np.uint8:
        raise ValueError("Fixed original TRAIN staged two-view RGB payload differs")
    # Full RAM snapshot prevents repeated disk I/O and permits stable finite runs.
    x = np.array(x, copy=True)
    with np.load(p["input_meta_path"], allow_pickle=False) as z:
        meta = {k:z[k] for k in z.files}
    with np.load(p["splits_path"], allow_pickle=False) as z:
        splits = {k:z[k] for k in z.files}
    with np.load(p["streams_path"], allow_pickle=False) as z:
        streams = {k:z[k] for k in z.files}
    with np.load(p["init_path"], allow_pickle=False) as z:
        init = {k:z[k] for k in z.files}
    for key in ("labels", "names"):
        if not np.array_equal(meta[key], splits[key]):
            raise ValueError("Ordered metadata/split identity mismatch: "+key)
    if meta["labels"].dtype != np.int64 or meta["labels"].shape != (5230,) or len(set(meta["names"].tolist())) != 5230:
        raise ValueError("Original69 integer labels and unique5230 row names required")
    if splits["fit_mask"].shape != (2,5230) or splits["held_mask"].shape != (2,5230) or splits["fit_mask"].dtype != np.bool_ or splits["held_mask"].dtype != np.bool_:
        raise ValueError("Fixed boolean partition mask schema differs")
    if set(meta["role"].tolist()) != {"train_pool"} or len(meta["labels"]) != 5230:
        raise ValueError("Only original TRAIN_POOL accepted")
    pid, seed = int(p["partition_id"]), int(p["training_seed"])
    fit = np.flatnonzero(splits["fit_mask"][pid]); held = np.flatnonzero(splits["held_mask"][pid])
    if len(np.intersect1d(fit, held)) or len(fit)+len(held)!=5230:
        raise ValueError("Invalid fit/held complement")
    for group in np.unique(splits["group_ids"]):
        rows = splits["group_ids"] == group
        if len(np.unique(splits["fit_mask"][pid][rows])) != 1:
            raise ValueError("Known group leaks across fit/held")
    rows = np.flatnonzero((streams["partition_ids"] == pid) & (streams["training_seeds"] == seed))
    if len(rows) != 1:
        raise ValueError("No unique fixed stream row")
    row = int(rows[0]); nfit = int(streams["lengths"][row])
    order = streams["sample_indices"][row, :, :nfit]
    flips = streams["hflip"][row, :, :nfit]
    if order.shape != (20, len(fit)) or flips.shape != order.shape or flips.dtype != np.bool_:
        raise ValueError("Fixed20epoch order/flip schema mismatch")
    for epoch in range(20):
        if not np.array_equal(np.sort(order[epoch]), fit):
            raise ValueError("Epoch stream is not one complete fit permutation")
    if not np.all(streams["sample_indices"][row, :, nfit:] == -1):
        raise ValueError("Stream padding must be -1")
    if init["prototype_factors"].shape != (2,69,32,32) or init["scales_raw"].shape != (2,) or init["scales_log"].shape != (2,):
        raise ValueError("Fixed class prototype/scale initialization schema differs")
    for key, expected in (("partition_id",pid),("training_seed",seed),("projection_seed",3407)):
        if key not in init or np.asarray(init[key]).shape != () or int(init[key]) != expected:
            raise ValueError("INIT identity metadata mismatch: "+key)
    if len(np.unique(meta["labels"][fit])) != 69 or len(np.unique(meta["labels"][held])) != 69:
        raise ValueError("Fit/held class support incomplete")
    return x, meta, splits, init, fit, held, order, flips


def validate_protocol(p, mode):
    if p.get("runner_sha256") != sha_file(__file__):
        raise ValueError("Runner source hash mismatch")
    if mode not in ("train", "smoke"):
        raise ValueError("Unsupported actual run mode")
    fixed = {"n_images":5230, "n_classes":69, "epochs":20, "batch_size":32,
             "projection_seed":3407, "threads":4, "encoder_lr":1e-4, "head_lr":1e-3,
             "weight_decay":1e-4, "clip_grad_norm":5., "shrinkage":.05,
             "epsilon":1e-4, "bn_policy":"FROZEN_RUNNING_STATS_TRAIN_AFFINE",
             "checkpoint_selection":CHECKPOINT_SELECTION}
    if mode == "train":
        for key, value in fixed.items():
            if p.get(key) != value:
                raise ValueError("Frozen protocol mismatch: "+key)
        if p["method"] not in ("raw", "log") or p["partition_id"] not in (0,1) or p["training_seed"] not in (3407,3408,3409,3410,3411):

            raise ValueError("Not one of the fixed paired20 runs")
        if p.get("timeout_sec") != 2700 or p.get("input_scope") != "ORIGINAL_5230_TRAIN_ONLY":
            raise ValueError("Fixed finite scope/runtime required")
    else:
        if p.get("smoke_steps") != 5 or p.get("batch_size") != 32 or p.get("timeout_sec") != 180:
            raise ValueError("Only one fixed5step synthetic batch32 smoke")
    if p.get("device") != "cuda:0":
        raise ValueError("Selected actual protocol uses only local cuda:0")
    return p


def train_run(p, protocol_sha256):
    start = time.monotonic(); output = Path(p["output_path"])
    output.mkdir(exist_ok=False, parents=False)
    deadline = start + p["timeout_sec"]
    last = {"status":"STARTING", "run_id":p["run_id"], "started_utc":utc(),
            "protocol_sha256":protocol_sha256, "runner_sha256":sha_file(__file__),
            "last_flushed_step":0, "checkpoint_selection":CHECKPOINT_SELECTION}
    json_write(output/"PROGRESS.json", last)
    def expire():
        json_write(output/"TIMEOUT.json", {"status":"TIMEOUT", "run_id":p["run_id"],
            "fixed_timeout_sec":p["timeout_sec"], "no_retry":True}, exclusive=True)
        os._exit(124)
    timer = threading.Timer(p["timeout_sec"], expire); timer.daemon=True; timer.start()
    try:
        configure_runtime(p["training_seed"], p["threads"])
        if not torch.cuda.is_available():
            raise RuntimeError("Frozen CUDA run unavailable; no CPU fallback")
        device = initialize_cuda_device()
        x, meta, splits, init, fit, held, order, flips = load_bound_inputs(p)
        model = build_model(p["backbone_source_path"], p["weights_path"], p["backbone_source_sha256"],
                            p["weights_sha256"], init["prototype_factors"], init["scales_raw"],
                            init["scales_log"], p["method"], p["training_seed"]).to(device)
        initial_state_sha = state_digest(model)
        optimizer = make_optimizer(model)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=20)
        bn_before = {k:v.detach().cpu().clone() for k,v in model.state_dict().items()
                     if k.endswith(("running_mean","running_var","num_batches_tracked"))}
        selected_state = {k:v for k,v in p.items() if k.endswith("_sha256")}
        selected_state.update({"initial_model_state_sha256":initial_state_sha,
            "fit_names_sha256":array_sha(meta["names"][fit]), "held_names_sha256":array_sha(meta["names"][held]),
            "sample_stream_sha256":array_sha(order), "flip_stream_sha256":array_sha(flips),
            "prototype_factors_sha256":array_sha(init["prototype_factors"]),
            "scales_raw":init["scales_raw"].tolist(), "scales_log":init["scales_log"].tolist(),
            "log_temperature_initial":float(model.log_temperature), "projection_sha256":array_sha(projection_qr()),
            "seed_scope":"Target prototype initialization, order and paired hflip. Same official pretrained encoder in all runs.",
            "all_init_metadata_keys":sorted(init)})
        json_write(output/"INITIALIZATION_BINDING.json", selected_state, exclusive=True)
        epoch_rows=[]; step=0
        stepfile=open(output/"STEPS.jsonl","x",encoding="utf8")
        try:
            for epoch in range(20):
                set_train_frozen_bn(model)
                epoch_start=time.monotonic(); epoch_loss=0.; epoch_examples=0
                for pos in range(0,len(fit),32):
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Fixed run deadline reached")
                    ii=order[epoch,pos:pos+32]; ff=flips[epoch,pos:pos+32]
                    yy=torch.as_tensor(meta["labels"][ii],dtype=torch.long,device=device)
                    xx=normalized_batch(x,ii,device,ff)
                    optimizer.zero_grad(set_to_none=True)
                    out=model(xx); loss,ll=model_loss(out,yy)
                    if not bool(torch.isfinite(loss)):
                        raise FloatingPointError("Nonfinite optimization loss")
                    loss.backward()
                    gradients=gradient_summary(model)
                    preclip=float(torch.nn.utils.clip_grad_norm_(model.parameters(),5.,error_if_nonfinite=True))
                    optimizer.step()
                    for name,param in model.named_parameters():
                        if not bool(torch.isfinite(param).all()):
                            raise FloatingPointError("Nonfinite parameter after update: "+name)
                    step+=1; epoch_examples+=len(ii); epoch_loss+=float(loss.detach())*len(ii)
                    row={"epoch":epoch+1,"step":step,"batch_n":len(ii),
                         **{k:float(v.detach()) for k,v in ll.items()},**gradients,
                         "global_grad_norm_before_clip":preclip,"clip_triggered":bool(preclip>5.),"log_temperature":float(model.log_temperature.detach()),
                         "elapsed_sec":time.monotonic()-start,
                         "encoder_lr":optimizer.param_groups[0]["lr"],"head_lr":optimizer.param_groups[1]["lr"]}
                    if step % 100 == 0 or step == 1:
                        with torch.no_grad():
                            ce=torch.linalg.eigvalsh(out["covariance"].detach().double())
                            pe=torch.linalg.eigvalsh(out["prototype_covariance"].detach().double())
                            row.update({"cov_min_eigenvalue":float(ce.min()),"cov_max_eigenvalue":float(ce.max()),
                                        "prototype_min_eigenvalue":float(pe.min()),"prototype_max_eigenvalue":float(pe.max())})
                    stepfile.write(json.dumps(row,allow_nan=False)+"\n")
                    if step % 100 == 0:
                        stepfile.flush()
                        last.update({"status":"RUNNING","epoch":epoch+1,"last_flushed_step":step,
                                     "elapsed_sec":time.monotonic()-start,"latest_loss":row["total"]})
                        json_write(output/"PROGRESS.json",last)
                        print(json.dumps({"run_id":p["run_id"],"epoch":epoch+1,"step":step,"loss":row["total"]}),flush=True)
                stepfile.flush()
                train_eval=evaluate(model,x,meta["labels"],fit,device,32,deadline)
                held_eval=evaluate(model,x,meta["labels"],held,device,32,deadline)
                epoch_row={"epoch":epoch+1,"step":step,"optimization_loss_weighted_mean":epoch_loss/epoch_examples,
                           "train":train_eval["metrics"],"held":held_eval["metrics"],
                           "epoch_wall_sec":time.monotonic()-epoch_start,"elapsed_sec":time.monotonic()-start}
                epoch_rows.append(epoch_row); scheduler.step()
                json_write(output/"EPOCHS.json",{"rows":epoch_rows,"selection":"FIXED_FINAL_NOT_HELD_BEST"})

                last.update({"status":"RUNNING","epoch":epoch+1,"last_flushed_step":step,"elapsed_sec":time.monotonic()-start})
                json_write(output/"PROGRESS.json",last)
                print(json.dumps({"run_id":p["run_id"],"epoch_complete":epoch+1,"held_macro_f1":held_eval["metrics"]["macro_f1_fixed"]}),flush=True)
            expected_steps=20*math.ceil(len(fit)/32)
            if step != expected_steps:
                raise AssertionError("Fixed complete20epoch stream budget not met")
            for key,value in bn_before.items():
                if not torch.equal(model.state_dict()[key].detach().cpu(),value):
                    raise AssertionError("Frozen BatchNorm running state changed: "+key)
            # The last epoch's exact state and scores are the sole selected result.
            final_state_sha=state_digest(model)
            torch.save({"state_dict":{k:v.detach().cpu() for k,v in model.state_dict().items()},
                        "method":p["method"],"epoch":20,"step":step,"protocol_sha256":protocol_sha256,
                        "initial_state_sha256":initial_state_sha,"final_state_sha256":final_state_sha,
                        "checkpoint_selection":CHECKPOINT_SELECTION},output/"FINAL_CHECKPOINT.pt")
            np.savez_compressed(output/"FINAL_PREDICTIONS.npz",
                held_probabilities=held_eval["probabilities"],held_indices=held,
                held_labels=meta["labels"][held],held_names=meta["names"][held],
                train_probabilities=train_eval["probabilities"],train_indices=fit,
                train_labels=meta["labels"][fit],train_names=meta["names"][fit])
            result={"status":"COMPLETE","run_id":p["run_id"],"method":p["method"],
                    "training_seed":p["training_seed"],"partition_id":p["partition_id"],
                    "used_steps":step,"expected_steps":expected_steps,"epochs":20,
                    "elapsed_sec":time.monotonic()-start,"finished_utc":utc(),
                    "train":train_eval["metrics"],"held":held_eval["metrics"],
                    "initial_state_sha256":initial_state_sha,"final_state_sha256":final_state_sha,
                    "BN_running_state_unchanged":True,"checkpoint_selection":CHECKPOINT_SELECTION,
                    "peak_cuda_memory_allocated_bytes":torch.cuda.max_memory_allocated(device),
                    "peak_cuda_memory_reserved_bytes":torch.cuda.max_memory_reserved(device),
                    "bindings":selected_state,
                    "limits":["Held rows are a frozen original TRAIN-pool partition, not old800 VAL/test/final.",
                              "Target initialization and data-order seeds do not repeat external ImageNet pretraining.",
                              "Raw/log have separate fixed initial TRAIN-distance unit scales but identical stored initial state.",
                              "Frozen BN running statistics and trainable affine parameters are common to both methods.",
                              "No mask, held-based fitting/early stopping/best epoch, final evaluation, or automatic retry occurred."]}
            result["output_sha256"]={name:sha_file(output/name) for name in ("FINAL_CHECKPOINT.pt","FINAL_PREDICTIONS.npz","STEPS.jsonl","EPOCHS.json","INITIALIZATION_BINDING.json")}
            json_write(output/"COMPLETED.json",result,exclusive=True)
            last.update({"status":"COMPLETE","last_flushed_step":step,"elapsed_sec":time.monotonic()-start})
            json_write(output/"PROGRESS.json",last)
            return result
        finally:
            stepfile.close()
    except BaseException as error:
        fail={"status":"FAILED","run_id":p["run_id"],"error_type":type(error).__name__,
              "error":str(error),"elapsed_sec":time.monotonic()-start,"last_flushed_step":last["last_flushed_step"],
              "no_retry":True,"checkpoint_selection":CHECKPOINT_SELECTION}
        json_write(output/"FAILED.json",fail,exclusive=True)
        raise
    finally:
        timer.cancel()


def synthetic_smoke(p, protocol_sha256):
    """Selected one finite GPU runtime/memory smoke; synthetic pixels only."""
    start=time.monotonic();out=Path(p["output_path"]);out.mkdir(exist_ok=False,parents=False)
    def expire():
        json_write(out/"TIMEOUT.json",{"status":"TIMEOUT","scope":"SYNTHETIC_SMOKE_ONLY","fixed_timeout_sec":180,"no_retry":True},exclusive=True)
        os._exit(124)
    timer=threading.Timer(180,expire);timer.daemon=True;timer.start()
    configure_runtime(3407,4)
    if not torch.cuda.is_available():
        raise RuntimeError("No GPU smoke fallback")
    device=initialize_cuda_device()
    rng=np.random.default_rng(51313)
    factors=np.broadcast_to(np.eye(32,dtype=np.float32)[None,None]*.15,(2,69,32,32)).copy()
    # Small deterministic class variation, positive definite by PP^T+epsilon I.
    factors+=rng.normal(0,.001,factors.shape).astype(np.float32)
    model=build_model(p["backbone_source_path"],p["weights_path"],p["backbone_source_sha256"],
                      p["weights_sha256"],factors,np.ones(2,np.float32),np.ones(2,np.float32),
                      method="log",seed=3407).to(device)
    optimizer=make_optimizer(model);set_train_frozen_bn(model)
    x=rng.integers(0,256,(32,2,3,224,224),dtype=np.uint8);labels=np.arange(32,dtype=np.int64)%69
    xx=normalized_batch(x,np.arange(32),device);yy=torch.as_tensor(labels,device=device)
    durations=[]
    before={k:v.detach().clone() for k,v in model.state_dict().items() if k.endswith(("running_mean","running_var","num_batches_tracked"))}
    for step in range(5):
        if time.monotonic()-start>=180:raise TimeoutError("Fixed synthetic smoke deadline")
        torch.cuda.synchronize();tt=time.monotonic()
        optimizer.zero_grad(set_to_none=True);result=model(xx);loss,_=model_loss(result,yy)
        if not bool(torch.isfinite(loss)):raise FloatingPointError("Nonfinite smoke loss")
        loss.backward();gradient_summary(model);torch.nn.utils.clip_grad_norm_(model.parameters(),5.,error_if_nonfinite=True)
        optimizer.step();torch.cuda.synchronize();durations.append(time.monotonic()-tt)
    assert all(torch.equal(model.state_dict()[k],v) for k,v in before.items())
    record={"status":"PASS","kind":"FIVE_STEP_SYNTHETIC_GPU_PERFORMANCE_MEMORY_SMOKE",
            "method":"log","batch_pairs":32,"steps":5,"step_seconds":durations,
            "median_last4_step_sec":float(np.median(durations[1:])),"elapsed_sec":time.monotonic()-start,
            "peak_cuda_memory_allocated_bytes":torch.cuda.max_memory_allocated(device),
            "peak_cuda_memory_reserved_bytes":torch.cuda.max_memory_reserved(device),

            "BN_running_state_unchanged":True,"all_trainable_gradients_finite_present":True,
            "real_data_opened":False,"source_sha256":sha_file(__file__),"protocol_sha256":protocol_sha256,
            "weights_sha256":p["weights_sha256"],"backbone_source_sha256":p["backbone_source_sha256"],
            "limits":["Synthetic image/label smoke is not an accuracy experiment.",
                      "It measures the selected log arm under the fixed batch, without automatic batch fallback.",
                      "Initialization scales are synthetic ones; real scales and target init belong only to the frozen training protocol."]}
    json_write(out/"SYNTHETIC_SMOKE.json",record,exclusive=True)
    timer.cancel()
    return record


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--protocol",required=True);ap.add_argument("--protocol-sha256",required=True)
    ap.add_argument("--mode",choices=("train","smoke"),required=True)
    args=ap.parse_args()
    if sha_file(args.protocol)!=args.protocol_sha256:
        raise ValueError("Protocol SHA mismatch")
    p=json.loads(Path(args.protocol).read_text("utf8"));validate_protocol(p,args.mode)
    result=train_run(p,args.protocol_sha256) if args.mode=="train" else synthetic_smoke(p,args.protocol_sha256)
    print(json.dumps({"status":result["status"],"output":p["output_path"],"elapsed_sec":result["elapsed_sec"]}),flush=True)


if __name__=="__main__":
    main()



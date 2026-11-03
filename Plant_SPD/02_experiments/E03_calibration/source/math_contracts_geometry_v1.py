"""Synthetic NumPy-only math checks; no datasets, models, torch, or GPU use."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import numpy as np


def spectral(a, f):
    w, q = np.linalg.eigh((a + a.T) * 0.5)
    assert np.min(w) > 0
    return (q * f(w)[None, :]) @ q.T


def le(a, b):
    return float(np.linalg.norm(spectral(a, np.log) - spectral(b, np.log)))


def ai(a, b):
    ih = spectral(a, lambda w: 1 / np.sqrt(w))
    return float(np.linalg.norm(np.log(np.linalg.eigvalsh(ih @ b @ ih))))


def sqrt_derivative(a, h):
    w, q = np.linalg.eigh(a)
    r = np.sqrt(w)
    return q @ ((q.T @ h @ q) / (r[:, None] + r[None, :])) @ q.T


def softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def main():
    a = np.diag([1., 4.])
    b = np.array([[2., 1.], [1., 2.]])
    g = np.array([[1., 1.], [0., 1.]])
    q = np.array([[0., -1.], [1., 0.]])
    le_before, le_after = le(a, b), le(g @ a @ g.T, g @ b @ g.T)
    ai_before, ai_after = ai(a, b), ai(g @ a @ g.T, g @ b @ g.T)
    assert abs(le_before - le_after) > 1e-3
    assert abs(ai_before - ai_after) < 1e-12
    assert abs(le_before - le(q @ a @ q.T, q @ b @ q.T)) < 1e-12
    assert abs(le_before - le(7. * a, 7. * b)) < 1e-12

    # Repeated spectrum: this closed form remains defined, unlike a naive 0/0.
    c = np.eye(2) * 1e-4
    h = np.array([[0.3, 0.2], [0.2, -0.1]])
    ds = sqrt_derivative(c, h)
    step = 1e-8
    fd = (spectral(c + step * h, np.sqrt) - spectral(c - step * h, np.sqrt)) / (2 * step)
    fd_relative_error = float(np.linalg.norm(ds - fd) / np.linalg.norm(ds))
    assert np.allclose(ds, 50. * h, rtol=1e-12, atol=1e-12)
    assert fd_relative_error < 1e-8
    lam = np.array([1e-4, 1e-8, 1e-12])
    sd = 1 / (2 * np.sqrt(lam))
    assert np.all(np.diff(sd) > 0)

    z = np.array([[2., 1., -1.], [-0.2, 0.6, 0.1], [1., 1., -0.5]])
    temperatures = [0.1, 1., 10., 100.]
    for t in temperatures:
        assert np.array_equal(np.argmax(z, axis=1), np.argmax(z / t, axis=1))
    shifts = np.array([[20.], [-15.], [50.]])
    assert np.allclose(softmax(z), softmax(z + shifts), atol=1e-14, rtol=1e-14)
    assert not np.allclose(np.linalg.norm(z, axis=1), np.linalg.norm(z + shifts, axis=1))

    result = {
        "status": "PASS", "utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Synthetic NumPy only; no input data, model loading, forward pass, training, GPU, or active-run changes.",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "affine_congruence_counterexample": {
            "A": a.tolist(), "B": b.tolist(), "G": g.tolist(),
            "log_euclidean_before": le_before, "log_euclidean_after": le_after,
            "affine_invariant_before": ai_before, "affine_invariant_after": ai_after,
            "orthogonal_and_common_scale_invariance": "PASS"},
        "sqrt_derivative": {
            "frechet_coefficients": "1/(sqrt(lambda_i)+sqrt(lambda_j))",
            "scalar_lambda": lam.tolist(), "scalar_derivative": sd.tolist(),
            "diverges_as_lambda_approaches_zero": True,
            "unscaled_sqrt_frobenius_operator_bound_at_existing_eps_1e-4": 50.,
            "log_frobenius_operator_bound_at_existing_eps_1e-4": 10000.,
            "repeated_spectrum_finite_difference_relative_error": fd_relative_error,
            "limitation": "Bounds concern only the matrix-function derivative, not the normalized loss, full-network gradient, or AdamW update."},
        "temperature_scaling": {
            "positive_temperatures_checked": temperatures,
            "argmax_unchanged_including_deterministic_tie_rule": True,
            "logit_common_shift_softmax_invariance": True,
            "raw_logit_norm_identifiable_from_probabilities": False},
        "primary_sources": [
            "https://doi.org/10.1002/mrm.20965",
            "https://www-sop.inria.fr/asclepios/Publications/Arsigny/arsigny_rr_tensors.pdf",
            "https://arxiv.org/pdf/1705.08561",
            "https://proceedings.mlr.press/v70/guo17a/guo17a.pdf",
            "https://proceedings.iclr.cc/paper_files/paper/2025/file/70270a1bc28ecb2a2aefad566c5e556b-Paper-Conference.pdf"]}
    out = Path(__file__).resolve().parents[1] / "proof" / "MATH_CONTRACTS_GEOMETRY_V1.json"
    out.parent.mkdir(exist_ok=True)
    with out.open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write("\n")
    print(json.dumps({"status": "PASS", "proof": str(out), "le_before": le_before,
                      "le_after": le_after, "sqrt_fd_relative_error": fd_relative_error}))


if __name__ == "__main__":
    main()

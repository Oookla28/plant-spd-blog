"""CPU contracts for the rigorous audit theory V2.

These contracts verify the stated algebraic/local conditions and the audit
state machine on synthetic inputs. They do not validate HELD generalization,
batch/AdamW dynamics, or any real-data mechanism claim.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

import numpy as np


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def softmax(x: np.ndarray) -> np.ndarray:
    z = x - np.max(x)
    q = np.exp(z)
    return q / q.sum()


def rank2(x: np.ndarray, tol: float = 1e-9) -> int:
    return int(np.linalg.matrix_rank(x, tol=tol))


def check(name: str, condition: bool, detail: str = "") -> dict:
    return {"name": name, "pass": bool(condition), "detail": detail}


def audit_decision(
    delta_obs: float,
    bound: float,
    *,
    same_objects: bool,
    gap_certified: bool,
    norm_certified: bool,
    regularization_bias_certified: bool,
    eval_same: bool,
    budget_same: bool,
    saturated: bool,
) -> tuple[str, str]:
    if not (same_objects and eval_same and budget_same):
        return "REJECT", "comparison objects or evaluation/budget are mismatched"
    if saturated or not (gap_certified and norm_certified and regularization_bias_certified):
        return "INDETERMINATE", "certificate or non-saturation condition is missing"
    if abs(delta_obs) <= bound:
        return "INDETERMINATE", "observed difference is inside the certificate radius"
    return "ACCEPT", "observed sign is separated from zero by the certificate radius"


def ce_q_qbeta(a: np.ndarray, beta: float, target: int) -> tuple[np.ndarray, np.ndarray]:
    p = softmax(-beta * a)
    y = np.zeros_like(a)
    y[target] = 1.0
    abar = float(p @ a)
    q = beta * (p - y)
    qbeta = (p - y) - beta * p * (a - abar)
    return q, qbeta


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    rng = np.random.default_rng(20261102)
    checks: list[dict] = []

    # A1/A2: exact unregularized-risk certificate for a quadratic objective.
    A = np.diag([1.5, 2.0, 3.0])
    b = np.array([0.4, -0.2, 0.7])
    lam = 0.03
    theta0 = np.linalg.solve(A, b)
    theta_lam = np.linalg.solve(A + lam * np.eye(3), b)
    theta_hat = theta_lam + np.array([1e-4, -2e-4, 1.5e-4])

    def F(theta: np.ndarray) -> float:
        return float(0.5 * theta @ A @ theta - b @ theta)

    def J(theta: np.ndarray) -> float:
        return F(theta) + 0.5 * lam * float(theta @ theta)

    delta = J(theta_hat) - J(theta_lam)
    e0 = F(theta_hat) - F(theta0)
    bound0 = delta + 0.5 * lam * float(theta0 @ theta0)
    checks.append(check("A1_unregularized_risk_certificate", e0 <= bound0 + 1e-12, f"e={e0:.16g}, bound={bound0:.16g}"))

    # A2: safe bound around the regularized optimum does not call it R^0.
    reg_abs = abs(F(theta_hat) - F(theta_lam))
    reg_bound = delta + 0.5 * lam * (float(theta_hat @ theta_hat) + float(theta_lam @ theta_lam))
    checks.append(check("A2_regularized_target_certificate", reg_abs <= reg_bound + 1e-12, f"abs={reg_abs:.16g}, bound={reg_bound:.16g}"))

    # A3: strong-convex gradient certificate.
    grad = A @ theta_hat - b + lam * theta_hat
    grad_bound = float(grad @ grad) / (2.0 * lam)
    checks.append(check("A3_gradient_gap_certificate", delta <= grad_bound + 1e-12, f"gap={delta:.16g}, grad_bound={grad_bound:.16g}"))

    # A4: sign separation and indeterminate branch.
    decision, _ = audit_decision(0.8, 0.2, same_objects=True, gap_certified=True, norm_certified=True, regularization_bias_certified=True, eval_same=True, budget_same=True, saturated=False)
    checks.append(check("A4_sign_separation_accepts", decision == "ACCEPT", f"decision={decision}"))
    decision, _ = audit_decision(0.1, 0.2, same_objects=True, gap_certified=True, norm_certified=True, regularization_bias_certified=True, eval_same=True, budget_same=True, saturated=False)
    checks.append(check("A5_inside_radius_indeterminate", decision == "INDETERMINATE", f"decision={decision}"))

    # A6: native comparator is explicitly not treated as R^0.
    native_only, reason = audit_decision(0.8, 0.2, same_objects=True, gap_certified=True, norm_certified=True, regularization_bias_certified=False, eval_same=True, budget_same=True, saturated=False)
    checks.append(check("A6_native_anchor_does_not_certify_R0", native_only == "INDETERMINATE" and "certificate" in reason, f"decision={native_only}, reason={reason}"))

    # B1: exact K=2 one-dimensional output tangent.
    a2 = np.array([0.5, 2.0])
    q2, qb2 = ce_q_qbeta(a2, 0.7, target=0)
    A2jac = np.array([[0.4, -0.2], [-0.1, 0.3]])
    g2 = A2jac.T @ q2
    h2 = A2jac.T @ qb2
    c2 = abs(float(g2 @ h2)) / (np.linalg.norm(g2) * np.linalg.norm(h2))
    checks.append(check("B1_K2_single_sample_rank_one", rank2(np.column_stack([g2, h2])) <= 1 and abs(c2 - 1.0) < 1e-12, f"rank={rank2(np.column_stack([g2, h2]))}, abs_cos={c2:.16g}"))

    # B2: K>=3 non-target spectrum condition plus injective Jacobian.
    a3 = np.array([0.2, 1.1, 3.7])
    q3, qb3 = ce_q_qbeta(a3, 0.7, target=0)
    g3 = q3.copy()  # A=I, so the pullback is injective.
    h3 = qb3.copy()
    c3 = abs(float(g3 @ h3)) / (np.linalg.norm(g3) * np.linalg.norm(h3))
    checks.append(check("B2_K3_distinct_non_target_rank_two", rank2(np.column_stack([g3, h3])) == 2 and c3 < 1.0 - 1e-8, f"rank={rank2(np.column_stack([g3, h3]))}, abs_cos={c3:.6f}"))

    # B3: K>=3 with equal non-target margins collapses to one direction.
    adeg = np.array([0.2, 1.1, 1.1])
    qd, qbd = ce_q_qbeta(adeg, 0.7, target=0)
    checks.append(check("B3_K3_equal_non_target_rank_one", rank2(np.column_stack([qd, qbd])) <= 1, f"rank={rank2(np.column_stack([qd, qbd]))}"))

    # B4: K=69 with nondegenerate margins is rank two only under an injective pullback.
    a69 = np.linspace(0.1, 6.9, 69) ** 2
    q69, qb69 = ce_q_qbeta(a69, 0.73, target=0)
    checks.append(check("B4_K69_identity_jacobian_rank_two", rank2(np.column_stack([q69, qb69])) == 2, f"rank={rank2(np.column_stack([q69, qb69]))}"))
    # A rank-one pullback can preserve one nonzero direction but cannot
    # preserve the two-dimensional output span.
    collapsed = np.vstack([np.arange(1.0, 70.0), np.zeros(69)])
    gcol = collapsed @ q69
    hcol = collapsed @ qb69
    checks.append(check("B5_K69_rank_one_jacobian_counterexample", rank2(np.column_stack([gcol, hcol])) <= 1, f"rank={rank2(np.column_stack([gcol, hcol]))}"))

    # B6: K=2 batch caveat: different sample Jacobians can create rank two.
    def one_sample(margin: float, beta: float) -> tuple[float, float]:
        q, qb = ce_q_qbeta(np.array([0.0, margin]), beta, target=0)
        # q and qb are multiples of v=(1,-1); return the first coordinate.
        return float(q[0]), float(qb[0])

    c1, d1 = one_sample(0.5, 0.7)
    c2b, d2b = one_sample(2.0, 0.7)
    gbatch = np.array([c1, c2b])
    hbatch = np.array([d1, d2b])
    checks.append(check("B6_K2_batch_jacobian_counterexample", rank2(np.column_stack([gbatch, hbatch])) == 2, f"rank={rank2(np.column_stack([gbatch, hbatch]))}"))

    # C: deterministic protocol states.
    reject, _ = audit_decision(0.8, 0.2, same_objects=False, gap_certified=True, norm_certified=True, regularization_bias_certified=True, eval_same=False, budget_same=True, saturated=False)
    checks.append(check("C1_mismatched_objects_reject", reject == "REJECT", f"decision={reject}"))
    indet, _ = audit_decision(0.8, 0.2, same_objects=True, gap_certified=False, norm_certified=True, regularization_bias_certified=True, eval_same=True, budget_same=True, saturated=False)
    checks.append(check("C2_missing_gap_indeterminate", indet == "INDETERMINATE", f"decision={indet}"))
    sat, _ = audit_decision(0.8, 0.2, same_objects=True, gap_certified=True, norm_certified=True, regularization_bias_certified=True, eval_same=True, budget_same=True, saturated=True)
    checks.append(check("C3_saturation_indeterminate", sat == "INDETERMINATE", f"decision={sat}"))
    accept, _ = audit_decision(-0.8, 0.2, same_objects=True, gap_certified=True, norm_certified=True, regularization_bias_certified=True, eval_same=True, budget_same=True, saturated=False)
    checks.append(check("C4_certified_negative_sign_accept", accept == "ACCEPT", f"decision={accept}"))

    failed = [x for x in checks if not x["pass"]]
    script = Path(__file__)
    result = {
        "status": "PASS" if not failed else "FAIL",
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "numpy_version": np.__version__,
        "device": "cpu",
        "synthetic_seed": 20261102,
        "contract_count": len(checks),
        "checks": checks,
        "theory_file": "RIGOROUS_AUDIT_THEORY_V2.md",
        "theory_sha256": sha256(script.with_name("RIGOROUS_AUDIT_THEORY_V2.md")),
        "limits": [
            "Contracts verify algebraic identities, local rank conditions, and protocol state transitions only.",
            "They do not establish HELD generalization or real-data causal mechanisms.",
            "K=2 collinearity is single-sample with fixed Jacobian; a batch counterexample is included.",
            "Native comparator norms do not certify the unregularized optimum without an additional bias/norm argument.",
        ],
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": result["status"], "contract_count": len(checks), "failed": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()

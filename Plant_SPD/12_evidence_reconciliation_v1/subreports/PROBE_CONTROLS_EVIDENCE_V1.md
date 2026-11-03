# Probe controls evidence reconciliation

This is a new retrospective evidence index. It does not rewrite any original ledger, result or pre-registration.

## Disposition

| New entry | Existence | Prior ledger | Use |
|---|---|---|---|
| REC-NATIVE | Exists | C06 | Enable after this reconciliation; four original native controls, symmetry repair retained |
| REC-RISK | Exists | Budget embedded in E08a protocol, related C06/C07 | Enable with diagonal-only risk scope and complete parameter norm |
| REC-UNDERFIT | Exists | C05/C09 | Enable as distinct E06 and E07 diagnostic generations |

## Exact findings

- E06 eight prototype-head endpoints: TRAIN fixed69 Macro-F1 range 0.1390362108 to 0.7355903554.
- E07 eight convex affine endpoints: lambda=.001, max full-gradient norm 9.83770573415e-07, max gap 4.83902270558e-10, TRAIN F1 range 0.1911376419 to 0.3189394550. Thus convergence and TRAIN fit are separate checks.
- E08a M=1598050.056101633 is maximum of four complete73002-parameter native norms including bias; lambda=1.251525252518626e-08; penalty budget=.01; risk allowance=.01+actualgap, native diagonals only. There is no missing69-row factor.
- E08a original five accepted completions plus E08b three separately named new completions form the historical accepted eight. Original failed/unfinished namespace is retained. All eight metadata TRAIN F1=1.0; this outcome is distinct from their gap certificates.
- E08a repaired native control START 2026-10-25T17:54:05.115679+00:00, finish 2026-10-25T17:55:12.871340+00:00; example anchored solve START 2026-10-25T17:57:21.178361+00:00. Local START/hash records are not externally authenticated timestamps.
- Later native_pc10 has ten controls and a different commonlambda. New F2 fixed-feature certificates are later current-endpoint evidence and do not inherit E08a native-risk bounds.

## Mathematical scope

J_lambda(theta)=L_aug(theta)+(lambda/2)||theta||², with all W and b in theta. M=max_r||theta_native,r||² across complete classifiers. lambda=min(.001,.02/M). For native diagonal cells only, L(theta_hat)<=L(theta_native)+.01+||gradJ||²/(2lambda). This is a TRAIN risk bound, not a parameter norm bound or HELD guarantee.

## Evidence detail

All numerical values and source-key pointers, selected sources/protocols/completion receipts and their hash checks are in PROBE_CONTROLS_EVIDENCE_V1.json. No arrays, labels or checkpoints were semantically read; no training/model import/evaluation was performed. Selected files were hash-checked against the original F package manifest or D delivery seal. This validates bytes, not independent scientific execution or timeless immutability.

Selected artifact files checked: 47; all matches: True.

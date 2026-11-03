# DES-AS-style optimization decision and next plan

Date: 2026-10-22 (server-authoritative offline audit)

## What was run

The audit reused only the frozen 904-image DEV masks and the existing 256-letterbox prediction NPZ files. It did not decode RGB, download data, retrain a model, access CAL/FINAL labels, or start a GPU. Five candidate segmentation models were evaluated on the two seeds for which all five outputs are complete (3408 and 3409). Every one of the 32 model coalitions was scored by foreground micro-IoU. Exact five-player algorithm-Shapley values were then converted to positive-only normalized weights, following the model-selection and weighting idea of DES-AS. DES-AS is prior work; this transfer is a baseline optimization audit, not a novelty claim.

## Evidence

| Evaluation | Equal five-model fusion | Shapley-weighted fusion | Difference |
|---|---:|---:|---:|
| Calibrate 3408, evaluate 3409 | 67.623787% | 67.828069% | +0.204282 pp |
| Calibrate 3409, evaluate 3408 | 67.646962% | 67.845362% | +0.198400 pp |

Paired duplicate-group bootstrap intervals for the two transfers were [0.109706, 0.290653] pp and [0.116026, 0.278993] pp, respectively, over 864 groups and 2,000 resamples. The effect is small but directionally stable in this two-seed screen. SegFormer-B2 received the largest Shapley value in both seeds (15.56 pp on the IoU utility scale); U-Net received the smallest (9.74–10.03 pp). The best coalition values (68.246380% and 68.085907%) are GT-scored offline upper bounds and are not deployable results.

## Decision

`SCREENING_POSITIVE_BUT_NOT_PROMOTED`. The result is strong enough to justify one preregistered confirmation step, but not enough to present DES-AS weighting as a final method. It is a known ensemble-selection principle, uses a repeatedly reused DEV set, and lacks the complete seed-3407 EfficientViT runs.

## Next finite research window

1. Complete only the two missing seed-3407 EfficientViT runs under the frozen SAT protocol; do not alter data, resize, optimizer, update budget, or model definitions.
2. Run the exact three-seed Shapley analysis with cross-seed calibration/evaluation. Report mean, seed-wise values, duplicate-group paired intervals, and the equal-fusion control. A promotion gate should require a positive effect in all three transfer directions or a preregistered aggregate interval excluding zero, together with no small-lesion regression.
3. Measure actual CPU/GPU latency for the five fixed models before discussing cost-aware subset selection. FLOPs or positive Shapley values alone do not establish savings.
4. Only if step 2 passes, test a pre-call per-image selector using prediction-only observables (entropy, inter-model disagreement, valid-area fraction and calibrated confidence). Calibrate on a seed/model split and evaluate on a different seed; GT must never be an online feature. Compare against equal fusion, global Shapley weighting, entropy-only and random controls.
5. If the three-seed effect is unstable or disappears under the held-out direction, stop static-weight tuning and return to information-bearing local correction. Do not add Ridge/HGB scans or rename Shapley weighting as a new algorithm.

## Current paper implication

The safe claim is: “A DES-AS-inspired, positive-contribution ensemble weighting gives a small, cross-seed screening gain over equal fusion on the repeated DEV protocol.” The paper must disclose the two-seed limitation, repeated DEV use, missing seed-3407 EfficientViT runs, and lack of online latency evidence. It should not claim a new ensemble theory, dynamic per-image routing, compute reduction, or independent final-test improvement from this audit.

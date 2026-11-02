# F1–F4 and A-series: final read-only findings

This report integrates the fixed completed runs and original preregistration. It reports prescribed endpoints, not the best epoch. All new A metrics are repeated original/unflipped FIT diagnostics; no new HELD/generalization evaluation was performed. The JSON stores each numerical conclusion as value, formula, sourcefile, key, and its resolved source chain.

## 1. What F established, and what it did not

The completed saved-state audit reconstructed actual head learning-rate budgets and terminal AdamW moments. The finite weighted-Cauchy ceiling is a rigorous necessary coefficient/RMS cap under zero initialization; terminal q99×B remains a dotted heuristic, never a historical bound. Terminal large |u| does not prove useful direction or SNR.

For strict classification, positive score rescaling preserves argmax and the coefficient-norm infimum is zero. Fixed CE demand is a different question. Below, constructive **ray-scaled** feasible upper bounds replace the much larger unscaled explicit-L2 endpoint norms. Neither endpoint nor ray is a minimum-norm classifier.

| Fixed features / scope | CE target | Jensen necessary RMS lower | Constructive ray RMS upper | Status |
|---|---:|---:|---:|---|
| raw_frozen / original_unflipped | 1 | 0.1419 | 1.33558 | CONSTRUCTIVE_RAY_UPPER_WITNESS |
| raw_frozen / original_unflipped | 0.5 | 0.179479 | 1.85522 | CONSTRUCTIVE_RAY_UPPER_WITNESS |
| raw_frozen / original_unflipped | 0.1 | 0.24967 | 3.11728 | CONSTRUCTIVE_RAY_UPPER_WITNESS |
| raw_frozen / augmented_both_true_flips | 1 | 0.142046 | 1.33549 | CONSTRUCTIVE_RAY_UPPER_WITNESS |
| raw_frozen / augmented_both_true_flips | 0.5 | 0.179663 | 1.85561 | CONSTRUCTIVE_RAY_UPPER_WITNESS |
| raw_frozen / augmented_both_true_flips | 0.1 | 0.249926 | 3.11876 | CONSTRUCTIVE_RAY_UPPER_WITNESS |
| log_joint / original_unflipped | 1 | 0.030013 | 0.633119 | CONSTRUCTIVE_RAY_UPPER_WITNESS |
| log_joint / original_unflipped | 0.5 | 0.0379612 | 0.884715 | CONSTRUCTIVE_RAY_UPPER_WITNESS |
| log_joint / original_unflipped | 0.1 | 0.0528071 | 1.49396 | CONSTRUCTIVE_RAY_UPPER_WITNESS |
| log_joint / augmented_both_true_flips | 1 | 0.0300131 | 0.633645 | CONSTRUCTIVE_RAY_UPPER_WITNESS |
| log_joint / augmented_both_true_flips | 0.5 | 0.0379613 | 0.88535 | CONSTRUCTIVE_RAY_UPPER_WITNESS |
| log_joint / augmented_both_true_flips | 0.1 | 0.0528073 | 1.49479 | CONSTRUCTIVE_RAY_UPPER_WITNESS |

Demand numbers come from the fixed ray receipt; every row retains its exact pointer in the JSON. The explicit-L2 gap certificates establish objective accuracy for those reference endpoints and do not establish AdamW accessibility.

## 2. Original predictions versus finite observations

| Experiment | Original account α prediction | Original account β prediction | Actual endpoint FIT Macro-F1 | Actual dual CE |
|---|---|---|---:|---:|
| A0 | 约24% | 约24% | 24.178% | 2.79022 |
| A | 仍约24% | 若直接WD占主导，接近100% | 24.178% | 2.79015 |
| A2 | 接近100% | 原固定点论称不变 | 87.5436% | 0.897228 |
| A2prime | 持续改善 | 未给唯一预测 | 53.4716% | 1.86772 |
| A3 | 恢复 | 未给唯一预测 | 76.6747% | 1.06173 |
| A4-Log (joint, separate feature path) | 若头预算主导则恢复 | 未给唯一预测 | 89.1929% | 0.501291 |

The original prediction text is copied verbatim from the preregistered table with source line pointers in the JSON. A response to an intervention does not select a unique account or causal mechanism.

## 3. Matched cached controls and interpretation

- **A**: final FIT Macro-F1 change versus A0 = 0 pp; actual head LR sum B = 1.3755; dual CE = 2.79015. Provenance: `D:\PlantSPD_forensics_F1F4_A_v1_20261026\cached_a_s3407\COMPLETED.json#/train/macro_f1_fixed`.
- **A2**: final FIT Macro-F1 change versus A0 = 63.3656 pp; actual head LR sum B = 13.755; dual CE = 0.897228. Provenance: `D:\PlantSPD_forensics_F1F4_A_v1_20261026\cached_a2_s3407\COMPLETED.json#/train/macro_f1_fixed`.
- **A2prime**: final FIT Macro-F1 change versus A0 = 29.2936 pp; actual head LR sum B = 3.9955; dual CE = 1.86772. Provenance: `D:\PlantSPD_forensics_F1F4_A_v1_20261026\cached_a2prime_s3407\COMPLETED.json#/train/macro_f1_fixed`.
- **A3**: final FIT Macro-F1 change versus A0 = 52.4968 pp; actual head LR sum B = 1.3755; dual CE = 1.06173. Provenance: `D:\PlantSPD_forensics_F1F4_A_v1_20261026\cached_a3_s3407\COMPLETED.json#/train/macro_f1_fixed`.

WEAKENED_BY_MATCHED_FINITE_CONTROL. Removing direct WD is a finite matched intervention; unchanged F1 weakens a direct-WD-dominance explanation without disproving every gradient/noise hypothesis.

PRESPECIFIED_GE10PP_TRAIN_RECOVERY_THRESHOLD_MET; NOT_100PERCENT_ORIGINAL_FIT. The fixed 10pp recovery criterion is not a 100% fitting criterion or a significance test.

Changes visits, updates, and epoch-cosine horizon together; finite response does not identify a unique budget or noise mechanism.

Temperature reparameterization changes AdamW coordinates, decay exposure, and shared clipping; not uniquely a geometry intervention.

The complete recorded head travel is reported below. Actual path includes the actual decoupled-decay contribution; adaptive path is the sum of eta times RMS(u). Net/path is a descriptive triangle-inequality ratio, not a gradient-SNR estimate. For A3 it concerns only native W+b, excluding the temperature coordinate and the motion of exp(s)theta.

| Cached arm | Actual head path RMS | Adaptive head path RMS | Net displacement RMS | Net / actual path |
|---|---:|---:|---:|---:|
| A0 | 0.352821 | 0.352828 | 0.195751 | 0.554818 |
| A | 0.352827 | 0.352827 | 0.195764 | 0.554843 |
| A2 | 2.83887 | 2.83914 | 1.01514 | 0.357585 |
| A2prime | 0.959193 | 0.959238 | 0.455652 | 0.475037 |
| A3 | 0.410887 | 0.410892 | 0.171873 | 0.418296 |

## 4. Joint Log intervention and conditional controls

A4-Log changes FIT Macro-F1 by 53.1427 pp relative to its original **Log-joint** baseline. It is not compared as the same feature space as the cached Raw arms. Head LR and warmup cochange. Comparison is to same mapping joint baseline, not the cached Raw target. Conditional Raw control must be considered before claiming Log-specific failure.

- **A2_seed3408**: COMPLETE; prescribed FIT Macro-F1 87.8193%; corresponding-baseline change 63.7323 pp. This is a repeated-FIT training response.
- **A2_seed3409**: COMPLETE; prescribed FIT Macro-F1 88.0291%; corresponding-baseline change 63.7528 pp. This is a repeated-FIT training response.
- **A4_Raw**: NOT_INCLUDED_AFTER_ROOT_CONDITIONAL_CLOSURE; SKIPPED_BY_PREDECLARED_RECOVERY_CONDITION: A4 Log gain >=10pp; see CLOSED_PRIMARY_A_SERIES_V1.json.

## 5. Norm trajectories and F4 endpoint audit

Original whole W/b histories and whole encoder-RMS histories remain **UNAVAILABLE**. The A0/cache/A4 trajectories were recorded prospectively and cannot be retroactively attributed to the old runs. Actual cumulative LR, W/b norms, and TRAIN CE are shown with their original units. A2prime is a fresh 60-epoch run with a stretched cosine schedule and the original 20-epoch stream repeated three times; it is not a continuation of A0.

F4 measured 4184 identical original FIT images at the three fixed endpoints. Global activation RMS and mean per-image RMS are reported separately; they do not establish a uniform scalar change or historical trajectory.

## 6. Retained limits and reasonable conclusion

The evidence supports a dependence of finite training performance on the optimization recipe and parameterization. It does not identify one unique coefficient ceiling, classify terminal u as useful signal, or prove a geometry-specific failure from a failed Log intervention alone. The mature E08 norm reference uses another encoder/scaler/precision path and is kept separate. F2b remains an endpoint spectral/amplitude-family diagnostic.

A defensible narrative is: **a fixed representation and a nominally identical affine task can exhibit very different finite optimization responses; auditable optimizer budgets, same-feature CE witnesses, matched interventions, and prospectively recorded norms are required before attributing low fitting to geometry.** This is a training-mechanism audit, not new generalization or publication-tier evidence.

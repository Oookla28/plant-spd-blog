# English abstract and contribution draft

**Before Comparing Geometry: Auditing Optimization and Readout in Covariance Pooling**

This is the current manuscript draft after artifact reconciliation. It draws on completed evidence generations with different scopes; it is not a claim of a new matrix mapping, uniquely identified mechanism, or completed novelty review.

## Abstract

Comparisons of covariance representations often use end-to-end performance or frozen readouts to motivate geometric explanations. Such interpretations require separating the information available to a readout from the optimization procedure used to recover it. We audit Raw and Log covariance mappings in a 69-class visual classification setting through four checks: mathematical admissibility of the proposed criterion, native-function reachability, numerical convergence, and sufficient training fit. We additionally formalize a deterministic fixed-representation certificate that separates regularized readout optima from solver and regularization gaps, and derive a local rank criterion for distinguishing temperature perturbations from scalar learning-rate scaling in squared-distance softmax models. A five-source-seed crossed-readout study, comprising twenty new fits, reveals setting-specific encoder-source-by-readout dependencies and different preferences under Macro-F1 and NLL, with seed-level exceptions to a simple native-matching rule. In a separate equal-head stress test, two corresponding fixed-feature sets admit perfect training classification under independently certified convex readouts despite poor fitting under the default training recipe. Removing head weight decay leaves frozen-Raw training Macro-F1 unchanged at 24.18%, whereas a tenfold head learning rate reaches 87.80% with a sample standard deviation of 0.24 percentage points across three prespecified training seeds. A Log-joint intervention combining a fivefold head learning rate and warmup raises same-seed training Macro-F1 from 36.05% to 89.19%. Two proposed hard-budget criteria fail mathematical admissibility and are retired rather than counted as empirical falsifications. These results support a substantial role for finite training recipes in training fit without identifying a unique budget, curvature, or signal-to-noise mechanism. The audit provides a traceable basis for interpreting covariance comparisons; independent generalization and real-data validation of the local temperature mechanism remain open.

## Contribution statements

1. **A four-check comparison protocol.** We separate mathematical admissibility, native-function reachability, convergence of a specified objective, and sufficient training fit, retaining criterion failures separately from valid empirical prediction misses.
2. **Conditional readout evidence.** Twenty fully refitted, numerically certified source-by-mapping readouts expose source-dependent and metric-dependent outcomes, including exceptions that preclude a rigid native-matching claim.
3. **Prespecified training interventions with explicit limits.** Frozen-head and joint-training interventions quantify large fitting responses while distinguishing single-factor controls, cochanges, unavailable histories, and unresolved mechanism attribution.
4. **A conservative mathematical audit certificate.** For fixed representations and specified readout families, we provide a deterministic sign certificate for TRAIN risk differences and a local (K=2)/(K\ge3) rank criterion with explicit Jacobian and batch caveats. The protocol returns an indeterminate or reject state when the required assumptions or solver certificates are missing.

## Abstract evidence map

The following is an authoring aid, not abstract prose. Every numerical statement above must retain its evidence ID through revision.

| Statement | Evidence ID and packaged source |
|---|---|
| 69 classes; five source seeds and twenty refits | REC-MATRIX-5S; `../09_scientific_supplement_v1/expanded_batch/BATCH_PROTOCOL.json`; `../12_evidence_reconciliation_v1/subreports/MATRIX_EVIDENCE_V1.json#/records/0` |
| Both current fixed-feature sets TRAIN100% | REC-F2-RAW/REC-F2-LOG; `../11_f1_f4_A_forensics_v1/f2_convex_raw_frozen_v1/RESULT.json` and `f2_convex_log_joint_v1/RESULT.json`, each `#/train_original_unflipped/macro_f1_fixed`, `#/train_augmented/macro_f1_fixed`, `#/certificate` |
| WD deletion 24.18→24.18% | REC-A-SERIES; `../11_f1_f4_A_forensics_v1/cached_a0_s3407/COMPLETED.json` and `cached_a_s3407/COMPLETED.json`, each `#/train/macro_f1_fixed` |
| A2 87.80%±0.24pp | REC-A-SERIES; `../11_f1_f4_A_forensics_v1/cached_a2_s3407/COMPLETED.json#/train/macro_f1_fixed`, `../11_f1_f4_A_forensics_v1/cached_a2_s3408/COMPLETED.json#/train/macro_f1_fixed`, and `../11_f1_f4_A_forensics_v1/cached_a2_s3409/COMPLETED.json#/train/macro_f1_fixed`; mean and sampleSD across these three endpoints |
| A4 36.05→89.19% | REC-A-SERIES; `../11_f1_f4_A_forensics_v1/F1_F4_FORENSICS.json#/A4_Log`, with original source chain and same-seed baseline retained |
| Two retired mathematical criteria | MAF-Q99/MAF-ONEHOT; `../12_evidence_reconciliation_v1/EVIDENCE_REGISTER_V1.json#/mathematical_admission_failures`; original authority `../11_f1_f4_A_forensics_v1/DECISION_TREE_ADDENDUM_V1.md` |
| Fixed-representation certificate and local rank criterion | `../09_scientific_supplement_v1/math/RIGOROUS_AUDIT_THEORY_V2.md`; CPU contracts `../09_scientific_supplement_v1/math/RIGOROUS_AUDIT_CONTRACTS_V2.json` (16/16 PASS) |

## Required scope notes

- The five source seeds describe encoder-training randomness on the same data partition. They are not five independent datasets, and the affine readouts use deterministic zero starts.
- The twenty-fit matrix uses a repeatedly examined 1,046-image HELD pool. Its earlier eight-cell generation uses another lambda and is not pooled with it. The current F/A experiments are FIT/TRAIN-only and do not add HELD evidence.
- The current F2 certificates concern two current fixed-feature sets and their explicit L2 objectives. Mature E08 native-risk certificates are historical references with different encoder/scaler/target bindings; certificates are not transferable.
- Numerical convergence and perfect training classification are separate empirical checks. Neither proves an unregularized optimum, optimizer accessibility, or generalization.
- A2 mean±SD denotes 100×mean(F1) and 100×sampleSD(F1), with denominator 3−1. A4 uses the same-seed baseline; 34.12% is a cross-seed background mean and is not its comparator.
- Duration extension changes updates, visits, and the cosine horizon; A4 changes both head LR and warmup. Use “prespecified interventions,” not “all single-factor” or “all matched.”
- A0 and A3 share B=1.3755 but differ by 52.4968pp in training F1 (REC-B-NONSUFFICIENT). Do not claim a common logarithmic dose-response across heterogeneous interventions.
- Local preregistration and SHA records establish inspectable protocol history and byte integrity; they are not externally authenticated timestamps. This reconciliation itself is retrospective.
- Do not write “first,” “rigid coupling,” “intrinsic calibration disproved,” “WD ruled out,” or “joint training is necessary.” The evidence does not license those claims.


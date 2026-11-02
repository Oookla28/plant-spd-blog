# Mechanism pre-registration: frozen two-branch decision

Frozen 2026-10-27 03:31 UTC. Neither window has been run.

Both windows test one question: **a certified good head exists, but head-only SGD did not find it—is the failure budget insufficiency or parameterization/K-path restriction?**

The prior is now explicit. The already measured Plant E01 `−0.4143pp` TRAIN value is **not** a K=2 or @320 result: it is the original fixed69 E01 default trainable-prototype+encoder family at 20 complete epochs/2620 updates, final fixed epoch-20 checkpoint, with two partitions × five paired seeds. The K=2 window is therefore an incremental end-to-end test against an already registered K=69 baseline, not a relabeling or rerun of that E01 value. The equal-head affine family (`54.9088%` Raw HELD versus `25.7443%` Log HELD at @2620) is a separate audit family and is not used as the E01 baseline.

The A0/A3 checkpoint does not expose an explicit scalar `u`; therefore the control arm uses the exact inverse-temperature ratio `exp(0.2183221006)=1.2439876923`, not an exact physical `uT` multiplier. A class-difference head-norm proxy is recorded separately as a parameterization diagnostic.

| Window | Branch | Frozen decision |
|---|---|---|
| ISIC LR×100 | Recovery | matched-seed recovery rate ≥0.80 supports budget insufficiency / M-B dominance |
| ISIC LR×100 | Platform | recovery remains about 0.40–0.70 without instability: budget alone is insufficient; parameterization/K-path or state resistance contributes |
| ISIC LR×100 | Worse | worse than LR×10 or late clipping/update instability: non-monotone unstable regime / M-C |
| ISIC LR×100 control | Step-like reproduction | LR multiplier `1.2439876923`; HELD delta versus A0 ≤−1.15pp supports the effective-step channel |
| ISIC LR×100 control | Neutral | HELD delta versus A0 ≥−0.50pp supports a residual temperature/parameterization channel |
| ISIC LR×100 control | Mixed | HELD delta between −1.15pp and −0.50pp supports both channels |
| Plant K=2 E01 | Collapse | Raw/Log difference approaches the certified K=2 readout scale (0–3.72pp): supports the end-to-end K component of M-A |
| Plant K=2 E01 | Hold | difference remains at K=69 order: points to encoder/optimization layers |
| Plant K=2 E01 | Partial | intermediate shrinkage: split readout geometry from encoder/optimization contributions |

Both runs must preserve paired seeds, fixed checkpoint rules, TRAIN/HELD separation, and same-seed recovery denominators. These are registered decision rules, not results. Any future difference must carry the four-part identity `(construction K, budget/updates, checkpoint strategy, seed structure)` before entering the ledger.

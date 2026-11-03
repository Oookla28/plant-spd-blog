# Plant equal-head paired audit

This is the independent Plant p0 equal-head **affine-head** family. It is not the original E01 trainable-prototype+encoder family; its values must not be used to relabel the E01 `-0.4143pp` TRAIN difference.

Read-only audit of the original Plant p0 fixed-20-epoch endpoints. Each row pairs the same training seed across Raw/Log and frozen/joint modes.

| seed | Raw frozen TRAIN | Raw joint TRAIN | Log frozen TRAIN | Log joint TRAIN | Raw joint−frozen | Log joint−frozen |
|---:|---:|---:|---:|---:|---:|---:|
| 3407 | 24.1780% | 99.6364% | 24.0421% | 36.0502% | +75.4584pp | +12.0081pp |
| 3408 | 24.0870% | 99.5533% | 23.9045% | 32.7693% | +75.4663pp | +8.8648pp |
| 3409 | 24.2762% | 99.6432% | 23.9158% | 33.1956% | +75.3670pp | +9.2798pp |
| 3410 | 24.2309% | 99.4867% | 23.8318% | 36.8208% | +75.2558pp | +12.9890pp |
| 3411 | 24.3392% | 99.4176% | 23.7158% | 31.7449% | +75.0784pp | +8.0291pp |

Five-seed TRAIN means: Raw frozen `24.2223%`, Raw joint `99.5474%`, Log frozen `23.8820%`, Log joint `34.1162%`. The same-arm paired joint-minus-frozen gains are `+75.3252pp` for Raw and `+10.2342pp` for Log. The K=69 Raw-joint versus Log-joint gap is therefore `−65.4313pp` at the same seed/mode family, but the gap is reported as a descriptive comparison, not a causal attribution.

The same endpoints also contain HELD: Raw frozen `17.5007%`, Raw joint `54.9088%`, Log frozen `17.1826%`, Log joint `25.7443%` (five-seed means). Thus Plant Raw-joint HELD @2620 is `54.9088%`; `25.7443%` is Plant Log-joint HELD @2620, and the within-family Raw−Log HELD difference is `+29.1645pp`. This is a five-seed affine-family result, not the original E01 prototype-family result.

Source paths are the corresponding `COMPLETED.json` and `EPOCHS.json` files under the source directory in the JSON. No GPU or training was started.

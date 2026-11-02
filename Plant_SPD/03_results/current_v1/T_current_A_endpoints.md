# Current A-series prescribed TRAIN endpoints

REC-A-SERIES. Existing scalar metadata transcription; no new metric computation. Raw cached arms and Log joint A4 are separate feature paths. All original/unflipped FIT; no HELD.

| Arm | FIT Macro-F1 (%) | Dual CE | Actual head LR sum B |
|---|---:|---:|---:|
| A0 | 24.177986 | 2.790217600 | 1.375500 |
| A | 24.177986 | 2.790154800 | 1.375500 |
| A2 | 87.543632 | 0.897228165 | 13.755000 |
| A2prime | 53.471598 | 1.867715323 | 3.995500 |
| A3 | 76.674743 | 1.061734151 | 1.375500 |
| A2_seed3408 | 87.819328 | 0.896272021 | 13.755000 |
| A2_seed3409 | 88.029062 | 0.893232992 | 13.755000 |
| A4_Log | 89.192864 | 0.501291275 | 6.630000 |

A2 seeds 3407/3408/3409 are displayed individually; no new uncertainty calculation. A2prime changes updates, visits and cosine horizon. A4 changes LR and warmup. A3 adds a temperature parameter.

# Zero-GPU follow-up mechanism checks

- Plant baseline Log-joint: there is no exact step-320 checkpoint. The nearest saved points are **2.22%** TRAIN macro-F1 at step 262 and **5.37%** at step 393, reaching only **36.05%** at step 2620. The curve rises slowly; there is no saved 70%+ early peak followed by collapse.
- Plant Log A4: TRAIN macro-F1 rises from **1.53%** at step 131 to **89.81%** at step 2489 and **89.19%** at step 2620. This is the LR5x/warmup intervention curve.
- ISIC logs: A2 head clipping is 0% with no encoder update; A4 encoder clipping is 5.9375%, head clipping 0%.
- A3 temperature: one shared scalar `log_inverse_temperature` is present in each step log; no separate two-branch temperatures or per-step checkpoint files are available. The terminal scalar is 0.218322 (inverse temperature 1.243988).
- A0 vs A3: reconstructed head budget B is equal at 0.168, while A3 changes endpoint TRAIN F1 by -1.67pp and HELD F1 by -2.15pp. Budget alone is insufficient.
- Cached K lever: `MECHANISM_ZERO_COST.json` contains Raw/Log cached PlantSPD K=69→2 readouts (4 label constructions each) and existing K=69 baselines.

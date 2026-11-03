# Terminal zero-GPU mechanism reads

This artifact reads existing F: logs only; it starts no training and uses CPU-only parsing.

## Plant Log-joint: 320 to 2620 updates
- Interpolated step 320: TRAIN 2.960±0.583pp; HELD 2.526±0.483pp.
- Step 2620: TRAIN 34.116±2.199pp; HELD 25.744±2.673pp.
- HELD slopes (pp per 100 updates) over 320→786, 786→1310, 1310→1834, 1834→2620: 1.963, 1.585, 0.783, 0.212.
- Verdict: slow climb with late deceleration, no late collapse; this favors a severe-delay/truncated-budget description, while the remaining positive slope does not prove that a future ceiling is absent.

## ISIC A2/A4 stability signatures
- A2 (three seeds): encoder is frozen, encoder update L2 is exactly 0, and head clip rate is 0%; head update median/q95/max are approximately 0.048–0.051 / 0.129 / 0.460.
- A4 Log-joint: encoder clip rate 5.938%, coefficient minimum 0.4316; encoder update median/q95/max 0.03303/0.09189/0.11478.
- Baseline equal Log-joint: encoder clip rate 4.062%, so A4 is a mild increase, not a clipping storm.

## Temperature and B non-sufficiency
- A0 and A3 have equal head LR traces and equal 320 head-update opportunities; final HELD F1 is 66.501% vs 64.352%.
- A3 log-inverse-temperature moves from 0.000000 to 0.218322; inverse temperature ends at 1.2440.
- This upgrades B-non-sufficiency to a second descriptive instance: equal head-LR budget does not ensure equal F1 when a temperature coordinate is added; it does not by itself identify why.

## M-A status
The cached 69→2 Plant readouts were already completed in MECHANISM_ZERO_COST.json. They remain cross-domain readout evidence and cannot be called an ISIC K intervention.

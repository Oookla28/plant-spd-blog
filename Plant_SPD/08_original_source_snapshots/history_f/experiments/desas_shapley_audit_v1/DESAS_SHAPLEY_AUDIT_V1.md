# DES-AS-style Shapley Audit v1

This CPU-only audit reused frozen 904-DEV prediction NPZs and masks. It did not decode RGB, retrain, download data, or start GPU.

Protocol SHA-256: `6b7ba0a06938511675bf887970aba498357a4aa137c05baf4cce37ce407a6db2`

## Scope and method

Five segmentation models were treated as the candidate coalition. Exact 32-coalition foreground micro-IoU utilities were computed for each complete seed. Algorithm-Shapley values were obtained by the exact 5-player permutation formula; only positive values were normalized for the DES-AS-style weighted ensemble.

## Results

| seed | equal five-model IoU | positive-Shapley IoU | best coalition IoU | best coalition mask |
|---:|---:|---:|---:|---:|
| 3408 | 67.646962% | 67.854903% | 68.246380% | 22 |
| 3409 | 67.623787% | 67.828462% | 68.085907% | 14 |

### Shapley values

| seed | unet | deeplabv3plus_r50 | segformer_b2 | efficientvit_fpn | efficientvit_mlp |
|---:|---:|---:|---:|---:|---:|
| 3408 | 10.030157 pp | 14.466203 pp | 15.563464 pp | 13.584369 pp | 14.002768 pp |
| 3409 | 9.735880 pp | 14.274443 pp | 15.557703 pp | 14.014546 pp | 14.041215 pp |

### Cross-seed transfer

| calibrate → evaluate | equal IoU | Shapley-weighted IoU | delta | paired group 95% CI |
|---|---:|---:|---:|---:|
| 3408 → 3409 | 67.623787% | 67.828069% | 0.204282 pp | [0.109706, 0.290653] pp |
| 3409 → 3408 | 67.646962% | 67.845362% | 0.198400 pp | [0.116026, 0.278993] pp |

## Decision

The Shapley audit is a screening result. A positive cross-seed delta with a CI excluding zero would justify a preregistered three-seed confirmation and cost-aware selector. Otherwise, stop tuning static ensemble weights and prioritize a new information-bearing correction mechanism.

## Limitations

- The two missing seed-3407 EfficientViT runs prevent a complete three-seed comparison.
- The repeated 904-image DEV protocol is not an independent final test.
- Offline Shapley weighting does not establish per-image dynamic selection or latency reduction.
- DES-AS is prior art; no novelty is claimed for Shapley weighting itself.

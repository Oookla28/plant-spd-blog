# Zero-GPU mechanism diagnostics

Generated 2026-10-27T00:21:40.312620+00:00; CPU-only (`CUDA_VISIBLE_DEVICES=-1`), no new training and no main-report edits.

## M-A: class-count leverage

The medical replication has only K=2 labels, so a valid 69→2 merger cannot be made from its cache. The diagnostic therefore uses the saved PlantSPD K=69 raw/log head-input features for a readout-only discriminator and labels it cross-domain.
- `raw/merge_contiguous_half`: support=[1842, 2342], train macro-F1=0.7162, status=COMPLETE, gap=1.4e-10.
- `raw/merge_balanced_support`: support=[2091, 2093], train macro-F1=0.7244, status=COMPLETE, gap=4.24e-10.
- `raw/random_pair`: support=[179, 102], train macro-F1=0.9961, status=COMPLETE, gap=1.72e-10.
- `raw/one_vs_rest`: support=[3840, 344], train macro-F1=0.4786, status=COMPLETE, gap=2.17e-10.
- `log/merge_contiguous_half`: support=[1842, 2342], train macro-F1=0.7258, status=COMPLETE, gap=4.23e-10.
- `log/merge_balanced_support`: support=[2091, 2093], train macro-F1=0.7349, status=COMPLETE, gap=2.75e-10.
- `log/random_pair`: support=[179, 102], train macro-F1=0.9961, status=COMPLETE, gap=2.42e-10.
- `log/one_vs_rest`: support=[3840, 344], train macro-F1=0.5158, status=COMPLETE, gap=4.14e-10.
- Existing K=69 `raw` baseline (copied TRAIN endpoint): macro-F1=0.2418; no refit in this diagnostic.
- Existing K=69 `log` baseline (copied TRAIN endpoint): macro-F1=0.8919; no refit in this diagnostic.

Interpretation: binary readouts can be certified on multiple 69→2 label constructions, but this is a separability/readout result on PlantSPD features. It does not establish what an ISIC K change would do.

## M-D: spectrum and native head scale

Medical T1 values are read from the saved normalized initial FIT cache; plant values are recomputed from saved raw/log head-input caches. Participation ratio, conditioning, and per-parameter head RMS are reported in the JSON.

## M-C: clipping and update signature

Saved A2/A4 step logs are parsed without reconstructing missing per-step learning rates. A4 encoder clipping and sampled update alignment are reported alongside A2’s frozen-encoder zero-update signature; reconstructed recipe budgets remain explicitly non-observed.

## Evidence boundary

These are hypothesis discriminators. They do not promote M-A/M-C/M-D to causal conclusions; LR×100 and plant 2-class paired training remain required for that.

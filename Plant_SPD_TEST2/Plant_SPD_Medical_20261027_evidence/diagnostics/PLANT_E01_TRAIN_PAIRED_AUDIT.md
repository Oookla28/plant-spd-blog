# Plant E01 TRAIN 侧 Raw/Log 配对审计
## 结论
原始 Plant E01 的 10 个同分区、同 seed 配对在 TRAIN 侧均为 **Log < Raw**：pooled Log−Raw = **−0.4143pp**，10/10 为负。此前已登记的 HELD 侧 Log−Raw 为正；因此净额分解必须同时列出 TRAIN 与 HELD，不能只用 HELD 叙事代替训练端点。
这是一项只读端点审计，不是新训练，也不把 TRAIN 侧差异解释成纯几何因果。它只补齐了 E01 “风暴成本/几何收益”分解的另一端。
## 汇总（macro-F1）
| 配对组 | n | Raw TRAIN 均值 | Log TRAIN 均值 | Log−Raw 均值 | SD | SE | 正/零/负 |
|---|---:|---:|---:|---:|---:|---:|---:|| p0 | 5 | 99.6377% | 99.1717% | -0.4660pp | 0.1726pp | 0.0772pp | 0/0/5 || p1 | 5 | 99.6081% | 99.2454% | -0.3626pp | 0.0799pp | 0.0357pp | 0/0/5 || pooled | 10 | 99.6229% | 99.2085% | -0.4143pp | 0.1380pp | 0.0436pp | 0/0/10 |
## 逐对端点
| partition | seed | Raw TRAIN | Log TRAIN | Log−Raw |
|---:|---:|---:|---:|---:|| 0 | 3407 | 99.6364% | 99.2268% | -0.4096pp || 0 | 3408 | 99.5802% | 98.9750% | -0.6052pp || 0 | 3409 | 99.6268% | 99.1962% | -0.4307pp || 0 | 3410 | 99.7611% | 99.1017% | -0.6594pp || 0 | 3411 | 99.5841% | 99.3587% | -0.2253pp || 1 | 3407 | 99.6256% | 99.2033% | -0.4223pp || 1 | 3408 | 99.5898% | 99.1775% | -0.4123pp || 1 | 3409 | 99.5691% | 99.3368% | -0.2323pp || 1 | 3410 | 99.6633% | 99.2561% | -0.4072pp || 1 | 3411 | 99.5925% | 99.2534% | -0.3391pp |
## 审计边界
- 配对键为 `partition_id × training_seed`；10 对均报告 `initial_state_identical=true` 与 `sample_and_flip_streams_identical=true`。
- 指标来自原始 E01 `PAIRED_TRAINING_RESULTS.json` 的 final 20-epoch `raw_train_macro_f1` / `log_train_macro_f1`。
- 本文件不重新计算 HELD，不把两个分区当作 10 个独立数据集，也不把 TRAIN 侧结果外推为 HELD 泛化。
- 反向的 TRAIN 侧方向说明：在训练集终点上 Log 并未优于 Raw；因此“HELD Log 优势”不能被描述为 TRAIN 侧同步提升。
## 持证来源
- 原始记录：`F:\Plant_SPD\02_experiments\E01_paired_training\PAIRED_TRAINING_RESULTS.json`
- 原始记录 SHA-256：`163f2358adbd545020a882436fe3597d282dcb57f11401f8f71e54c400f63026`
- 原分析记录：`F:\Plant_SPD\02_experiments\E01_paired_training\analysis_v1\ANALYSIS.json`
- 原分析 SHA-256：`f41a93e02ac2ca948f318cf579d4e6c4fe41b0b5dcccc8af1e7efb4c68a8a897`
- 机器可读审计：`F:\Plant_SPD_Medical_20261027\diagnostics\PLANT_E01_TRAIN_PAIRED_AUDIT.json`

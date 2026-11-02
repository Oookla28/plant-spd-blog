# 新五source-seed二十格：最终receipt审计与结果汇总

**状态：COMPLETE20_NEW_REFITS_FIVE_SOURCE_SEEDS；有效完成 20/20；完整四格seed 5/5。**

共同lambda来自本轮十个TRAIN-native正控制：`1.165957154427756e-08`。没有并入原八格终点。

## 每seed四格与数值证书

| seed | encoder/readout | TRAIN F1 % | HELD F1 % | HELD NLL | gradient L2 | numerical gap | native风险检查 |
|---|---|---:|---:|---:|---:|---:|---|
| 3407 | raw/raw | 100.000 | 59.159 | 1.803946 | 9.51e-07 | 3.87e-05 | PASS |
| 3407 | raw/log | 100.000 | 56.033 | 1.743664 | 8.43e-07 | 3.05e-05 | 不适用 |
| 3407 | log/raw | 100.000 | 53.794 | 2.453685 | 9.59e-07 | 3.94e-05 | 不适用 |
| 3407 | log/log | 100.000 | 58.003 | 1.803504 | 8.71e-07 | 3.26e-05 | PASS |
| 3408 | raw/raw | 100.000 | 58.474 | 1.818393 | 9.94e-07 | 4.24e-05 | PASS |
| 3408 | raw/log | 100.000 | 56.546 | 1.696652 | 9.08e-07 | 3.54e-05 | 不适用 |
| 3408 | log/raw | 100.000 | 56.001 | 2.589693 | 9.99e-07 | 4.28e-05 | 不适用 |
| 3408 | log/log | 100.000 | 56.920 | 1.779105 | 9.22e-07 | 3.65e-05 | PASS |
| 3409 | raw/raw | 100.000 | 55.648 | 1.786559 | 8.65e-07 | 3.21e-05 | PASS |
| 3409 | raw/log | 100.000 | 55.407 | 1.685291 | 9.71e-07 | 4.04e-05 | 不适用 |
| 3409 | log/raw | 100.000 | 53.031 | 2.461810 | 9.87e-07 | 4.18e-05 | 不适用 |
| 3409 | log/log | 100.000 | 56.802 | 1.752735 | 8.7e-07 | 3.25e-05 | PASS |
| 3410 | raw/raw | 100.000 | 56.626 | 1.738505 | 9.62e-07 | 3.97e-05 | PASS |
| 3410 | raw/log | 100.000 | 56.215 | 1.689641 | 9.95e-07 | 4.25e-05 | 不适用 |
| 3410 | log/raw | 100.000 | 55.994 | 2.464945 | 9.86e-07 | 4.17e-05 | 不适用 |
| 3410 | log/log | 100.000 | 54.935 | 1.764078 | 9.24e-07 | 3.66e-05 | PASS |
| 3411 | raw/raw | 100.000 | 57.886 | 1.731968 | 8.52e-07 | 3.11e-05 | PASS |
| 3411 | raw/log | 100.000 | 58.305 | 1.698860 | 9.84e-07 | 4.16e-05 | 不适用 |
| 3411 | log/raw | 100.000 | 54.835 | 2.509525 | 8.65e-07 | 3.21e-05 | 不适用 |
| 3411 | log/log | 100.000 | 58.251 | 1.811931 | 9.53e-07 | 3.9e-05 | PASS |

## 每seed simple effects与DID

F1以百分点pp表示；NLL为原始损失单位，不能也写成pp。Simple effect均定义为同encoder来源下Log readout减Raw readout；DID为Log encoder的simple effect减Raw encoder的simple effect。正/负的有利方向依指标而定。

| seed | 四格状态 | Raw来源 F1 effect pp | Log来源 F1 effect pp | F1 DID pp | Raw来源 NLL effect | Log来源 NLL effect | NLL DID |
|---|---|---:|---:|---:|---:|---:|---:|
| 3407 | COMPLETE | -3.125866 | +4.209813 | +7.335679 | -0.060282 | -0.650181 | -0.589899 |
| 3408 | COMPLETE | -1.927662 | +0.919453 | +2.847114 | -0.121741 | -0.810588 | -0.688847 |
| 3409 | COMPLETE | -0.240530 | +3.771100 | +4.011630 | -0.101268 | -0.709076 | -0.607807 |
| 3410 | COMPLETE | -0.410981 | -1.059750 | -0.648769 | -0.048864 | -0.700867 | -0.652003 |
| 3411 | COMPLETE | +0.418716 | +3.416041 | +2.997325 | -0.033108 | -0.697595 | -0.664487 |

## Source-training seed分布

只汇总四格齐全的seed；保留所有方向，不按结果挑seed。均值、样本SD、范围与正负计数见SEED_DISTRIBUTIONS.csv，不据此把同1046张HELD膨胀成五个独立数据集。
- f1_effects_pp / raw_encoder_log_minus_raw_readout: n=5, mean=-1.057265, SD=1.440482574550825, positive/zero/negative=1/0/4。
- f1_effects_pp / log_encoder_log_minus_raw_readout: n=5, mean=+2.251331, SD=2.2493916723349883, positive/zero/negative=4/0/1。
- f1_effects_pp / difference_in_differences: n=5, mean=+3.308596, SD=2.858419417523324, positive/zero/negative=4/0/1。
- nll_effects / raw_encoder_log_minus_raw_readout: n=5, mean=-0.073053, SD=0.037116312836980296, positive/zero/negative=0/0/5。
- nll_effects / log_encoder_log_minus_raw_readout: n=5, mean=-0.713661, SD=0.058879890567729395, positive/zero/negative=0/0/5。
- nll_effects / difference_in_differences: n=5, mean=-0.640609, SD=0.0408483067977505, positive/zero/negative=0/0/5。

## 未完成/无效格

完整状态表见SUMMARY.json；缺失格不补值，也不以旧八格替代。

## 解释范围

- New batch only; no old8 endpoints reused or pooled.
- Source seeds3407/3408 share encoders and HELD with earlier studies; expanding seeds is not independent confirmation.
- No image/label arrays loaded, no recomputation of predictions or metrics, no HELD endpoint/temperature/lambda selection.
- Inherited original run_cell limit strings mention two seeds/four encoders; the new frozen batch scope is ten encoders/five seeds/twenty refits.
- All inference is conditional on this partition, cached encoders and affine readout family. Training-seed SD is not a confidence interval across datasets.

每个原始输入receipt/protocol SHA和输出链SHA均保留在SUMMARY.json。图使用最终记录指标，不重新评价、不按HELD选择、不加载预测数组。

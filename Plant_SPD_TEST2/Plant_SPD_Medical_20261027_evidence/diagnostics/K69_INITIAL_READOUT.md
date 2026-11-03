# K=69 初始冻结特征认证读出（CPU-only）

这是对 PlantSPD 初始冻结特征缓存的固定 TRAIN 凸读出复核；不访问 HELD、不训练编码器、不启动 GPU。

| map | TRAIN original F1 | TRAIN augmented F1 | accuracy | gap bound | status |
|---|---:|---:|---:|---:|---|
| raw | 100.000000% | 100.000000% | 100.000000% | 4.17e-05 | COMPLETE |
| log | 100.000000% | 100.000000% | 100.000000% | 3.84e-05 | COMPLETE |

## 证书边界
- 证书授权：在冻结的 K=69 TRAIN 特征上，显式 L2 凸 affine readout 的目标已收敛；TRAIN 分类读出指标与绝对水平已列出。
- 证书不授权：HELD 泛化，或非凸端到端联合训练可达该读出。
- 读出使用 two-view free affine W[2,528,69]+b[2,69]，lambda=1.1659571544277561e-8，所有 W/b 显式 L2；dual logits 为两 view 平均。

## 输入绑定
- Raw: `F:\Plant_SPD\10_equal_head_T1_audit_20261026\alpha_preflight_v1\actual_fit_gpu_v2\head_input_raw.npy`
- Log: `F:\Plant_SPD\10_equal_head_T1_audit_20261026\alpha_preflight_v1\actual_fit_gpu_v2\head_input_log.npy`
- labels: `SPLITS.npz labels[partition0 fit]`; n=4184, augmented=8368, K=69
- solver source SHA256: `b4b25012321fe3c92f1817706b06d4058ca5fb4dd5714491f633248cb30d03a8`

## 解释
若两张表均接近 100%，此前“认证层参照因饱和不可测”应升级为已测事实；若 Log/Raw 处于中间水平，则这些值构成 K=69 的持证读出层参照。

# F2：实际 Log-joint 端点的 FIT 特征与谱

状态：代码和合成合同已完成，实际图像前向**尚未执行**。正式协议仍需root在原study窗口内选择、SHA绑定、资源空闲身份核验、有限外层登记。所有写入仅本目录，F:\Plant_SPD只读。

## 输出与来源

冻结 `ehc1_p0_s3407_log_joint` FINAL_CHECKPOINT：strict加载全部参数和buffer，包括 means/scales。使用原T1的label-free FIT membership与统计验证、冻结等头族forward的实际head输入AST。原协方差AST只追加 `return covariance,fmap`，没有更改数学节点；端点encoder RMS直接来自该次fmap，没有重复encoder前向。

- `FINAL_FIT_FEATURES.npy`：[8368,2,528] float64，当前端点的真实Log映射、svec、固定原GPU FIT center/scale后的输入。
- `FINAL_FIT_B_EIGENVALUES.npy`：[8368,2,32] float64，B_obs=float64(实际F32 C)−1e-4I 的对称特征值；不floor，不夹断，保存可能的舍入小负值。
- `FINAL_FIT_ENCODER_RMS.npy`：[8368,2] float64，同次原encoder fmap逐row/view RMS。
- `FIT_ROWS.npz`：FIT原图ID与flip，行序 r=2*FITposition+flip；没有标签。
- `F2B_PER_ROW_DIAGNOSTICS.npz`：阈值mask/count、总trace／阈值内trace／有符号trace比例、每个特征值的幅度导数、与2I偏离及固定scale归一化结果。
- `RESULT.json`／`COMPLETED.json`：每值公式、source/array/row/checkpoint/statistics SHA及状态证据。

B=a²B_obs的实矩阵族下，d/dlog(a) log(a²B_obs+εI)|a=1 的特征值等于 2λB/(λB+ε)。原scaler固定，svec为Frobenius等距，所以归一化2I偏离为 sqrt(sum_i(2λB/(λB+ε)−2)²)/fixed_scale[view]。该解析导数是重构矩阵族的导数，不是历史F32编码器的实测反传；λB<10ε的个数本身**不是**偏离上界。

## 合成准入

`f2_endpoint_contracts_v1/CONTRACTS.json` PASS：原协方差prefix逐位一致；fmap同次捕获；真实head-input AST与冻结forward features逐位一致；幅度导数有限差分验证；无floor保留微小负B谱。合同仅CPU合成张量，无真实checkpoint加载或图像前向。

## 正式运行接口（尚未运行）

```powershell
$env:PYTHONPATH='D:\PlantSPD_work\linear_probe_cross_v1_20261025\cpu_env\Lib\site-packages'
& 'D:\PlantSPD_work\paired_seed_training_v1_20261025_recovery1\gpu_env\Scripts\python.exe' -B `
  'D:\PlantSPD_forensics_F1F4_A_v1_20261026\source\extract_F2_endpoint_v1.py' `
  --stage extract --protocol '<正式协议>' --protocol-sha256 '<实际SHA>' `
  --output-root '<正式协议绑定的全新目录>'
```

实际仅RTX5060指定UUID／CUDA0，CPU control2，已核Intel sequential OpenMP stub允许1；内部600秒、外部610秒且原GPU硬截止前须完整615秒预算。无日志分数、无优化器、无拟合、无标签或HELD前向。root后续若在此当前端点上做凸读出，必须使用这里保存的同特征与固定scaler。

## 历史E08单独处理

`F2_E08_MATURE_SOURCE_INFO.json` 独立记录E01成熟Log编码器的FIT cache、scaler与两版认证θ。它与本F2当前端点来源不同。历史θ不移植到当前F10特征，也不将历史证书写成当前端点的新证书。

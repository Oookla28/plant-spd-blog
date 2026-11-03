# 当前论文的实验与代码导航

先使用根目录 `RUN_REPRODUCTION.ps1`，具体命令见[复现说明](../07_reproducibility/REPRODUCIBILITY.md)。本页把论文问题、证据ID和科学实现对应起来；历史脚本及其原关闭窗口保留作溯源，新复现写到新的输出目录。

| 论文用途 | 证据/状态 | 工件与代码 |
|---|---|---|
| 原端到端现象 | C01，固定20epoch配对结果；两划分五seed | [E01](E01_paired_training/)；`source/runner_v2.py`及其绑定协议 |
| 优化配置与采样更新 | REC-CLIP/C03；16格含1carryover+15新；实际更新为采样 | [E02](E02_optimizer_controls/)与[E04](E04_fit_and_clip_diagnostics/) |
| 温标与概率尺度 | REC-TS/C02；既有HELD探索性五折 | [E03](E03_calibration/) |
| TRAIN CE阶段比较 | REC-FITPROGRESS/C04；事后阈值匹配 | [E04](E04_fit_and_clip_diagnostics/) |
| Sqrt参照 | 补充材料，不作普遍赢家 | [E05](E05_sqrt_reference/) |
| 欠拟合读出与正则目标 | REC-UNDERFIT/C05/C09 | [E06](E06_prototype_cross/)与[E07](E07_regularized_linear_probe/) |
| native函数可达、风险预算 | REC-NATIVE/REC-RISK；完整W+b范数，native范围 | [E08a](E08a_native_control_and_old5/) |
| 早期八格 | REC-PROBE-2S；5完成+3恢复，仅附录 | [E08a](E08a_native_control_and_old5/)与[E08b](E08b_anchored_probe_recovery/) |
| 五source-seed20格主矩阵 | REC-MATRIX-5S；全20重拟合；另一代lambda | [09/expanded_batch](../09_scientific_supplement_v1/expanded_batch/)；`expanded_probe/expanded_probe_v1.py` |
| 等头族20格与T1 | 五seed×Raw/Log×frozen/joint，固定预算 | [10](../10_equal_head_T1_audit_20261026/)；`equal_head_control/equal_head_control_v2.py` |
| F取证、两批同特征认证读出 | REC-F2-RAW/LOG；本轮新证书，不是成熟E08 | [11](../11_f1_f4_A_forensics_v1/)；`f2_solver_tool/source/F2_gpu_convex_demand_v1.py` |
| A系列恢复与反例 | REC-A-SERIES/REC-B-NONSUFFICIENT；FIT-only | [11/cached_head_Aseries_v1](../11_f1_f4_A_forensics_v1/cached_head_Aseries_v1/)；`source/train_A4_fit_only_v2.py` |
| 证据登记与准入 | 事后工件对账，不补称预注册 | [12](../12_evidence_reconciliation_v1/) |

## 可实际启动的新入口

- `tools/run_reproduction.py cached` / `cached-suite`：冻结Raw缓存上的A系列。
- `tools/run_reproduction.py convex`：两批当前固定特征的认证凸读出。
- `tools/run_reproduction.py equal-head`：20格默认等头配方及记录过的A4配方；只评价FIT。
- `tools/reproduce_cross_readout.py`：五source-seed交叉读出的一格重求解；历史HELD只作原开发评价。
- `04_figures/current_v1/build_current_assets.py --output-root ...`：仅已有元数据重建/导出论文材料。

当前入口复用SHA绑定的冻结科学kernel，新建手工协议和输出；不会覆盖上述历史命名空间。输入/样本顺序/scaler/精度/正则和停止标准以入口生成的协议及对应源工件为准。完整历史Python文件见[代码索引](../07_reproducibility/CODE_INDEX.md)。

# 五种子20格交叉读出的手动复现

对应论文证据：`REC-MATRIX-5S`。本入口复现五种子扩展矩阵，和早期八格分开，不复用旧格的系数作为新拟合结果。

## 从哪里开始

入口为 `F:\Plant_SPD\tools\reproduce_cross_readout.py`。十个编码器的冻结协方差缓存、20份原协议、TRAIN scaler、十个 native 正控制及旧结果均已在包中。复现交叉读出不需要重新训练编码器、不需要读取原始 RGB。

保留当前机器绝对路径。建议使用当前机器的原生 Python 和现有 CPU 数值依赖：

```powershell
$P = 'C:\Users\lenovo\AppData\Local\Programs\Python\Python311\python.exe'
$env:PYTHONPATH = 'D:\PlantSPD_work\linear_probe_cross_v1_20261025\cpu_env\Lib\site-packages'
$Runner = 'F:\Plant_SPD\tools\reproduce_cross_readout.py'

# 只校验文件绑定和协议重定位；不打开科学数组、不拟合。
& $P -B $Runner --encoder-source log --mapping raw --seed 3409 --plan-only --output-root 'D:\PlantSPD_manual_cross_plan_01'

# 合成数据合同：目标与梯度、凸求解、native仿射等价、10锚点公式与拒绝分支。
# 无真实数据，不读取 HELD 标签。
& $P -B $Runner --contracts --output-root 'D:\PlantSPD_manual_cross_contracts_01'

# 实际复现一个格：E_log_s3409 -> Raw读出；只开CPU2线程。
& $P -B $Runner --encoder-source log --mapping raw --seed 3409 --output-root 'D:\PlantSPD_manual_cross_s3409_Elog_Rraw_01'

# 实际按固定顺序串行复现全部20格。每格有独立600s内限/610s外限。
# 某格失败就停止此批，不跳过、不重试、不恢复。
& $P -B $Runner --suite-20 --output-root 'D:\PlantSPD_manual_cross_20cells_01'
```

每条命令的输出目录必须不存在，而且在 `F:\Plant_SPD` 包外。`--suite-20 --plan-only` 可检查全部20格而不启动求解。不要把同一输出路径重复执行。

## 矩阵和种子究竟是什么

- 训练种子：3407、3408、3409、3410、3411，对应五组已经训练完成的 Raw/Log 编码器，共10个编码器。
- 每个编码器分别使用 Raw/Log 两种协方差读出映射：`5×2×2=20`格。
- 求解系数全部全零初始化，使用确定性凸求解；这里的 seed 指编码器训练来源，不是另抽20组读出随机种子。
- 所有格共用原先已多次查看的固定分区：4184 FIT、1046 HELD；五种子不等于五个独立图像分区。

## 复现了哪些算法，改了哪些基础设施

科学算法按固定 SHA 从包内旧源导入，入口不复制重写其 objective、梯度、特征映射、scaler、L-BFGS求解器或证书计算：

| 资产 | 包内位置 |
|---|---|
| 扩展20格适配器 | `09_scientific_supplement_v1/expanded_probe/expanded_probe_v1.py` |
| 路径支持与合成合同 | `09_scientific_supplement_v1/expanded_probe/portable_support_v1.py` |
| 冻结LP数学核心 | `02_experiments/E07_regularized_linear_probe/source/linear_probe_v1.py` |
| 冻结anchored run_cell | `02_experiments/E08a_native_control_and_old5/source/anchored_probe_v1.py` |
| 十编码器缓存 | `09_scientific_supplement_v1/cache10/` |
| 原20份协议与TRAIN scaler | `09_scientific_supplement_v1/expanded_batch/protocols/`、`scalers/` |
| 十个native TRAIN正控制 | `09_scientific_supplement_v1/native_pc10/` |
| 原结果 | `09_scientific_supplement_v1/expanded_batch/runs/` |

新入口每次另写 `MANUAL_PROTOCOL.json`，只把运行时输入定位到本包内现有文件，把输出定位到新目录；冻结历史协议保持原样。旧窗口和旧控制器不被调用。`INPUT_LINEAGE.json`标明原协议SHA、依赖SHA、新入口SHA及本次创建时间；这是新手动复现，不追认成原预注册。

保留的数值设置：

- `C0=.95S+.05 tr(S)/32 I`；下游只加一次 `epsilon=1e-4`。
- 两种真实RGB翻转的缓存均参与 FIT 变换与scaler：8368样本、每样本2视图、svec维528。
- 每视图以FIT均值中心化，平均L2能量归一化；HELD不参与scaler、λ或停止规则。
- 目标：`CE(mean logits)+0.25[CE(view0)+CE(view1)]+λ/2 (||W||²+||b||²)`；完整W+b共73002维。
- `M=max10 ||theta_native||²`，`λ=min(.001,.02/M)=1.1659571544277561e-8`，20格共用。梯度容差为 `min(1e-6,sqrt(2λ×1e-4))=1e-6`。
- CPU2线程、最多1500迭代、100000函数调用；最终独立完整梯度证书 `||g||²/(2λ)≤1e-4`；native同映射格另查原有TRAIN风险界。
- 保留历史协议的 NumPy2.4.6、SciPy1.17.1、threadpoolctl3.6.0 数值版本约束。换环境若版本不符会明确拒绝；本次交付不私改版本约束。

函数可达、求解收敛、训练充分拟合和主张数学准入是不同条件。gap证书仅证明目标求解精度；不自动证明TRAIN100%，不自动证明泛化。

## 结果和检查

单格目录：

- `MANUAL_PROTOCOL.json`：本次协议；`INPUT_LINEAGE.json`：来源与文件绑定。
- `STDOUT.log` / `STDERR.log`、`MANUAL_EXECUTION.json`：进程、超时、退出码。
- `run/ITERATIONS.jsonl`、`PROGRESS.json`：逐迭代和当前进度。
- `run/COEFFICIENTS.npz`、`TRAIN_SCALER.npz`：新求解系数与scaler。
- `run/COMPLETED.json`：原算法的收敛、gap、TRAIN/历史HELD指标；不满足验收则保留非完成记录。
- `run/FINAL_PREDICTIONS.npz`：本次预测及固定分区身份。

查看进度示例：

```powershell
Get-Content -LiteralPath 'D:\PlantSPD_manual_cross_s3409_Elog_Rraw_01\run\PROGRESS.json'
Get-Content -LiteralPath 'D:\PlantSPD_manual_cross_s3409_Elog_Rraw_01\run\ITERATIONS.jsonl' -Tail 3
```

`--plan-only`仅流式核SHA和读取JSON元数据，不通过NumPy反序列化 FIT/HELD 数组。实际手动复现则会读取原分区标签，优化只用FIT，完成求解后计算原已查看HELD评分。这个入口不将已查看HELD包装成独立确认集。

冻结 `anchored_probe_v1.py` 的旧 `limits` 字段仍有早期四编码器/两种子字样，按原字节保留；本入口的实际范围由新协议的五种子encoder_id和本文件定义，不能据旧文字把20格当成早期八格。

## 整理时验证范围

交付前已运行纯合成合同，以及全部20格的plan-only绑定检查。独立审查另有一次执行偏差：worker路径测试的spy因模块别名不同而未拦截实际求解，意外执行一格 `Eraw → Rlog / seed3409`，并评价原已见HELD。该工件保留在交付偏差记录中，不计论文结果、不计复现验收。进程已退出，原冻结资产未改动。

没有重跑完整20格；老师可执行上面的实际复现命令生成新结果。当前 `--plan-only` 命令本身仍只检查元数据，发生偏差的是审查额外直接调用worker的测试；不能把两者混淆。详见[交付验收记录](teacher_delivery_update_v1/)。

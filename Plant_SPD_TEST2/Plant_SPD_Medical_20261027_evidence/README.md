# Plant_SPD → ISIC2016 医学数据复验

本目录将 `F:\Plant_SPD` 中已完成的论文主线实验迁移到 ISIC2016 皮肤病灶二分类，重新训练并检查原结论是否保持。工作目录、输入缓存、模型、临时文件、日志和报告均位于 F 盘。原始实验包和旧医学数据保持原位。

运行状态以 `results\STATUS.json`、`TRAINING_SUMMARY.json`、`readouts\SUITE_RESULT.json` 为准；最终入口为 `results\REPORT_ZH.md`。这些文件随工作推进更新，README 不把尚未完成的单元写为已完成。`PROGRESS.json` 是高频更新的进度文件；Windows 上避免持续占用该文件，以免阻塞原子替换。

## 数据和划分

- 数据来源：`F:\Plant_Disease\01_datasets\isic2016_task3b`，900 组同图像 ID 的 RGB、分类标签和二值病灶掩码。
- 只使用已修复原划分中的 train630：benign509、malignant121，编码为 0、1。原 val135/test135 共270行排除；历史医学 checkpoint、旧特征和无效结果不作为初始化。
- p0/p1 分区种子10407/10408，各 FIT504 / HELD126；FIT 为408/96，HELD 为101/25。两组 HELD 重叠22图，不能当作独立队列。
- SHA精确重复分组不可拆分。官方 CSV 无患者 ID，不能声称患者独立或临床盲测；旧医学数据在此前研究中已接触。
- 两视图沿用原代码：全图短边256后中心224；原图中央半宽×半高区域执行同样规则。PIL BILINEAR，缓存为 `uint8 [630,2,3,224,224]`；每图同一水平翻转位作用于两视图，随后 ImageNet 归一化一次。掩码仅提供划分的面积软分层，不进入模型。
- 数据细节、患者/近重复限制见 `prepared\DATASET_AUDIT.md`；逐文件 SHA、裁剪几何和排除清单见 `prepared\MANIFEST.json` 及相邻 JSONL。

## 复验范围与108个实际拟合端点

| 单元 | 实际新增拟合端点 | 范围 |
|---|---:|---|
| E01 | 20 | 2分区×5训练seed×Raw/Log |
| E02 | 12 | 16格优化器对照中的4个同配方端点复用本数据E01，另训12格 |
| E05 | 2 | Sqrt参考，p0×2seed |
| 等头族 | 20 | Raw/Log×frozen/joint×5seed |
| A系列 | 8 | A0、A、A2三seed、A2prime、A3、A4-Log |
| E06 | 8 | 2seed×2来源编码器×2原型映射 |
| E07 | 8 | 固定lambda=.001仿射读出 |
| 旧锚定读出 | 8 | 独立重算两seed共用lambda并重拟合 |
| 五seed锚定读出 | 20 | 独立重算五seed共用lambda并重拟合 |
| F2 | 2 | 初始Raw-frozen与等头Log-joint各一个凸证书 |
| 合计 | 108 | 主训练62 + 原型读出8 + 仿射读出36 + F2证书2 |

native代数正控制、交叉拟合温标、T1、谱恒等式、F1/F3/F4和合成测试单独记录，不加进108个模型拟合端点。虚拟E02四个复用格有明确lineage，不被重复计为新训练。

共同设置为官方 ImageNet ResNet18 layer3、256→32固定QR投影、5%迹收缩协方差和epsilon=1e-4。Raw/Log/Sqrt矩阵核及解析反向复用原始源码。原型头与仿射头分别沿用相应实验的损失、初始化、优化器和裁剪；训练seed3407–3411，batch32，每epoch16次更新。默认20epoch；A2prime60epoch且循环原20epoch流。BN running statistics冻结，固定最后epoch，不用HELD选择checkpoint。

样本数、类别数与每epoch更新数变化是显式迁移差异；同epoch预算不等于原植物实验的同更新数。A/A4本轮额外计算HELD指标，此为新增评价，不用于调参。原结论可能不复现；尤其二分类默认已拟合时，不能为制造原“拟合断裂”继续调参。

已读原实验过程、原数字、逐项判读标准与排除的NOT_RUN提案见 `ORIGINAL_EXPERIMENT_INVENTORY.md`、`ORIGINAL_SOURCE_READING_MANIFEST.json`。用户已确认范围：论文主线全部复跑；历史探索分支只做适用性说明。因此完成标准为已完成论文主线E01–E08、等头族及A/F/T1；CRCG、旧分割/RMT/合成估计等异构历史分支列明可迁移性、所缺数据或任务差异，不另行启动训练。

## 环境与盘符

主解释器为 `F:\Plant_Disease\.venv5060\Scripts\python.exe`：Python3.11.2、PyTorch2.11.0+cu128、CUDA build12.8、NumPy2.4.6、Pillow13.0.0。SciPy1.17.1和threadpoolctl3.6.0来自现有 `D:\PlantSPD_work\linear_probe_cross_v1_20261025\cpu_env\Lib\site-packages`。结果绘图使用本项目 `F:\Plant_SPD_Medical_20261027\vendor\matplotlib` 的matplotlib3.11.2及其本地依赖；当前依赖已齐全，无需另外安装。精确版本、模块文件路径和Python基础解释器见 `ENVIRONMENT.json`。

该F盘venv引用C盘已安装的基础Python3.11标准库。少量读取/执行C盘基础运行时不可避免，但工作文件、下载/模型缓存、临时文件、matplotlib配置均指向本目录F盘。`build_results.py`将本项目vendor追加至现有解释器路径，NumPy仍从已验证的F盘训练venv加载，不替换训练环境中的数值库。不要把其他Python版本的二进制site-packages插入训练环境。

## 执行入口

在没有另一条本项目科学计算队列运行时，使用：

```powershell
powershell -ExecutionPolicy Bypass -File F:\Plant_SPD_Medical_20261027\RUN_MEDICAL_REPLICATION.ps1
```

脚本逐阶段串行执行，遇错停止，已完成的训练/读出按其完成凭证复用。它不会覆盖未完成单元目录；发生失败应先保存该尝试并复核原因。也可用 `-Stage Train`、`Readouts`、`F4`、`Diagnostics`、`Results`、`Verify` 指定阶段。`-Stage Prepare` 只在 `prepared\COMPLETE.json` 缺失时准备数据。

实际顺序为：

```powershell
$py = 'F:\Plant_Disease\.venv5060\Scripts\python.exe'
# 仅首次、prepared\COMPLETE.json缺失时：
& $py -B F:\Plant_SPD_Medical_20261027\source\prepare_data.py
& $py -B F:\Plant_SPD_Medical_20261027\source\replication.py --stage train
& $py -B F:\Plant_SPD_Medical_20261027\source\run_readouts.py --stage all --device cuda:0
& $py -B F:\Plant_SPD_Medical_20261027\source\endpoint_gpu_diagnostics.py
& $py -B F:\Plant_SPD_Medical_20261027\source\diagnostics.py --output F:\Plant_SPD_Medical_20261027\diagnostics\final_v1
& $py -B F:\Plant_SPD_Medical_20261027\source\build_results.py
& $py -B F:\Plant_SPD_Medical_20261027\source\verify_final.py
```

`diagnostics.py`要求全新输出目录；重复生成时用 `final_v2` 等新目录，入口脚本自动选择尚不存在的final版本。GPU端点提取应排在主训练和原型读出之后。`run_readouts.py`另外支持native/prototypes/affine/calibration/spectral/f2单阶段，合成测试用 `--stage contracts --device cpu`。

## 输出结构与审计

| 路径 | 内容和schema |
|---|---|
| `prepared\COMPLETE.json` | 准备完成凭证、N/K、输出SHA；`SPLITS.npz`含[2,630] fit/held掩码，`STREAMS.npz`含[10,20,504]样本顺序/翻转 |
| `cache\INITIAL.npz` | 初始协方差[630,2flip,2view,32,32]；按映射/分区固定的FIT双翻转均值和能量尺度 |
| `cache\INIT_p*_s*.npz` | 每个分区/seed的同源原型因子和Raw/Log/Sqrt单位；`INITIAL_BINDING.json`绑定初始缓存 |
| `PLAN.json` | 62个主训练/A单元及原科学核SHA；`TRAINING_SUMMARY.json`为累计完成状态 |
| `runs\<run_id>` | PROTOCOL、INITIALIZATION_BINDING、逐步STEPS、逐epoch EPOCHS、固定终点FINAL_CHECKPOINT、FINAL_PREDICTIONS和COMPLETED/SHA |
| `readouts\native` | 十个新来源端点的原生仿射等价性正控制；不计独立训练 |
| `readouts\prototypes` | 八个冻结来源编码器的新原型头及预测 |
| `readouts\affine` | 36个证书读出：COEFFICIENTS(theta/gradient)、TRAIN_SCALER、ITERATIONS、阈值快照、最终预测和完整证书 |
| `readouts\f2` | 两个同特征凸证书、实际特征和B谱、固定CE需求界、幅度导数诊断；不评价HELD |
| `readouts\calibration` | 四个单元的五折交叉拟合温标、固定fold及argmax不变检查 |
| `diagnostics\F4_ENDPOINTS` | 原始fmap与中心化前tokens的逐图平方和、实际计数、RMS；[model,FIT504,view2] |
| `diagnostics\final_v*` | CPU诊断快照，T1谱、F1/F3末态优化器与轨迹可用性、原结论逐项对账 |
| `results` | 中文报告、CSV/JSON统计和可用图形；STATUS/RESULT_POINTER标记是否完整 |
| `FINAL_QA.json` | CPU独立终检：108实际端点、各文件SHA、固定epoch/step、二分类预测/标签对齐、BN冻结声明与读出证书 |

`VALIDATION_SETUP.json`已有71项CPU合约检查，包含真实RGB视图逐位一致、两视图共同翻转/归一化、原矩阵核梯度、全部train-only初始化、缓存仿射等价性。`diagnostics\F4_SETUP_CONTRACTS.json`核验真实activation AST与RMS聚合。输入绑定检查在主队列启动前补入，并保留启动源码快照；核心科学代码在队列运行期间保持冻结。

本轮批评后的机制登记见 `results\MECHANISM_MODEL.md`。它把 M-E（检验力）、M-A（类数杠杆）、M-B（预算不迁移）、M-C（状态依赖）和 M-D（特征可分性）都保留为 hypothesis，并为每个假设列出置信度、判别器以及支持/削弱规则。认证边界明确为：TRAIN 冻结特征表征/认证读出可达，HELD 泛化未证，非凸端到端可达未证。K=69 初始冻结特征认证已补测为 Raw/Log original/augmented TRAIN F1 全部100%，因此饱和参照已从推断升级为持证事实。TRAIN 等头族配对表与 Plant E01 TRAIN 侧审计分别见 `diagnostics\EQUAL_HEAD_PAIRED_AUDIT.md` 和 `diagnostics\PLANT_E01_TRAIN_PAIRED_AUDIT.md`。零 GPU 诊断见 `diagnostics\ME_POWER_AND_320CURVE.json`、`diagnostics\MECHANISM_ZERO_COST.json`、`diagnostics\MECHANISM_FOLLOWUP_ZERO_COST.json` 和 `diagnostics\MECHANISM_TERMINAL_ZERO_COST.json`；曲线读数显示 Plant Log-joint 在 320 更新时约 2.96% TRAIN、2.53% HELD，320→2620 是慢爬后弯平，更适合写成严重拟合延迟/固定预算截断。K=2 缓存重读出的四种 Raw/Log 差值受界在0–3.72pp，支持 M-A 的读出层成分，但仍不是 ISIC 因果证据，也不把“收窄”写成端到端事实。A2 的 encoder 零更新按 mode=frozen 记为协议常量，不再作为梯度吸收诊断。两个 GPU 窗口的冻结预测见 `results\MECHANISM_PREREGISTRATION.md/json`；本轮没有启动。

一次Windows元数据原子替换错误导致 `E01_0_3408_log` 的首次尝试在写PROGRESS时失败。该尝试完整保存在 `attempts\E01_0_3408_log_metadata_failure_attempt1`；后续从相同初始化、相同seed和相同样本/翻转流重新完整训练，未从无快照的中间epoch伪续训。`attempts\METADATA_RECOVERY_QA.json`已证明重跑前112步loss逐位一致；新增的有界元数据I/O重试只改变写文件容错。失败尝试不计有效端点，不隐藏在最终均值里。

最终解读以全部有效终点和证书为依据。图像bootstrap、训练seed区间和两个重叠分区分别报告；不能把它们混成独立患者数，也不能把TRAIN拟合、谱形状或末态Adam量表述为已识别唯一因果机制。

## 本轮账本更正与证据包

`results\REPORT_ZH.md` 和 `results\MECHANISM_MODEL.md` 已把两种 Plant K=69 配方分开登记：`−0.4143pp` 属原始 fixed69 E01 的 trainable-prototype+encoder 配方（20个完整epoch、2620 updates、2个分区×5个配对seed）；`54.9088%` 与 `25.7443%` 属独立 equal-head affine family 的五种子 @2620 HELD 均值，族内 Raw−Log 为 `+29.1645pp`。二者不能拼接成一个差值或相互贴标签。差值身份四元组（构造K、预算/updates、checkpoint策略、seed结构）已加入 QA 规则4。

可审计证据包位于 `deliverables\Plant_SPD_Medical_20261027_evidence_20261027.zip`，其清单为同目录下的 `Plant_SPD_Medical_20261027_evidence\PACKAGE_MANIFEST.json`。包内含报告、机制登记、诊断、读出证书、源代码、QA 和失败尝试记录；完整训练权重与输入数据仍保留在本目录的 `runs\`、`prepared\`、`cache\` 和 `vendor\`。

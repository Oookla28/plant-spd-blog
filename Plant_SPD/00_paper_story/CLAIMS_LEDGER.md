# 声明—证据台账：当前写作入口

本页分成**当前准入**和**历史 C01–C09 原文**。原九项编号与历史表述保留，不回写为新的事前预测；当前正文优先采用本页上半部及 [证据对账](../12_evidence_reconciliation_v1/EVIDENCE_REGISTER_V1.md)。机器台账保存每个数字的原始文件、JSON键、公式和SHA。本次只是事后证据登记与论文材料整理，没有新增训练或读取HELD标签。

## 当前核心主张

> 默认端到端配方下的训练拟合差异，不能单独用来判定固定表示质量。协方差比较须分别通过数学准入、函数可达、求解收敛和充分拟合检查。

当前证据支持有限配方对**训练拟合**的实质影响；不识别唯一预算／方向／曲率／SNR机制，不新增独立泛化结论。题目采用 **Before Comparing Geometry: Auditing Optimization and Readout in Covariance Pooling**。

## 当前证据ID与原始指针

下列相对路径均从本页所在目录出发。复制进11/12的文件保持原字节和内部绝对路径；旧D路径是原执行来源，包内同名文件是可直接查阅的副本。

| ID | 可以写入论文的内容 | 数字、公式与工件 | 必须保留的边界 |
|---|---|---|---|
| REC-MATRIX-5S | 经审计读出存在来源×映射的条件依赖，F1与NLL偏好不同 | `../09_scientific_supplement_v1/analysis/expanded_probe_final_v1/SUMMARY.json#/per_cell_distributions`及`#/per_seed_effects`；详细20格原文件/SHA：`../12_evidence_reconciliation_v1/subreports/MATRIX_EVIDENCE_V1.json#/records/0` | 5个来源训练seed、20个全新fit；全部TRAIN100%；同一1046张反复开发HELD；有反向seed，不称原配必胜 |
| REC-PROBE-2S | 早期八格作为诊断流程演进 | 上述子报告`#/records/1`，含5接受端点＋3另行恢复端点 | 另一代lambda，不能与新20格混成28格统计；只放附录 |
| REC-NATIVE | 候选仿射族具有被审查的native函数嵌入 | `../12_evidence_reconciliation_v1/subreports/PROBE_CONTROLS_EVIDENCE_V1.json#/entries/0`，逐个控制和修复记录均保留 | 代数和数值等价控制，不是held泛化证书 |
| REC-RISK | 指定native对角格上的TRAIN风险预算 | 同子报告`#/entries/1`；M=1598050.056101633，lambda=min(.001,.02/M)，完整73002维W+b | 预算B=.01约束相对native的TRAIN风险加gap，不是参数范数预算；不移植到另一特征来源 |
| REC-UNDERFIT | 数值收敛与充分拟合是不同验收项 | 同子报告`#/entries/2`；E07 lambda=.001，8格TRAIN F1约19.11–31.89%，完整梯度／gap另验 | 只说明此目标、此配方；不是表征能力上限；E06原型头与E07仿射头分代 |
| REC-TS | 温标大幅压缩本次NLL差距 | `../02_experiments/E03_calibration/temperature_crossfit_v1/RESULT.json#/rows`与`#/contrasts`；gap 1.187902837095→.126558002514；1−新gap/旧gap=89.346098% | 探索性、已查看HELD、四条件齐列；不是89%因果份额或Raw自身NLL降幅 |
| REC-FITPROGRESS | 共同训练预算不保证相同拟合进度 | `../02_experiments/E04_fit_and_clip_diagnostics/MATCHED_TRAIN_CE.json#/threshold_results`；TRAIN CE≤.1首次完整epoch：Raw7–8，Log18–19 | 事后条件分析；不声称排除全部隐式正则或路径差异，保留未达到阈值格 |
| REC-CLIP | 高频裁剪不等于采样实际更新更小 | `../02_experiments/E04_fit_and_clip_diagnostics/CLIP_COEFFICIENT_DIAGNOSTICS.json#/summaries_two_seed_pooled`；Raw60.667939%、Log96.106870%；更新来源`../02_experiments/E02_optimizer_controls/analysis/FINAL_ANALYSIS.json#/rows/*/diagnostics` | 系数全步，更新仅136采样步；不能冒充历史m/v或全路径结论 |
| REC-F2-RAW | 本轮Raw冻结对应特征可被指定仿射族完全分类 | `../11_f1_f4_A_forensics_v1/f2_convex_raw_frozen_v1/RESULT.json#/train_original_unflipped/macro_f1_fixed`与`#/train_augmented/macro_f1_fixed`均1；`#/certificate/gap_bound`约8.65408e−5 | 当前F2代次、明确L2目标；不代表原AdamW能到达，不是成熟E08证书 |
| REC-F2-LOG | 本轮Log joint末期对应特征仍可完全分类 | `../11_f1_f4_A_forensics_v1/f2_convex_log_joint_v1/RESULT.json`同上述键，均1；gap约8.71331e−5 | 只排除这批固定特征在所用仿射族中不可分的解释；不能称表示更优 |
| REC-A-SERIES | 预注册干预大幅改变有限训练拟合 | `../11_f1_f4_A_forensics_v1/F1_F4_FORENSICS.json#/A_primary_cached`、`#/conditional_results`、`#/A4_Log`；逐臂completion见下一表 | 全为FIT/TRAIN；A2′、A3、A4须写共变；不是全单因素，不是泛化证据 |
| REC-B-NONSUFFICIENT | LR总和B不决定跨参数化终点 | `../11_f1_f4_A_forensics_v1/cached_a0_s3407/COMPLETED.json`与`../11_f1_f4_A_forensics_v1/cached_a3_s3407/COMPLETED.json`，`#/actual_LR_budget_B/head`均1.3755；100×两文件`#/train/macro_f1_fixed`之差=52.49675681pp | 非充分性反例，不等于预算完全无关；不拟合统一对数剂量曲线 |

## A系列数字卡

所有F1表中百分数=100×原始`macro_f1_fixed`，原始键保留0–1单位。此处端点来自预定完成点，不挑最好epoch。

| 臂 | 训练F1(%) | 原始工件／键 | 因素与解释范围 |
|---|---:|---|---|
| A0 | 24.177986 | `../11_f1_f4_A_forensics_v1/cached_a0_s3407/COMPLETED.json#/train/macro_f1_fixed` | 缓存匹配对照 |
| A | 24.177986 | `../11_f1_f4_A_forensics_v1/cached_a_s3407/COMPLETED.json#/train/macro_f1_fixed` | 仅删除头部WD；当前配方下直接WD主导解释被削弱 |
| A2 seed3407 | 87.543632 | `../11_f1_f4_A_forensics_v1/cached_a2_s3407/COMPLETED.json#/train/macro_f1_fixed` | 头LR×10 |
| A2 seed3408 | 87.819328 | `../11_f1_f4_A_forensics_v1/cached_a2_s3408/COMPLETED.json#/train/macro_f1_fixed` | 原定关键重复 |
| A2 seed3409 | 88.029062 | `../11_f1_f4_A_forensics_v1/cached_a2_s3409/COMPLETED.json#/train/macro_f1_fixed` | 原定关键重复 |
| A2′ | 53.471598 | `../11_f1_f4_A_forensics_v1/cached_a2prime_s3407/COMPLETED.json#/train/macro_f1_fixed` | 60epoch、访问／更新数与cosine时长共变 |
| A3 | 76.674743 | `../11_f1_f4_A_forensics_v1/cached_a3_s3407/COMPLETED.json#/train/macro_f1_fixed` | 可学温度改变参数化及优化暴露 |
| A4-Log | 89.192864 | `../11_f1_f4_A_forensics_v1/A4_log_actual_v1/RESULT.json#/final_TRAIN/macro_f1_fixed` | 头LR×5＋100step warmup；同seed旧Log baseline36.050169%，不与34.12%跨seed均值相减 |

A2聚合为87.797341%±0.243461pp，公式为三个F1百分数的均值与样本SD（分母3−1）。只衡量相同FIT上的训练种子变化。A4增益53.142695pp的来源链在`F1_F4_FORENSICS.json#/A4_Log`；条件Raw控制按预定恢复门未选择，不填造结果。

## 数学准入、预测与未决项分列

| 编号／状态 | 当前处置 | 权威来源 |
|---|---|---|
| MAF-Q99 | q99×B不是逐坐标全历史硬界；判据退役，不作为经验miss | `../12_evidence_reconciliation_v1/EVIDENCE_REGISTER_V1.json#/mathematical_admission_failures`；原六判据以11中DECISION_TREE_ADDENDUM_V1.md为准 |
| MAF-ONEHOT | 严格分类可正缩放到任意小范数；one-hot最小插值范数不是分类必要下界 | 同上；改用固定CE必要界＋可行射线，不偷换问题 |
| EPM | 仅登记有效且事前可追踪的经验预测未命中；不补称“三次在册miss已核实” | `../12_evidence_reconciliation_v1/EVIDENCE_REGISTER_V1.json#/empirical_prediction_misses`及原A预测表 |
| τ(t) | 字段存在，未找到对应事前定量预测；确证评分显式延期 | `../12_evidence_reconciliation_v1/PENDING_AND_RETIRED_ITEMS_V1.json` |
| 曲线时代三预测 | 正文撤下／被取代，不计EPM；未定位历史“修订#3”不补造 | 同上 |
| 原完整轨迹 | 不可用；新A前瞻轨迹与F4端点不回填旧历史 | `../11_f1_f4_A_forensics_v1/DECISION_TREE_ADDENDUM_V1.md` |

当前不能写“严格预算机制已经被实验证伪”：两项原操作化首先未通过数学准入。合法界及固定CE区间本轮已计算，尚不能唯一确立预算、SNR、方向或曲率。完整说明应在正文Audit Protocol和Discussion，不全部藏进附录。

## 当前稿的术语闸门

- 用“预注册干预”，不用“全部匹配干预／全部单因素”。
- 用“直接WD主导解释在当前配方下被削弱”，不用“WD出局”。
- 用“条件性交互与指标依赖”，不用“刚性原配、联合进化已识别”。
- 用“本地事前冻结、字节核验、事后证据登记”，不称外部可信时间戳／OSF注册。
- 当前F2两批与成熟历史E08分代，旧八格与新20格分lambda，不移植证书、不合并统计。
- 旧E代次重复HELD开发与本轮FIT-only分别披露；F1恢复不等于泛化提升。

## 历史 C01–C09：原文保留，仅作旧代次追踪

以下文字保持原编号与原内容，记录旧材料当时的解释范围；其中“两seed／八格”等指旧代次，**当前主文的五seed／20格以REC-MATRIX-5S为准**。当前允许写法如与历史措辞有冲突，以上半部和12中的NARRATIVE_ADMISSION_V2.md为准。原版本备份在`../07_reproducibility/inventory_archive/20261026T115443Z_before_teacher_update/`。

## 已支持、可以突出写的观察

| ID | 可以使用的强表述 | 对应证据 | 必须同现的范围 |
|---|---|---|---|
| C01 | 固定端到端配方下，Log 的 F1 增益在十个配对中方向一致。 | 20 个 Raw/Log 端点；两划分五种子；平均约 +2.10pp。 | 同一数据池、固定 20 轮；held 重叠；固定模型图像 bootstrap 的两个区间跨零。 |
| C02 | 概率尺度调整大幅压缩 Raw–Log 的 NLL 差距。 | 四冻结模型、五折分组交叉拟合；1.18790→0.12656，缩小 89.3%。 | 同一已查看 held；不是 89.3% 因果贡献，也不是 Raw 自身 NLL 降幅。 |
| C03 | 高频裁剪不能直接当作有效更新受限的计量器。 | Raw/Log 触发约 60.67%/96.11%；采样实际更新出现相反排序。 | 已有采样、指定 AdamW 配方；不能推断全部参数、全部步。 |
| C04 | 共同训练预算不保证不同映射处于相同拟合进度。 | TRAIN CE≤0.1 首次完整 epoch：Raw约7–8，Log约18–19。 | 事后 TRAIN 条件比较；不能排除所有隐式正则或路径差异。 |
| C05 | 求解收敛与充分拟合必须分开审查。 | λ=.001 八格凸 probe 梯度证书通过，但 TRAIN F1约19–31%。 | 只说明此目标、此正则下的表现；不是特征能力上限。 |
| C06 | 新头应先通过 native 函数可达性正控制。 | 四个 native 仿射等价控制，保留微不对称修复审计。 | 基础代数不是新定理；控制通过不保证 held 泛化。 |
| C07 | 经审计的八格读出显示来源与映射的 F1 交互。 | 全部 TRAIN F1=100%、梯度<1e-6、gap<1e-4；两 seed 交互+6.2947/+2.6325pp。 | 两来源种子，同一1046张held；不作显著性、因果或普适性判断。 |
| C08 | F1 与 NLL 对映射的偏好可以不同。 | Raw来源F1偏Raw而NLL偏Log；Log来源两者偏Log。 | 限于本仿射读出族与目标；NLL不是纯校准指标。 |
| C09 | 一个低分交叉头可以制造表征失败的假象。 | 旧原型 Raw/Log held约10.12%，后续审计仿射读出约56.30%均值且充分拟合。 | 两轮头族、目标、训练方式不同；不能把差值解释成单独某个修复的效果。 |

## 当前不能采用的包装与替代写法

| 原拟措辞 | 为什么超出证据 | 可替换为 |
|---|---|---|
| 我们证明广泛接受的隐式正则化和内蕴校准解释均不成立。 | 未核实“广泛接受”；温标和一个 TRAIN CE条件没有排除所有机制。 | 我们检验两类常用解释，并量化仅凭固定预算与未校准损失归因的局限。 |
| 89%的 Log 优势归属于置信度尺度。 | 缩小的是特定 NLL差距；没有因果分解。 | 温标使本次 Raw–Log NLL差距描述性缩小89.3%，而F1不变。 |
| Log拥有完美校准。 | 低NLL不是完美校准；ECE依赖定义且仍非零。 | Log在本设置有较低未校准NLL；温标后的比较改变了差距。 |
| 96%裁剪使模型处于灾难性、极度受限的更新状态。 | 裁剪率不等于更新量；实际采样Log更新未必更小。 | Log在本配方频繁触发裁剪，值得与实际更新一起审查。 |
| 我们首次揭示 Log 的优化病理。 | 谱归一化梯度与数值问题已有文献，未做全面新颖性检索。 | 我们量化本管线的裁剪行为及其与实际更新的不一致。 |
| 二阶矩被污染；Jensen解释了全部分组裁剪收益。 | 历史m/v未保存；缩放摘要不能替代Adam路径分析。 | 裁剪系数分布与更新统计发生变化，底层机制尚未识别。 |
| 刚性表征—度量耦合，流形优势只能在原配兑现。 | 仅两种子条件交互；Raw/Log交叉仍充分拟合；头族已变化。 | 读出效果依赖编码器训练来源，且这种依赖随评价指标变化。 |
| 已证明协同进化是端到端增益的因果来源。 | 冻结probe不干预原训练路径，也不等同原头族。 | 结果支持来源依赖的读出比较，尚未定位端到端增益来源。 |
| TRAIN100%测出纯表征质量/泛化上限。 | 训练可分与留出泛化、正则和读出族仍不同。 | TRAIN充分拟合并通过指定目标证书后，读出比较减少了一类拟合混淆。 |
| Sqrt是最终赢家/首选工程方案。 | 只有两个新增seed；相对Log一胜一负；无跨设置证据。 | Sqrt是本设置中有竞争力的参考，排名仍需更多独立验证。 |
| sqrt在零点导数有界，因此没有数值脆弱性。 | sqrt导数也可在零谱附近无界，只是与log相比更温和。 | 有谱下限时，两类矩阵函数的梯度尺度有不同敏感性。 |
| Log-Euclidean具有一般仿射不变性。 | 与AIRM混淆。 | 本文使用Log-Euclidean映射；不声称其一般仿射不变。 |
| Raw展平破坏拓扑和信息。 | 对称矩阵svec可以保留信息及Frobenius内积。 | Raw和Log诱导不同的比较结构与尺度。 |
| 我们首次证明病害信号主要位于通道关系。 | 缺充分的一阶强基线、病理依据和跨任务证据。 | 本研究检验二阶协方差管线中的映射与读出效应。 |

## 有价值但仍处于假设层的解释

| 假设 | 当前状态 | 要升级必须增加的证据 |
|---|---|---|
| 对数映射通过特定优化轨迹改善表示。 | 合理候选，未因果识别。 | 同头族、等预算与拟合条件的路径干预；独立held验证。 |
| 分组裁剪通过解耦头和编码器改善泛化。 | 有配置差异，无完整机制。 | 预先记录每组实际更新、m/v与输入梯度；针对性干预。 |
| 近零特征值决定高裁剪行为。 | 矩阵函数导数提供数学动机，未分离真实主因。 | 与谱统计联合的时间序列和ε干预；不能用预期曲线代替。 |
| 原生匹配映射是一般读出规律。 | 当前两seed支持方向。 | 更多来源、独立held、头族和正则敏感性验证。 |
| 高质量谱收缩改善小病斑识别。 | RMT/ANS曾出现准入或适用性缺陷，正式收益未形成。 | 先过真实特征准入，再预注册真实分类对照。 |

## 数字核对卡

- “+2.10”单位是 **F1百分点**，不是相对百分比；这是两划分十配对的描述性平均，不是十独立数据集。
- “89.3%”分母是原Raw–Log NLL差距1.18790；新差距0.12656。Raw自身NLL从2.36519到1.28522，不能说Raw NLL降低89%。
- “96.11%”是特定配方的裁剪触发比例，不是梯度丢失比例、有效更新缩小比例或因果贡献。
- “八格”是两编码器来源×两映射×两来源训练seed；不是八个独立数据集。
- “100%”是TRAIN Macro-F1；梯度与gap另有证书，不以100%充当求解停止规则。
- “Sqrt六行”包含两个新增Sqrt训练和四个旧Raw/Log端点，不能说新增六次训练。
- “16格优化控制”含一个旧完整端点carryover和15个新端点；标准全局条件还精确重放了旧配方，不提供独立图像复现。

## 图注的最低要求

每张主图同时写明：数据划分、图像数量、种子数量、头族、训练/冻结状态、指标单位、误差条定义、数据是否事后分析、是否已重复查看held。跨协议拼图必须明确各面板不是一条已识别的因果链。

HEAD_CLIP_WINDOWS只能称“裁剪系数窗口均值与标准差”，不得称梯度方差图、Adam二阶矩图。热图只能称“经审计仿射读出的条件比较”，不得称纯表征上限。温标图保留Raw/Log校准前后四个条件，避免只拿Raw校准后对比Log未校准。

## 投稿前声明闸门

任何“首次”“证明机制”“根本解决”“优于所有方法”“数据无泄漏”“达到某档论文标准”都需要对应证据，不能凭写作偏好放行。已有最终聚合元数据意外暴露及held重复使用应保留原披露。未完成专家复核，不声称病理正确性。

核心原始依据为研究总述EVIDENCE_SOURCES.json所列45项文档及最新FINAL_ANALYSIS.json；此台账是写作解释，不替代它们。

## 交付审查偏差，不属于研究证据

`DELIVERY-DEV-001`：本次项目整理的独立审查中，调用路径spy拦截失效，意外触发一格真实交叉读出及原已见HELD评价。该进程已退出；原科学档案未改写。产物仅为审查偏差存证，**不增加REC证据条目、不更新论文数值、不计复现成功或独立确认**。精确时间、输入范围与产物SHA见[偏差记录](../07_reproducibility/teacher_delivery_update_v1/independent_cross_probe_review/REVIEW_EXECUTION_DEVIATION.md)。



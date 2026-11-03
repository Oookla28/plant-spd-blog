# 原始实验流程审计与医学数据复验矩阵

审计日期：2026-10-27（Asia/Shanghai）。原包 `F:/Plant_SPD` 只读；本报告写入新的 F 盘复验目录。扩展阅读清单已覆盖146份过程文档、140个不同内容SHA：00–12中除显式排除的备份/独立数学参考/格式测试之外全部当前Markdown、02中全部非空过程TXT，以及22份相关早期实验指南/完成报告。另读14份核心源码或协议。完全重复文本按SHA链接，3份近似重复的过渡README按完整差异阅读。文档中的历史禁止重启、旧截止时间、draft 和下一步建议属于历史材料，不替代本次用户授权。并未把每篇数学全文、参考论文、历史原始证据或每个Python文件都声明为逐字审阅；清单、排除原因和逐文件SHA见相邻JSON。初版36份过程文档清单保留在diagnostics下。

**已确认执行范围：用户选择论文主线全部换医学数据重跑；退休历史分支仅说明适用性与未执行原因。本次不增加历史分支训练，也不存在待回答的范围问题。** 主线包括E01–E08、五seed20格、等头族、T1、F1–F4及A系列；历史材料用于追溯与解释，不计入本次完成端点。

## 1. 原实验的统一科学对象

- ResNet18 ImageNet 官方权重，仅计算至 layer3（256 通道）；固定 QR 投影 256→32，projection seed=3407。
- 两视图：整图中心视图、中央半幅视图，均为固定 224×224 RGB；不使用 GT 病灶掩码，也不能把中央半幅当专家病灶 ROI。
- 每视图协方差：`C=.95*S+.05*trace(S)/32*I+1e-4*I`，`S` 为 token 的无偏样本协方差。
- Raw / Log / Sqrt 为完整矩阵映射；Log、Sqrt 谱分解及解析 Fréchet 反向为 F64，模型协方差与映射输出为 F32；关闭 AMP/TF32。
- 原型头 `P=B B^T+1e-4 I`，平方 Frobenius 距离，经 TRAIN-only 固定距离单位归一化，再除可学温度。自由仿射头使用保 Frobenius 内积的 svec（528 维，非对角乘 sqrt(2)）。
- 共同损失：`CE(mean(branch logits))+.25*(CE(branch0)+CE(branch1))`。
- 训练主终点固定最终 epoch；不选择 HELD 最佳 epoch。BN running statistics 冻结，joint 时 affine 参数仍可训。
- 原数据：5230 个 TRAIN 图像，69 类；两分区各 4184 FIT / 1046 HELD，HELD 重叠 211 图。训练种子 3407–3411、分区种子 10407/10408。医学任务必须改 K/N 及更新数，不能沿用 69 类维度或原指标分母。

## 2. 已完成主线：全部复验矩阵

| 代次 | 新数据复验组合 | 原科学预算与设置 | 复验地位 |
|---|---|---|---|
| E01 | 2 分区 × 5 seed × Raw/Log =20 | 20 epoch，batch32；AdamW encoder LR1e-4 / head1e-3，WD1e-4，epoch cosine20，global clip5 | 核心现象；报告全部10配对 |
| E02 | p0 × seed3407/3408 × Raw/Log × LR{1,.3} × clip{global,block}=16 | 同 E01，block 每组阈值5/sqrt(2)；实际更新采样 step1–5 与每20步 | 原包1carryover+15新端点；新数据可显式复用4个 E01 同配方端点，另训12格 |
| E03 | p0 seed3407/3408 的4个冻结 Raw/Log 模型 | 5 折组交叉拟合单标量温度；inverseT 范围[.001,1000]，二分70轮；保持 argmax | 概率诊断，无编码器训练 |
| E04 | E01 全20端点日志及 E02 逐步日志 | TRAIN CE 完整 epoch 首次过阈值；主阈值.1、敏感性.05，保留 NOT_REACHED；clip率和实际更新分列 | 事后诊断，无新训练 |
| E05 | p0 Sqrt × seed3407/3408 =2 | 原型初态、损失、预算同 E01；另算 Sqrt TRAIN-only 距离单位；20 epoch | 参考方法，无普适胜出假设 |
| E06 | p0 ×2来源seed×来源编码器 Raw/Log×新原型头 Raw/Log =8 | 编码器冻结；原始初态 B，而非学成 B；每来源/映射重算原图 FIT 距离单位；head AdamW1e-3 WD1e-4 cosine20 globalclip5，20epoch | 欠拟合诊断代次，仍属已完成需复验 |
| E07 | 同 E06 的4来源编码器 × Raw/Log 仿射读出=8 | 零初始化 F64 W+b；TRAIN 两真实翻转 scaler；显式 lambda=.001；L-BFGS，最多1500迭代/100000评估，gtol1e-6 | 强正则收敛与欠拟合分开检查 |
| E08旧八格 | 4个 native 正控制 →2seed×2来源×2读出=8 | `M=max4 ||theta_native||²`，`lambda=min(.001,.02/M)`；零初始化及完整梯度 gap<=1e-4 | 已被20格主表取代，但属于工具演进；单独复验、单独统计 |
| 五seed20格 | 10个新 native 正控制 →5seed×2来源×2读出=20 | 新共同 lambda 按 max10 完整 native W+b 范数确定；20格全部重拟合；不得复制植物 lambda 数字 | 当前交叉读出主结果 |
| 等头族 | p0×5seed×Raw/Log×frozen/joint=20 | 从共同 ImageNet encoder 起步；零 F64 仿射头；固定初始 FIT scaler；encoder1e-4 / head1e-3，WD1e-4；两组各 clip5/sqrt(2)，20epoch | 不是从 E01 学成 encoder 起步 |
| F1/F3 | 五seed×三个等头族条件 Raw-frozen、Raw-joint、Log-joint=15既有端点 | 从实际 optimizer m/v/step、逐步真实 LR 取证；不制造历史缺失轨迹 | 参数预算与末态更新诊断 |
| F2 | seed3407 初始 Raw-frozen 特征、最终等头族 Log-joint 特征各1凸证书 | 保留各自实际 scaler；相同仿射族及显式L2目标；GPU F64 objective + CPU SciPy L-BFGS-B；完整梯度 gap<=1e-4 | 与成熟 E08 编码器证书严格分代 |
| T1 | 共同初始 encoder 的 FIT 两翻转 Raw/Log 实际归一化输入 | 范数、最佳标量拟合及残差、每视图528维协方差谱、双视图/含bias零点 Hessian block | 描述性诊断，不训练新模型 |
| 谱方向诊断 | 10个成熟 E01 encoder×2view×每类1同类+1跨类对 | 原为2760对；医学 K=2 时为80对（如每类均有两图），固定类内前2图；保留相对gap1e-6近简并块 | 恒等式核验与能量描述，不等于判别信息 |
| F4 | seed3407三端点 Raw-frozen/Raw-joint/Log-joint | 同全部原图 FIT、不翻转；实际 fmap 与投影 token 的 global RMS / mean-image RMS分列 | 端点诊断，不能补写历史演化 |

上述拟合单元若不去重，共112个：E01 20 + E02 16 + Sqrt2 + E06 8 + E07 8 +旧锚定8 +新锚定20 +等头族20 + A系列8 + F2 2。native 代数正控制、温标、谱诊断与合成合同不计编码器训练次数；若复用新数据 E01 的4个 E02 baseline，需明确 lineage，不能标作4次独立新训练。

## 3. A系列精确干预

全部主臂 seed3407；A2另固定3408/3409。A 原实验只评价 FIT；若医学复验另报 HELD，应标为本次新增评价，且不据其调参。

| 臂 | 设置 | 原历史实际状态 |
|---|---|---|
| A0 | Raw-frozen 缓存，20epoch，head LR.001 WD1e-4 | 完成，必须与同数据 RGB等头臂对齐 |
| A | 仅头 WD=0 | 完成 |
| A2 | 仅 head LR=.01，20epoch，三个seed3407/3408/3409 | 完成；原追加规则为3407恢复>=10pp |
| A2prime | 60epoch、cosine T_max60；原20epoch数据流循环3次 | 完成；不是A0续训，也不是同LR轨迹重复3次 |
| A3 | 全局逆温度 exp(s)，s初始0，sWD=0且LR同头；W+b+s共同clip5/sqrt(2) | 完成；另报有效系数 exp(s)*(W,b) |
| A4-Log | Log-joint从ImageNet+零头起步；headLR.005，前100步乘 min(1,step/100)，encoderLR1e-4无warmup，20epoch | 完成；头LR与warmup共变，每步后恢复epoch base LR再做epoch scheduler |
| 条件A4-Raw | 仅当Log未达相对同seed默认臂10pp恢复才启用 | 原历史未运行，不应冒称已完成 |

A0原桥接容差：最终 accuracy 和 Macro-F1 绝对差<=1e-12；W/b最大绝对差<=1e-4；所有步loss最大绝对差<=1e-6。医学数据应建立自身相同桥接，不套用植物端点。

## 4. 初始化与数据流不可隐式更改

`prepare_initializations_v1.py.initialize(cov,y,fit,seed,partition,nclasses=K)`：每视图各类 FIT 算术均值协方差 `pp`；`base=chol(pp-eps*I)`；噪声标准差 `.01*sqrt(trace(pp)/32)/sqrt(32)`，由 SHA256(`['prototype_init',seed,partition]`) 前8字节 little-endian RNG 产生；B写F32；以F64重建 `B B^T+epsI` 算 Raw/Log单位。距离单位为所有 FIT→所有K初始原型的正平方距离中位数，各视图/映射固定。Sqrt使用完全相同B另算单位。

原数据流 RNG 为 SHA256(`order|trainingseed|partitionseed`) 与 `augment|...` 前8字节 little-endian，两随机流独立；每epoch完整FIT排列、tail batch保留；每图/epoch一个水平翻转bit，同时应用两视图、共享于配对臂。新的医学内部划分应先固定，再训练；精确重复图必须同组。原 ISIC2016 历史结果已因跨split重复泄漏、全900标签类权重、浅拷贝best、shuffle后分支错位等问题作废，修复源码存在不代表历史有效复训。

医学 ISIC2016 是既往已接触的二分类外领域重复研究，不是旧69类头的独立盲测；若患者/病灶ID不可用，不能把 SHA组称为患者独立。采用原 corrected train630 的决定和外部 holdout隔离由本次数据审计另行记录。

## 5. 原结论及需要逐项比较的指标

| 原观察 | 原数字 | 医学复验判读 |
|---|---|---|
| E01 Log配方优势 | 10/10配对为正，均值约+2.10pp；p0 Raw55.230/Log57.259%，p1 Raw52.888/Log55.068% | 报每配对差、均值/样本SD与图像组区间；不以近似绝对分数当成功要求 |
| 概率尺度 | NLL差1.18790→.12656，收缩89.346%，F1不变 | 数学上正温度应保持argmax；收缩幅度可能不复现，不算89%因果份额 |
| 训练进度 | CE<=.1 Raw7–8epoch/Log18–19，.05 Log全部未达 | 原阈值照用并报告未达；不外插/换阈值追结论 |
| 裁剪和实际更新不同 | Raw触发60.67%/Log96.11%；采样更新不支持Log必更小 | 分别报触发、系数、采样真实AdamW变化 |
| 强正则收敛仍欠拟合 | E07 TRAIN F1约19.11–31.89%，但残差合格 | 必须分别验梯度gap和TRAIN拟合 |
| 新20格可拟合 | 全部TRAIN100%且证书过；F1四组合均值57.5586/56.5013/54.7310/56.9823% | 不预设医学必100%；未收敛和可分不足分别标注 |
| 来源/映射交互非刚性 | Raw来源4/5偏Raw、Log来源4/5偏Log；3411/3410为反例；NLL两来源5/5偏Log | 展示全部seed、F1/NLL简单效应与DID；保留反例 |
| 等头族拟合断裂 | Raw-joint约99.55%、Log-joint34.12%，冻结约24% | 二分类难度不同，可能无断裂，必须如实报告 |
| T1具体排除项 | 归一化RMS比1；Log初始条件数更小 | 总能量归一化为设计性质，不证明表示等价；不得用谱单独推断标签信息 |
| A干预有限配方效应 | A0/A24.178%；A2均87.7973%；A2prime53.4716%；A3 76.6747%；A4 89.1929% | 逐臂与同seed基线配对，若默认已充分拟合可出现天花板效应 |
| 唯一机制未识别 | q99硬界、onehot分类必要范数退役 | 不把数学无效量尺交给新数据判真伪；B=sum LR不是跨参数化充分解释 |

明确不应复述：Log普适优胜、Sqrt最终赢家、原配必胜、已证明SNR/曲率/硬范数天花板、TRAIN100%等于泛化100%。

## 6. 历史分支与尚未完成提案

`06_history/EARLY_RESEARCH_MAP.md` 将 CRCG/DES-AS/动态融合、旧PlantSeg十组与2×2、旧E0/S0三seed、RMT失败、ANS/LW/OAS合成估计、局部支持/ReLU/上下文、冲突证据库、训练健康/共同特征和ISIC旧尝试分别归档。这些不是当前 E01–F/A 的统一性能矩阵：任务/标签/分割IoU/分类F1不同，不可把它们直接接成医学主线实验。

- CRCG冻结十控制、DES-AS/Shapley、旧2×2有历史完成结果，但完整CRCG、有效背景反事实v2、上下文七方法正式分类未运行。
- RMT正式训练非有限loss，无有效性能终点；ANS合成估计完成不等于真实分类收益完成。
- ISIC2018配对交集0、图像包partial，不具备直接运行的完整配对任务。
- 方向性Fréchet实际增益、epsilon剂量、专家病理审查、独立新域确认在原档案是 NOT_RUN/HOLD；本次复验不把它们冒称历史已做。
- 09/10/11子目录有形成时的 NOT_STARTED/RUNNING旧README；以最终COMPLETED/根README/12对账为状态权威，不据旧草稿否定已完成终点。

## 7. 初次 replication.py 只读复核（待root修订回读）

复核对象为2026-10-27当时的 `source/replication.py`；下列是初次快照观察，修复后应另留QA记录。

1. A4每batch显式重设cosine×warmup，因此当前实际使用LR看起来符合数学公式；但未恢复epoch base再scheduler.step，scheduler状态会被warmup污染。应按原实现恢复base，保存scheduler state并核每步实际LR。
2. 当前每个A/A4 epoch均评价HELD，原A为FIT-only；需明确作为本次新增评价，或保持原FIT-only范围。
3. 当前A0尚无缓存对RGB的W/b、全步loss与最终指标桥接门，后续A臂会直接执行。该门是排除缓存算术差异的必要步骤。
4. A3目前只记录aggregate preclip和loss，未保存原A/F所需全头m/v/u历史包络、有效head范数、实际路径/累计LR；默认等头族只含部分坐标仪器化。不能凭此宣称完整复现原机制轨迹。
5. 既有INITIAL.npz直接复用，未核初始cache源码/输入SHA、N/K/shape或split/scaler绑定；input/scientific源码只记录部分hash，缺强制比对。建议新目录完整绑定后运行，防止中断后误接旧缓存。
6. 当前PLAN覆盖RGB/A共62格（E01 20+E02新增12+Sqrt2+equal20+A8）；E06/E07/旧8/新20/F2/温标/F/T1必须由后续队列补齐，62格结束不能标为全部实验完成。

原科学脚本、原模型权重、原科学数据和旧结果在本审计中未修改；没有启动GPU训练。

## 8. 启动快照回读与初次问题的处置

Root确认上述训练修复均在正式完整队列首次启动前完成。已独立读取三个实际源码快照并比较函数AST，结果保存为 `diagnostics/REPLICATION_SNAPSHOT_AST_QA.json`：

- 首次实际启动快照 `replication_launched_snapshot.py`：SHA256 `610a43b8c64da4d50d4de5a16a8b1798e230b99515261e5060b67fc77f79bb13`。
- 元数据恢复快照及当前 `replication.py`：SHA256 `5fd88981104f22531b695e10eeaca101eb1e6a37047d39a091b213316e9e8204`，两者一致。
- 首次快照到恢复快照仅 `write` 包装函数AST改变，复用原Sqrt脚本的Windows共享锁容错；训练函数AST完全一致，科学训练未因恢复改变。
- E01 seed3408 Log曾在第6epoch遭遇WinError5元数据替换失败，该未完成尝试存于 `attempts/E01_0_3408_log_metadata_failure_attempt1`，不计入完成端点或结果均值。后续成功端点须单独有完整COMPLETED与20epoch。
- A4已恢复epoch base LR后再调scheduler；初始cache及数据已有SHA/shape核验；epoch参数范数、A3逐步全头观测和A0新数据桥接门已在正式启动快照中存在。
- A0本次桥接规则为head最大差<=1e-6、F1差<=1e-4、NLL差<=1e-5，和原包accuracy/F1精确门、全步loss门不是逐项同一验收；报告保留两组规则，不能把本次新增gate描述为原四项原样复现。
- 随后已完成原四项桥接阈值的独立回读，见 `diagnostics/A0_ORIGINAL_BRIDGE_QA.json`：TRAIN accuracy/F1差均0，W最大差约7.73749e-7、b约5.93334e-11，全部320步loss最大差约7.69958e-8，`original_bridge_passed=true`。因此A0也通过原始accuracy/F1<=1e-12、W/b<=1e-4、全步loss<=1e-6四项阈值；上述初次验收口径差异现已由实测补齐。
- A/A4额外评价HELD属于已披露的本次协议扩展；未据其选择配方或终点。
- 首次CPU T1脚本因误用 `input/` 而非实际 `prepared/` 路径失败，修正后独立新目录 `diagnostics/T1_initial_CPU_v2` 完成；这是路径修复，无数学/样本/参数变化。初始v1目录不计科学结果。

当前CPU脚本 `source/diagnostics.py` 仅在已完成输出上做矩阵、TRAIN-CE匹配、终点Adam m/v/u、范数/WD预算、T1谱和读出元数据对照；不读RGB、不创建CUDA context。F4真实激活由另一个显式endpoint脚本测量，绝不由协方差trace代替；F2完整梯度证书与需求射线由readout队列单独产生。所有快照都有独立输出目录，部分结果不会冒称全矩阵完成。

实际affine路径回读已完成：`diagnostics/READONLY_PARTIAL_AFFINE_QA/RESULT.json`读取59个完成训练端点，包括25个真实affine checkpoint，全部完整头参数数为2116，CPU末态m/v/u与逐步日志解析均成功。F4当时尚未执行而明记PENDING，未补造结果；最终队列仍需在全部完成后生成独立FINAL_CPU快照。

## 9. 扩展阅读补发现的已完成步骤及范围分流

### 同一当前主线内的补充分析（不增加GPU训练）

1. E03早期另有**TRAIN F1进度匹配**：主阈值95%、敏感性90%/99%，区别于后来E04的CE阈值.1/.5/.05。`source/diagnostics.py`现已同时覆盖两套，首次完整epoch、overshoot、步数、elapsed和NOT_REACHED均单列。
2. E01完成过面积分层和逐类探索：前景<=1%、1%–5%、>5%，以及各类升降；本次CPU脚本已从新数据保存预测、既有前景比例元数据按同门槛计算，空子组明记EMPTY_SUBGROUP、固定K=2，前景比例只用于事后分析，不进入推理。医学病灶面积分层不等于植物小病斑的直接同任务确认。
3. 等头族曾完成3407/3408四个joint任务的logit幅度/选中坐标方向审计。CPU脚本补充全部可用终点的centered-logit mean L2和RMS（分别报告），以及预选坐标 `-g·delta` 和cosine。原始医学训练未保存逐epoch logits时，不能补造完整logit-norm历史。
4. 两批F2的幅度族导数、`B_obs=C-epsI`谱、固定CE射线及必要界均属于已完成主线，不是新候选模型；对应readout队列已纳入。
5. 原E04还含裁剪系数CV、mean/RMS proxy、100step窗和与原始梯度范数相关性。这些是同一日志的派生诊断，不是新的训练单元。主线复验应保留可计算描述，不能用它宣称Adam因果机制。

### 早期完成实验的适用性说明（用户已确认本次不训练）

这些步骤确有历史完成记录，但用户已明确只重跑论文主线，要求对历史分支给出适用性说明。下列任务均不在本次执行范围，不再等待授权或自动追加。当前R18矩阵完成不表示它们已经换数据复验。

| 历史完成实验 | 已读原证据 | 本次不执行的原因及医学适用性 |
|---|---|---|
| 原PlantSeg G0–G9十组pilot，seed3407、5epoch、batch64 | `08_original_source_snapshots/history_f/01_datasets/plantseg/runs/ten_groups_ep5_seed3407/RESULT_NOTE.md`及十组协议/逐组退役决定 | 属于退休的分类/分割/多任务/融合课题，用户本次不选。医学上可另定义G0分类、G1分割、G2多任务等；旧G7仅log-spectrum、旧G9无真实反事实训练、G4非OOF，不能作为现行完整SPD主线的同义替代 |
| 早期E0/S0与普通/扰动2×2、后续三seed E0/S0 | `PLANTSEG_2X2_MECHANISM_PLAN_V2.md`、`FOLLOWUP_ANALYSIS_V1.md`、`INTERVENTION_AUDIT_V1.md`、早期研究地图 | 普通/全图外观扰动×Euclidean/fullLog SPD；原背景干预实际改变整图，保持该实际语义才能复验，不可宣称背景保持病灶不变。修复v2干预清单虽生成但未准入、从未训练 |
| C0/S2冻结输出十项融合筛查、独立reliability gate | `paper/CRCG_FULL_MATRIX_SCREEN_5060_V1.md`、`paper/CRCG_RELIABILITY_HEAD_FULL_5060_V2.md` | 787DEV、3917TRAIN，等权Top1/IoU最强；医学需重新训练对应两分支/生成独立预测池，再按同融合规则比较；不能直接用R18单头协方差结果代替 |
| CRCG-lite实现烟测 | `paper/CRCG_LITE_END2END_PILOT_5060_V1.md` | 16TRAIN/8DEV/16更新，验证有限loss和反传；属于已执行实现测试，不是完整CRCG性能确认 |
| 五分割模型池DES-AS/Shapley离线审计 | `experiments/desas_shapley_audit_v1/DESAS_SHAPLEY_AUDIT_V1.md` | 五模型32coalitions，完整seed3408/3409，904DEV；跨seedIoU约+0.20pp；医学需要对应模型预测池和统一分割指标，当前R18分类矩阵不包含此实验 |
| ANS/LW/OAS/empirical/fixed.05合成估计、独立扩量、ReLU×相关性机制 | `experiments/spd_estimation_stage_a_v1/REPORT.md`与followup/precision报告 | 合成数据不随医学图片变化，重新执行只是数值复验；不同于在医学图像重新训练。18场景92160/1474560估计器组合、ReLU机制737280组合，均不能计医学样本量 |
| 三旧S0模型550TRAIN的真实token/支持/零通道/ANS适用性诊断 | `experiments/spd_estimation_followup_v1_20261025/REPORT.md`、context支持审计 | 可在医学新模型上另定义支持压力诊断，但原d16/N256旧模型与当前d32/R18特征接口不同；原StageC分类没有完成，不能称需要复训的已完成性能对照 |
| 冲突选择器/等预算复核审计 | `experiments/dasfaa_complementarity_v1/REPORT.md` | 3seed同800图，熵80对比熵40+冲突40，结果负；医学需真实双分支预测/错误池，不能拿单R18置信度冒充两分支冲突 |

朴素RMT正式训练因非有限loss无有效端点，ISIC2016旧轮因泄漏等作废、ISIC2018配对0、完整CRCG、有效反事实v2、上下文七方法分类、Aircraft确认、epsilon剂量及全程方向性Fréchet仍未完成。它们与上表的历史已完成实验分开登记；按已确认范围，本次均不执行，不列为“已换数据复验”。

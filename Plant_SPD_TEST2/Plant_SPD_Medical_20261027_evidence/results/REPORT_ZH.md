# ISIC2016 跨数据集复跑结果

状态：完整训练与读出均完成。

本轮将 Plant_SPD 的已完成论文主线实验迁移至 ISIC2016 皮肤病灶二分类，比较哪些结论保持、哪些发生变化。它是跨数据集与跨任务复核；类别数、样本量和难度均改变，不能要求绝对分数相同。

## 数据与可比性

- 仅使用原已修复 TRAIN 池 630 张（良性509、恶性121）；旧 val/test 共270张排除，未使用历史医学权重。
- 内层 p0/p1 各为 FIT504、HELD126（HELD良性101、恶性25），两组HELD重叠22张；精确重复图像分组不跨划分。
- 原 CSV 无患者ID，本次只能检验图像分组结果；该医学域之前已有探索，不能称全新盲测。
- 原图双视图、ImageNet ResNet18到layer3、QR32维、协方差收缩/epsilon、Raw/Log/Sqrt、双视图损失、五种子、batch32、20完整epoch、最终轮选择均继承；A2prime为60轮。
- 新FIT每轮16步、20轮320步，原植物FIT每轮131步/共2620步。本轮匹配epoch配方，不匹配更新次数；以此解释跨任务优化差异。
- 掩码仅用于事前面积分层，不输入分类模型；没有微小于1%病灶样本，无法复核原植物微小病斑分层主张。

## E01 配对训练

| 划分 | Raw HELD Macro-F1（均值±SD） | Log HELD Macro-F1（均值±SD） | Log−Raw | 正方向配对 |
|---|---:|---:|---:|---:|
| p0 | 67.78% ± 6.29pp | 69.09% ± 1.99pp | +1.30pp | 2/5 |
| p1 | 56.32% ± 4.32pp | 56.56% ± 3.32pp | +0.24pp | 3/5 |

两列均值与样本SD严格使用同一组已完成配对种子；未配成对的单臂只进入端点CSV，不进入配对表。单种子不能估计样本SD。

原植物数据描述性均差约 +2.10pp（该数属于原始固定69类 E01：K=69、20个完整epoch=2620 updates、最终第20轮固定检查点、无HELD选轮；2个partition×5个配对seed，默认可训练prototype+encoder模型）；本轮ISIC E01是K=2、20轮=320 updates，已完成 10 对的均差为 **+0.7704pp**，其中 5正、4负、1平。当前 HELD=126 且 seed 级波动较大；该设计下小效应不可分辨，方向一致性检验功效不足。

p0：训练种子条件t区间 [-8.29, +10.90]pp；同图配对bootstrap区间 [-8.25, +9.77]pp（2000次）。两者衡量不同不确定性，均不建立患者独立性。

p1：训练种子条件t区间 [-5.97, +6.44]pp；同图配对bootstrap区间 [-7.41, +7.84]pp（2000次）。两者衡量不同不确定性，均不建立患者独立性。

两个划分的图像组bootstrap区间均跨0；+0.7704pp是本轮观察均差，不能据此宣称稳定的医学域Log优势，也不能把跨0解释为两方法等效。

## 原始病灶面积与类别探索切片

| 原始掩码面积 | p0/p1 HELD图数（类别数） | Raw/Log平均固定K2 F1 | Log−Raw F1 |
|---|---|---|---:|
| ≤1% | 0（0类）/0（0类） | UNAVAILABLE_NO_IMAGES | 不可用 |
| 1%–5%（左开右闭） | 11（2类）/11（2类） | 47.62% / 47.62% | +0.00pp |
| >5% | 115（2类）/115（2类） | 62.17% / 63.07% | +0.90pp |

固定K=2 F1保留缺失类别为零；GT-present balanced accuracy单独统计。≤1%无样本时不能伪造小病灶F1。以上是已有标签/面积元数据的探索性切片，掩码不输入模型；种子复用及分区重叠不增加独立图像数。完整分区表、良性/恶性recall与限制见 [E01_EXPLORATORY_SUBGROUPS.md](E01_EXPLORATORY_SUBGROUPS.md) 和 [JSON](E01_EXPLORATORY_SUBGROUPS.json)。

## 等头族与拟合恢复

| 映射 | 编码器 | TRAIN F1 | HELD F1 |
|---|---|---:|---:|
| raw | frozen（n=5） | 70.83% ± 0.28pp | 65.42% ± 0.87pp |
| raw | joint（n=5） | 99.74% ± 0.35pp | 68.36% ± 3.54pp |
| log | frozen（n=5） | 70.83% ± 0.32pp | 61.44% ± 0.88pp |
| log | joint（n=5） | 60.00% ± 4.98pp | 55.77% ± 4.27pp |

原植物等头族 TRAIN：Raw joint约99.55%、Log joint约34.12%、冻结臂约24%。上表检验这种拟合断裂在医学任务是否仍出现，不能用原绝对数值当作医学任务目标。

| 恢复臂 | seed | TRAIN F1 | HELD F1（补充评价） |
|---|---|---:|---:|
| A | 3407 | 71.09% | 66.50% |
| A0 | 3407 | 71.09% | 66.50% |
| A2 | 3407 | 70.86% | 52.30% |
| A2prime | 3407 | 64.41% | 52.30% |
| A3 | 3407 | 69.41% | 64.35% |
| A2 | 3408 | 70.86% | 52.30% |
| A2 | 3409 | 69.82% | 52.30% |
| A4 | 3407 | 69.16% | 54.59% |

A0先检查缓存与RGB配方一致性。A系列/A4的HELD前向是本轮补充记录；原历史A系列为FIT-only。没有使用HELD调参、挑轮或决定是否执行追加臂。

| 干预 | 同seed基线TRAIN F1 | 干预TRAIN F1 | 配对变化 |
|---|---:|---:|---:|
| A / 3407 | 71.09% | 71.09% | +0.00pp |
| A2 / 3407 | 71.09% | 70.86% | -0.23pp |
| A2prime / 3407 | 71.09% | 64.41% | -6.67pp |
| A3 / 3407 | 71.09% | 69.41% | -1.67pp |
| A2 / 3408 | 70.66% | 70.86% | +0.19pp |
| A2 / 3409 | 70.45% | 69.82% | -0.63pp |
| A4 / 3407 | 51.88% | 69.16% | +17.28pp |

seed3407的Raw-frozen A2、A2prime、A3均未恢复TRAIN F1，三个预定A2种子也没有形成原植物实验的大幅恢复。A2三种子均为mode=frozen，因此encoder零更新是协议常量；可持证的A2残余是head-only未恢复、head有更新且无裁剪。A的去权重衰减臂与A0分类F1相同；不把原域干预收益预设为跨域必然。

A4按同seed3407的Log-joint基线比较：51.88% → 69.16%，恢复+17.28pp。五种子Log-joint的60.00%均值不作为该单seed干预的基线；LR与warmup共同变化，因此不能拆成单独机制贡献。

## 固定特征读出

| 读出阶段 | 完成/认证格数 | TRAIN unflipped F1范围 | HELD F1范围 |
|---|---:|---:|---:|
| fixed_lambda_0p001 | 8/8 | 96.33%–100.00% | 61.38%–74.21% |
| anchored_historical_two_seed | 8/8 | 100.00%–100.00% | 62.60%–76.23% |
| anchored_five_seed | 20/20 | 100.00%–100.00% | 57.05%–76.23% |

新数据五种子共同 λ=4.53717985e-06；仅由新TRAIN native头的完整W+b范数和风险预算得到，没有复用植物数据λ。历史两种子八格与五种子二十格分别重拟合、分别报告。

E06原型交叉头完成 8 格；TRAIN F1范围 44.74%–80.56%。固定预算低分必须同时检查TRAIN残差，不能直接归因于几何错配。

同特征F2独立认证：

- raw_frozen：COMPLETE，TRAIN F1 100.00%，完整梯度范数 9.88e-07。
- log_joint：COMPLETE，TRAIN F1 100.00%，完整梯度范数 7.69e-07。

## 温度与优化诊断

E03原范围两种子四模型的 Raw−Log NLL均差：温度前 +0.549059，五折交叉拟合温度后 +0.035173。每个HELD评估折只用另外四个HELD折的标签拟合温度，保持argmax；这是开发HELD上的概率尺度审计，不是额外独立测试。

E02完整16条件由12个新端点加4个本轮E01同配方端点组成。E04拟合阶段匹配、裁剪和实际更新，T1初态谱、F1/F3预算及Adam状态、F4实际端点激活详见 diagnostics；不能把梯度裁剪阈值当作Adam参数更新上限。

## 统一机制模型与判别实验

以下 M-E、M-A、M-B、M-C、M-D 全部是 hypothesis；置信度是当前先验可信度，不是已识别因果机制。零成本结果与逐项“判别什么/何结果支持什么”见 [MECHANISM_MODEL.md](MECHANISM_MODEL.md)、[ME_POWER_AND_320CURVE.md](../diagnostics/ME_POWER_AND_320CURVE.md)、[MECHANISM_ZERO_COST.md](../diagnostics/MECHANISM_ZERO_COST.md)、[MECHANISM_FOLLOWUP_ZERO_COST.md](../diagnostics/MECHANISM_FOLLOWUP_ZERO_COST.md) 与 [MECHANISM_TERMINAL_ZERO_COST.md](../diagnostics/MECHANISM_TERMINAL_ZERO_COST.md)。

| 假设 | 解释对象 | 当前证据 | 下一步判别 |
|---|---|---|---|
| M-E 检验力不足（中高） | E01 的 5/4/1 与 +0.77pp | n=10 配对差 SD=6.16pp、SE=1.95pp；2pp 功效约15.1%，区间跨零。当前有算术支持。 | 增加有效图像/配对，或仅把 E01 登记为不可分辨；不写成方向失败。 |
| M-A 类数杠杆（中；读出层成分中高，ISIC因果未判） | Plant fixed69 E01 的 +2.1044pp HELD 与 ISIC K=2 E01 的 +0.7704pp | Plant K=69 缓存做 K=2 读出时，四种标签构造的 Raw/Log 差受界在0–3.72pp；这是跨域读出相容证据，不把“收窄”升级为ISIC端到端事实。等头affine族在K=69 @2620反而 Raw−Log HELD=+29.1645pp，不能与E01 prototype族混为同一机制读数。 | Plant K=2 配对 E01；若同域也收缩，支持M-A的端到端部分；若保持差异，机制指向编码器/优化层。 |
| M-B 预算不迁移（高，仅算术前提） | A2/A4 幅度、匹配方案依赖 | Plant 20轮=2620步，ISIC=320步；320步时 Plant Log-joint TRAIN≈2.96%、HELD≈2.53%，ISIC equal Log-joint TRAIN≈60.00%、HELD≈55.77%。HELD差距随匹配约为 epoch匹配30.03pp、更新数匹配53.24pp。 | 预注册 LR×100；恢复率≥0.8、平台、或变差分别支持预算主导、混合、或失稳。 |
| M-C 基态衰减/状态依赖（中；裁剪风暴变体限植物侧） | A2/A4、温度臂、恢复率轴 | A2 的 mode=frozen 使 encoder 零更新成为协议常量；可持证残余是 head-only 未恢复、head 有更新且无裁剪。A4 encoder 裁剪5.94%，baseline Log-joint4.06%，不是裁剪风暴。A0/A3头部B均0.168但A3 HELD低2.15pp；稳定性与参数化解释未证因果。 | 比较 LR×100 的裁剪/更新震荡；稳定而不恢复会削弱 M-C，等B而分道支持预算不充分的第二实例。简并吸收需 joint A2 或冻结前 encoder 梯度记录。 |
| M-D 特征可分性尺度（高，仍为 hypothesis） | 强正则96–100%、断裂缩小、A4部分恢复 | 医学 T1 有效秩528、Log参与比46.47/53.76；共同读出20/20 TRAIN100%。跨域静态签名支持，但不识别因果。 | 完成跨域谱/读出对照与同预算配对；不要把线性可分性写成已证明机制。 |

| K=2标签构造（Plant K=69缓存重读出） | support | Raw TRAIN F1 | Log TRAIN F1 | Log−Raw |
|---|---:|---:|---:|---:|
| merge_contiguous_half | 1842/2342 | 71.6165% | 72.5826% | +0.9661pp |
| merge_balanced_support | 2091/2093 | 72.4392% | 73.4939% | +1.0548pp |
| random_pair | 179/102 | 99.6144% | 99.6144% | +0.0000pp |
| one_vs_rest | 3840/344 | 47.8564% | 51.5755% | +3.7191pp |
K=69参照固定为原PlantSPD TRAIN-only端点（n=4184、K=69、未在本诊断重拟合）：Raw 24.1780% 来自 F:\Plant_SPD\11_f1_f4_A_forensics_v1\cached_a0_s3407\COMPLETED.json；Log 89.1929% 来自 F:\Plant_SPD\11_f1_f4_A_forensics_v1\A4_log_actual_v1\RESULT.json；参照差为 +65.0149pp。K=2表同样只有TRAIN读出，无HELD。

K=69初始冻结特征认证已补测：n=4184、K=69、d=528、TRAIN-only two-view free-affine凸读出；Raw/Log original与augmented TRAIN F1均100.0000%，证书gap分别为4.1713e-05/3.8361e-05。这使‘认证层参照因饱和不可测’升级为TRAIN侧已测饱和事实；不授权HELD或端到端可达。详见 diagnostics/K69_INITIAL_READOUT.md。

K阶梯与谱注册已冻结但未运行：K={2,4,8,16,34,69}、contiguous主规则＋support-balanced备选，登记绝对TRAIN F1、饱和标记、CV(d²)与S_beta；冻结方向为：在两条锁定规则（contiguous/support-balanced）的非饱和档，Log−Raw差随S_beta单调放大且S_beta比原始K更有预测力；one-vs-rest的+3.72pp是已知离群/构造效应，不用于证伪该预测；K=69双侧饱和只作ceiling-censored参考。它是CPU读出注册，不替代Plant K=2端到端窗口。

动力学命题已修正：K=2时温度对类权重的局部扰动与标量LR扰动共线，但不等于全局优化严格同构；K≥3时单温度可产生非共线的样本聚合梯度扰动，但并不自动张出完整K−1维空间。

A0/A3的EqualModel没有显式u参数，因此精确kappa=uT不能直接观测；class-difference head norm仅作proxy，A3/A0 proxy-uT约1.2488，未用来冻结LR乘数。详见 diagnostics/A0_A3_UT_PROXY.md。

三数严格标签：ISIC equal Log-joint HELD @320 updates =55.7719%；Plant equal-head affine Log-joint HELD @2620 =25.7443%；Plant equal-head affine Log-joint HELD @320 插值=2.5256%；Plant equal-head affine Raw-joint HELD @2620=54.9088%。因此等头affine族的Raw−Log HELD=+29.1645pp；2.53不是Raw-joint @2620。所有差值另须带构造K、预算、checkpoint策略和seed结构四元组，不能把此组数贴到原始E01 prototype族。

认证授权边界：冻结特征支持TRAIN 100%的认证读出头，这表示TRAIN表征足够且指定凸读出目标可达；证书不授权HELD泛化，也不授权非凸端到端联合训练能到达该解。

等头族（独立 affine-head family，不是原始E01 prototype-head）同臂同seed TRAIN均值：Raw frozen 24.2223%、Raw joint 99.5474%、Log frozen 23.8820%、Log joint 34.1162%；同臂joint−frozen增益为Raw +75.3252pp、Log +10.2342pp。HELD均值：Raw frozen 17.5007%、Raw joint 54.9088%、Log frozen 17.1826%、Log joint 25.7443%；这些是@2620。等头族端到端 @2620 的 Raw−Log HELD = +29.1645pp，TRAIN Raw−Log = +65.4313pp，两个层面方向一致；这不是原始E01的同一头族。详见 diagnostics/EQUAL_HEAD_PAIRED_AUDIT.md。

Plant E01 TRAIN侧补读（身份四元组：K=69 fixed original classes；默认可训练prototype+encoder模型，不是等头affine family；20个完整epoch=2620 updates；最终第20轮固定检查点、无HELD选轮；2个partition×5个matched seeds）：pooled Raw 99.6229%、Log 99.2085%，Log−Raw -0.4143pp；p0 -0.4660pp、p1 -0.3626pp，10/10为负。对应同一身份的HELD均差为+2.1044pp；不要拿等头affine的34.1162/25.7443曲线给这行贴标签。与equal-head frozen差−0.3403pp近重合按巧合处理，不互证；TRAIN与HELD方向不同，净额分解必须并列两侧。详见 diagnostics/PLANT_E01_TRAIN_PAIRED_AUDIT.md。

A2协议边界：三种子均为mode=frozen，encoder零更新首先是协议常量；持证残余是head-only未恢复、head有更新且无裁剪。简并吸收仍是未证机制，需joint A2或冻结前encoder梯度记录。

K=2缓存重读出判决已完成：Plant K=69特征的Raw/Log四种标签构造差值收窄到约0–3.72pp，支持M-A的读出层成分；由于这是跨域只读证据，若同域K=2配对仍保持差异，则机制应转向编码器/优化层，当前不把它写成ISIC因果结论。

曲线判别已完成：Plant p0 Log-joint 在 320 步插值 TRAIN 2.960±0.583%、HELD 2.526±0.483%，最终2620步 TRAIN34.116%、HELD25.744%。320→2620 的 HELD 斜率约由1.96降至0.21pp/100步，属于慢爬后的晚期弯平；没有先到70%后崩落。因此“严重拟合延迟/固定预算截断”比“终态断裂”更稳健，但尚不足以证明不存在未来硬天花板。epoch匹配的ISIC−Plant HELD差约30.03pp，更新数匹配约53.24pp；每句都必须带匹配标签。

A4 warmup 的零成本后果：原植物 Log A4 TRAIN 曲线由step131的1.53%持续升至step2489的89.81%，step2620为89.19%，归档实际head-B=6.630；原数学审计记录的Log裁剪频率约96.11%。这与“warmup保护前期高LR/裁剪段”的解释相容，但不把warmup单独写成已识别因果，也不把96.11%直接归因于A4单臂。

E01 功效的结构性后果：在现有配对SD=6.162pp下，若目标仍是双侧α=.05、80%功效检测+2pp，所需SE约0.71pp，对应约75对配对（约150次端到端训练）；增加少量seed不能把该设计变成精密测量。认证读出因此承担TRAIN侧精密测量仪器的角色，HELD端到端差异仍须按不可分辨边界报告。

温度与B非充分性第二实例：ISIC A0/A3头部重构B均为0.168（320步）；A3共享log_inverse_temperature从0升至0.218322（inverse temperature=1.243988），最终TRAIN/HELD相对A0分别低1.67/2.15pp。等头部预算不保证等结果，支持跨臂的描述性REC-B-NONSUFFICIENT；不单独锁定失稳机制。

损伤/可恢复性两轴：植物frozen/joint起点缺口约24.18/34.12%，同口径恢复率0.8391/0.8310；ISIC equal Log-joint起点缺口约71.09/60.00%，A4 matched-seed恢复率0.3591。起点更健康并不意味着恢复更容易，M-D的“只是更容易”朴素版被削弱；恢复率暂按状态依赖假设登记。

A2/A4 恢复率必须同一基线计算：Plant A2=0.8391、Plant A4=0.8310；ISIC A4 同 seed3407=0.3591。若使用ISIC五种子Log-joint均值，分子也必须改为9.161pp，恢复率为0.2290；17.28/40=0.432混用了单seed分子和均值分母。

两个后续窗口是同一个问题“固定特征已有可认证好头，但head-only SGD没找到：预算不足还是参数化/K路径限制？”的两叉：ISIC LR×100走预算叉（含inverse-temperature ratio=1.2439876923控制臂），Plant K=2配对E01走端到端K叉。冻结预测见 [MECHANISM_PREREGISTRATION.md](MECHANISM_PREREGISTRATION.md)；本次不启动额外GPU训练。窗口预测冻结时必须注明已知先验：它们是相对已入账E01/读出阶梯的增量判别，不得把旧E01重复登记为新确认性结果。

QA规则累计四条：1) matched-seed配对；2) 参照必须同臂同配方同层且绝对水平并列；3) 协议常量不得作为诊断观测量——mode=frozen导致的encoder零更新不能叙述为梯度吸收，若要主张吸收须有joint A2或冻结前encoder梯度记录；4) 每个差值必须带身份四元组（构造K、预算/updates、checkpoint策略、seed结构），缺一不得入账。

## 原数值与医学结果逐项对照

| 观察项 | 原植物实验 | 本次医学复验 | 判读范围 |
|---|---|---|---|
| E01: Log−Raw HELD F1 | +2.104pp；10/10 配对为正 | +0.770pp；5正/4负/1平 | 当前 HELD=126 且 seed 级波动较大；效应在本设计下不可分辨，方向一致性检验功效不足；不等价于两方法等效，也不证明医学域不存在 Log 优势。二分类与69类绝对F1不作同难度比较。 |
| E03: Raw−Log NLL温标前→后 | +1.187903 → +0.126558 | +0.549059 → +0.035173 | 温标保持argmax；差距收缩是概率尺度观察，不是几何因果份额。 |
| 等头族 raw/frozen: TRAIN F1 | 24.22% ± 0.10pp | 70.83% ± 0.28pp | 默认配方拟合差异；任务难度及20轮更新次数均改变。 |
| 等头族 raw/joint: TRAIN F1 | 99.55% ± 0.10pp | 99.74% ± 0.35pp | 默认配方拟合差异；任务难度及20轮更新次数均改变。 |
| 等头族 log/frozen: TRAIN F1 | 23.88% ± 0.12pp | 70.83% ± 0.32pp | 默认配方拟合差异；任务难度及20轮更新次数均改变。 |
| 等头族 log/joint: TRAIN F1 | 34.12% ± 2.20pp | 60.00% ± 4.98pp | 默认配方拟合差异；任务难度及20轮更新次数均改变。 |
| 20格 Eraw/Rraw: HELD F1 | 57.56% ± 1.42pp | 68.34% ± 4.92pp | 同一来源编码器下比较映射；每个端点仍须同时通过TRAIN拟合和完整梯度认证。 |
| 20格 Eraw/Rlog: HELD F1 | 56.50% ± 1.09pp | 65.62% ± 6.67pp | 同一来源编码器下比较映射；每个端点仍须同时通过TRAIN拟合和完整梯度认证。 |
| 20格 Elog/Rraw: HELD F1 | 54.73% ± 1.32pp | 71.47% ± 4.97pp | 同一来源编码器下比较映射；每个端点仍须同时通过TRAIN拟合和完整梯度认证。 |
| 20格 Elog/Rlog: HELD F1 | 56.98% ± 1.31pp | 70.22% ± 2.84pp | 同一来源编码器下比较映射；每个端点仍须同时通过TRAIN拟合和完整梯度认证。 |
| E07: λ=.001 TRAIN F1范围 | 19.11%–31.89% | 96.33%–100.00% | 完整梯度收敛与能否拟合是两个判定；强正则可在最优解处仍欠拟合。 |

原数字直接重读归档CSV/完成收据；来源路径与SHA、机器可读逐项对照见 [ORIGINAL_VS_MEDICAL.json](ORIGINAL_VS_MEDICAL.json)。未完成项目保持待定；没有用原植物分数作为医学任务验收阈值。

## 哪些结论保留、哪些改变

核心配方比较：医学任务的Log−Raw平均差为+0.7704pp，正方向5/10；当前样本量与配对波动下，方向一致性不可分辨；不能把这个结果写成已复现，也不能写成方向性失败。

等头affine族：Raw-joint与Log-joint的TRAIN F1均差为+39.739pp，且@2620 HELD的Raw−Log为+29.1645pp；该族在TRAIN与HELD均为Raw占优。它与原始E01的K=69 prototype-head身份不同，不能把其+29.1645pp HELD差解释成E01的同一效应。本次等头affine的Log-joint仍明显欠拟合，有限预算下的拟合差异方向保留，但差距不能外推为原始E01 prototype-head机制。

成熟编码器的共同λ凸读出：20/20完整梯度认证通过，其中20/20原图TRAIN F1=100%。强正则λ=.001为96.33%–100.00%，没有复现植物域19.11%–31.89%的严重欠拟合；同特征F2的Raw-frozen、Log-joint两组也均认证且TRAIN100%。这区分了固定特征中的可读信息与某种有限预算训练配方的拟合表现；TRAIN可拟合仍不保证HELD泛化。

数学与机制边界继续保留：正温度不改变分类决策，完整梯度证书只认证指定显式L2目标；Adam裁剪阈值不是实际参数更新硬界，onehot最小二乘也不是分类必要范数。

## 保留的失败与恢复记录

训练曾发生 Windows 元数据文件替换 `WinError 5`；该事件发生于 `PROGRESS.json` 写入，不能视为非有限loss、模型失败或OOM。失败尝试及其逐步日志保存在 `../attempts/`，不计作有效终点。对应单元从相同初始化、样本顺序和翻转流重新完整运行；最终统计只读当前 `runs/*/COMPLETED.json`，没有用部分权重补终点。

- E01_0_3408_log_metadata_failure_attempt1：保留失败前 112 步；重跑初始化绑定核验：一致。

详见 [PRESERVED_FAILED_ATTEMPTS.json](PRESERVED_FAILED_ATTEMPTS.json)；恢复仅处理文件写入可靠性，不改变科学配方。

## 工件与复现

- [全部训练端点CSV](training_endpoints.csv)、[配对逐种子CSV](E01_paired.csv)、[配对不确定性JSON](E01_PAIRED_ANALYSIS.json)。
- [原实验逐项清单](../ORIGINAL_EXPERIMENT_INVENTORY.md)、[数据审计](../prepared/DATASET_AUDIT.md)、[设置验证](../VALIDATION_SETUP.json)。
- `../runs/`：每格新协议、初始化SHA、逐步/逐轮日志、最终权重、逐样本logits；`../readouts/`：native控制、E06、三代凸probe、F2与校准。
- `../source/`保存适配代码与启动时快照；`../logs/`保存标准输出和失败；原Plant_SPD科学函数保持不变。
- 本机GPU为RTX5060 Laptop 8GB；编码器训练及E06在CUDA执行，E07/E08及F2使用CPU F64解析目标与SciPy认证。报告汇总、独立QA与文案修订没有启动额外训练或GPU工作。
- 早期CRC G/反事实/RMT/估计器探索与本轮SPD主线不是同一已完成协议，具体退役或不适用项目逐项列在原实验清单；未把它们伪称重训完成。

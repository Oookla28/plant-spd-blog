# 统一机制模型与判别登记

本文件把观测、机制假设和判别实验分开。M-E、M-A、M-B、M-C、M-D 都是 hypothesis；置信度表示先验可信度，不是已识别的因果机制。总括判断是：K 是目前最强的组织变量，但还没有被两个域的实验单独识别为唯一因果。

## 认证授权边界

| 命题 | 证书授权 | 精确含义 |
|---|---|---|
| 冻结特征支持一个 TRAIN 100% 的认证读出头 | ✓ | 表征在 TRAIN 意义上足够，且指定显式凸读出目标可达 |
| 该解的 HELD 泛化同样好 | ✗ | 证书是 TRAIN 侧，不授权泛化结论 |
| 非凸端到端联合训练能到达该解 | ✗ | 这正是默认配方失败与预算/参数化窗口要判别的部分 |

因此认证边界应写成“TRAIN 表征可达、HELD 泛化未证、端到端可达未证”，而不是把表征可达性一并降级为未知。

K=69 初始冻结特征的认证参照已补测并持证：在 `n=4184, K=69, d=528`、8368 个双视图增强行、TRAIN-only 的 two-view free-affine 凸读出中，Raw 与 Log 的 original/augmented TRAIN F1 均为 `100.0000%`，accuracy 均为 `100%`；证书 gap 分别为 `4.1713e-05` 与 `3.8361e-05`。因此“认证层参照因饱和不可测”已升级为 TRAIN 侧已测饱和事实，仍不授权 HELD 或端到端可达。详见 [K69_INITIAL_READOUT.md](../diagnostics/K69_INITIAL_READOUT.md)。

## 动力学命题的精确版本

静态上，若分数只通过 `\beta=1/(uT)` 进入，`(u,T)` 仍有一维规范等价，所有 K 都只直接识别 `uT`。K 的差别在动力学：K=2 时类权重偏差空间是一维，温度对该权重的**局部**扰动与标量学习率扰动共线；这不等于全局优化严格同构，因为概率、Adam 状态、正则和饱和都会随轨迹变化。K≥3 时温度可使不同样本的聚合梯度产生非共线扰动，但一个温度参数不自动张出完整的 K−1 维空间。读出阶梯因此同时登记 `CV(d²)` 和加权 `S_beta=E Var_p(d²)`，而不把 K 当作唯一自变量。

| 假设 | 解释对象 | 当前证据 | 判别实验与判别规则 |
|---|---|---|---|
| **M-E 检验力不足（中高）** | E01 的 5/4/1 与 +0.77pp | 10 对差值 SD=6.162pp，SE=1.949pp，2pp 效应功效约15.1%，95%区间跨零。当前只有统计精度的算术支持。 | 读取 SD、SE、t 区间和目标效应；若小效应仍在噪声内，支持 M-E；不能把 E01 写成方向性失败。 |
| **M-A 类数杠杆（中；读出层成分中高，ISIC因果未判）** | E01 优势缩小、温度/A3 | Plant K=69 缓存做 K=2 读出时，四种标签构造的 Raw/Log 差受界在0–3.72pp；这是跨域只读相容证据，不把“收窄”升级为 ISIC 端到端事实。 | Plant K=2 配对 E01；若同域也收缩，支持 M-A 的端到端部分；若保持差异，机制指向编码器/优化层。 |
| **M-B 预算不迁移（高，仅算术前提）** | A2/A4 幅度、匹配方案依赖 | Plant 20轮=2620步，ISIC 20轮=320步；Plant Log-joint 在320步 TRAIN≈2.96%、HELD≈2.53%，ISIC equal Log-joint 320步 TRAIN≈60.00%、HELD≈55.77%。以HELD计，epoch匹配差约30.03pp，更新数匹配差约53.24pp；幅度随匹配方案改变。预算事实成立，因果尚未成立。 | 预注册 LR×100：恢复率≥0.8支持预算主导；0.4–0.7支持预算与状态混合；低于LR×10支持非单调失稳。 |
| **M-C 基态衰减/状态依赖（中；裁剪风暴变体限植物侧）** | A2/A4、温度臂、恢复率轴 | A2 的 `mode=frozen` 使 encoder 零更新成为协议常量；可持证残余是 head-only 未恢复、head 有更新且无裁剪。A4 encoder clip=5.94%，Log-joint baseline=4.06%，不是裁剪风暴。A0/A3头部B均为0.168但A3 HELD低2.15pp；稳定性/参数化解释仍未证因果。 | 比较 LR×100 的裁剪、实际更新和后期震荡；稳定而不恢复会削弱M-C，等B而分道支持“预算不充分”的第二实例。若要判“简并吸收”，需 joint A2 或冻结前 encoder 梯度记录。 |
| **M-D 特征可分性尺度（高，仍为 hypothesis）** | 强正则96–100%、断裂缩小、A4部分恢复 | 医学初始 T1 有效秩528，Log participation ratio 46.47/53.76；20格共同λ读出20/20 TRAIN100%。这是静态可分性签名，不能单独识别因果。 | 跨域谱/读出对照与同预算配对；若更强线性可分性与更快320步拟合一致，支持 M-D；否则削弱。 |

## 已完成的零训练判别

- **曲线对读**：Plant p0 Log-joint 320步插值 TRAIN 2.960±0.583%、HELD 2.526±0.483%；step262 为 TRAIN 1.973%、HELD 1.782%；step393 为 TRAIN 4.203%、HELD 3.461%；最终2620步 TRAIN34.116%、HELD25.744%。320→2620 的 HELD 斜率从约1.96降到0.21pp/100步，表现为慢爬后的晚期弯平；没有先到70%再后期崩落。因此论文用词应优先写“严重拟合延迟/固定预算截断”，保留“未证明最终硬天花板”的边界。
- **E01 功效**：p0 均值+1.304pp、SD7.730pp、SE3.457pp；p1 +0.237pp、SD4.997pp、SE2.235pp；合并 +0.770pp、SD6.162pp、SE1.949pp。合并约2pp效应的精确功效约15.1%。
- **K=2 只读探针**：Plant K=69 端点特征重编码到二类后，Raw/Log 的 contiguous 与 support-balanced TRAIN Macro-F1 约为0.716–0.735，随机原类 pair 约0.996，one-vs-rest 约0.479–0.516（标签极不平衡）。它们是跨域只读证据，没有ISIC K=69缓存，不能升级为M-A因果结论。
- **K=2 读出层判决**：四种标签构造的 Raw/Log 差分别约为+0.97、+1.05、0.00、+3.72pp，均远小于K=69端点的Raw/Log差；因此支持M-A的读出层成分，但不外推为ISIC端到端因果。若未来Plant同域K=2配对不收窄，机制应转向编码器/优化层。

| K=2标签构造（Plant K=69缓存重读出） | support | Raw TRAIN F1 | Log TRAIN F1 | Log−Raw |
|---|---:|---:|---:|---:|
| merge_contiguous_half | 1842/2342 | 71.6165% | 72.5826% | +0.9661pp |
| merge_balanced_support | 2091/2093 | 72.4392% | 73.4939% | +1.0548pp |
| random_pair | 179/102 | 99.6144% | 99.6144% | +0.0000pp |
| one_vs_rest | 3840/344 | 47.8564% | 51.5755% | +3.7191pp |

K=69参照固定为原PlantSPD TRAIN-only端点（n=4184、K=69、未在本诊断重拟合）：Raw `24.1780%` 来自 `F:\Plant_SPD\11_f1_f4_A_forensics_v1\cached_a0_s3407\COMPLETED.json`；Log `89.1929%` 来自 `F:\Plant_SPD\11_f1_f4_A_forensics_v1\A4_log_actual_v1\RESULT.json`；参照差为 `+65.0149pp`。K=2表同样只有TRAIN读出，无HELD。

## 两叉基线的持证读数

- **等头族同臂同 seed**：这是独立的 affine-head family，不是原始 E01 的 trainable-prototype+encoder 配方。五 seed TRAIN 均值为 Raw frozen `24.2223%`、Raw joint `99.5474%`、Log frozen `23.8820%`、Log joint `34.1162%`；同臂 joint−frozen 增益为 Raw `+75.3252pp`、Log `+10.2342pp`。同 seed/mode 家族的 TRAIN Raw-joint−Log-joint 描述差为 `65.4313pp`；HELD 均值为 Raw frozen `17.5007%`、Raw joint `54.9088%`、Log frozen `17.1826%`、Log joint `25.7443%`，故该 affine-head family 的 @2620 HELD Raw−Log = `+29.1645pp`，TRAIN 与 HELD 同向 Raw 占优。这个三分叉已判为 Raw 占优；“风暴有正则化面”不适用于此 family。详见 [EQUAL_HEAD_PAIRED_AUDIT.md](../diagnostics/EQUAL_HEAD_PAIRED_AUDIT.md)。
- **Plant E01 TRAIN 侧的身份四元组**：10 对 pooled Raw `99.6229%`、Log `99.2085%`，Log−Raw `−0.4143pp`（SD `0.1380pp`，SE `0.0436pp`）；p0 `−0.4660pp`，p1 `−0.3626pp`，10/10 为负。它属于原始 fixed69 E01：`K=69` fixed original classes；可训练 prototype+encoder 默认模型（不是等头 affine family）；20 个完整 epoch = `2620 updates`；最终第20轮固定检查点、无 HELD 选轮；2 个 partition × seeds 3407–3411，Raw/Log 按 partition×seed 配对。对应同一身份的 HELD 均差为 `+2.1044pp`。因此 `−0.4143` 与 affine-head Log-joint `34.1162%` 不在同一配方/头族，不能用后者给前者贴 @320 或 @2620 的“不可容纳”标签，更不能改判为 K=2；这是配方族混淆，不是无处安放的数。与 equal-head frozen 差 `−0.3403pp` 近重合按巧合处理，不互证；TRAIN 与 HELD 方向不同，净额分解必须并列两侧。详见 [PLANT_E01_TRAIN_PAIRED_AUDIT.md](../diagnostics/PLANT_E01_TRAIN_PAIRED_AUDIT.md)。
- **三数预算/臂/层标签**：ISIC equal Log-joint HELD @320 updates=`55.7719%`；Plant **equal-head affine** Log-joint HELD @2620=`25.7443%`；Plant equal-head affine Log-joint HELD @320 插值=`2.5256%`；Plant **equal-head affine** Raw-joint HELD @2620=`54.9088%`。因此该 affine-head family 的 Raw−Log HELD=`+29.1645pp`；`2.53` 不是 Raw-joint @2620，也不是原始 E01 prototype-head 的端点。每个差值还必须带构造 K、预算/updates、checkpoint 策略和 seed 结构四元组。
- **M-C 日志**：A2 三种子均为 `mode=frozen`；head clip=0%，head 有实际更新，encoder update=0 是协议常量，不是 encoder 收到梯度后的诊断观测。A4 encoder clip=5.94%，head clip=0%，Log-joint baseline encoder clip=4.06%。裁剪率是梯度尺度/有效条件性的代理观测，不是 Hessian 条件数本身；裁剪风暴变体限定为植物侧假设。
- **A4 warmup 读数**：原植物 Log A4 曲线从 step131 TRAIN 1.53%持续升至 step2489 89.81%，step2620 89.19%，且归档实际 head-B=6.630；原数学审计记录 Log 裁剪频率约96.11%。这与“前期高LR/裁剪段需要warmup保护”的解释相容，但仍是相容证据，不是warmup单独因果证明，也不把96.11%直接归因于A4单臂。
- **温度与 B 非充分性第二实例**：ISIC A0/A3 的头部重构B均为0.168（320步），A3共享 `log_inverse_temperature` 从0升至0.218322（inverse temperature=1.243988），最终TRAIN/HELD相对A0分别低1.67/2.15pp。等头部预算不保证等结果，支持将B非充分性登记为跨臂描述事实；不单独锁定失稳机制。
- **τ(t) 处置**：A3 的逐步日志在320个optimizer step都保存了共享 `log_inverse_temperature`；它从0升到0.218322。没有逐view/逐branch独立τ，也没有逐步checkpoint文件，只有最终 `FINAL_CHECKPOINT.pt`；终稿只报告共享τ轨迹，不虚构“两侧独立温标”。
- **损伤/可恢复性两轴**：植物 frozen/joint 的起点缺口约24.18/34.12%，恢复率0.8391/0.8310；ISIC equal Log-joint 起点缺口约71.09/60.00%，A4 matched-seed恢复率0.3591。起点更健康与恢复更容易并不同向，M-D的“只是更容易”朴素版本被削弱；恢复率表现为状态依赖假设，而不是配方内禀常数。
- **M-D 静态签名**：医学 Raw/Log participation ratio 为 19.05/31.12 与 46.47/53.76，condition 为 9288/5632 与 1593/1337；医学内部 Log 是 PR 上升、condition 下降的方向。植物最终 raw/log 的谱方向依 view 而变（Log 仅一 view 改善），且时间点和尺度不同，只作描述性对照。

## 恢复率口径

恢复率必须使用同一数据集、映射、encoder mode 和 seed 的基线：

| 臂 | 恢复率 |
|---|---:|
| Plant A2（3 seed，同口径聚合） | 0.8391 |
| Plant A4-Log（seed3407） | 0.8310 |
| ISIC A4（matched seed3407） | 0.3591 |
| ISIC A4（若使用五种子均值基线，分子也改为9.161pp） | 0.2290 |

`17.28/40≈0.43` 混用了单seed分子和五种子均值缺口，不登记为正式恢复率。Plant A4 归档的 actual-B 为6.630；其他理论排程值必须标为理论值。

预算记录也分开保留：ISIC A2 的头部预算约1.68、A4约0.84；Plant A2 归档 actual-B 为13.755，Plant A4 归档 actual-B 为6.630。用户草案中的6.88若要保留，必须标为理论排程值而不是实际观测。

## 后续预注册：同一个 head-only 失败问题的两叉

两个窗口不是互不相关的残余检查，而是同一问题的互斥判别叉：**固定特征已有可认证好头，但 head-only SGD 没找到；失败究竟是预算不足，还是参数化/K 路径限制？**

1. **ISIC LR×100（预算叉）**：把 ISIC head-only 预算从 A2 约 `1.68` 提到约 `16.8`，越过 Plant A2 的 actual-B `13.755`。恢复率≥0.8支持预算伪影；仍平台支持预算路径被排除、转向参数化/简并；更差支持非单调失稳。
   同一窗口追加一个冻结的 inverse-temperature-ratio control：LR multiplier=`1.2439876923`（A3 `exp(log_inverse_temperature)`），若 HELD 相对A0下降≤`−1.15pp`，支持有效步长通道；若下降≥`−0.50pp`，支持残余温度/参数化通道；中间值记为混合。它不是未定义 `uT` 的物理精确乘数。
2. **Plant K=2 配对 E01（端到端 K 叉，4–6 runs）**：若 Raw/Log 差塌缩，支持 K 杠杆的端到端成分；若保持原量级，结合 K=2 读出层已收窄的证据，机制转向编码器/优化层；部分收窄则按两层分账。

在这两个实验完成前，M-A/M-B/M-C/M-D 不升级为已识别机制；M-E 只说明当前设计无法可靠区分小效应。

## 额外 CPU 注册：K 阶梯与 margin 谱

K=69 初始认证已不再是欠账。若要把“K 是代理”进一步改成“margin 谱结构是自变量”，另行注册同一缓存上的 `K={2,4,8,16,34,69}` 读出阶梯：contiguous 主规则＋support-balanced 备选规则；每档同时登记绝对 Raw/Log TRAIN F1、差值、饱和标记、`CV(d²)` 和加权灵敏度 `S_beta=E Var_p(d²)`。冻结的中心预测是：在两条锁定规则（contiguous/support-balanced）的非饱和档，Log−Raw 差随 `S_beta` 单调放大且 `S_beta` 比原始 K 更有预测力；one-vs-rest 的 `+3.72pp` 是已知构造/不平衡离群，不能拿来事后证伪这条预测；K=69 双侧饱和只登记为 ceiling-censored、无剂量信息。这是 CPU 读出注册，不替代 Plant K=2 端到端窗口；冻结预测与饱和处理见 [MECHANISM_READOUT_STAIRCASE_REGISTRATION.md](MECHANISM_READOUT_STAIRCASE_REGISTRATION.md)。

## QA 规则（累计四条）

1. matched-seed 配对：恢复量和恢复率必须使用同 seed、同映射、同 encoder mode 的基线。
2. 参照持证：参照必须同臂、同配方、同层，并与绝对水平并列；禁止用跨臂跨配方拼接参照差。
3. 协议常量不作观测：`mode=frozen` 导致的 encoder 零更新不得被当作梯度诊断；凡引用 encoder/头部行为，必须先引用 mode 字段。若要主张梯度吸收，必须有 joint 训练或冻结前梯度记录。
4. 差值身份四元组：进入账本的每个差值必须同时登记构造 K、预算/updates、checkpoint 选择策略和 seed 结构（包括配对键）；缺一不得入账。不同头族/配方的绝对值不能互相充当参照。该规则直接解决 `−0.4143` 与 `34.1162` 的配方混淆。

## 后续数据集/设计筛选规则

- **R1 离流形**：新域必须在标准化协变量空间中脱离现有域的仿射跨度；否则第三个观察域的 Bayes factor 预期接近1。
- **R2 先验谱**：训练前登记 `CV(d²)` 与加权 `S_beta`，避免事后挑谱变量解释结果。
- **R3 可测窗口**：先做 CPU 认证门控，至少一臂非饱和；固定预算端点不能两侧都贴近0或100。
- **R4 update-matched**：预算主语义统一用更新数，n 与预算标签开跑前冻结。
- **R5 可归并且平衡**：类归并规则预注册，至少 contiguous 主规则加一个备选；每档保留绝对水平与差值。
- **R6 成本排序**：先做同域 K/谱干预，再考虑完整新域复跑；干预端点成本应远低于新域。
- **R7 模态距离只作普遍性探针**：模态差异不能单独立项证明机制，只能在识别设计成立后作为观察域。

证据文件：[K69_INITIAL_READOUT.md](../diagnostics/K69_INITIAL_READOUT.md)、[EQUAL_HEAD_PAIRED_AUDIT.md](../diagnostics/EQUAL_HEAD_PAIRED_AUDIT.md)、[PLANT_E01_TRAIN_PAIRED_AUDIT.md](../diagnostics/PLANT_E01_TRAIN_PAIRED_AUDIT.md)、[A0_A3_UT_PROXY.md](../diagnostics/A0_A3_UT_PROXY.md)、[ME_POWER_AND_320CURVE.json](../diagnostics/ME_POWER_AND_320CURVE.json)、[MECHANISM_ZERO_COST.json](../diagnostics/MECHANISM_ZERO_COST.json)、[MECHANISM_FOLLOWUP_ZERO_COST.md](../diagnostics/MECHANISM_FOLLOWUP_ZERO_COST.md)、[MECHANISM_TERMINAL_ZERO_COST.md](../diagnostics/MECHANISM_TERMINAL_ZERO_COST.md)、[MECHANISM_REPORT_PATCH.md](../diagnostics/MECHANISM_REPORT_PATCH.md)。冻结预测登记见 [MECHANISM_PREREGISTRATION.md](MECHANISM_PREREGISTRATION.md)；K阶梯登记见 [MECHANISM_READOUT_STAIRCASE_REGISTRATION.md](MECHANISM_READOUT_STAIRCASE_REGISTRATION.md)。

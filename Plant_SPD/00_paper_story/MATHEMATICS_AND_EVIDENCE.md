# 数学—代码—证据对应表

本表与根README的M1–M8对应，用于连接证明、实现、已有验收及论文位置。本次只整理现有推导和工件，不运行训练、读出、标签评价或新数值实验。标准数学工具与本项目的经验发现分开定位。

## 1. 数学资产总览

| README编号 | 完成内容及解析地位 | 原推导/实现 | 已有验收与实证接口 | 论文位置 |
|---|---|---|---|---|
| 背景 | SPD收缩、svec等距、Log-Euclidean拉回度量与测地线；标准定义 | [E01 runner](../02_experiments/E01_paired_training/source/runner_v2.py)；[数学附录§0–1](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md) | 模型/svec合同，不主张新度量 | Background |
| M1 | 完整矩阵距离谱—方向精确恒等式，含非交换情形 | [完整证明§1](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md) | `noncommuting_distance_identity_raw/log/sqrt`、同谱异向反例、svec等距 | Background，附录简证 |
| M2 | Fréchet导数、固定SPD矩阵精确算子范数、方向增益、floor上界 | [附录§2](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md)；[floor复核](../09_scientific_supplement_v1/math/MATH_FLOOR_BOUND_REVIEW.md)；E01 `_StableLogm` | 有限差分、重复谱、可达等号、方向能量恒等式；不直接解释裁剪因果 | 诊断工具/附录 |
| M3 | 原型得分嵌入仿射族，类别公共项与gauge | [附录§3.1](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md)；[E08a](../02_experiments/E08a_native_control_and_old5/) | 旧4 native与新10 native控制分代；REC-NATIVE | Audit Protocol |
| M4 | 完整W+b的TRAIN风险预算、强凸梯度gap上界 | [附录§3.2–3.3](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md)；[完整范数核验](../09_scientific_supplement_v1/analysis/GLOBAL_NATIVE_NORM_AUDIT.md) | REC-RISK；旧8格、新20格、本轮F2分别认证 | Audit Protocol及读出结果 |
| M5 | 多类NLL对逆温度凸、正缩放保持argmax | [E03数学合同源码](../02_experiments/E03_calibration/source/math_contracts_geometry_v1.py) | [保存合同](../02_experiments/E03_calibration/proof/MATH_CONTRACTS_GEOMETRY_V1.json)；REC-TS | Probability-scale audit |
| M6 | Adam加权Cauchy、AdamW乘积递推、有效路径界 | [F准入V1](../11_f1_f4_A_forensics_v1/math/MATHEMATICAL_ADMISSION_REVIEW.md)；[V2调度勘误](../11_f1_f4_A_forensics_v1/math/MATHEMATICAL_ADMISSION_CORRECTION_V2.md) | 准入合同、实际LR日志；q99盖帽不通过准入 | Mathematical admission/附录 |
| M7 | argmax缩放反例、固定双view CE必要范数界 | [V2§2](../11_f1_f4_A_forensics_v1/math/MATHEMATICAL_ADMISSION_CORRECTION_V2.md)；[六判据核对](../11_f1_f4_A_forensics_v1/DECISION_TREE_ADDENDUM_V1.md) | 24项V2合同；必要下界和射线可行上界分列 | Mathematical admission/附录 |
| M8 | 尺度/L2、Log增益平移与floor残差、零头Hessian、裁后梯度矩比 | [尺度/正则复核V2](../10_equal_head_T1_audit_20261026/math_scale_regularization_audit_v1/MATHEMATICAL_REVIEW_V2.md)；F准入§4；[历史附录§4](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md) | T1和日志限定适用性；Adam-CV未获定量机制确认 | 辅助分析/Discussion |

合同名称通过JSON的`contracts`数组中`name`字段定位，不用列表下标作跨版本身份。完整经验登记见[证据台账](../12_evidence_reconciliation_v1/EVIDENCE_REGISTER_V1.json)。

## 2. 已有数学合同

### 历史主数学合同

[MATH_CONTRACT_RESULTS_WITH_HISTORY_V2.json](../09_scientific_supplement_v1/math/MATH_CONTRACT_RESULTS_WITH_HISTORY_V2.json)：`/status=PASS`、`/contract_count=30`。对应[verify_math_contracts.py](../09_scientific_supplement_v1/math/verify_math_contracts.py)，包含非交换距离、归一化权重、等距坐标、Fréchet有限差分与可达等号、native等价、全头范数、强凸风险和独立假设反例。

这是当时完成的合成数值合同及所列旧JSON核对，本次没有重新执行。解析结论依赖证明与条件；有限样例检查实现一致性。浮点数值证书不是覆盖舍入误差的机器形式化证明。

### F/A数学准入合同

- [V1合同](../11_f1_f4_A_forensics_v1/math/SYNTHETIC_ADMISSION_CONTRACTS.json)：加权Cauchy、递推、范数/方向反例等；调度示例由V2更正。
- [V2合同](../11_f1_f4_A_forensics_v1/math/SYNTHETIC_ADMISSION_CONTRACTS_V2.json)：`/contract_count=24`，`/actual_B=1.3755`（浮点为1.3755000000000002）、`/actual_rho_known_wd_1e_4=0.9998624594543486`。
- [实际LR元数据](../11_f1_f4_A_forensics_v1/BASIC_B_FROM_LOGS.json)：与逐epoch调度对应，避免名义逐step公式替代真实LR。
- 旧失败尝试及修订manifest保留；V1/V2合同数量不相加称为独立科学实验。

## 3. 风险证书的代次

| 证据 | native与目标 | 机器指针 |
|---|---|---|
| 历史E08 | 4完整73002维native头；M≈1598050.0561，λ≈1.2515252525e−8；8格 | [历史合同](../09_scientific_supplement_v1/math/MATH_CONTRACT_RESULTS_WITH_HISTORY_V2.json)的`historical_audit`；[全头范数审计](../09_scientific_supplement_v1/analysis/GLOBAL_NATIVE_NORM_AUDIT.json) |
| 当前五seed20格 | 10完整native头；M=1715328.897296905，λ=1.1659571544277561e−8；20格全部重拟合 | [BATCH_PROTOCOL.json](../09_scientific_supplement_v1/expanded_batch/BATCH_PROTOCOL.json)的`max_native_norm_squared`、`regularization_lambda`；[SUMMARY.json](../09_scientific_supplement_v1/analysis/expanded_probe_final_v1/SUMMARY.json) |
| 本轮Raw frozen | 初始固定特征、独立F2目标 | [RESULT.json](../11_f1_f4_A_forensics_v1/f2_convex_raw_frozen_v1/RESULT.json)的`certificate/gap_bound`、`train_original_unflipped/macro_f1_fixed` |
| 本轮Log joint末期 | 旧低拟合Log joint末态编码器固定特征、另一次F2目标 | [RESULT.json](../11_f1_f4_A_forensics_v1/f2_convex_log_joint_v1/RESULT.json)的相同键 |

风险预算只在对应native可达且目标一致时使用。完整梯度gap、TRAIN拟合、HELD表现分别报告。等头族AdamW不会自动获得凸证书；显式L2与AdamW解耦WD也不是同一目标。

## 4. 辅助数学的准确适用域

### 实际双视图零头Hessian

设$P=I-\mathbf{1}\mathbf{1}^\top/K$、$\tilde x_v=(x_v,1)$。实际损失为

$$
\ell((z_0+z_1)/2)+.25\ell(z_0)+.25\ell(z_1).
$$

两个仿射头均为零时，块Hessian准确为

$$
H_{vw}=c_{vw}E[\tilde x_v\tilde x_w^\top]\otimes(P/K),
\qquad c_{vv}=.5,\quad c_{v\ne w}=.25.
$$

忽略cross-view块、bias或用中心协方差替代未中心二阶矩会改变结论。该式仅在零头点准确，不能把其谱当全程AdamW可训练性判据。来源：[数学复核V2§1](../10_equal_head_T1_audit_20261026/math_scale_regularization_audit_v1/MATHEMATICAL_REVIEW_V2.md)。

### Log幅度响应和floor

令$a>0$、$C(a)=a^2C_B+\epsilon I$、$C_B\succeq0$、$\epsilon>0$，则

$$
\frac{\partial\log C(a)}{\partial\log a}
=U\operatorname{diag}\left(\frac{2a^2\lambda_i(C_B)}{a^2\lambda_i(C_B)+\epsilon}\right)U^\top.
$$

无floor且矩阵正定时，共同Log位移可以由自由bias重参数化吸收；固定floor时残差依谱和$a$变化。函数等价不保证初始化、优化轨迹、正则及裁剪等价；不能据此指定联合拟合断裂的唯一原因。

### 有符号梯度矩比

当$0<E[Z^2]<\infty$、$E[Z]\ne0$且$CV(Z)=sd(Z)/|E[Z]|$：

$$
\frac{E[Z]}{\sqrt{E[Z^2]}}
=\frac{\operatorname{sign}E[Z]}{\sqrt{1+CV(Z)^2}}.
$$

对$Z=cG$再分离$c$需要独立性等附加条件。真实EMA不同窗口、epsilon、偏差修正和WD仍须保留。历史4.04% proxy和5.57%采样更新窗口不同，不能当作定量机制验证。

## 5. 退役量尺与仍有效的工具

| 内容 | 准入状态 | 论文处理 |
|---|---|---|
| q99×累计LR是全程硬界 | MAF：分位数不覆盖全轨迹 | 退役，合法逐步界保留 |
| one-hot最小范数是分类必要范数 | MAF：argmax正缩放反例 | 退役，固定CE必要界另列 |
| 末态abs(u)判定方向/SNR | 幅度不包含方向或全程历史 | 描述性统计，不唯一归因 |
| 范数平台证明硬天花板 | 余弦LR、方向抵消等也可产生平台 | 保留竞争解释及历史缺失 |
| B相同则终点相同 | A0/A3同B不同F1 | 非充分性反例，不作统一剂量曲线 |

判决以[DECISION_TREE_ADDENDUM_V1.md](../11_f1_f4_A_forensics_v1/DECISION_TREE_ADDENDUM_V1.md)为准。MAF与经验未命中EPM分列；量尺退役不是有效经验假说被实验否证。

## 6. 稿件可以使用的定位

**本研究将SPD距离、局部灵敏度、读出可达性、TRAIN风险预算和优化验收落实为同一协方差管线中的可核查比较条件，并展示缺少这些条件时解释会怎样变化。**

标准恒等式和强凸界不是原创定理；认证可分不是独立泛化；谱灵敏度界不是历史裁剪因果；训练恢复不是唯一机制归因。完整证明与代码使这些范围也可以被核查。

V1 理论核心和10项合同保留为历史快照；论文正文以 [RIGOROUS_AUDIT_THEORY_V2.md](../09_scientific_supplement_v1/math/RIGOROUS_AUDIT_THEORY_V2.md) 为准。V2 补齐了显式正则化目标、正则化偏差、参数 Jacobian 条件和审计拒绝状态，16项 CPU 合同见 [RIGOROUS_AUDIT_CONTRACTS_V2.json](../09_scientific_supplement_v1/math/RIGOROUS_AUDIT_CONTRACTS_V2.json)。两条命题的适用域仍限制在 TRAIN/指定读出族或单样本固定 Jacobian 局部动力学；batch、AdamW、裁剪、HELD 泛化和 K 的唯一因果不由这些证明推出。

## 7. 文献与公式源码

出处、版本和阅读范围见[参考文献库](../13_references/REFERENCES.md)，引用可导入[BibTeX](../13_references/references.bib)。本文和[完整数学附录](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md)均保持Markdown与LaTeX源码。历史[V1准入审查](../11_f1_f4_A_forensics_v1/math/MATHEMATICAL_ADMISSION_REVIEW.md)的预算数字以[V2勘误](../11_f1_f4_A_forensics_v1/math/MATHEMATICAL_ADMISSION_CORRECTION_V2.md)为准；原始文件保持原样。

## 8. V2 可认证审计理论与原创性边界

本轮理论升级不增加一个新的 SPD 距离或新的优化器，而是把比较结论的准入条件写成三个可核查对象：

1. **正则化读出证书。** 使用 \(J_{\lambda,\mathcal H}^\star\) 区分显式 L2 目标和无正则 \(R^\star\)，将 solver gap、正则化偏差和参数范数分别列出；native 参考头只产生 comparator-anchor 证书，不能冒充 \(R^\star\)。
2. **局部秩判据。** 对 one-hot、平方距离 softmax 和固定单样本 Jacobian，证明 K=2 的输出切空间一维；K≥3 时，非目标 margin 不全相等给出输出空间二维来源，参数空间秩2还必须满足 Jacobian 在该二维子空间上保持秩2。batch、AdamW 和 clipping 明确列为反例边界。
3. **拒绝状态的 soundness。** `ACCEPT` 只在对象一致、gap/范数/正则偏差证书齐全、无饱和且观测差超过证书半径时产生；对象不一致返回 `REJECT`，证书不足返回 `INDETERMINATE`。这保证协议不会把未认证的端点差异写成表示最优风险差。

文献边界见 [PRIOR_ART_AND_NOVELTY_BOUNDARIES_V2.md](../09_scientific_supplement_v1/math/PRIOR_ART_AND_NOVELTY_BOUNDARIES_V2.md)。该文件明确把 Alain–Bengio、Hewitt–Liang、conditional probing、Dünner、Agarwala，以及 Chou、Barin-Pacela、Garg 等人的结果保留为先例，把本文贡献限制在固定协方差读出比较的证书化组织和拒绝判定上。V2 CPU合同为16项，结果见 [RIGOROUS_AUDIT_CONTRACTS_V2.json](../09_scientific_supplement_v1/math/RIGOROUS_AUDIT_CONTRACTS_V2.json)。

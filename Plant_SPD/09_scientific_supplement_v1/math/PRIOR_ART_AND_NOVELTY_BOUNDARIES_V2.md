# PRIOR ART AND NOVELTY BOUNDARIES V2

本文件用于限制原创性表述。只记录与当前数学主线直接相关的先前工作，不作完整系统综述。

## 1. 直接近邻

| 方向 | 先前工作 | 已经覆盖 | 本项目不能再声称 | 可保留的差异 |
|---|---|---|---|---|
| Probe 容量与选择性 | Hewitt & Liang, *Designing and Interpreting Probes with Control Tasks*, EMNLP 2019. [ACL](https://aclanthology.org/D19-1275/) | 用随机控制任务区分表示携带的信息与 probe 自身记忆能力 | “只要 probe 得分高就能证明表示好” | 把 probe 族、训练目标、求解 gap 和几何表示比较放入同一个确定性审计证书 |
| 条件 probing | Hewitt et al., *Conditional probing: measuring usable information beyond a baseline*, EMNLP 2021. [ACL](https://aclanthology.org/2021.emnlp-main.122/) | 以 baseline 为条件讨论 representation 中的 usable information | “固定读出准确率就是表示本身的信息量” | 对 SPD 固定读出加入正则化偏差、solver gap 和读出可达条件 |
| 线性读出评估 | Alain & Bengio, *Understanding intermediate layers using linear classifier probes*, ICLR Workshop 2017. [OpenReview](https://openreview.net/forum?id=HJ4-rAVtl) | 线性分类器作为冻结表示诊断工具 | “线性 probe 等于所有下游可用信息” | 明确证书只对指定 \(\mathcal H\)、TRAIN 和冻结 \(\phi\) 成立 |
| 凸优化 gap 证书 | Dünner, Forte, Takáč & Jaggi, *Primal-Dual Rates and Certificates*, ICML 2016. [PMLR](https://proceedings.mlr.press/v48/dunner16.html) | primal/dual gap 作为近似最优性的证书 | “solver gap 证书本身是新的凸优化理论” | 把 gap 证书转化为两个固定表示之间的可归因符号判定 |
| 温度动力学 | Agarwala et al., *Temperature Check: Theory and Practice for Training Models with Softmax-Cross-Entropy Losses*, 2020. [arXiv](https://arxiv.org/abs/2010.07344) | 逆温度影响 softmax 训练动力学和泛化 | “温度影响训练是首次发现” | 在平方距离 softmax 中给出输出切空间的精确 \(K=2\)/多类秩条件，并显式加入参数 Jacobian 保持条件 |
| SPD 矩阵函数导数 | Al-Mohy, Higham & Relton, *Computing the Fréchet Derivative of the Matrix Logarithm and Exponential*, 2013. [SIAM](https://epubs.siam.org/doi/10.1137/120885991) | 矩阵 Log/Exp 的 Fréchet 导数计算与分析 | “Log 的 Fréchet 导数是本项目原创” | 只把导数当作当前管线的灵敏度工具，并保留实际方向与最坏算子范数的区别 |
| 表示—读出动力学分解 | Chou et al., *Two Speeds of Learning: A Representation-Readout Decomposition of Grokking and Double Descent*, 2026. [arXiv](https://arxiv.org/abs/2605.27078) | 将编码器表示学习与分类器读出校准作为两个相互作用的学习过程，并用于解释 grokking 与 double descent | “表示—读出分解本身是本文首次提出”或“训练端点差天然就是表示差” | 本文把分解收紧为固定表示、指定读出和 TRAIN 风险上的可认证符号判定，并显式审计求解缺口、正则化偏差及对象匹配 |
| 线性可访问性与摊销缺口 | Barin-Pacela et al., *Stop Probing, Start Coding: Why Linear Probes and Sparse Autoencoders Fail at Compositional Generalisation*, UAI 2026. [PMLR](https://proceedings.mlr.press/v337/barin-pacela26a.html) | 区分线性表示与线性可访问性，并讨论非线性推断/摊销造成的缺口 | “linear accessibility gap/可访问性缺口是本文原创”或“线性 probe 高分足以推出组合泛化” | 本文不重新定义可访问性；只研究固定 SPD 表示下指定凸读出族的求解—正则化证书，并把缺口写成可检验的审计状态 |
| 线性表示容量界 | Garg, Kleinberg & Peng, *How Many Features Can a Language Model Store Under the Linear Representation Hypothesis?*, COLT 2026. [PMLR](https://proceedings.mlr.press/v336/garg26a.html) | 对线性表示假设下的线性特征容量给出定量上下界 | “表示与线性可访问性的定量理论从本文开始” | 本文不做容量定理；贡献是对一个给定数据集、给定读出族和给定预算提供确定性风险差认证 |

## 2. 本项目真正可主张的增量

本项目不提出新的 SPD 距离，也不提出新的 softmax 或凸优化算法。可主张的增量必须同时满足：

1. **对象特异性**：平方距离 softmax、固定协方差表示和指定读出族；
2. **条件完整**：包括正则化、solver gap、参数范数、Jacobian 秩和评估口径；
3. **可反驳**：存在明确的 `REJECT/INDETERMINATE` 分支与合成反例；
4. **可复核**：证明、CPU 合同和现有 Plant/TEST2 证据之间有一一对应关系。

因此，相关工作的差异不是“第一次把表示和读出分开”，而是把已有的分解思想改造成一个有拒绝分支的确定性审计协议：当表示、读出、评估集或预算不匹配时，协议必须拒绝比较；当缺少 gap、范数或正则化偏差证书时，只能返回 `INDETERMINATE`。

把这四点合在一起，论文贡献应命名为“certified audit protocol / 可认证审计协议”，而非“新的深层 SPD 理论”或“温度—学习率统一定理”。

## 3. 明确禁止的表述

- “Log 在所有协方差任务上普遍更优”；
- “\(K\ge3\) 必然使温度与学习率不共线”；
- “Fisher 灵敏度等于真实 AdamW 更新灵敏度”；
- “native 风险预算就是无正则表示最优风险证书”；
- “TRAIN 读出认证推出 HELD 泛化”；
- “表示—读出分解、线性可访问性或可访问性缺口本身是本文首次提出”；
- “本文给出了线性表示容量或组合泛化的普适定理”；
- “K 阶梯或真实 margin-spectrum 机制已经被验证”。

## 4. 推荐引用位置

正文理论相关工作应先引用 probe 选择性和 conditional probing，再说明本文的差异在于“solver/readout audit”；温度部分引用 Temperature Check，随后明确本文只给出局部、固定 Jacobian 的平方距离 softmax 判据；凸 gap 与矩阵函数导数均作为标准工具引用，不列入原创贡献。

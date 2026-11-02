# RIGOROUS AUDIT THEORY V2

状态：CPU 合同与文献边界补齐版。本文档把项目的数学主张改写为可审计、可证伪的形式；它不把标准凸优化、softmax 微积分或矩阵函数导数冒充原创理论。

## 0. 贡献边界

已有工作已经覆盖了以下相邻工具：

- 线性 probe 的容量控制、随机控制任务和 probe 选择性；
- 以 baseline 为条件的 usable-information probing；
- 凸优化的 primal/dual gap 与强凸梯度证书；
- 逆温度对 softmax 训练动力学和泛化的影响；
- SPD 矩阵函数的 Fréchet 导数。

因此本文不主张重新发现这些工具。本文的可保留贡献是：

1. 把固定表示比较写成一个同时处理正则化偏差、solver gap 和读出族的 TRAIN 归因证书；
2. 对平方距离 softmax 给出 \(K=2\) 的精确一维性、\(K\ge3\) 的 margin 条件与参数 Jacobian 保持条件；
3. 把上述证书嵌入一个带 `ACCEPT / INDETERMINATE / REJECT` 状态的审计协议，并证明接受规则的确定性 soundness。

这些结论只适用于文中明确列出的假设。它们不构成 HELD 泛化定理，也不等价于 batch、AdamW、global clipping 下的训练动力学定理。

## 1. 固定表示与读出目标

给定训练集 \(D_T=\{(x_n,y_n)\}_{n=1}^N\)、固定表示 \(\phi_i\)、读出族

\[
\mathcal H_i=\{h_{i,\theta}:\theta\in\Theta_i\},
\]

其中 \(\Theta_i\) 是非空闭凸集。以下定理还假设 \(F_i\) 在 \(\Theta_i\) 上是 proper、下半连续且有下界；这些条件保证在 \(\lambda_i>0\) 时正则化目标具有最小解（在有限维参数空间中）。定义无正则 TRAIN 风险

\[
F_i(\theta)=\frac1N\sum_{n=1}^N\ell(h_{i,\theta}(\phi_i(x_n)),y_n),
\qquad
R_i^0=\inf_{\theta\in\Theta_i}F_i(\theta).
\]

真实读出若使用 L2 正则，优化目标必须单独记为

\[
J_i(\theta)=F_i(\theta)+\frac{\lambda_i}{2}\|\theta\|_2^2,
\qquad
J_i^\star=\min_{\theta\in\Theta_i}J_i(\theta).
\]

除非另有证明，\(J_i^\star\) 不能写成无正则的 \(R_i^0\)。不同 λ、不同 Θ 或不同损失的证书不能合并成一个共同的 \(R^\star\)。

## 2. 定理 1：正则化读出的可认证归因

### 2.1 代数分解（引理，不主张原创）

若 \(\hat\theta_i\in\Theta_i\)，定义

\[
e_i^0=F_i(\hat\theta_i)-R_i^0\ge0.
\]

则任意两个固定表示满足

\[
F_i(\hat\theta_i)-F_j(\hat\theta_j)
=
(R_i^0-R_j^0)+(e_i^0-e_j^0).
\tag{A1}
\]

这是定义的直接展开。它的价值在于明确：端点差在没有控制 \(e_i^0,e_j^0\) 时不能唯一解释成表示差。

### 2.2 正则化 solver gap 的两种证书

假设 \(F_i\) 凸、\(\lambda_i>0\)，存在无正则最优解 \(\theta_{0,i}^\star\in\arg\min F_i\)，并且

\[
\|\theta_{0,i}^\star\|_2^2\le M_{0,i}.
\]

若求解器输出 \(\hat\theta_i\) 满足

\[
0\le J_i(\hat\theta_i)-J_i^\star\le\delta_i,
\tag{A2}
\]

则

\[
0\le F_i(\hat\theta_i)-R_i^0
\le \delta_i+\frac{\lambda_iM_{0,i}}2.
\tag{A3}
\]

**证明。** 由 \(F_i(\hat\theta_i)\le J_i(\hat\theta_i)\)、(A2) 和正则化最优性，

\[
\begin{aligned}
F_i(\hat\theta_i)-R_i^0
&\le J_i(\hat\theta_i)-R_i^0\\
&\le \delta_i+J_i(\theta_{\lambda,i}^\star)-R_i^0\\
&\le \delta_i+J_i(\theta_{0,i}^\star)-R_i^0\\
&=\delta_i+\frac{\lambda_i}{2}\|\theta_{0,i}^\star\|^2\\
&\le\delta_i+\frac{\lambda_iM_{0,i}}2.
\end{aligned}
\]
证毕。

如果无正则最优解的范数上界未知，仍可对正则化最优解给出安全的比较。令 \(\theta_{\lambda,i}^\star\in\arg\min J_i\)，则

\[
\left|F_i(\hat\theta_i)-F_i(\theta_{\lambda,i}^\star)\right|
\le
\delta_i+\frac{\lambda_i}{2}
\left(\|\hat\theta_i\|^2+\|\theta_{\lambda,i}^\star\|^2\right).
\tag{A4}
\]

这是由

\[
F_i(\hat\theta_i)-F_i(\theta_{\lambda,i}^\star)
=J_i(\hat\theta_i)-J_i^\star
-\frac{\lambda_i}{2}(\|\hat\theta_i\|^2-\|\theta_{\lambda,i}^\star\|^2)
\]

和三角不等式得到的。它不需要把正则化解误写成无正则解。

### 2.3 两个表示的确定性归因界

在 (A3) 的条件下，令

\[
\widehat\Delta_{ij}=F_i(\hat\theta_i)-F_j(\hat\theta_j),
\qquad
\Delta^0_{ij}=R_i^0-R_j^0.
\]

则

\[
\left|\widehat\Delta_{ij}-\Delta^0_{ij}\right|
\le B^0_{ij},
\qquad
B^0_{ij}=\delta_i+\delta_j+
\frac{\lambda_iM_{0,i}+\lambda_jM_{0,j}}2.
\tag{A5}
\]

因此有确定性符号规则：

\[
\widehat\Delta_{ij}>B^0_{ij}\Rightarrow \Delta^0_{ij}>0,
\qquad
\widehat\Delta_{ij}<-B^0_{ij}\Rightarrow \Delta^0_{ij}<0.
\tag{A6}
\]

若 \(|\widehat\Delta_{ij}|\le B^0_{ij}\)，协议必须返回 `INDETERMINATE`，不能把端点差符号写成表示差结论。

当前项目用 native 参数范数计算的 \(M\) 是**比较器风险预算**或 native-anchor 证书；除非另有证明 native 参数就是无正则最优解或给出 \(M_{0,i}\) 的上界，否则它不能直接代入 (A5) 声称 \(R_i^0\) 已被精确认证。

更弱但代码可直接支持的 native-anchor 结论是：对任意可达比较器 \(\bar\theta_i\)，

\[
F_i(\hat\theta_i)
\le F_i(\bar\theta_i)+\delta_i+\frac{\lambda_i}{2}\|\bar\theta_i\|^2.
\tag{A7}
\]

### 2.4 梯度 gap 的使用条件

若 \(\Theta_i=\mathbb R^d\)、\(F_i\) 可微且 \(J_i\) 为 \(\lambda_i\)-强凸，则

\[
J_i(\hat\theta_i)-J_i^\star
\le
\frac{\|\nabla J_i(\hat\theta_i)\|_2^2}{2\lambda_i}.
\tag{A8}
\]

证明来自强凸不等式对 \(\theta_{\lambda,i}^\star\) 的下界，并对 \(\theta_{\lambda,i}^\star-\hat\theta_i\) 完成平方。若优化域有边界，必须使用 projected-gradient 或 normal-cone residual；裸梯度范数不再是一般证书。

### 2.5 TRAIN/HELD 边界

(A1)–(A8) 都是 TRAIN、固定表示、指定读出族的结论。若要转到 HELD，至少需要对每个表示给出统一的

\[
\sup_{h\in\mathcal H_i}|R_H(h;\phi_i)-R_T(h;\phi_i)|\le\gamma_i
\]

界，并把 \(2\gamma_i+2\gamma_j\) 加入归因半径。当前项目没有为联合训练建立该界，因此认证读出不能写成 HELD 泛化定理。

## 3. 定理 2：平方距离 softmax 的局部温度—学习率秩判据

### 3.1 定义

令 \(a(\theta)=(d_1(\theta)^2,\ldots,d_K(\theta)^2)\) 在 \(\theta_0\) 附近可微，\(A=\partial a/\partial\theta\in\mathbb R^{K\times m}\) 为该点固定 Jacobian。对 \(\beta>0\)，

\[
p_\beta=\operatorname{softmax}(-\beta a),
\qquad
L(\theta,\beta)=-y^\top\log p_\beta.
\]

定义纯学习率方向和温度扰动方向为

\[
g_{\mathrm{LR}}=\nabla_\theta L(\theta_0,\beta),
\qquad
g_\beta=\partial_\beta\nabla_\theta L(\theta_0,\beta),
\]

即把温度改变的一阶变化与原梯度方向分开。这个定义不包含 Adam 状态、裁剪、weight decay 或 batch 历史。

静态地，若 \(a_k=d_k^2\)、\(\beta=(uT)^{-1}\)，则 logits 只依赖 \(uT\)。变换

\[
(u,T)\mapsto(u/c,cT),\qquad c>0
\]

保持所有概率不变。因此静态 softmax 不能分别识别 \(u\) 与 \(T\)；下面的区分只讨论局部动力学。

对 \(p_k=\exp(-\beta a_k)/\sum_j\exp(-\beta a_j)\)，直接求导得到

\[
\frac{\partial p_k}{\partial\beta}
=-p_k(a_k-\bar a),
\qquad \bar a=\mathbb E_p[a].
\tag{B0}
\]

于是温度方向的 Fisher 灵敏度为

\[
I_\beta
=\sum_k\frac1{p_k}\left(\frac{\partial p_k}{\partial\beta}\right)^2
=\sum_kp_k(a_k-\bar a)^2
=\operatorname{Var}_p(a).
\tag{B0'}
\]

对 one-hot 交叉熵，

\[
L(\beta)=\beta y^\top a+\log\sum_k e^{-\beta a_k},
\]

因此

\[
L'(\beta)=y^\top a-\bar a,
\qquad
L''(\beta)=\operatorname{Var}_p(a)=I_\beta\ge0.
\tag{B0''}
\]

这里的 \(S_\beta=\operatorname{Var}_p(d_k^2)\) 是输出概率对温度的一阶灵敏度，不是参数更新方向的充分条件；参数 Jacobian 仍需满足 (B5)。

对 one-hot 标签 \(y=e_t\)，令 \(\bar a=p_\beta^\top a\)。则

\[
g_{\mathrm{LR}}=A^\top q,
\qquad
q=\beta(p_\beta-y),
\tag{B1}
\]

\[
g_\beta=A^\top q_\beta,
\qquad
q_\beta=(p_\beta-y)-\beta p_\beta\odot(a-\bar a\mathbf1).
\tag{B2}
\]

两者均属于概率单纯形的切空间 \(\mathbf1^\perp\) 的拉回。

### 3.2 \(K=2\) 的精确一维性

在单样本、固定 \(A\)、有限 \(a_k\)、固定 one-hot 损失的条件下，\(\dim(\mathbf1^\perp)=1\)。因此

\[
\operatorname{rank}[g_{\mathrm{LR}},g_\beta]\le1.
\tag{B3}
\]

若两列均非零，则

\[
|\cos(g_{\mathrm{LR}},g_\beta)|=1,
\]

但余弦的符号不能无条件指定为 \(+1\)。若 \(A^\top\) 消掉该唯一切向，则某一列可能为零，余弦也不定义。

### 3.3 \(K\ge3\) 的 margin 条件与 Jacobian 条件

对 \(K\ge3\)，在 softmax 概率为正的条件下，\(q\) 与 \(q_\beta\) 线性无关，当且仅当至少存在两个非目标类别 \(r,s\ne t\) 满足

\[
a_r\ne a_s.
\tag{B4}
\]

**证明。** 若 \(q_\beta=cq\)，对每个 \(k\ne t\) 有

\[
1-\beta(a_k-\bar a)=c\beta.
\]

右侧与 \(k\) 无关，因此所有非目标 \(a_k\) 必须相等。反之，若所有非目标 \(a_k\) 相等，上式对非目标坐标给出同一比例，目标坐标由两个向量的坐标和为零自动满足同一比例。证毕。

但是 \(B4\) 只发生在输出切空间。参数空间秩二还需要

\[
\operatorname{rank}\left(A^\top\big|_{\operatorname{span}\{q,q_\beta\}}\right)=2.
\tag{B5}
\]

在 \(B4\) 与 \(B5\) 同时成立时，

\[
\operatorname{rank}[g_{\mathrm{LR}},g_\beta]=2.
\tag{B6}
\]

因此“\(K\ge3\) 必然不共线”是错误的；正确命题是：非退化 margin spectrum 提供输出空间的二维来源，而参数 Jacobian 必须保持这两个方向。

### 3.4 必须保留的反例

1. 即使 \(K=69\) 且所有 \(a_k\) 不同，若 \(A\) 的秩为 1，参数梯度仍至多一维。
2. 单样本 \(K=2\) 的结论不能直接推广到 batch：不同样本的 \(A_n\) 不同，\(\sum_nA_n^\top q_n\) 与 \(\sum_nA_n^\top q_{\beta,n}\) 可以不共线。
3. AdamW、global clipping 和有限状态会改变实际参数更新，不能把 \(B3\)–\(B6\) 直接称为优化器级定理。

## 4. 定理 3：带拒绝状态的审计 soundness

定义协议状态

\[
\mathsf{Audit}\in\{\mathsf{ACCEPT},\mathsf{INDETERMINATE},\mathsf{REJECT}\}.
\]

对“固定表示的无正则 TRAIN 风险差”主张，`ACCEPT` 的必要准入项包括：

1. 两侧使用同一 TRAIN 样本、标签、损失和读出族；
2. 表示在读出阶段冻结；
3. \(\lambda_i,\lambda_j\) 和参数 gauge 已登记；
4. 两侧都有可复核的 \(\delta\) 和 \(M_0\) 证书；
5. 评估集、seed、预算和 checkpoint 口径一致；
6. 无 saturation/ceiling-censored 标记；
7. 若涉及无正则目标，正则化偏差已由 (A3) 或独立 \(A_i\) 界控制。

若基本对象不一致，例如评估集、标签、读出族或表示冻结状态不一致，返回 `REJECT`，表示该比较不符合命题定义。若对象一致但 gap、范数、正则偏差或饱和信息缺失，返回 `INDETERMINATE`。

在所有准入项成立且满足 \(A6\) 时，`ACCEPT` 的确定性 soundness 为：输出差异与目标最优风险差同号。若 \(|\widehat\Delta|\le B\)，协议不得输出方向。这个结论是确定性证书，不是抽样意义上的 Type-I error 控制；后者需要额外的概率模型。

## 5. 论文可主张的独特贡献

建议使用如下贡献表述：

> We develop a conservative audit protocol for comparing fixed covariance representations. The protocol separates regularized readout optima from solver and regularization gaps, provides a deterministic sign certificate on TRAIN risk differences, and derives an exact local rank criterion that distinguishes temperature perturbations from scalar learning-rate scaling for squared-distance softmax models. When the required invariants or certificates are missing, the protocol returns an explicit indeterminate/reject state rather than upgrading an endpoint difference into a representation claim.

这段贡献不声称发明矩阵 Log 微分、Fisher 信息、softmax 温度理论或一般凸 gap 证书；它的增量是把这些标准工具组织成同一个、带条件和拒绝规则的协方差几何比较审计协议。

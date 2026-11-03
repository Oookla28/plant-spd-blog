# 数学附录：协方差读出审计的三个标准结论与一个待检验模型

本附录服务于已完成的Raw/Log/Sqrt训练、裁剪诊断和E08读出审计。三个命题是标准矩阵分析或凸优化工具在当前协议中的明确化，不主张这些公式本身为新理论。第四部分只有机制假设，不作定理。数学证明与float64合同分别提供解析依据和实现检查；它们都不替代独立确认实验。

## 0. 与实际代码的接口

当前矩阵维度为32，完整对称矩阵的`svec`维度为528。每个模型有两个图像视图、69类，仿射头包含两个视图的全部权重和偏置：

\[
\theta=\operatorname{pack}(W,b)\in\mathbb R^{2\times69\times(528+1)}
=\mathbb R^{73002}.
\]

`Raw`仍是二阶协方差表征，不是原始RGB，也不是一阶池化。`Log`指Log-Euclidean映射及其Frobenius读出，不是一般仿射不变黎曼度量。完整对称矩阵展平不丢失信息；本文不使用“展平破坏拓扑”的表述。

原冻结实验、阈值、数据和输出不在本附录工作中修改。新增合成合同仅使用固定随机种子的微型矩阵；历史核对仅读取四个JSON，不读取真实图像、checkpoint或未见划分。

## 1. 命题一：完整矩阵距离的谱—方向加权恒等式

设对称矩阵有谱分解
\[
A=U\operatorname{diag}(\lambda_1,\ldots,\lambda_d)U^\top,\qquad
B=V\operatorname{diag}(\mu_1,\ldots,\mu_d)V^\top.
\]
对谱函数\(f\)，定义\(q_{ij}=(u_i^\top v_j)^2\)。则
\[
\boxed{\|f(A)-f(B)\|_F^2
=\sum_{i,j}q_{ij}\big[f(\lambda_i)-f(\mu_j)\big]^2.}\tag{1}
\]

**证明。** 正交性给出\(\sum_jq_{ij}=\sum_iq_{ij}=1\)。另一方面，
\[
\begin{aligned}
\|f(A)-f(B)\|_F^2
&=\operatorname{tr}f(A)^2+\operatorname{tr}f(B)^2
-2\operatorname{tr}(f(A)f(B))\\
&=\sum_i f(\lambda_i)^2+\sum_j f(\mu_j)^2
-2\sum_{ij}q_{ij}f(\lambda_i)f(\mu_j),
\end{aligned}
\]
利用行列和为1展开右侧即得。(1)同时保留特征值和特征方向的作用，不是两个独立非负项“谱误差+方向误差”的普适加性分解。

**归一化细节。** \(Q\)双随机，但\(\sum_{ij}q_{ij}=d\)，不是1。只有
\[
\frac1d\|f(A)-f(B)\|_F^2
=\sum_{ij}\frac{q_{ij}}d\big[f(\lambda_i)-f(\mu_j)\big]^2
\]
才是以\(q_{ij}/d\)为概率权重的凸平均。重复特征值允许不同基选择，单个\(q_{ij}\)可变，但完整加权和不变。

**共享基特例。** 若A和B可同时正交对角化，并在共同方向上配对，则退化为
\[
\|f(A)-f(B)\|_F^2=\sum_i[f(\lambda_i)-f(\mu_i)]^2.
\]
独立排序特征值再做该差值一般不对。相同谱、不同方向即可使仅特征值公式得到0而完整距离非零。

取\(f(t)=t,\log t,\sqrt t\)得到三种映射。共享方向上的微小扰动下，Raw约测绝对变化\(\delta\lambda\)，Log约测相对变化\(\delta\lambda/\lambda\)。Log不是对所有谱位“等权”：相对于绝对特征值扰动，其敏感度是\(1/\lambda\)，小特征值更敏感。

### svec与Frobenius等距

对称矩阵的`svec`保留对角项，将上三角非对角项乘\(\sqrt2\)，因此
\[
\langle\operatorname{svec}(A),\operatorname{svec}(B)\rangle
=\langle A,B\rangle_F.
\]
这解释线性读出中的528维坐标；若只取未经\(\sqrt2\)修正的上三角，就不能保持该内积。

**可核验项与边界。** 合成合同验证非交换矩阵恒等式、共享基特例、同谱异向反例和`svec`等距。真实矩阵上的谱/方向诊断可以检查特定错误模式，但本命题本身不推出“原配一定胜于交叉”，也不证明Log普遍优于Raw。

## 2. 命题二：矩阵函数的局部导数范数与当前谱下界

对\(A=U\operatorname{diag}(\lambda)U^\top\succ0\)，Fréchet导数为
\[
Df_A[E]=U\big[K_f(\lambda)\circ(U^\top EU)\big]U^\top,\tag{2}
\]
其中Loewner矩阵的元素是
\[
(K_f)_{ij}=\begin{cases}
\dfrac{f(\lambda_i)-f(\lambda_j)}{\lambda_i-\lambda_j},&\lambda_i\ne\lambda_j,\\
f'(\lambda_i),&\lambda_i=\lambda_j.
\end{cases}
\]
相等特征值处采用连续延拓，分母接近0不意味着谱函数本身必有该形式的奇点。实现不能直接用不稳定的两个近值相减除法。

在对称矩阵空间、Frobenius诱导范数下，
\[
\boxed{\|D\log_A\|_{F\to F}=\lambda_{\min}(A)^{-1},\qquad
\|D\sqrt{\cdot}_A\|_{F\to F}=[2\sqrt{\lambda_{\min}(A)}]^{-1}.}\tag{3}
\]

**证明。** 正交变换保持Frobenius范数；Hadamard线性算子的诱导范数是最大元素绝对值。Log的非对角差商由均值定理夹在相关两个倒特征值之间，因此最大值在最小特征值的对角项达到。Sqrt的差商可直接写为\(1/(\sqrt{\lambda_i}+\sqrt{\lambda_j})\)，同理。选择\(E=u_{\min}u_{\min}^\top\)即可达到两者最大值。

### 当前协方差构造给出的界

当前输入为
\[
C=0.95\widehat C+0.05\frac{\operatorname{tr}\widehat C}{32}I+10^{-4}I,
\qquad\widehat C\succeq0.
\]
精确算术下
\[
\lambda_{\min}(C)\ge0.05\operatorname{tr}(\widehat C)/32+10^{-4}\ge10^{-4},
\]
故
\[
\|D\log_C\|\le10^4,\quad
\|D\sqrt{\cdot}_C\|\le50,\quad
\frac{\|D\log_C\|}{\|D\sqrt{\cdot}_C\|}
=\frac2{\sqrt{\lambda_{\min}(C)}}\le200.\tag{4}
\]
只有最小特征值恰为floor时才达到这些最松的上限。实际trace收缩常使界更小。这里有量纲、映射归一化及实现精度前提；并非宣称两个全网络梯度相差200倍。Sqrt导数在特征值趋于0时同样无界，只是发散较温和，不应称其在0处有界。

### 上游方向决定实际增益：能直接测的连接点

令\(H\ne0\)为矩阵函数输出处反向梯度在对称矩阵空间上的分量（必要时先对称化）。SPD谱函数的此导数算子对Frobenius内积自伴，因此反向传播也有(2)。定义
\[
p_{ij}=\frac{|(U^\top HU)_{ij}|^2}{\|H\|_F^2}.
\]
此处\(p_{ij}\ge0\)、\(\sum p_{ij}=1\)，但它**通常不是双随机矩阵**，其行列和无需为1。实际局部增益满足
\[
\boxed{\frac{\|Df_C[H]\|_F^2}{\|H\|_F^2}
=\sum_{ij}p_{ij}(K_f)_{ij}^2\le\|Df_C\|^2.}\tag{5}
\]
若上游能量不朝高灵敏方向，实际增益远小于最坏情况。高界只能提出需要记录的诊断量，不能预测96.11%的裁剪率。完整链还包含损失、温度、距离单位、原型、协方差构造和编码器雅可比；原型侧梯度也不能遗漏。

**既有证据。** 当前日志有Raw约60.67%、Log约96.11%的裁剪频率；这与(3)可共同提出谱灵敏度机制假设，不能写“上限200倍解释了96%”。旧checkpoint没有保存完整Adam状态或每批矩阵层上游梯度，不能凭最终谱重构历史层级增益。

**合同。** 以中心有限差分核对(2)，检验重复特征值连续延拓、(3)的可达等号、(4)的floor以及(5)能量恒等式。真实谱/局部反向/参数梯度/裁剪事件的对应图属于需新日志的受控诊断，不得标作已完成。

## 3. 命题三：native可达的TRAIN风险锚定与数值gap

### 3.1 先验证头族包含关系

令\(Z=\phi(C)\)、\(P_c=\phi(P_c^{\mathrm{SPD}})\)，原生每视图得分是
\[
s_c(Z)=-\frac{\|Z-P_c\|_F^2}{uT},\qquad u,T>0.
\]
展开后，\(-\|Z\|_F^2/(uT)\)是类别共同项，不改变softmax。若TRAIN变换为
\(x=(\operatorname{svec}(Z)-\mu)/a\)，\(a>0\)为每视图单一尺度，则可取
\[
w_c=\frac{2a\,\operatorname{svec}(P_c)}{uT},\qquad
b_c=\frac{2\langle\mu,\operatorname{svec}(P_c)\rangle-\|P_c\|_F^2}{uT}.
\tag{6}
\]
两个视图分别应用(6)，其平均logit和分支logit的softmax均可保留。各视图跨类中心化权重/偏置是gauge选择，不改变这些概率；它会改变范数，因此必须先冻结gauge再计算预算。

**浮点对称性修正。** 原缓存原型可能有微小反对称残差。对称输入满足\(\langle Z,P\rangle=\langle Z,\operatorname{sym}P\rangle\)，因此权重使用`svec(sym(P))`，偏置仍保留完整\(\|P\|_F^2\)。既有修订据此使四个native正控制通过，没有提高数值容差。这是实现修正，不是新的分类模型。

### 3.2 TRAIN风险预算结论

设特征冻结，实际优化损失为增广TRAIN上的
\[
L(\theta)=\operatorname{CE}_{\mathrm{dual}}(\theta)
+0.25\big[\operatorname{CE}_{v0}(\theta)+\operatorname{CE}_{v1}(\theta)\big].
\]
所有项使用同一批8368行（4184图各两个冻结flip）、均匀权重、同一仿射特征和标签，故\(L\)是凸函数。定义
\[
J_\lambda(\theta)=L(\theta)+\frac\lambda2\|\theta\|_2^2.
\]
这里正则包括全部权重和偏置，否则不能直接使用以下全参数\(\lambda\)-强凸性。

令\(r\)索引**四个独立native模型**，每个\(\theta_{\mathrm{native},r}\)是完整73002维头。冻结
\[
M=\max_{r\in\{1,2,3,4\}}\|\theta_{\mathrm{native},r}\|_2^2,
\quad
\lambda=\begin{cases}\min(10^{-3},2B/M),&M>0,\\10^{-3},&M=0.\end{cases}\tag{7}
\]
\(M\)既不是参数坐标绝对值最大值，也不是69个类别行范数的最大值；没有按类取max或遗漏69倍的操作。

若在某个同源同映射格，(6)给出native可达参数，并且
\(J_\lambda(\hat\theta)-J_\lambda^\star\le\delta\)，则
\[
\boxed{L(\hat\theta)\le L(\theta_{\mathrm{native},r})+B+\delta.}\tag{8}
\]

**证明。** \(\lambda M/2\le B\)，并且
\[
L(\hat\theta)\le J_\lambda(\hat\theta)
\le J_\lambda(\theta_{\mathrm{native},r})+\delta
\le L(\theta_{\mathrm{native},r})+B+\delta.
\]
这约束相对native增加的TRAIN**损失风险**，不约束参数范数不超过B，也不保证训练准确率100%或任何HELD指标。强凸性还给出
\[
\boxed{J_\lambda(\hat\theta)-J_\lambda^\star
\le\frac{\|\nabla J_\lambda(\hat\theta)\|_2^2}{2\lambda}.}\tag{9}
\]
证明由强凸下界
\(J(y)\ge J(x)+\nabla J(x)^\top(y-x)+\lambda\|y-x\|^2/2\)
对y最小化即可。

### 3.3 与实际记录逐项对接

| 量 | 冻结记录 | 作用 |
|---|---:|---|
| B | 0.01 | TRAIN正则损失预算 |
| M | 1598050.0561016325 | 四个完整native头范数平方的最大值 |
| lambda | 1.251525252518626e-8 | `min(.001,.02/M)`，未用HELD挑选 |
| 完整梯度阈值 | 1e-6 | 与gap预算联立检查 |
| gap许可 | 1e-4 | 实际八格均低于此值 |
| 实际最大数值gap | 约3.6707e-5 | 来自完整梯度重新计算 |
| native风险检查 | 四格通过 | (8)只应用于这些native可达格 |
| TRAIN F1 | 八格均100% | 实测结果，不是命题保证 |

小lambda意味着\(\|\hat\theta-\theta^\star\|\le\|\nabla J\|/\lambda\)的参数距离界仍可较松；不能把较小目标gap说成参数被高精度唯一恢复。当前记录使用float64梯度与目标值，属于**数值收敛证书**，不是有区间舍入误差证明的机器验证。

跨映射格没有自动native可达性保证；八格都能使用(9)，但四格同映射native包含关系才支持(8)。使用同一已反复查看的HELD作评估仍有适应性选择限制，TRAIN-only定lambda不能消除全部研究者选择效应。

## 4. 假设模型：裁剪系数CV与Adam更新不能直接画等号

设某个**标量坐标**的原始梯度为G、裁剪系数C，暂时忽略EMA、偏差修正、分母epsilon和权重衰减。若C与G独立、二阶矩有限且非零，则比值模型给出
\[
\frac{E[CG]}{\sqrt{E[C^2G^2]}}
=\frac{E[C]}{\sqrt{E[C^2]}}
\frac{E[G]}{\sqrt{E[G^2]}}.\tag{10}
\]
对于\(E[C]>0\)，
\[
\rho_{\mathrm{toy}}=\frac{E[C]}{\sqrt{E[C^2]}}
=\frac1{\sqrt{1+\mathrm{CV}(C)^2}}.
\]
若\(\mu_G=E[G]\ne0\)，定义\(\mathrm{CV}(G)=\operatorname{sd}(G)/|\mu_G|\)，则
\[
\frac{E[G]}{\sqrt{E[G^2]}}
=\frac{\operatorname{sign}(\mu_G)}{\sqrt{1+\mathrm{CV}(G)^2}}.
\]
不能丢弃符号。\(\mu_G=0\)、二阶矩正时该比值为0，CV公式未定义；二阶矩也为0则原比值需单独定义，不能直接相除。

真实全局裁剪\(C=\min(1,\tau/\|g\|)\)由梯度决定，独立假设一般不成立；Adam的一阶/二阶EMA窗口也不同。\(E[m/\sqrt v]\ne E[m]/\sqrt{E[v]}\)，向量范数的比值更不能由标量公式替代。因此这不是实际AdamW的精确更新公式，“分组裁剪切断污染”也不能由(10)推出。

### 现有数据给出的仅是方向性比较

既有两seed共5240个裁剪系数中，Log头部global CV约0.386329，block CV约0.248455，对应proxy为0.932809和0.970494。proxy比值增加约**4.04%**。现有稀疏参数更新摘要中，Log头部block相对global均值增加约**5.57%**。

这些不是同一统计窗口：proxy使用全step，更新统计每seed只有131个采样点、且排除了前五个采样。不能用两个接近的百分数宣称机制验证。日志还显示C与梯度范数强相关；虽然与范数相关不等同于逐坐标独立性检验，它足以提醒真实裁剪不能未经检验按独立随机缩放建模。原模型checkpoint未保存Adam m/v，不能补画历史v曲线。

**未来可证伪检查。** 记录同步的原始有符号梯度、C、m/v、epsilon、学习率、衰减和实际参数变化；先检查EMA精确重建，再比较有/无相关性及不同窗口的简化模型误差。若预测不符，保留否定结果，而不是调假设使4.04%等于5.57%。

## 5. 数值合同与使用方式

代码：[verify_math_contracts.py](verify_math_contracts.py)。仅需NumPy，可在CPU执行：

```powershell
python .\verify_math_contracts.py --output .\MATH_CONTRACT_RESULTS.json
```

可选仅读四个原始JSON的历史数值核对：

```powershell
python .\verify_math_contracts.py --output .\MATH_CONTRACT_RESULTS_WITH_HISTORY.json --historical-root D:\PlantSPD_work
```

输出独占创建，已存在则拒绝覆盖。合同包括非交换恒等式、归一化权重、同谱异向反例、Fréchet有限差分、范数等号、重复特征值、shrinkage floor、完整native仿射等价、全头范数口径、凸风险界例子和独立假设失败反例。它们不是新真实数据实验，不增加seed或独立数据来源。

### 推荐写入论文的位置

| 内容 | 放置 | 可以主张 | 不能主张 |
|---|---|---|---|
| 命题一 | Background | 精确比较谱值和方向，纠正仅谱公式 | 新几何理论、Log普遍更好 |
| 命题二与(5) | 机制诊断/附录 | 给出需要测的局部灵敏度与能量方向 | 200倍界解释96%裁剪 |
| 命题三 | Readout auditing | TRAIN预算规则与数值收敛证书 | 数学保证100%或HELD泛化 |
| Adam-CV | 假设/附录 | 提出可失败的简化预测 | Jensen已解释5.57% |

## 6. 原始来源与定位

以下来源用于理论和既有工作的定位，未将其经验结论冒充本研究的实测结论；完整推导为本文针对SPD/Frobenius条件的书写。

1. Al-Mohy, Higham, Relton (2013), *Computing the Fréchet Derivative of the Matrix Logarithm and Estimating the Condition Number*, SIAM J. Sci. Comput. 35(4), C394–C410. [MIMS原文](https://eprints.maths.manchester.ac.uk/2015/1/120885991.pdf)，DOI 10.1137/120885991。标准矩阵函数导数、链式规则和条件数工具；不应声称本研究首次发现Log导数奇异性。
2. Lin and Maji (BMVC 2017), *Improved Bilinear Pooling with CNNs*. [官方PDF](https://www.bmva-archive.org.uk/bmvc/2017/papers/paper117/paper117.pdf)。已经比较matrix sqrt/log以及梯度实现；其结构和归一化不能与本研究的原型距离头直接等同。
3. Wang et al., *Deep CNNs Meet Global Covariance Pooling: Better Representation and Generalization*, TPAMI扩展版本。[arXiv:1904.06836v2](https://arxiv.org/html/1904.06836v2)。已有协方差估计、矩阵幂归一化和几何解释；不把谱归一化本身重新命名成原创贡献。

**最终证据边界：** 本附录使距离、导数及读出风险预算的说法可核查；独立确认、更多来源训练seed与等头族冻结/联合控制仍需实际补证。不存在由这几条命题自动推出的“顶会档次”、普适Sqrt最优、因果耦合或统计显著性保证。

# V2勘误与A实验准入：以实际逐epoch学习率为准

本文件**替代V1中累计学习率与直接WD收缩的数字**，并补充固定CE目标的必要范数界及A计划边界。V1源码、合同输出、文档与SHA全部保留，不回写或掩盖历史修正。

## 1. 必须纠正的预算数字

我此前用2620步逐step余弦算出1.3105；虽标为配置示例，该假设不符合真实v2逐epoch调度，不应作为当前实验预算。正确公式是每epoch131步，epoch e=0,…,19：
\[
\eta_e=.001\cdot\tfrac12[1+\cos(\pi e/20)],\qquad
B=131\sum_{e=0}^{19}\eta_e=1.3755.
\]
最后实际更新使用eta_19=6.15582970243117e-6，而不是逐step调度下接近0的末步LR。

root准入只读结果 [BASIC_B_FROM_LOGS.json](../BASIC_B_FROM_LOGS.json) 对15份STEPS日志（五seed×raw_frozen/raw_joint/log_joint）均记录B=1.3755。以归档源gamma=1e-4计算
\[
\rho=\prod_{e=0}^{19}(1-\gamma\eta_e)^{131}
=0.9998624594543486.
\]
因此直接WD收缩为**0.0137540546%**。这个数字替代旧0.013104%；“直接乘法衰减很小”的定性边界不变，仍不能排除其间接路径作用。这里明确区分日志实际LR已读到，checkpoint中WD取值另由root完整工具核验；本文不虚称读取了优化器payload。

若A2将全部head LR乘10且其它调度不变，配置B为13.755；若A2'是60epoch、每epoch131步、拉伸余弦T_max=60，则B=3.9955，**不是原B的精确3倍**。实际执行仍需以日志再次求和，不用配置值替代观测值。

## 2. 可替代one-hot r_min的有效必要界：固定TRAIN双view CE目标

固定FIT特征、K类、均匀样本权重。令每个错误类c的线性margin为
\(m_{ic}=\langle a_{ic},\Theta\rangle\)，定义
\[
g=\frac1{N(K-1)}\sum_i\sum_{c\ne y_i}a_{ic}.
\]
对单张图先用exp的Jensen，再对样本使用凸函数
\(h(t)=\log[1+(K-1)e^{-t}]\)的Jensen，可得
\[
\begin{aligned}
L_{dual}(\Theta)
&=\frac1N\sum_i\log\left[1+\sum_{c\ne y_i}e^{-m_{ic}}\right]\\
&\ge\frac1N\sum_i h\!\left(\frac1{K-1}\sum_{c\ne y_i}m_{ic}\right)\\
&\ge h(\langle g,\Theta\rangle).\tag{1}
\end{aligned}
\]
若预先指定0<epsilon<log K且要求Ldual<=epsilon，则
\[
\langle g,\Theta\rangle\ge a_\epsilon
=\log\frac{K-1}{\exp(\epsilon)-1}>0,
\quad
\boxed{\|\Theta\|_F\ge a_\epsilon/\|g\|_F.}\tag{2}
\]
g=0时(1)给Ldual>=log K，该固定X线性头不可能达到epsilon<log K。g近零时实际float64计算误差需披露，不将数值近零冒称严格等于0。epsilon>=log K时不产生正的范数下界。

### 实际双view及bias的坐标

dual logit为\(.5X_0W_0+.5X_1W_1+(b_0+b_1)/2\)。可用
\[
Z=[.5X_0,.5X_1,1/\sqrt2],\qquad
\Theta=[W_0;W_1;(b_0+b_1)/\sqrt2].
\]
则
\[
g=\frac1{N(K-1)}\sum_iZ_i\otimes(Ke_{y_i}-\mathbf1).
\]
compact Theta范数不超过完整[W0,W1,b0,b1]范数，因此(2)也给完整73002维头的必要范数下界。报告完整参数RMS时再除以sqrt(73002)，不能混用compact参数个数72933。

**梯度核验：** dual CE零头梯度为\(-(K-1)g/K\)。真实combined loss是dualCE+.25两branchCE，零头完整梯度恰为dual梯度的1.5倍；若从combined梯度推g，必须除以该因子。本文合同验证这两个关系。

### 如何与预算界搭配

从零头出发，逐坐标AdamW的C_max硬界与累计B可给完整头RMS上界C_max B（忽略衰减只会放宽界）；也可用rho得到更紧的正权重式。只有当可靠预算上界**低于**式(2)的必要需求，才得到特定固定X、特定CE目标下的不可达条件。上界高于需求不保证拟合，one-hot参考不参与这个必要性证明。

该界仅适用于计算g所对应的固定X。初始g不限制joint训练后改变的表示，不能用它宣布旧Log joint必然无法拟合。根任务若对固定FIT缓存计算g，需记录这些FIT特征/标签的准入、哈希与坐标定义；本数学子任务不读取这些真实数组。

该平均margin界可能很松，标签不均衡也会进入bias方向；它不给Macro-F1或逐类正确率保证。A3若训练tau，则线性界约束的是有效系数Theta_eff=tau*Theta（或除温度的对应形式），不能把原始W/b/tau的RMS预算直接当作Theta_eff的线性预算：其logit依赖参数乘积，不再对原始参数线性。

## 3. A0/A_lambda/A2/A2'/A3分别可以回答什么

### A0：先确定复现的是哪个旧条件

若全部A臂固定T1初始ImageNet编码器缓存，A0应首先复核旧**frozen**头的固定20epoch轨迹。它不可能同时复现旧joint encoder逐步变化的轨迹；不能将没复现joint的34%叫实现失败或反过来当机制证据。原始与缓存实现的dtype、样本/flip顺序、batch权重、scaler、初始W/b、AdamW、LR与clip需逐项一致，并提前规定容差与目标终点。

### A_lambda=0：删除的是AdamW解耦衰减

不能称为“去掉显式L2”。直接rho差约0.01375%，但路径可能有非线性放大，结果没有数学必然方向。若变化小，仅否定这个具体衰减幅度/配方下的大效应，不排除所有正则机制。

### A2：head LR乘10

改变累计步长，也改变瞬时轨迹、梯度/裁剪与动量历史；固定点式不含eta不能令这些有限过程保持不变。TRAIN拟合变快是与优化预算假设相容的结果，但不足以唯一识别它；发散或更慢也不能简单宣布几何无效。

### A2'：60epoch、原20epoch采样序列循环三次、余弦拉伸

它改变更新数、重复样本次数、LR时序、Adam状态演化与总计算，预算B约为原来的2.904倍。必须明确是**固定流重复控制**，不是获得三倍独立数据，也不是只改变一个“epoch数”变量而其余动力学保持相同。与A2的不同反应不能唯一拆成“幅度vs时间”。

### A3：自由正标量tau=exp(s)，初始1

先冻结定义究竟z'=tau*z还是z'=z/tau；两者初始相同，但s梯度符号相反。若tau乘logit，则W'=W/c、b'=b/c、tau'=c*tau可保持函数，属于表示冗余，不是新分类边界族。

tau不做WD，而W/b仍做WD，会改变优化/隐式正则；在假想显式L2模型中甚至能通过tau增长、W缩小绕开该罚项。当前AdamW不等于该模型，但也不能把A3收益唯一说成几何改善。若W/b/tau共享head clip阈值，新增tau梯度还会改变其它头参数的裁剪系数。

W=b=0时base logits=0，tau的初始梯度也为0，因此它不会凭空消除第一步零encoder梯度。预先记录tau、W/b范数、实际clip及finite状态，不能结果不理想后补约束/改WD。A3不是HELD温度缩放，不以HELD选tau或最佳epoch。

## 4. 叙事边界

这组A实验是固定X上的优化/配方控制，可以测响应，并与有条件理论预测比较。A0先验证实现等价；A_lambda、A2、A2'、A3均不唯一识别旧joint34%成因。既不能提前保证成功，也不因单个阴性臂否定Log/RMT。所有候选方向和容差在运行前明确，保留失败、全部终点与真实预算。

V2独占合同输出保留旧1.3105示例来源，以新实际epoch调度覆盖数值口径；其余V1加权Cauchy和rho推导仍然成立。

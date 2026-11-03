# 二阶谱、正则与“可训练性”：补充审计V2

本文件保留V1不变，仅核查新提出的Hessian、谱阈值、AdamW稳态和T0推断。**实际特征谱只能先作描述性诊断，不能以一个谱阈值裁定可训练性。** 本次不读取真实图像或标签、不做前向或拟合。

## 1. 零头Hessian：单视图公式正确，当前双视图需要交叉块和bias

对K类softmax CE、固定特征x，W=b=0时，令P=I−11^T/K，则类别logit Hessian为P/K。将bias并入增广特征\(\tilde x=(x,1)\)，单视图有
\[
\nabla^2 L(0)=E[\tilde x\tilde x^\top]\otimes(P/K).\tag{1}
\]
此处不是仅用中心协方差：bias需要最后一个常数坐标；若没有中心化，二阶矩也不能替换为中心协方差。

实际损失为
\[
\ell((z_0+z_1)/2)+.25\ell(z_0)+.25\ell(z_1).
\]
在两个头都为0时，按view及其增广参数排列，块Hessian为
\[
\boxed{H_{vw}=c_{vw}E[\tilde x_v\tilde x_w^\top]\otimes(P/K),
\quad c_{vv}=.5,\ c_{v\ne w}=.25.}\tag{2}
\]
证明：dual项每侧对z_v求导均引入1/2，故每块贡献1/4；分支项另给各对角块1/4。原始代码将全部W后接全部b打包，和这里逐视图增广坐标之间有确定的置换，不能不声明顺序就比较矩阵元素。式(2)也说明单独查看某一个view的Gram并不穷尽当前损失曲率。

当前scaler对每view中心化并除以中心L2能量RMS，在其初始完整TRAIN分布上满足tr(Sigma_x,v)=1。增广bias后二阶矩trace为2。Raw与Log既然各自完成这个初始能量归一，不能仅凭“Log数值范围更窄”推出其所有beta系统偏小；它们可能有不同谱形状、秩、方向和跨view相关。联合训练后固定scaler不保证trace继续为1。

## 2. 显式L2在局部二次模型中是连续收缩，不是硬“冻结方向”

仅考虑单视图、非gauge类别方向、固定特征和零头局部二次近似。若特征二阶矩某方向特征值beta>0，数据曲率是beta/K，沿该方向目标可写作
\[
L_0-a t+\tfrac12(\beta/K)t^2+\tfrac\lambda2 t^2.
\]
有非零a时，正则与无正则局部最优点的比为
\[
\boxed{t_\lambda/t_0=\beta/(\beta+K\lambda).}\tag{3}
\]
这是连续收缩：beta=Klambda时为1/2，beta小于阈值仍通常非零，不代表方向不可见、梯度为0或参数被冻结。完整非线性CE离开零头之后曲率变化；双视图应使用(2)的联合曲率，而非机械套每view阈值。

式(3)针对显式L2目标。当前训练用AdamW解耦衰减，不能直接把其weight_decay代入lambda称作“真实正则floor”。当前scaler、bias是否惩罚、loss组合系数和K也都要一致。

**方向计数与能量占比不同：**
\[
f_{count}=\#\{i:\beta_i<K\lambda\}/D,
\quad f_{energy}=\sum_{i:\beta_i<K\lambda}\beta_i/\sum_i\beta_i.
\]
例如很多极小特征值可以使方向计数接近100%，同时能量占比接近0。反之，低方差方向也可能恰好承载标签信号；能量小仍不等于判别不重要。两个摘要都应标为描述性统计，不能自动当作丢失有效信息的比例。

## 3. beta_min>Klambda不是“可训练当且仅当”的条件

Hessian在零头处不依赖真实标签；梯度和可分性依赖标签。因此仅由Sigma不可能对所有标签问题给出充分必要的拟合判据。

**不充分反例：** 固定一维X=(-2,-1,1,2)，Sigma=2.5。标签(0,0,1,1)可由一个阈值分开，标签(0,1,0,1)不可由任何一维仿射二分类头完全分开。两任务的X、Sigma、初始Hessian完全相同；即便beta_min远大于Klambda，后者仍不可能100%拟合。

**不必要反例：** 将前一个可分X乘极小的正数，beta可远小于Klambda，但符号不变，仍存在100%分类正确的线性头。是否在有限步、指定优化器、指定margin/CE预算下学到，是另一命题。没有定义“可训练”指表达能力、准确率、目标收敛还是预算内优化速度，就不能提出iff。

## 4. AdamW稳态不是RMS梯度除以weight decay

写实际AdamW更新为
\[
w_{t+1}=(1-\eta_t\gamma)w_t-\eta_t q_t,
\quad q_t=\hat m_t/(\sqrt{\hat v_t}+\epsilon_{Adam}).
\]
若学习率恒定、存在有限矩的平稳分布，并满足E[Delta w]=0，则
\[
\boxed{\gamma E[w]=-E[q].}\tag{4}
\]
这里不是\(\gamma E[w]\approx-\operatorname{RMS}(g)\)。q涉及有符号一阶动量、二阶动量、相关性与epsilon；不同EMA时间尺度不能靠RMS(g)单独恢复。学习率变化时只能直接得到E[eta_t gamma w_t]=−E[eta_t q_t]，还不能把eta约掉。

**递推反例而非真实损失实验：** externally imposed常数非零梯度g、epsilon_Adam=0且动量已稳态时，q=sign(g)，因此w*=−sign(g)/gamma，模长1/gamma与|g|无关。此例足以否定普适“||w||=RMS(g)/gamma”公式，但不证明真实训练存在该稳态或权重真会增长到1/gamma。

## 5. T0如何避免同时改变目标与优化器

若T0要纯检验solver，至少固定同一个encoder、相同缓存X、相同TRAIN scaler和增广、同一标签/样本权重、同一个affine头族、同一明确的**显式目标**。必须写明实际优化器是AdamW，不是SGD：把AdamW的解耦weight_decay与L-BFGS中的lambda-L2互换，会同时改变目标/算法含义。

把旧成熟encoder上的凸lambda≈1e-8求解结果与新ImageNet编码器joint训练比较，还改变了表示、目标、头族历史与轨迹，不能命名为纯solver对照。若要对同一显式CE+L2目标比较求解器，应另有明确实现与准入，不能热改正在运行的AdamW队列。

即使一个T0得到100%TRAIN，也只证明**该组固定X与所指定头族/目标/solver**可以达到该拟合度；另一个得到34%则只显示所指定条件下的不同结果。单个T0不能唯一分配尺度、表示、目标、优化器、学习率和联合训练轨迹的全部贡献。

## 6. 当前合理的最小顺序

1. 核对初始完整TRAIN scaler的trace=1、bias增广口径与两个view交叉块；只汇总实际冻结X谱，不拟合、不调阈值。
2. 同时报告方向计数、能量占比、rank/条件数、联合块曲率与标签相关梯度信息的可获得性；单独谱不当判决器。
3. 阅读已有同步AdamW更新日志，检验真实更新方程、坐标动量/梯度方向与weight decay分量；不能从RMS外推出稳态。
4. 明确T0固定什么/改变什么，再以新协议执行获准的最低成本控制。不得为得到34%或100%事后调参。

随附纯合成合同验证(1)–(4)、双view块系数、方向计数/能量分离、同Sigma不同可分性和AdamW递推反例。它们不等于真实Log欠拟合机制已经验证。

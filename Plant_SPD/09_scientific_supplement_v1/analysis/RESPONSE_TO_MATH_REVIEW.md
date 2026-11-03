# 对本轮数学验算的代码核对与定稿修正

## 先核实最可能影响证书的范数口径

**结论：原E08没有逐类别max替代全局范数的问题，也没有遗漏69倍预算。**

原实现中，`W.shape=(2,528,69)`、`b.shape=(2,69)`，`theta=np.concatenate([W.ravel(),b.ravel()])`。因此theta长73,002，`theta@theta`包含两个视图、所有类别的全部权重和偏置。计算M时的r索引四个**完整native模型**，不是69个类别行。求解器也对完全相同的theta使用`lambda/2 * theta@theta`，梯度同时包含`lambda*W`与`lambda*b`。

逐字节读取四份旧native参数后重新计算：

- `M = 1598050.0561016323`；
- `lambda = 1.251525252518626e-8`；
- 最大native正则罚项`lambda*M/2 = 0.009999999999999998`；
- 没有读取HELD标签来定义M或lambda，没有修改旧参数、划分或结果。

证据：[GLOBAL_NATIVE_NORM_AUDIT.json](GLOBAL_NATIVE_NORM_AUDIT.json)、[GLOBAL_NATIVE_NORM_AUDIT.md](GLOBAL_NATIVE_NORM_AUDIT.md)，以及独立复核[../math/NATIVE_NORM_SCOPE_REVIEW.md](../math/NATIVE_NORM_SCOPE_REVIEW.md)。完整证明见[数学附录](../math/MATHEMATICAL_APPENDIX.md)。

新五seed补证另有十个native完整头。它们必须重新确定共同M和lambda，20格全部重新求解；不能混用旧8格。新十头正控制已通过，协议记录`M=1715328.897296905`、`lambda=1.1659571544277561e-8`。这是TRAIN-only锚点集合扩展，不是根据HELD分数调小正则。

## 距离恒等式：成立，但权重和需除以d

\[
\|f(A)-f(B)\|_F^2=\sum_{ij}q_{ij}[f(\lambda_i)-f(\mu_j)]^2,
\quad q_{ij}=(u_i^\top v_j)^2.
\]

Q双随机意味着每行每列和为1，**全部元素之和为d**。只有距离除以d后，Q/d才是概率权重。近简并子空间内的单个q不应解释；实际谱诊断按特征值块聚合。公式没有推出“Log的判别信息必集中在低谱”或“原配一定更好”；这两点只能另做数据检验。

## 导数等式与floor界：区分两层陈述

固定某个SPD矩阵A时，精确等式为

\[
\|D\log_A\|_{F\to F}=1/\lambda_{\min}(A),\qquad
\|D\sqrt{\cdot}_A\|_{F\to F}=1/(2\sqrt{\lambda_{\min}(A)}).
\]

只有给出`lambda_min>=1e-4`时，才能推得**不超过**10000、不超过50、比值不超过200；不是实际矩阵一定等于这些数。选择最小特征向量方向可达到该矩阵自己的算子范数，不代表真实上游梯度恰好沿这个方向。

上游梯度的能量权重
\(p_{ij}=|(U^\top H U)_{ij}|^2/\|H\|_F^2\)
总和为1，但**一般不双随机**。因此距离与导数可用“谱函数与方向共同决定贡献”的统一视角组织，不能都称为“双随机平均”。真实方向增益需要新日志；旧checkpoint不能补回它。

## 风险预算与数值证书：适用对象保持不变

在完整theta都受L2正则、特征冻结、目标凸、native同映射可达的条件下：

\[
L(\hat\theta)\le L(\theta_N)+B+\delta,
\quad \delta=\|\nabla J_\lambda(\hat\theta)\|^2/(2\lambda).
\]

这保证的是相对native的TRAIN组合损失预算，不是参数范数预算，不保证100%训练F1或HELD效果。梯度阈值与lambda、gap目标共同设计，属于数值后验收敛证书；没有声称区间舍入意义上的机器验证证明。新等头族AdamW训练没有此凸求解证书，不能借用。

## Adam-CV：精确的是矩比，真实优化器仍需检验

令Z为某坐标**裁剪后的有符号梯度**，且二阶矩非零。若其均值非零，精确矩恒等式是

\[
\frac{E[Z]}{\sqrt{E[Z^2]}}
=\frac{\operatorname{sign}(E[Z])}{\sqrt{1+\mathrm{CV}(Z)^2}}.
\]

均值为0时左侧为0，而CV表达式未定义。这个恒等式不需要裁剪因子与原梯度独立；把它进一步拆成CV(c)因子才需要独立性。即使使用CV(Z)，它仍然不是带有不同EMA窗口、偏差修正、epsilon和weight decay的真实AdamW更新公式。

新增同头控制会在同一step、同一预选坐标记录原始/裁后梯度、m/v前后、实际参数差和AdamW方程残差。它能检验矩比近似与真实更新的差异；没有全局/分组新干预对照时，不能用它宣称已经因果解释旧5.57%的增幅。

## 本轮证据交付纪律

数学附录和合成合同已完成；原四头范数审计已完成；五seed20格读出正在本轮独立新目录执行；同头族真实训练在准入后执行。独立新来源确认、方向性Fréchet增益、常数裁剪干预与epsilon剂量响应均不得因“代码已写”被计为实验完成。所有状态以实际completion、协议SHA和进程退出记录为准。

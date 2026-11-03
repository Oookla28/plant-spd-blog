# F1–F4与A实验的数学准入复核

**准入结论：可执行有界的描述性取证与预注册干预；不能将分位数、插值范数、末态动量或范数平台升级成“无法拟合的数学证明”。** 以下推导仅用标准AdamW递推、固定微型数组与归档v2源码，不访问真实图像/标签、不前向或拟合，不修改F盘归档。

## 0. 日志变量要先对应到递推

归档`equal_head_control_v2.py`的AdamW使用beta1=.9、beta2=.999、epsilon_Adam=1e-8、weight_decay=1e-4，head基础LR=1e-3。实际字段`bias_corrected_adaptive_update`已经是
\[
-\eta_t u_t=-\eta_t\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon_{Adam}},
\]
不是裸u。`decoupled_weight_decay_update`同样含eta。要用u的矩或硬界，应从同step/同group学习率恢复；eta=0需单列，不能直接相除。更新方程需同时核对实际delta、adaptive部分和衰减部分，记录float32舍入残差。

日志只保存预定坐标样本时，坐标分布不自动等于整个头部或编码器的分布。q99是经验分位数，不是最大值；末态u不是整个训练轨迹的最大值。不能把二者代入“所有step均受U限制”的预算不等式。

## 1. F1可用的硬界：加权Cauchy，而不是经验q99

对某个坐标，令g_i为**裁剪后**输入Adam的梯度，标准零初始化动量、有限步t，有
\[
\hat m_t=\sum_{i=1}^t a_i g_i,\qquad
\hat v_t=\sum_{i=1}^t b_i g_i^2,
\]
\[
a_i=\frac{(1-\beta_1)\beta_1^{t-i}}{1-\beta_1^t},\quad
b_i=\frac{(1-\beta_2)\beta_2^{t-i}}{1-\beta_2^t}.
\]
当0<=beta1<1、0<beta2<1时，加权Cauchy给出
\[
|\hat m_t|^2\le\left(\sum_i a_i^2/b_i\right)\hat v_t,
\quad
\boxed{|u_t|\le C_t=\sqrt{\sum_i a_i^2/b_i}}.\tag{1}
\]
epsilon_Adam>=0只会降低比值；全零历史时m=v=0，实际正epsilon令u=0。有限步的准确闭式为
\[
C_t^2=\frac{(1-\beta_1)^2}{1-\beta_2}
\frac{1-\beta_2^t}{(1-\beta_1^t)^2}
\sum_{j=0}^{t-1}\left(\frac{\beta_1^2}{\beta_2}\right)^j.\tag{2}
\]
epsilon=0且g_i正比于a_i/b_i时可以达到该界；它不是假设梯度恒定的近似。若beta1²<beta2，还可取全时刻上界
\[
C_t\le C_\infty=
\frac{1-\beta_1}{\sqrt{(1-\beta_2)(1-\beta_1^2/\beta_2)}}.
\]
有限步因子不超过1，可由\((1-x)(1-y)\le(1-\sqrt{xy})^2\)验证。实际.9/.999得到C_infty约7.2703。若beta1²>=beta2，有限步(1)仍成立，但不能照搬这个无限时域常数。

这是逐坐标最坏界；d维组范数只得到粗糙界||u||<=sqrt(d) C_t。它通常很松，不等于真实可用学习信号，更不能用大U直接说明优化会成功。

## 2. F2预算：乘积递推成立，但需要全轨迹界和正收缩系数

逐组固定weight decay gamma>=0，更新为
\[
w_t=\rho_t w_{t-1}-\eta_t u_t,\quad\rho_t=1-\eta_t\gamma.
\]
若0<=eta_t gamma<1，则
\[
w_T=\left(\prod_{r=1}^T\rho_r\right)w_0
-\sum_{s=1}^T\eta_su_s\prod_{r=s+1}^T\rho_r.
\]
若**每个step**都有||u_s||<=U，则
\[
\boxed{\|w_T\|\le\rho_{1:T}\|w_0\|+
\frac U\gamma(1-\rho_{1:T})}\tag{3}
\]
（gamma>0）。证明用三角不等式与\(\gamma\sum_s\eta_s\rho_{s+1:T}=1-\rho_{1:T}\)。gamma=0时改为||w_0||+U sum eta。eta gamma越过1时不能把带符号乘积当正收缩权重，需重新取绝对值处理。

真正的有限预算上界也可逐步用U_s=sqrt(d) C_s，而非统一U。把末态u、采样均值或q99代替U_s则不是证明。上界宽于某个参考范数也不证明可达，上界窄于一个**非必要**参考范数也不证明无法分类。

### 当前直接WD的量级很小

仅按2620步、head LR由1e-3余弦降到0的标准步编号，sum eta约1.3105；gamma=1e-4时
\[
\prod_t(1-\eta_t\gamma)\approx0.99986896.
\]
即直接乘法收缩只有约0.0131%。实际应以日志的LR求和确认步序，但该量级不支持“强直接衰减把整个头锁住”的故事。WD还可通过路径影响优化，这个计算没有排除其间接作用。

AdamW若存在恒学习率平稳期望，满足gamma E[w]=-E[u]；该式不含eta，**不代表**改变LR后的有限预算A2效应只能来自步数预算。u依赖参数路径、随机梯度、EMA、epsilon和joint表示，均可随eta变化；达到稳态本身也需要证明。

## 3. F3的r_min：one-hot插值参考不是完美分类器的必要范数

对固定设计矩阵X求最小范数one-hot插值X Theta=Y，只在这组**精确插值约束**内有最小范数意义。分类只要求正确类得分大于其他类，不要求等于one-hot。

若某个仿射头Theta严格正确，则任意c>0的cTheta仍严格正确，但||cTheta||可趋近0。因此任意“100%准确率分类器都必须||Theta||>=r_onehot”的说法错误。使用bias时应把它纳入Theta及增广X，不能只比较W范数。

如果确实要必要范数条件，应预先固定**绝对logit margin**m>0及坐标单位，例如
\[
\langle\theta_{y_i}-\theta_k,\tilde x_i\rangle\ge m
\quad(k\ne y_i).
\]
由Cauchy可得较弱必要界||Theta||_F>=m/(sqrt(2)||x_tilde_i||)（每个约束都需满足）。更强的参考应明确定义为固定margin的最小范数问题，不能仍称one-hot插值的r_min为普适分类下界。

在不新增此类求解前，建议把r_min降级成“one-hot插值的范数参考”，只报告它与当前头范数的比例，不作可训练性或容量裁决。TRAIN F1=100%、CE接近0和固定margin本来就是不同要求。

## 4. A中的constant-gamma杠杆：预测可重参数化不等于训练等价

必须先指定gamma作用位置。

- 对无floor的C做共同gamma*C，log(gamma*C)=log C+log(gamma)I。固定TRAIN scaler后，每view特征只加\(d_v=(\log\gamma/s_v)\operatorname{svec}(I)\)。自由affine头可令\(b'_{vc}=b_{vc}-w_{vc}^Td_v\)保持分支与融合logit全部相同。
- 若同时重估TRAIN中心，纯全局Log位移会被中心消掉；但当前scaler固定，bias未相应重参数化时并不会自动消失。只有跨类相同logit位移由softmax gauge直接消掉。
- 对scaler后的特征乘gamma，W反向缩放可保持预测，但梯度、裁剪、Adam epsilon、WD、有限步LR和bias的学习动态不自动等价。
- 对特征F乘a且保留固定epsilon，真实变换为C(a)=a²(C−epsilon I)+epsilon I，不是纯共同缩放。

最后一种情形相对理想常数位移的准确残差是
\[
R(C,a)=\log C(a)-\log C-2\log(a)I
=U\operatorname{diag}\log\left[1+(a^{-2}-1)\epsilon/\lambda_i\right]U^T.\tag{4}
\]
因此“只有少数特征值靠近epsilon”这个**计数**不能单独给残差大小；必须给出a的范围、lambda相对epsilon的范围及所用范数。若C>=epsilon I且a>0，则可给最松界||R||_F<=2|log a|sqrt(d)；若要更紧界，需实际谱或分组阈值及各组最大残差。映射残差传到logit还需W范数与scaler单位，不能直接宣称预测近似不变。

“dead lever”只能在明确的理想化函数等价意义下使用。一个对预测容量冗余的参数，也可能改变优化与正则路径；不能未经控制就用负结果排除整个优化机制。

## 5. F4的范数平台与大u不识别唯一瓶颈

余弦eta趋0时，即便u持续非零，单步delta也趋0，范数自然呈平台；方向抵消、动量、margin变化、特征漂移或WD平衡也可造成平台。一个平台不唯一证明权重范数“天花板”。

大||u||只表示更新信号幅度大，不等于SNR高或对损失有益。例如方向正负交替，每步范数恒大而净位移接近0。需要同步的有符号方向、累积位移、与梯度/正确类margin的关系，并承认16个坐标样本不能代替全部参数统计。

## 6. 有界、可解释的执行顺序

1. 先做F1变量单位核验：裸u与含eta的adaptive delta分开，坐标/step覆盖率、q99与max分别报告，验证Adam更新残差。
2. F2分别给经验描述和(1)–(3)硬界，不能混用。记录实际累计eta与rho，先量化直接WD量级。
3. F3先固定margin/CE或将one-hot范数降级；避免不成立的“无法拟合”判决。
4. F4同步看方向与eta，而非仅norm平台。只用现有日志可用量，不从缺失状态重建虚构轨迹。
5. A实验在写明操作位置、固定预算、匹配/不匹配的目标及预定主指标之后才运行。一个34%或100%结果不能唯一分配全部病因；A2响应更不能由稳态式反向归因。

随附合成合同仅验证加权Cauchy、乘积展开、插值范数反例、理想Log位移/floor残差和平台/方向反例。没有由这些合同获得真实训练的因果证据。

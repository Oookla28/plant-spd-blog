# SPD估计研究：五项直接近邻与创新边界

2026-10-25；只读小范围核查，不安装代码、不运行实验、不增加候选实现。目的在于排除过宽的首创声明，不能视作完备系统综述。

| 文献与primary来源 | 实际查阅层级 | 已经覆盖的内容 | 与当前问题的区别及不能推出的结论 |
|---|---|---|---|
| **Ledoit & Wolf (2021), Shrinkage estimation of large covariance matrices: Keep it simple, statistician?** JMVA186,104796。[发表页](https://doi.org/10.1016/j.jmva.2021.104796)；[作者发表稿](https://www.ledoit.net/KISS_2021_JMVA.pdf) | 已核发表页摘要及作者稿被索引的正文、损失表和命题；作者PDF整篇打开多次超时，未逐页通读证明 | 多损失下的rotation-equivariant非线性收缩明确包括Log-Euclidean。对应oracle谱值为`d_i*=exp(u_iᵀlog(Σ)u_i)`。 | “把损失改成log”“最优谱收缩取决于几何目标”已经存在。这个oracle对应完整matrix-log目标，并不要求样本协方差与Σ交换；不能把noncommuting目标本身说成空白。有限样本ReLU相关窗的适用域并未由摘要或这些正文摘段直接解决，但这不是全领域未解决的证明。 |
| **Maurais et al. (2023), Multi-Fidelity Covariance Estimation in the Log-Euclidean Geometry.** ICML/PMLR202,24214–24235。[官方论文页](https://proceedings.mlr.press/v202/maurais23a.html)；[全文](https://proceedings.mlr.press/v202/maurais23a/maurais23a.pdf) | 已读摘要、§3.3–3.5和§4相关正文；未逐项审完附录证明 | 通过不同精度、成本且统计耦合的数据源，在log空间估计协方差并保证正定；给出LE-MSE分析和预算分配。实验区分普通Frobenius、LE与affine-invariant误差，并指出特征值截断可使几何误差恶化。 | “借另一来源减少协方差噪声且保SPD”“保正定比末端截断合理”不是新思想。其multi-fidelity源不等于同一图像局部块与全局网格，不能未经验证就套用其最优性或宣称完全相同。 |
| **Yang, Doss & Vemuri, An Empirical Bayes Approach to Shrinkage Estimation on the Manifold of Symmetric Positive-Definite Matrices.** JASA119(545),259–272(2024)，DOI10.1080/01621459.2022.2110877。[作者预印本](https://arxiv.org/html/2007.02153v3) | 查到预印本§2–3的定义、估计式与假设；发表版本元数据已核，未核对预印本与发表版全部差异 | 对log-normal SPD-valued observations使用LE损失、经验Bayes/SURE及层级先验，解析收缩Fréchet均值和相关参数。 | “在SPD流形上做LE风险收缩”“向共同几何原型收缩”已有直接先例。其观察单位是已经SPD的矩阵，并非本项目相关ReLU token先生成的可能奇异样本Gram；不能混同两层随机对象。 |
| **Rahim, Thirion & Varoquaux (2019), Population shrinkage of covariance (PoSCE) for better individual brain functional-connectivity estimation.** MedIA54,138–148。[发表页](https://doi.org/10.1016/j.media.2019.03.001)；[作者列出的全文](https://inria.hal.science/hal-02068389/file/MEDIA_PoSCe_2019.pdf) | 读取出版方摘要、highlights、方法section snippets，并由作者出版目录核对HAL全文链接；HAL访问受限，未通读全文 | 将总体协方差分布作为非各向同性先验，结合Riemannian切空间与概率模型，改善短而噪声大的个体时间序列估计。 | “不用各向同性I，转向全局/群体上下文prior”不能笼统算新。人口层先验不是同图全局条件先验；这种层次不同需要严格定义和对照，不能仅凭应用不同获得首创性。 |
| **Lu et al. (2020), Dying ReLU and Initialization: Theory and Numerical Examples.** CiCP28(5),1671–1706，DOI10.4208/cicp.OA-2020-0165。[作者预印本全文](https://arxiv.org/html/1903.06733v3) | 阅读摘要、§3定义/主要定理及结论；未重证全部附录 | 研究ReLU神经元或网络变成零/常数、初始化时的born-dead概率，以及初始化干预。 | “ReLU可以无激活/失去信息”早有理论。本文重点是网络在输入域上的死亡，不等同本项目仅某连续空间窗未观察到激活、而全图仍激活。零样本列导致样本协方差奇异是直接线性代数后果，不该包装成新定理。 |

## 对当前叙事的具体约束

保留三个不同层次，不能相互替代：

1. **既有数学**：Gaussian ReLU矩、相关样本谱收缩、LE风险与Bayes/上下文收缩均有先例。前一份[相关样本RMT核查](CORRELATED_SPECTRAL_RELATED_WORK_20261025.md)已覆盖Burda与Jarosz的可分离相关模型及作者代码，本文件不重复算作第六项文献。
2. **当前实证现象**：特定固定网络、固定TRAIN网格中，连续小窗经常不满足ANS原始谱适用域；局部全零通道多数在完整网格中重新出现。即使重复制约实验支持这一点，也只建立这条管线的有限窗现象。
3. **尚未建立的方法贡献**：需要对准一个明确目标，证明相对于上述直接近邻有新增结论及可部署价值；当前模拟成功不自动提供新估计器、下游疾病增益或顶会贡献。

较稳妥的工作问题是：**在明确的相关ReLU有限窗模型与实际冻结视觉token中，适用域缺失、样本均值去除偏差、几何误差排序是否能够被分别识别与预测？** 这仍是待证问题，不等于宣称此前无人研究它。

不能采用的概括：`RMT从未处理相关样本`、`LE损失收缩是我们首次提出`、`全局prior补局部covariance就是新方法`、`零谱就是数据总体不含信息`、`模拟数增加即证明真实视觉泛化`。本次核查没有授权或执行任何新增实验，也没有据此承诺顶会录用。

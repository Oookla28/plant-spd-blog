# PlantSeg 2×2 机制验证规划 v2

状态：`PLANNED_NOT_RUN`

本文件把文献证据、当前本地结果和下一轮可判定实验合并为一份冻结前规划。它不是训练授权。只有在接口审计、干预清单和四个单元的源代码哈希全部固定后，才进入有限训练窗口。

## 1. 研究问题和可声明范围

研究问题是：在背景、光照、遮挡和病斑尺度变化存在时，结构化的 SPD 表示是否会让反事实约束更有效，从而改善全局—局部证据融合？

主检验不是“加了两个理论后分数是否上涨”，而是 2×2 交互量：

```text
I = (S1 - S0) - (E1 - E0)
```

其中 E 表示欧氏协方差控制，S 表示 SPD/log-Euclidean 表示；0 表示普通训练，1 表示相同的反事实训练。只有在多种子下 I 的预注册置信区间稳定为正，并且反事实稳定性指标同步改善，才可以说存在“几何表示与反事实训练的协同证据”。

本研究不把受控图像干预当作真实因果识别。论文表述应使用“intervention-based counterfactual robustness”或“受控反事实鲁棒性”，不能写成已经识别病害的真实因果图。

## 2. 文献带来的硬约束

| 文献/资源 | 采用的数据或实验做法 | 对本项目的直接要求 |
|---|---|---|
| PlantSeg 数据集论文 | 田间/网络图像、病斑掩码和植物病害元数据；基准同时比较 CNN、Transformer 和混合模型，并报告 mIoU、mAcc、参数量等 | PlantSeg 作为主场景；分割和分类口径分开；至少保留 U-Net、DeepLabV3+、SegFormer 等基线，不能只和自有分支比较。见 [PlantSeg 数据集论文](https://www.nature.com/articles/s41597-025-06513-4)。 |
| PlantWild | 18,542 张、89 类的真实场景病害识别，官方划分 14,865/3,677；问题重点是小类间差异和大类内变化 | 适合作为模型冻结后的外部分类验证；不能用它反过来选择 2×2 超参数。见 [PlantWild 项目页](https://tqwei05.github.io/PlantWild/) 和 [原始论文](https://arxiv.org/abs/2408.03120)。 |
| PlantDoc | 约 2,598 张、13 种植物、27 类，自然光照、遮挡和复杂背景 | 适合作为第二个外部场景，检验跨来源退化和选择性预测；不应与 PlantSeg 的 69 类分割指标直接拼接。数据集原始论文 DOI 为 [10.1145/3371158.3371196](https://doi.org/10.1145/3371158.3371196)。 |
| SPDNet | SPD 协方差/二阶结构的双线性映射、特征值修正和 LogEig 已是成熟方法 | SPD 只能作为受控表示因素，不能把“使用 SPD”本身写成原创。见 [AAAI SPDNet](https://ojs.aaai.org/index.php/AAAI/article/view/10866)。 |
| DES-AS | 在 40 个真实数据集上做 30 次重复，用近似 Shapley 估计协同贡献，并使用统计检验 | Shapley 必须有独立校准/评价方向、重复实验和强的等权控制；本项目先不把 Shapley 调度混进 2×2。见 [DES-AS](https://www.sciencedirect.com/science/article/pii/S0031320324006502)。 |
| Learning from Failure | 先显式制造偏置分类器，再用训练信号让第二个分类器关注反偏样本 | 反事实约束要和普通增强、偏置控制分开，不能把反事实图像简单追加到训练集。见 [NeurIPS 论文](https://proceedings.neurips.cc/paper/2020/file/eddc3427c5d77843c2253f1e799fe933-Paper.pdf)。 |
| Whac-A-Mole | UrbanCars 和 ImageNet-W 同时控制多个捷径；缓解一个捷径可能放大另一个捷径 | 不能只做背景替换；至少要有背景/光照干预、病斑干预和多捷径退化报告。见 [CVPR 论文](https://openaccess.thecvf.com/content/CVPR2023/html/Li_A_Whac-A-Mole_Dilemma_Shortcuts_Come_in_Multiples_Where_Mitigating_One_CVPR_2023_paper.html)。 |

近年的植物病害工作已经开始把反事实/结构因果用于病害识别，因此“植物病害 + 因果反事实”本身不能作为首次创新。当前可辩护的贡献只能是：在同一全局—局部任务上，用等协方差、等参数量的欧氏控制，检验 SPD 表示是否改变反事实约束的有效性。公开摘要和元数据可参考 [Plant disease counterfactual reasoning 方向](https://www.sciencedirect.com/science/article/pii/S1574954126000154) 与 [Counterfactual Explanations for Plant Disease Classification](https://www.mdpi.com/2076-3417/16/16/7929)。这些近邻工作的全文、数据许可和实现细节仍需在投稿前逐项核对，不能把摘要级信息写成已复现结果。

面向 Smart Agricultural Technology 的相关工作常把检测、分割、分类和严重度串成应用管线，但有些工作主要在 PlantVillage 上报告近乎饱和的准确率，难以证明田间鲁棒性。我们的实验应借鉴其应用闭环，同时坚持 PlantSeg 的自然场景主验证和清晰的指标口径。可参考该刊的 [plant leaf disease segmentation/classification 管线文章](https://doi.org/10.1016/j.atech.2024.100526) 和 [植物病害数据集与挑战综述](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2024.1452551/full)。

这些工作共同支持一个实验原则：数据集必须有真实场景变化，模型必须接受成对干预，基线必须足够强，主结论必须来自跨划分或跨种子的统计结果。

## 3. 当前结果说明什么

现有十组 PlantSeg pilot 只能作为接口和失败证据：它使用单 seed、5 个 epoch；G7 只有压缩的 log-eigenvalue screen，G8/G9 没有真正的反事实训练；G4 的训练掩码是同图预测，OOF 掩码尚未完成。因此，G9 的低分不能解释为理论失败。

后续冻结输出审计也显示，简单等权融合仍是最强的完成控制；在本地可用的 787 张开发图上，等权分类 Top-1 为 80.8132%，mask IoU 为 62.1416%，SPD-only screen 的 Top-1 为 80.4320%，DES-AS 风格 Shapley 与等权的差异约为 0.20 个百分点。这说明继续扫描权重、阈值或收益函数没有足够收益空间，必须先做可辨识的机制对照。

参考文件：[十组 pilot 结果](F:/Plant_Disease/01_datasets/plantseg/runs/ten_groups_ep5_seed3407/RESULT_NOTE.md)、[冻结矩阵审计](F:/Plant_Disease/paper/CRCG_FULL_MATRIX_SCREEN_5060_V1.md)、[可靠性头审计](F:/Plant_Disease/paper/CRCG_RELIABILITY_HEAD_FULL_5060_V2.md)。

## 4. 固定数据协议

主场景只使用本地已验证的 PlantSeg v7 子集，不重新处理数据：

- 版本状态：`COMPLETE_VALIDATED_SUBSET`；
- 记录数：7,477；
- train/validation/test：5,230 / 800 / 1,447；
- manifest SHA-256：`ba5a8afffa3614aafe2512e9941a12181f9c7e2f14004368a7d8ba690a5441dc`；
- 8 个图像—掩码尺寸不一致的记录继续保留在审计中，不旋转、不自动修复；
- test 永远关闭，直到所有结构、超参数和阈值冻结。

PlantSeg 的 PNG 是病害区域掩码，不是完整植物轮廓。因此 `1-mask` 不能直接被称为真实背景；背景反事实优先使用全图光照、色温和低频纹理扰动，并记录病害区域保护比例。按植物病理数据集综述的建议，最终外推分析还要按 host、disease 和来源簇做分组，而不能只做随机图像 bootstrap；随机划分容易高估跨场景性能。见 [植物病害数据集挑战综述](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2024.1452551/full)。

主指标按图像 ID 配对。重复组或 `original_group_id` 必须只出现在一个 split。若现有检查点使用另一套 3,917/904 manifest，则不允许直接把两套结果混成一个主表；要么在完整验证子集上从共同初始化重新训练，要么明确写成冻结输出的辅助审计。

## 5. 四个单元的公平定义

| 单元 | 表示 | 训练压力 |
|---|---|---|
| E0 | 与 SPD 单元使用同一收缩协方差 `C`，取固定上三角向量 `u(C)`，平方欧氏距离 | 普通分类/局部训练 |
| E1 | 同 E0 | 普通训练 + 背景一致性 + 病斑敏感性 |
| S0 | 同一 `C`，计算 `log(C)`，使用 Log-Euclidean Frobenius 距离 | 普通分类/局部训练 |
| S1 | 同 S0 | 普通训练 + 相同的背景一致性 + 病斑敏感性 |

收缩协方差固定为：

```text
C = (1-gamma) Cov(F) + gamma * trace(Cov(F))/d * I + epsilon * I
```

`gamma`、`epsilon`、特征投影维度 `d`、原型数和参数量在四个单元中完全相同。上三角向量的非对角元素乘 `sqrt(2)`，使欧氏向量范数与矩阵 Frobenius 范数口径一致。S 单元使用稳定 `eigh` 计算完整 `log(C)=U log(lambda) U^T`，不能只取 log-eigenvalue 向量；否则只是谱特征筛选，不是 Log-Euclidean 对照。

四个单元必须从同一份初始化、同一批次顺序、同一普通增强、同一干预清单开始。任何单元缺少预测掩码时直接失败，不得回退到 GT 掩码。

## 6. 反事实训练和验证

### 6.1 训练干预

为每一张 train 图像预先生成并哈希固定的成对清单：

1. 背景/光照/颜色变化：病斑位置和标签保持不变；
2. 局部病斑遮挡或删除：只使用预测软掩码生成，限制删除面积范围，记录实际面积比例和掩码质量。

背景干预的目标是保持预测稳定；病斑干预的目标是置信度下降或证据变化。不能把“病斑被删除后标签仍完全不变”作为训练目标。

### 6.2 损失

四个单元的基本损失保持相同；E1/S1 额外加入：

```text
L_bg = symmetric_KL(p(x), p(x_bg_cf))
L_lesion = relu(margin - (z_y(x) - z_y(x_lesion_cf)))
L = L_base + lambda_bg * L_bg + lambda_lesion * L_lesion
```

`lambda_bg`、`lambda_lesion`、margin 在启动前固定，不在 validation 上搜索。普通颜色增强仍保留在四个单元中，避免把“增加增强”误当成反事实机制。

### 6.3 掩码和背景

局部分支只接收：

```text
x_local = x * (0.60 + 0.40 * m_soft)
```

背景被降权而不是删除。训练中的 GT 仅用于分割目标和构造有登记的干预；推理、验证路由和融合权重不能读取 GT。

## 7. 执行顺序和停止规则

### 阶段 0：静态接口审计，不启动 GPU

必须完成：OOF 预测掩码、无 GT fallback、逐图干预清单、同初始化克隆、SPD 特征值下界、原型只用 train、test 访问断言、源/协议/manifest 哈希。这里任何一项失败，先修复并重做 smoke，不进入全量训练。

### 阶段 1：四单元一 seed 的机制筛选

使用 seed 3407，先做短 smoke 验证形状和 loss，再做一次完整 train/validation 预算。保存每个 validation ID 的原始/反事实 logits、分支分歧、协方差特征、掩码来源和训练时间。只看 validation，不开 test。

阶段 1 不加入 Shapley scheduler，也不加入新主干、额外注意力或新损失。

### 阶段 2：三 seed 确认

只有阶段 1 的交互方向为正且实现合同全部通过，才运行 3407/3408/3409。三 seed 共享同一干预 manifest 和超参数。报告均值、标准差、逐 seed 结果和按图配对 bootstrap 95% CI。

### 阶段 3：Shapley 单独消融

只有阶段 2 通过后，才比较等权、普通 gate、DES-AS 风格静态 Shapley、几何联盟价值和完整反事实几何价值。Shapley scheduler 的交替训练是更后面的单独实验；它不能和 2×2 主检验同时引入。

## 8. 主要指标和统计检验

主指标：validation macro-F1、balanced accuracy 和 interaction `I`。辅助指标：accuracy、NLL、ECE、Brier、背景反事实的 KL/置信度变化、病斑删除后的真类 logit 下降、mask Dice/IoU、按病斑面积分层的结果。

使用相同 validation ID 的 paired stratified bootstrap，至少 5,000 次、固定随机种子。除总体结果外，按小病斑、背景复杂度、遮挡/光照扰动和预测掩码质量分层。单个平均分上涨不能替代交互置信区间。

对“越低越好”的指标必须在交互前统一方向：例如将 `-ECE`、`-NLL` 和 `-background_KL` 作为效用，或者单独报告反向定义的交互量，不能把不同方向的数值直接相减。`macro-F1` 的类别数固定为 69；即使某个单元没有预测出尾部类，也必须保留全部类别支持数并按预注册的 zero-support 规则计算，不能由预测最大类别动态截断。

晋级条件固定为：

1. 四个单元的输入、初始化、预算和干预清单完全一致；
2. 三 seed 的总体 interaction CI 下界大于 0，且至少两个 seed 的方向一致；
3. S1 相对 E0 的主任务指标不下降，且背景稳定性和病斑敏感性至少一项明确改善；
4. S1 不明显损害小病斑、掩码质量分层和 ECE/NLL；
5. 所有在线特征均来自预测前可观测量，GT 不进入路由；
6. 真实延迟、参数量和显存被测量后，才讨论部署收益。

如果 interaction CI 跨 0，停止“继续加理论”。此时只能报告 SPD 或反事实的独立作用，不能宣称二者存在协同；若 S1 仅提高干净 validation 分数而反事实指标不变，按普通正则化处理。

## 9. 外部数据和论文基线的时机

PlantSeg 2×2 通过后，冻结模型，再在 PlantWild 和 PlantDoc 做外部分类/鲁棒性验证；外部数据不参与模型选择。PlantSeg 主表至少补齐 U-Net、DeepLabV3+、SegFormer-B2，并把当前官方基准中的 mIoU/mAcc 与本地同口径重训结果分开标注。外部数据不能替代 PlantSeg 的主机制证据。

## 10. 目前不做的事情

- 不先做 Shapley-guided scheduler；
- 不扫描多个 `gamma`、阈值、mask alpha、损失权重或新主干；
- 不把现有 G7 的 log-spectrum screen 叫作完整 SPD 网络；
- 不把背景替换实验写成真实因果识别；
- 不用 GT oracle 选择部署模型；
- 不在 test 上反复看结果；
- 不因为 GPU 空闲而启动四个单元。

这份规划的成功标准是“能够判断连接点是否成立”，而不是预先保证 S1 一定胜出。这样即使交互为负，也会得到一个可投稿的机制结论和明确的后续方向。


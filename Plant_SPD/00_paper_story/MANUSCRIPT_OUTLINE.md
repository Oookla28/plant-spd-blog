# 可直接展开的骨架

**Before Comparing Geometry: Auditing Optimization and Readout in Covariance Pooling**

写作主线：协方差几何表示的比较，必须先审计读出能力、优化完成度和评价指标；否则有限训练配方的失败可能被误判为表示本身的失败。

本稿定位为受控实证研究与比较协议审计。SPD／二阶表示是研究对象，69类图像分类是当前验证任务。正文采用下列七节；数学命题、训练设置和证据代次必须与 [当前台账](CLAIMS_LEDGER.md) 一致。

完整研究过程与数学短证明见[根README](../README.md)，证明—代码—合同的逐项索引见[数学—证据对应表](MATHEMATICS_AND_EVIDENCE.md)。写作应从SPD通道关系、Log-Euclidean比较和谱灵敏度的正面动机展开，再用审计流程分离训练与读出因素，保持几何对象和验证方法的联系。

## 1 Introduction：先用反例提出问题

开篇两段可围绕以下事实展开：默认端到端低拟合不意味着固定特征不可分；本轮两批对应固定特征在指定凸目标的认证读出下均达 TRAIN100%，而有限头部配方干预显著恢复训练拟合（REC-F2-RAW、REC-F2-LOG、REC-A-SERIES）。

随后解释为何二阶池化尤其需要这种审计：矩阵映射同时改变特征尺度、读出参数化及反向传播，端点分数难以单独区分这些因素。已有几何和矩阵函数研究是起点，不能立“前人不知道 Log 为什么有效”的靶子。

贡献按四项写：

1. 四查审计：数学准入、函数可达、求解收敛、充分拟合；
2. 五来源种子20格中的条件性读出规律与指标分歧；
3. 预注册干预对有限训练配方影响的量化，以及未通过数学准入的判据退役。
4. 一个可认证的固定表示比较协议：正则化读出 gap/偏差界、平方距离 softmax 的局部秩条件，以及缺少证书时的 `ACCEPT / INDETERMINATE / REJECT` 决策。

**不要在引言使用：** 新几何、原配必胜、协同进化已识别、一般性 Log 优势、独立泛化已确认。首次新颖性和投稿档次不在本包结论范围内。

## 2 Background and Related Work：定义对象与已知危险类别

### 2.1 Covariance representations

定义全局／局部视图、协方差构造、收缩与谱下限、Raw/svec、Log 和 Sqrt；公式必须对应实际源码。svec 对称展平保留矩阵信息和 Frobenius 内积，不写成“破坏拓扑”；Log-Euclidean 不冒称一般仿射不变。

### 2.2 Matrix functions and optimization

谱距离分解与 Fréchet 公式作为标准背景；有谱下限时给出局部灵敏度的适用域。不要把局部算子范数等同参数梯度或裁剪率，更不能从历史日志补造上游梯度谱对齐。

协方差池化的优化已有[CVPR2020及TPAMI2023直接先例](../13_references/REFERENCES.md)。Related Work须说明本文审计的是指定映射、读出族与有限拟合条件；不宣称首次研究GCP优化。完整[文献及阅读范围](../13_references/REFERENCES.md)与[BibTeX](../13_references/references.bib)已整理。

### 2.3 Probing and measurement validity

把读出条件依赖放在既有 probing／control-task 的问题脉络中；本文实例化于协方差管线，不把“探针可能误导”本身称为新发现。引用前核对 [文献目录](../09_scientific_supplement_v1/) 与已有参考来源，正式全文阅读情况如实记录。

相关工作应明确区分：Alain–Bengio 的独立线性 probe、Hewitt–Liang 的 control-task/selectivity、conditional probing 的 baseline 条件信息、Dünner 等人的 primal-dual gap 证书、Temperature Check 对逆温度训练动力学的分析，以及 Chou 等人对表示—读出学习速度的分解、Barin-Pacela 等人对线性可访问性/摊销缺口的讨论和 Garg 等人的线性表示容量界。本文不重复这些结果，也不把“表示—读出分解”或“可访问性缺口”写成首次提出；新切口是把固定协方差表示比较写成带正则化偏差、solver gap、Jacobian 条件和明确拒绝分支的确定性归因协议，完整边界见 [PRIOR_ART_AND_NOVELTY_BOUNDARIES_V2.md](../09_scientific_supplement_v1/math/PRIOR_ART_AND_NOVELTY_BOUNDARIES_V2.md)。

## 3 Audit Protocol：四项检查进入正文

主表：

| 闸门 | 通过凭据 | 不通过后 |
|---|---|---|
| 主张／量尺数学准入 | 公式、单位、量词、适用域与问题一致 | 登记 MAF，判据退役，不计 EPM |
| 函数可达 | native 嵌入及数值等价正控制 | HOLD，不归罪表示 |
| 求解收敛 | 明确目标、完整梯度与 gap | 不进入认证读出比较 |
| 充分训练拟合 | 独立报告 TRAIN accuracy/F1/CE | 低拟合不当作表示质量裁决 |

用 REC-NATIVE、REC-RISK、REC-UNDERFIT 展示后三项为何不能相互替代。说明完整 W+b 风险预算约束 TRAIN 超额风险，不是参数范数预算、不是 HELD 风险界。MAF-Q99 与 MAF-ONEHOT 则展示第一项的必要性。

本地事前冻结、执行前后 SHA、偏差记录与事后登记分开。EPM 只收数学有效、事前可否证且来源链可定位的经验预测；不补造“三次 miss”或外部不可篡改注册。

正文在本节末加入两个理论框：

- **固定表示证书：** 先定义 \(J_{\lambda,\mathcal H}^\star\)，再给出无正则目标的 \(B^0_{ij}\) 和 native-anchor 的弱证书，明确哪些范数界真正被证明；
- **局部动力学证书：** (K=2) 时单样本固定 Jacobian 的秩至多1；(K\ge3) 时必须同时满足非目标 margin 不全相等和 Jacobian 在二维输出切空间上保持秩2。batch、AdamW 和 clipping 作为反例边界放入附录。

完整证明写入 [RIGOROUS_AUDIT_THEORY_V2.md](../09_scientific_supplement_v1/math/RIGOROUS_AUDIT_THEORY_V2.md)，CPU合同入口为 [verify_rigorous_audit_v2.py](../09_scientific_supplement_v1/math/verify_rigorous_audit_v2.py)。

## 4 End-to-End Observations：不同数字的解释边界

证据：原 C01 配对结果，以及 REC-TS、REC-FITPROGRESS、REC-CLIP。

- 分类与概率：保留 Raw/Log 温标前后四条件。NLL差距压缩是描述性结果，不是校准的因果份额。
- 训练阶段：事后 TRAIN CE 条件比较保留全部达到／未达到端点；不能称为完全消除隐式正则或优化路径差异。
- 裁剪与更新：并列触发率、系数与采样实际更新；不把系数方差图冒充 Adam 二阶矩图。

此节用原 HELD 聚合结果，必须说明反复开发池、重叠划分及分析的探索性。它不与本轮 FIT-only 结果合并估计。

**图2：** 三类边界面板。建议标题“Scores and diagnostics answer different questions”，不使用“Not Calibration, Not Underfitting!”这种排他性结论。

## 5 Certified Cross-Readout Analysis：条件规律与例外同现

主证据为 REC-MATRIX-5S：5个来源编码器训练seed×2来源×2读出，共20次全新拟合；同一重复开发池，确定性读出全零初始化。本文将“种子”区分为来源训练随机性与求解器随机性。

先给四查验收，再给 F1/NLL。主图使用扩展20格，附种子级简单效应、交互及反向例外。F1与NLL并列，不用平均热图遮住例外。所有 TRAIN100% 与完整数值证书分别报告，互不代替。

**图3：** 四cell分布／热图＋逐种子差异＋指标分歧。

早期八格 REC-PROBE-2S 放附录，注明五个接受端点加三个另行恢复端点、另一lambda。新20格全部重拟合，不是旧8格直接补12格；不能混合成28格平均。

## 6 Equal-Head Stress Test and Preregistered Interventions

### 6.1 同头族仍出现拟合断裂

固定头族的四种条件使用 TRAIN 指标。Raw joint与Log joint的跨seed均值只作原矩阵背景；A4 必须对同种子旧 Log joint 36.05%比较，不借34.12%均值增加增益。

**图1（放引言附近，详细说明在此）：** 默认低拟合、对应固定特征认证100%、有限干预恢复；不同特征来源与证据代次分面。本轮 F2 两批与历史 E08 分开。

### 6.2 F1–F4：哪些量可测，哪些解释不能入场

数值求和实际头LR而非名义LR；参数形状核对完整73002维 W+b；逐坐标与RMS单位不能混用。q99×B 非硬界、one-hot插值范数非分类必要范数，以MAF退役，不写成被实验否证。

固定CE需求区间、有效预算和终态u进入附录；正文保留六判据核对的结论。末态绝对u不是SNR，旧完整轨迹不可用；新前瞻轨迹不回填历史。

### 6.3 预注册干预与竞争解释

按 A0→A→A2/A2′/A3→A4 的设计顺序报告全部预定端点。删除头部WD未恢复拟合（24.18→24.18），当前配方下直接WD主导解释被削弱。A2三种子87.80±0.24pp为训练seed样本SD；A2′同时改变步数、访问数和cosine时长；A4同时改变LR与warmup；A3为温度重参数化。

**B非充分性反例进正文：** A0和A3的B同为1.3755，F1差52.4968pp。它足以拒绝统一预算剂量轴，但不说明预算因素完全无关。禁止拟合异质干预“近似对数恢复曲线”。

**图4：** 干预点、必要前瞻轨迹、共变量和判决边界。τ(t)确证评分延期，不从已存轨迹倒写事前预测。条件A4-Raw按事前恢复门跳过，保留状态而不补齐一个未选择的对照。

## 7 Discussion and Conclusion：分层结账

### 已支持

低训练拟合不足以判定对应固定表示不可分；不同读出、目标和训练配方影响解释。认证读出中的来源×映射比较有条件且依赖指标，预注册干预显示有限配方对训练拟合有实质影响。

### 仍开放

唯一的行进／方向／曲率／SNR归因、原端到端优势的因果来源、独立任务和独立泛化。原有重复HELD与本轮FIT-only边界明确披露；训练100%不等于表示上限。

### 方法学总结

数学准入先于经验打分；函数可达、收敛和充分拟合独立验收；历史缺失记不可用；事后登记不反向赋予预注册身份。保留未命中和失败，但不把数量当论文贡献。

## 主表与附录清单

| 位置 | 内容 | 工件入口 |
|---|---|---|
| Table 1 | 数据、代次、头族、FIT/HELD范围、seed定义 | 12中的证据登记＋各原协议 |
| Table 2 | 可达控制、认证读出与充分拟合分代 | 09中的native_pc10及expanded_probe_final_v1，11中的两批F2证书 |
| Table 3 | 五种子20格聚合、逐seed例外 | 09中的expanded_probe_final_v1/SUMMARY.json |
| Table 4 | 全A端点、共变、原预测与判决 | 11中的F1_F4_FORENSICS.json和DECISION_TREE_ADDENDUM_V1.md |
| Table 5 | 数学准入、四查与失败处置 | 12中的AUDIT_PROTOCOL_FOUR_GATES_V1.md及11中的DECISION_TREE_ADDENDUM_V1.md |
| Appendix A | 谱距离／Fréchet、风险预算、固定CE需求界 | 09 math与11 math，区分标准工具与本次诊断 |
| Appendix B | 旧原型／强正则／早期八格演进 | 02历史目录、REC-UNDERFIT、REC-PROBE-2S |
| Appendix C | 完整取证、前瞻轨迹、SHA与偏差记录 | 11与12，不新造历史轨迹或外部时间戳 |

表图的已有文件和具体待做排版以 [05_table_figure_plan](../05_table_figure_plan/) 为准；本页只规定论证任务，不把计划图当已完成成果。

## 推荐落笔顺序

先第3和第6节，确保四查与A结果逐条站在证据上；再第5节，保留全部例外；再第4、2节；最后写第1、7节与摘要。每个数字先写REC ID，定稿时替换为正式表图引用，数据指针继续保留在补充材料。

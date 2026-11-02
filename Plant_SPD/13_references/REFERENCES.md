# 参考文献与项目用途

本清单区分正文依据、历史方法、近邻审查及数据出处。每条给出原始入口、项目用途、阅读范围和本地PDF（如已取得）。**下载到PDF不等于已阅读全文，文献身份成立不等于方法已经复现。**

共39条，已放入25份公开PDF；其余保留官方入口。机器清单见[REFERENCE_CATALOG.json](REFERENCE_CATALOG.json)，引用可导入[references.bib](references.bib)。本轮新增的八条条目用于限定 probe、凸 gap、温度动力学、表示—读出分解和线性可访问性的原创性边界，不把标准工具写成本文新理论。

## 正文理论与方法

<a id="arsigny2006logeuclidean"></a>
### arsigny2006logeuclidean · Log-Euclidean metrics for fast and simple calculus on diffusion tensors

Vincent Arsigny; Pierre Fillard; Xavier Pennec; Nicholas Ayache. **2006**. Magnetic Resonance in Medicine 56(2):411–421.

- 正式出处：[原始页面](https://onlinelibrary.wiley.com/doi/abs/10.1002/mrm.20965)；DOI：`10.1002/mrm.20965`。
- 文件：**官方链接级**：本次未取得可核定的公开全文，不冒充本地已有PDF。
- 项目用途：SPD对数域、Log-Euclidean黎曼几何及与AIRM的区别；标准背景，不是本文原创度量。
- 本次核对范围：本次核对出版社元数据、作者机构公开PDF可检索正文片段；项目README已有引用。未发现可证明此前逐页全文精读的记录。
- 项目依据：[README.md](../README.md)

<a id="almohy2013frechet"></a>
### almohy2013frechet · Computing the Fréchet Derivative of the Matrix Logarithm and Estimating the Condition Number

Awad H. Al-Mohy; Nicholas J. Higham; Samuel D. Relton. **2013**. SIAM Journal on Scientific Computing 35(4):C394–C410.

- 正式出处：[原始页面](https://doi.org/10.1137/120885991)；DOI：`10.1137/120885991`。
- 文件：[本地PDF](pdfs/almohy2013frechet.pdf)；SHA-256 `033d2f36176eb56b7f573484c81aee1daf86cd14b313a7aef59cc91583ae4e12`。
- 项目用途：矩阵Log Fréchet导数、条件数与数值算法的标准工具出处；本文SPD/Frobenius范数证明应说明专门条件，不能声称首次发现Log导数敏感性。
- 本次核对范围：本次核对作者大学库PDF题名页、DOI及摘要/引言公开片段；09数学附录已有引用。未宣称本次阅读全文。
- 项目依据：[09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md)；[README.md](../README.md)

<a id="lin2015bilinear"></a>
### lin2015bilinear · Bilinear CNN Models for Fine-Grained Visual Recognition

Tsung-Yu Lin; Aruni RoyChowdhury; Subhransu Maji. **2015**. ICCV 2015:1449–1457.

- 正式出处：[原始页面](https://openaccess.thecvf.com/content_iccv_2015/html/Lin_Bilinear_CNN_Models_ICCV_2015_paper.html)；DOI：`10.1109/ICCV.2015.170`。
- 文件：[本地PDF](pdfs/lin2015bilinear.pdf)；SHA-256 `2ff93a7e850e62de5ae76fceb6a2c7d3efaf224e47ff4d0c9f24f99b805b0a0a`。
- 项目用途：局部特征外积与二阶通道交互的视觉先例，支撑二阶池化背景；本文不是重新发明双线性池化。
- 本次核对范围：本次核对CVF/IEEE元数据与摘要；公开PDF只核对题名页和引言片段。此前是否全文精读未确认。
- 项目依据：[README.md](../README.md)

<a id="lin2017improved"></a>
### lin2017improved · Improved Bilinear Pooling with CNNs

Tsung-Yu Lin; Subhransu Maji. **2017**. BMVC 2017:117.1–117.12.

- 正式出处：[原始页面](https://www.bmva-archive.org.uk/bmvc/2017/papers/paper117/index.html)；DOI：`10.5244/C.31.117`。
- 文件：[本地PDF](pdfs/lin2017improved.pdf)；SHA-256 `ba3b6b10ee0616f592e556c4200f207d1863ae0a4806d05de85aebf2395c555f`。
- 项目用途：已比较矩阵sqrt/log归一化与梯度实现。其sqrt优势带有后续elementwise sqrt及L2归一化条件，不能移植为任意头族的普遍定理。
- 本次核对范围：本次核对BMVA官方页面题名、作者、BibTeX、摘要；项目数学附录已有参考定位。不将本次核对记作全文复现。
- 项目依据：[09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md)；[README.md](../README.md)

<a id="li2017mpncov"></a>
### li2017mpncov · Is Second-Order Information Helpful for Large-Scale Visual Recognition?

Peihua Li; Jiangtao Xie; Qilong Wang; Wangmeng Zuo. **2017**. ICCV 2017:2070–2078.

- 正式出处：[原始页面](https://openaccess.thecvf.com/content_iccv_2017/html/Li_Is_Second-Order_Information_ICCV_2017_paper.html)；DOI本次未核定或原条目未提供，不编造。
- 文件：[本地PDF](pdfs/li2017mpncov.pdf)；SHA-256 `46b5768e92119f2379e34d090f206d5fa81acdbc038144d19812582e73ff84fc`。
- 项目用途：MPN-COV会议原作：协方差鲁棒估计、矩阵幂归一化与视觉识别背景。与2021期刊扩展分版本登记。
- 本次核对范围：本次核对CVF官方元数据与摘要。未将其他平台论文总结冒充原文。
- 版本说明：Public local PDF is author arXiv v3 (2018 revision), not asserted byte-identical to the 2017 CVF proceedings PDF.
- 项目依据：[09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md)

<a id="li2018isqrtcov"></a>
### li2018isqrtcov · Towards Faster Training of Global Covariance Pooling Networks by Iterative Matrix Square Root Normalization

Peihua Li; Jiangtao Xie; Qilong Wang; Zilin Gao. **2018**. CVPR 2018:947–955.

- 正式出处：[原始页面](https://openaccess.thecvf.com/content_cvpr_2018/html/Li_Towards_Faster_Training_CVPR_2018_paper.html)；DOI：`10.1109/CVPR.2018.00105`。
- 文件：[本地PDF](pdfs/li2018isqrtcov.pdf)；SHA-256 `f72352788c1644a3c07a72a422b8d326f13485ad60ba30bab217b6c97a9733d3`。
- 项目用途：iSQRT-COV：可微矩阵平方根与训练效率先例。本文Sqrt参考臂不能默认等同完整iSQRT-COV体系。
- 本次核对范围：本次核对CVF/IEEE元数据、摘要及引言公开片段；未新跑原代码。
- 项目依据：[README.md](../README.md)；[09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md)

<a id="wang2021globalcovariance"></a>
### wang2021globalcovariance · Deep CNNs Meet Global Covariance Pooling: Better Representation and Generalization

Qilong Wang; Jiangtao Xie; Wangmeng Zuo; Lei Zhang; Peihua Li. **2021**. IEEE Transactions on Pattern Analysis and Machine Intelligence 43(8):2582–2597.

- 正式出处：[原始页面](https://arxiv.org/abs/1904.06836)；DOI：`10.1109/TPAMI.2020.2974833`。
- 文件：[本地PDF](pdfs/wang2021globalcovariance.pdf)；SHA-256 `9d40dae307f64699a470d1dfd91c7a9e2a3bd14ddf3e29d123eb1b51da01b738`。
- 项目用途：MPN-COV/全局协方差池化期刊扩展，已有鲁棒估计与Power-Euclidean几何论述；谱归一化不是本文新发现。
- 本次核对范围：本次核对作者arXiv版本及作者所属大学正式期刊记录、摘要。项目附录已有引用；未把引用本身当作完整精读证明。
- 版本说明：本地PDF为arXiv:1904.06836v2的2020年作者稿；正式引用为2021年TPAMI卷期，DOI包含2020。作者稿与正式发表版本分开标记，不声称逐字节一致。
- 项目依据：[09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md)

<a id="wang2020optimization"></a>
### wang2020optimization · What Deep CNNs Benefit From Global Covariance Pooling: An Optimization Perspective

Qilong Wang; Li Zhang; Banggu Wu; Dongwei Ren; Peihua Li; Wangmeng Zuo; Qinghua Hu. **2020**. CVPR 2020:10771–10780.

- 正式出处：[原始页面](https://openaccess.thecvf.com/content_CVPR_2020/html/Wang_What_Deep_CNNs_Benefit_From_Global_Covariance_Pooling_An_Optimization_CVPR_2020_paper.html)；DOI本次未核定或原条目未提供，不编造。
- 文件：[本地PDF](pdfs/wang2020optimization.pdf)；SHA-256 `0404c70a3505087b82636928f179a5a765ed4dd717124b949393cc8c587033e1`。
- 项目用途：直接优化先例：已有GCP损失光滑性、梯度预测性与二阶优化关系分析。论文不能立靶子称前人只报精度或不理解优化。本文切口须限定到映射/读出/有限拟合的受控审计。
- 本次核对范围：本次新核对CVF正式PDF题名页、摘要与引言片段；没有此前项目完整阅读记录，标注本轮补充相关工作。
- 项目依据：[README.md](../README.md)；[00_paper_story/MANUSCRIPT_OUTLINE.md](../00_paper_story/MANUSCRIPT_OUTLINE.md)

<a id="wang2023optimization"></a>
### wang2023optimization · Towards a Deeper Understanding of Global Covariance Pooling in Deep Learning: An Optimization Perspective

Qilong Wang; Zhaolin Zhang; Mingze Gao; Jiangtao Xie; Pengfei Zhu; Peihua Li; Wangmeng Zuo; Qinghua Hu. **2023**. IEEE Transactions on Pattern Analysis and Machine Intelligence 45(12):15802–15819.

- 正式出处：[原始页面](https://doi.org/10.1109/TPAMI.2023.3321392)；DOI：`10.1109/TPAMI.2023.3321392`。
- 文件：**官方链接级**：本次未取得可核定的公开全文，不冒充本地已有PDF。
- 项目用途：直接优化/后归一化期刊先例，已讨论更平坦极小值、梯度预条件与DropCov。必须在新颖性边界中单列。
- 本次核对范围：本次核对作者主页、作者团队官方项目README、所属大学页面及书目摘要；作者PDF按钮仅指向IEEE，未取得合法公开全文，不作逐公式或逐实验复核声明。
- 项目依据：[00_paper_story/MANUSCRIPT_OUTLINE.md](../00_paper_story/MANUSCRIPT_OUTLINE.md)

<a id="guo2017calibration"></a>
### guo2017calibration · On Calibration of Modern Neural Networks

Chuan Guo; Geoff Pleiss; Yu Sun; Kilian Q. Weinberger. **2017**. ICML 2017, Proceedings of Machine Learning Research 70:1321–1330.

- 正式出处：[原始页面](https://proceedings.mlr.press/v70/guo17a.html)；DOI本次未核定或原条目未提供，不编造。
- 文件：[本地PDF](pdfs/guo2017calibration.pdf)；SHA-256 `df7c93f97204f8a3c2b10f6d5bf5265baac25f00c1ae3b473a3e1dbc102dacb2`。
- 项目用途：Temperature scaling和概率校准背景。本文的差距收缩89.3%不能解释成几何因果贡献被精确分摊。
- 本次核对范围：本次核对PMLR官方元数据与摘要；项目README已有引用与E03温标方法对应。未声明原论文全文复现。
- 项目依据：[README.md](../README.md)；[02_experiments/E03_calibration/](../02_experiments/E03_calibration/)

<a id="hewitt2019controlprobes"></a>
### hewitt2019controlprobes · Designing and Interpreting Probes with Control Tasks

John Hewitt; Percy Liang. **2019**. EMNLP-IJCNLP 2019:2733–2743.

- 正式出处：[原始页面](https://aclanthology.org/D19-1275/)；DOI：`10.18653/v1/D19-1275`。
- 文件：[本地PDF](pdfs/hewitt2019controlprobes.pdf)；SHA-256 `557f5d7dc18b17d641c9e54c91c0071b00612f9ec051fc788bcc7117f4d194d0`。
- 项目用途：探针性能依赖读出容量与控制任务的解释警示。本文借鉴审计视角，不声称复现NLP控制任务或继承其结论到所有视觉表示。
- 本次核对范围：本次核对ACL正式作者、题名、DOI、摘要和BibTeX；README已有引用。未声明本项目实施过其随机标签控制任务。
- 项目依据：[README.md](../README.md)；[00_paper_story/MANUSCRIPT_OUTLINE.md](../00_paper_story/MANUSCRIPT_OUTLINE.md)

<a id="kingma2015adam"></a>
### kingma2015adam · Adam: A Method for Stochastic Optimization

Diederik P. Kingma; Jimmy Ba. **2015**. ICLR 2015.

- 正式出处：[原始页面](https://arxiv.org/abs/1412.6980)；DOI：`10.48550/arXiv.1412.6980`。
- 文件：[本地PDF](pdfs/kingma2015adam.pdf)；SHA-256 `eab9c73ae2ceda884b94830bda99312254bac4806f6c9f045cbab90721ecda31`。
- 项目用途：一二阶矩EMA、偏差修正与Adam更新背景。本文M6加权Cauchy推导是指定窗口下的数学审查，不把原Adam收敛声称无条件推广。
- 本次核对范围：本次核对作者arXiv题名、作者、会议注释与摘要；项目M6方法对应。不声称本轮从头审阅全部收敛证明。
- 项目依据：[README.md](../README.md)；[09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md](../09_scientific_supplement_v1/math/MATHEMATICAL_APPENDIX.md)

<a id="loshchilov2019adamw"></a>
### loshchilov2019adamw · Decoupled Weight Decay Regularization

Ilya Loshchilov; Frank Hutter. **2019**. ICLR 2019.

- 正式出处：[原始页面](https://arxiv.org/abs/1711.05101)；DOI：`10.48550/arXiv.1711.05101`。
- 文件：[本地PDF](pdfs/loshchilov2019adamw.pdf)；SHA-256 `9d5af48931e773d6983d167e15c06ef594475b751c1f263827f5ed3c7a00d0d8`。
- 项目用途：AdamW解耦WD与显式L2正则不等价；是本项目避免把凸目标证书直接移植到AdamW路径的重要依据。
- 本次核对范围：本次核对作者arXiv元数据、ICLR2019发表注释和摘要；OpenReview触发浏览器验证，未绕过。
- 项目依据：[README.md](../README.md)；[00_paper_story/MATHEMATICS_AND_EVIDENCE.md](../00_paper_story/MATHEMATICS_AND_EVIDENCE.md)

## 历史方法与早期探索

<a id="H-SPDNET-2017"></a>
### H-SPDNET-2017 · A Riemannian Network for SPD Matrix Learning

Zhiwu Huang; Luc Van Gool. **2017**. Proceedings of the AAAI Conference on Artificial Intelligence, 31(1), 2036–2042.

- 正式出处：[原始页面](https://ojs.aaai.org/index.php/AAAI/article/view/10866)；DOI：`10.1609/aaai.v31i1.10866`。
- 文件：[本地PDF](pdfs/H-SPDNET-2017.pdf)；SHA-256 `1ba52073d19f7d858d8e2660a08f9298b175fd173fe4a745e2d55292227aad50`。
- 项目用途：SPD网络、双线性映射、特征值修正与LogEig的既有方法锚点；用于限制“使用SPD即原创”的主张。
- 本次核对范围：本次核对AAAI官方题名、作者、摘要、年份、DOI，并打开7页官方PDF；未逐页重审全部证明和实验。
- 项目依据：[08_original_source_snapshots/history_f/PLANTSEG_2X2_MECHANISM_PLAN_V2.md](../08_original_source_snapshots/history_f/PLANTSEG_2X2_MECHANISM_PLAN_V2.md)

<a id="H-GBWBN-2025"></a>
### H-GBWBN-2025 · Learning to Normalize on the SPD Manifold under Bures-Wasserstein Geometry

Rui Wang; Shaocheng Jin; Ziheng Chen; Xiaoqing Luo; Xiao-Jun Wu. **2025**. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 8289–8298.

- 正式出处：[原始页面](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_Learning_to_Normalize_on_the_SPD_Manifold_under_Bures-Wasserstein_Geometry_CVPR_2025_paper.html)；DOI本次未核定或原条目未提供，不编造。
- 文件：[本地PDF](pdfs/H-GBWBN-2025.pdf)；SHA-256 `05fc8c3ba7a8ef30bdc88eae128828104db7c9dc2acc606f486777f189b72568`。
- 项目用途：可学习SPD度量与病态协方差归一化的近邻；本项目早期讨论和官方代码参考，不是本项目已实现或已复现的新模块。
- 本次核对范围：本次核对CVF官方PDF索引的题名、作者、摘要及首段，并核对作者官方仓库声明；未通读或复现全文。出版DOI未在本次primary页面确定，留空；预印本标识为2504.00660。
- 项目依据：[08_original_source_snapshots/history_f/TOP_CONFERENCE_EXTENSION_PLAN_V1.md](../08_original_source_snapshots/history_f/TOP_CONFERENCE_EXTENSION_PLAN_V1.md)

<a id="H-MP-1967"></a>
### H-MP-1967 · Distribution of eigenvalues for some sets of random matrices

V. A. Marchenko; L. A. Pastur. **1967**. Mathematics of the USSR-Sbornik, 1(4), 457–483.

- 正式出处：[原始页面](https://www.mathnet.ru/eng/sm4101)；DOI：`10.1070/SM1967v001n04ABEH001994`。
- 文件：[本地PDF](pdfs/H-MP-1967.pdf)；SHA-256 `a7ed92b80fd17f24f7e49f87e0cbf236a53ef98768d5aeebededf62d873c3b4a`。
- 项目用途：RMT谱边界与样本量/维度条件的理论出处；不能把各向同性独立采样条件直接等同于相关视觉token。
- 本次核对范围：本次核对MathNet官方元数据并打开27页英文PDF；未重证全篇随机矩阵极限定理。
- 项目依据：[08_original_source_snapshots/history_f/SPD_ESTIMATION_RESEARCH_PLAN_V2.md](../08_original_source_snapshots/history_f/SPD_ESTIMATION_RESEARCH_PLAN_V2.md)

<a id="H-LW-2004"></a>
### H-LW-2004 · A well-conditioned estimator for large-dimensional covariance matrices

Olivier Ledoit; Michael Wolf. **2004**. Journal of Multivariate Analysis, 88(2), 365–411.

- 正式出处：[原始页面](https://www.sciencedirect.com/science/article/pii/S0047259X03000964)；DOI：`10.1016/S0047-259X(03)00096-4`。
- 文件：**官方链接级**：本次未取得可核定的公开全文，不冒充本地已有PDF。
- 项目用途：Ledoit–Wolf线性自适应收缩基线的出处；与固定gamma收缩、OAS、ANS分别比较。
- 本次核对范围：本次核对出版方摘要/元数据及作者发表稿的首页信息；未逐页重读证明。
- 项目依据：[08_original_source_snapshots/history_f/SPD_ESTIMATION_RESEARCH_PLAN_V2.md](../08_original_source_snapshots/history_f/SPD_ESTIMATION_RESEARCH_PLAN_V2.md)；[08_original_source_snapshots/history_f/experiments/spd_estimation_stage_a_v1/REPORT.md](../08_original_source_snapshots/history_f/experiments/spd_estimation_stage_a_v1/REPORT.md)

<a id="H-OAS-2010"></a>
### H-OAS-2010 · Shrinkage Algorithms for MMSE Covariance Estimation

Yilun Chen; Ami Wiesel; Yonina C. Eldar; Alfred O. Hero III. **2010**. IEEE Transactions on Signal Processing, 58(10), 5016–5029.

- 正式出处：[原始页面](https://ieeexplore.ieee.org/abstract/document/5484583)；DOI：`10.1109/TSP.2010.2053029`。
- 文件：[本地PDF](pdfs/H-OAS-2010.pdf)；SHA-256 `0a74b89eb3e63ee49b15272668185186e3d3a9a3da64a79d9d14abe912379333`。
- 项目用途：原始OAS/RBLW基线，尤其原OAS公式中的2/p因子与高斯条件；不是仅以库默认实现代替原算法。
- 本次核对范围：本次核对IEEE出版元数据/摘要与作者arXiv摘要。历史stage-A报告记录原OAS Eq.23口径；本次不重新执行或重证。
- 项目依据：[08_original_source_snapshots/history_f/SPD_ESTIMATION_RESEARCH_PLAN_V2.md](../08_original_source_snapshots/history_f/SPD_ESTIMATION_RESEARCH_PLAN_V2.md)；[08_original_source_snapshots/history_f/experiments/spd_estimation_stage_a_v1/REPORT.md](../08_original_source_snapshots/history_f/experiments/spd_estimation_stage_a_v1/REPORT.md)

<a id="H-LW-NLS-2012"></a>
### H-LW-NLS-2012 · Nonlinear shrinkage estimation of large-dimensional covariance matrices

Olivier Ledoit; Michael Wolf. **2012**. The Annals of Statistics, 40(2), 1024–1060.

- 正式出处：[原始页面](https://doi.org/10.1214/12-AOS989)；DOI：`10.1214/12-AOS989`。
- 文件：[本地PDF](pdfs/H-LW-NLS-2012.pdf)；SHA-256 `9a5744f59fa588f016bf9e70e91fa2c32cc1b1d730cf3eed027537993d12e268`。
- 项目用途：说明非线性谱收缩已有成熟先例；与2020解析ANS版本分开，不把所有非线性收缩统称为项目原创。
- 本次核对范围：本次核对出版方Project Euclid元数据/摘要及作者发表稿首页索引；未通读全部证明。
- 项目依据：[08_original_source_snapshots/history_f/SPD_ESTIMATION_RESEARCH_PLAN_V2.md](../08_original_source_snapshots/history_f/SPD_ESTIMATION_RESEARCH_PLAN_V2.md)

<a id="H-ANS-2020"></a>
### H-ANS-2020 · Analytical nonlinear shrinkage of large-dimensional covariance matrices

Olivier Ledoit; Michael Wolf. **2020**. The Annals of Statistics, 48(5), 3043–3065.

- 正式出处：[原始页面](https://doi.org/10.1214/19-AOS1921)；DOI：`10.1214/19-AOS1921`。
- 文件：[本地PDF](pdfs/H-ANS-2020.pdf)；SHA-256 `d28a7f6897f28f60aaabd1ea4416386c151be31c0fde737790cdad9ca07254ad`。
- 项目用途：历史合成估计实验正式ANS实现来源；适用域、带宽、Hilbert核与原作者算法已经单独保留审查，不宣称新估计器。
- 本次核对范围：本次核对作者发表稿摘要/首页及本地REFERENCE_AUDIT.json；历史审查已逐公式记录适用域。未在本次重新运行算法或复核全部证明。
- 项目依据：[08_original_source_snapshots/history_f/SPD_ESTIMATION_RESEARCH_PLAN_V2.md](../08_original_source_snapshots/history_f/SPD_ESTIMATION_RESEARCH_PLAN_V2.md)；[08_original_source_snapshots/history_f/references/ledoit_wolf_ans_primary_v1/REFERENCE_AUDIT.json](../08_original_source_snapshots/history_f/references/ledoit_wolf_ans_primary_v1/REFERENCE_AUDIT.json)；[08_original_source_snapshots/history_f/experiments/spd_estimation_stage_a_v1/REPORT.md](../08_original_source_snapshots/history_f/experiments/spd_estimation_stage_a_v1/REPORT.md)

<a id="H-KISS-2021"></a>
### H-KISS-2021 · Shrinkage estimation of large covariance matrices: Keep it simple, statistician?

Olivier Ledoit; Michael Wolf. **2021**. Journal of Multivariate Analysis, 186, 104796.

- 正式出处：[原始页面](https://www.sciencedirect.com/science/article/pii/S0047259X21000749)；DOI：`10.1016/j.jmva.2021.104796`。
- 文件：[本地PDF](pdfs/H-KISS-2021.pdf)；SHA-256 `f6a653d3c4ecbf5d6c6895d584ca2cbe1f5e8ffde127c0dc3f1a3d2108291554`。
- 项目用途：创新边界：多损失下的旋转等变收缩已经覆盖Log-Euclidean目标；不能把“按几何目标改谱值”笼统写成空白。
- 本次核对范围：本次核对出版方摘要和UZH作者发表稿索引；历史审查只读相关摘段与损失表/命题，明确未逐页通读证明。
- 项目依据：[08_original_source_snapshots/history_f/paper/SPD_ESTIMATION_NOVELTY_BOUNDARIES_20261025.md](../08_original_source_snapshots/history_f/paper/SPD_ESTIMATION_NOVELTY_BOUNDARIES_20261025.md)

<a id="H-DESAS-2025"></a>
### H-DESAS-2025 · DES-AS: Dynamic ensemble selection based on algorithm Shapley

Zhong-Liang Zhang; Yun-Hao Zhu; Xing-Gang Luo. **2025**. Pattern Recognition, 157, 110899.

- 正式出处：[原始页面](https://www.sciencedirect.com/science/article/pii/S0031320324006502)；DOI：`10.1016/j.patcog.2024.110899`。
- 文件：**官方链接级**：本次未取得可核定的公开全文，不冒充本地已有PDF。
- 项目用途：早期Shapley正贡献筛选与归一化权重审计的直接既有方法；本项目离线五模型筛查不是完整复现其逐查询DES系统。
- 本次核对范围：本次核对出版方摘要、元数据与section snippets；未获得开放全文，不能称全文逐公式复核。出版年份2025，DOI带2024不等于2024卷期。
- 项目依据：[08_original_source_snapshots/history_f/PLANTSEG_2X2_MECHANISM_PLAN_V2.md](../08_original_source_snapshots/history_f/PLANTSEG_2X2_MECHANISM_PLAN_V2.md)；[08_original_source_snapshots/history_f/DESAS_SHAPLEY_NEXT_PLAN_V1.md](../08_original_source_snapshots/history_f/DESAS_SHAPLEY_NEXT_PLAN_V1.md)；[08_original_source_snapshots/history_f/experiments/desas_shapley_audit_v1/DESAS_SHAPLEY_AUDIT_V1.md](../08_original_source_snapshots/history_f/experiments/desas_shapley_audit_v1/DESAS_SHAPLEY_AUDIT_V1.md)

<a id="H-ACTIVEDIAG-2026"></a>
### H-ACTIVEDIAG-2026 · ActiveDiag: Dynamic Fusion of Discrepancy and Uncertainty in Active Learning for Database Anomaly Diagnosis

Peize Yuan; Zixuan Li; Xiyue Gao; Mingzhe Wang; Hui Li; Yanguo Peng; Yaofeng Tu; Jiangtao Cui. **2026**. Database Systems for Advanced Applications (DASFAA 2026), LNCS 16536, 507–525.

- 正式出处：[原始页面](https://link.springer.com/chapter/10.1007/978-981-92-0366-6_31)；DOI：`10.1007/978-981-92-0366-6_31`。
- 文件：**官方链接级**：本次未取得可核定的公开全文，不冒充本地已有PDF。
- 项目用途：用户提供的早期摘要级阅读启发：动态融合差异性和不确定性选择标注样本。没有证据表明本项目实现或复现了TSN/DUDF；不进入当前SPD主结果证据。
- 本次核对范围：本次已在Springer primary核对题名、八位作者、会议/卷页/DOI和摘要。全文需机构访问，未取得开放全文，未复核DUDF公式、数据集或实验细节。
- 项目依据：本对话用户提供的摘要级材料或本轮补充相关工作；没有虚构本地全文阅读记录。

<a id="H-LFF-2020"></a>
### H-LFF-2020 · Learning from Failure: De-biasing Classifier from Biased Classifier

Junhyun Nam; Hyuntak Cha; Sungsoo Ahn; Jaeho Lee; Jinwoo Shin. **2020**. Advances in Neural Information Processing Systems, 33 (NeurIPS 2020).

- 正式出处：[原始页面](https://proceedings.neurips.cc/paper/2020/hash/eddc3427c5d77843c2253f1e799fe933-Abstract.html)；DOI本次未核定或原条目未提供，不编造。
- 文件：[本地PDF](pdfs/H-LFF-2020.pdf)；SHA-256 `85a7935b53656a07c242569660ea126bf81641a1ec0d40fd1ac949f391b40f11`。
- 项目用途：早期偏置/反事实训练规划的对照启发：偏置模型与反偏样本学习应分开控制，不能把受控图像增强直接当成已识别因果。
- 本次核对范围：本次核对NeurIPS官方题名、作者、卷年和摘要；未在本次通读或复现全文。官方页未提供DOI，留空。
- 项目依据：[08_original_source_snapshots/history_f/PLANTSEG_2X2_MECHANISM_PLAN_V2.md](../08_original_source_snapshots/history_f/PLANTSEG_2X2_MECHANISM_PLAN_V2.md)

<a id="H-WHAC-2023"></a>
### H-WHAC-2023 · A Whac-a-Mole Dilemma: Shortcuts Come in Multiples Where Mitigating One Amplifies Others

Zhiheng Li; Ivan Evtimov; Albert Gordo; Caner Hazirbas; Tal Hassner; Cristian Canton Ferrer; Chenliang Xu; Mark Ibrahim. **2023**. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 20071–20082.

- 正式出处：[原始页面](https://openaccess.thecvf.com/content/CVPR2023/html/Li_A_Whac-a-Mole_Dilemma_Shortcuts_Come_in_Multiples_Where_Mitigating_One_CVPR_2023_paper.html)；DOI：`10.1109/CVPR52729.2023.01922`。
- 文件：[本地PDF](pdfs/H-WHAC-2023.pdf)；SHA-256 `e6dc4e8398697cd32b396255a605f69c00b005401246ba078ff4cf1fe0858d60`。
- 项目用途：早期多捷径鲁棒性压力测试的文献依据；提醒背景、纹理、共现对象等不能合并成单一噪声轴，不是本项目已做的外部基准。
- 本次核对范围：本次核对CVF官方作者/标题/卷页与摘要及PDF首段，DOI由书目条目交叉核验；未逐项复现UrbanCars或ImageNet-W。
- 项目依据：[08_original_source_snapshots/history_f/PLANTSEG_2X2_MECHANISM_PLAN_V2.md](../08_original_source_snapshots/history_f/PLANTSEG_2X2_MECHANISM_PLAN_V2.md)

## 近邻与新颖性审查

<a id="N-MULTIFIDELITY-2023"></a>
### N-MULTIFIDELITY-2023 · Multi-Fidelity Covariance Estimation in the Log-Euclidean Geometry

Aimee Maurais; Terrence Alsup; Benjamin Peherstorfer; Youssef Marzouk. **2023**. Proceedings of the 40th International Conference on Machine Learning, PMLR 202, 24214–24235.

- 正式出处：[原始页面](https://proceedings.mlr.press/v202/maurais23a.html)；DOI本次未核定或原条目未提供，不编造。
- 文件：[本地PDF](pdfs/N-MULTIFIDELITY-2023.pdf)；SHA-256 `486276dde31859cd7b6a4104fea38cfc86680c16836ce69e39574d2b29160110`。
- 项目用途：多来源降协方差方差并保证SPD已经有直接先例；其multi-fidelity来源不等于同图全局与局部token。
- 本次核对范围：本次只核实primary元数据和摘要，不新声称通读；以下historical_reading_scope逐字依据旧审查层级。
- 原有阅读记录：已读摘要、§3.3–3.5和§4相关正文；未逐项审完附录证明。
- 项目依据：[08_original_source_snapshots/history_f/paper/SPD_ESTIMATION_NOVELTY_BOUNDARIES_20261025.md](../08_original_source_snapshots/history_f/paper/SPD_ESTIMATION_NOVELTY_BOUNDARIES_20261025.md)

<a id="N-EMPBAYES-2024"></a>
### N-EMPBAYES-2024 · An Empirical Bayes Approach to Shrinkage Estimation on the Manifold of Symmetric Positive-Definite Matrices

Chun-Hao Yang; Hani Doss; Baba C. Vemuri. **2024**. Journal of the American Statistical Association, 119(545), 259–272.

- 正式出处：[原始页面](https://doi.org/10.1080/01621459.2022.2110877)；DOI：`10.1080/01621459.2022.2110877`。
- 文件：[本地PDF](pdfs/N-EMPBAYES-2024.pdf)；SHA-256 `e8fa81addfc45a6cd6f272dad29821f842f4cc280386a7e900c46235a3e37b89`。
- 项目用途：LE风险、经验Bayes和SPD层级先验已有先行研究；观察单位为SPD矩阵而非相关ReLU token先形成Gram。
- 本次核对范围：本次只核实primary元数据和摘要，不新声称通读；以下historical_reading_scope逐字依据旧审查层级。
- 原有阅读记录：查到预印本§2–3的定义、估计式与假设；发表版本元数据已核，未核对预印本与发表版全部差异。
- 版本说明：PDF为2020年arXiv v3作者预印本；正式期刊卷期为2024，DOI含2022。三者不合并成同一版本年份。
- 项目依据：[08_original_source_snapshots/history_f/paper/SPD_ESTIMATION_NOVELTY_BOUNDARIES_20261025.md](../08_original_source_snapshots/history_f/paper/SPD_ESTIMATION_NOVELTY_BOUNDARIES_20261025.md)

<a id="N-POSCE-2019"></a>
### N-POSCE-2019 · Population shrinkage of covariance (PoSCE) for better individual brain functional-connectivity estimation

Mehdi Rahim; Bertrand Thirion; Gaël Varoquaux. **2019**. Medical Image Analysis, 54, 138–148.

- 正式出处：[原始页面](https://doi.org/10.1016/j.media.2019.03.001)；DOI：`10.1016/j.media.2019.03.001`。
- 文件：**官方链接级**：本次未取得可核定的公开全文，不冒充本地已有PDF。
- 项目用途：非各向同性群体先验与Riemannian切空间已有方法；人口层先验不能无检验地等同于同图上下文先验。
- 本次核对范围：本次只核实primary元数据和摘要，不新声称通读；以下historical_reading_scope逐字依据旧审查层级。
- 原有阅读记录：读取出版方摘要、highlights、方法section snippets，并由作者出版目录核对HAL全文链接；HAL访问受限，未通读全文。
- 项目依据：[08_original_source_snapshots/history_f/paper/SPD_ESTIMATION_NOVELTY_BOUNDARIES_20261025.md](../08_original_source_snapshots/history_f/paper/SPD_ESTIMATION_NOVELTY_BOUNDARIES_20261025.md)

<a id="N-DYINGRELU-2020"></a>
### N-DYINGRELU-2020 · Dying ReLU and Initialization: Theory and Numerical Examples

Lu Lu; Yeonjong Shin; Yanhui Su; George Em Karniadakis. **2020**. Communications in Computational Physics, 28(5), 1671–1706.

- 正式出处：[原始页面](https://www.global-sci.com/cicp/article/view/6894)；DOI：`10.4208/cicp.OA-2020-0165`。
- 文件：[本地PDF](pdfs/N-DYINGRELU-2020.pdf)；SHA-256 `9d2276e42f1cc72bc6602c278530670267e9cc3c10ef32e9be24d01b169d28f0`。
- 项目用途：域上神经元死亡有成熟理论；本项目的局部窗未采到激活而全图仍响应不能等同为神经元死亡。
- 本次核对范围：本次只核实primary元数据和摘要，不新声称通读；以下historical_reading_scope逐字依据旧审查层级。
- 原有阅读记录：阅读摘要、§3定义/主要定理及结论；未重证全部附录。
- 版本说明：2020年v3作者预印本；与2020正式期刊版本区分保存。
- 项目依据：[08_original_source_snapshots/history_f/paper/SPD_ESTIMATION_NOVELTY_BOUNDARIES_20261025.md](../08_original_source_snapshots/history_f/paper/SPD_ESTIMATION_NOVELTY_BOUNDARIES_20261025.md)

<a id="N-CORRELATED-2022"></a>
### N-CORRELATED-2022 · Cleaning large-dimensional covariance matrices for correlated samples

Zdzislaw Burda; Andrzej Jarosz. **2022**. Physical Review E, 105, 034136.

- 正式出处：[原始页面](https://doi.org/10.1103/PhysRevE.105.034136)；DOI：`10.1103/PhysRevE.105.034136`。
- 文件：[本地PDF](pdfs/N-CORRELATED-2022.pdf)；SHA-256 `68242be903be62cad2004b34ef78b0e656b7341027d376bfacfd3ea36743c09a`。
- 项目用途：相关样本的RMT/谱收缩已有直接近邻；共享A的可分离假设、Frobenius目标及视觉token失配须分开检验。
- 本次核对范围：本次核对作者arXiv的身份/摘要和相关出版DOI，没有重新逐节阅读。
- 原有阅读记录：旧审查明确：阅读原论文全文的建模、推导、实验与结论，以及作者仓库README和相关源码；只读、不安装、不执行。未复现实现或审计全部数值边界。
- 项目依据：[08_original_source_snapshots/history_f/paper/CORRELATED_SPECTRAL_RELATED_WORK_20261025.md](../08_original_source_snapshots/history_f/paper/CORRELATED_SPECTRAL_RELATED_WORK_20261025.md)

## 数据出处

<a id="D-PLANTSEG-2026"></a>
### D-PLANTSEG-2026 · A Large-Scale In-the-wild Dataset for Plant Disease Segmentation

Tianqi Wei; Zhi Chen; Xin Yu; Scott Chapman; Paul Melloy; Zi Huang. **2026**. Scientific Data, 13, 205.

- 正式出处：[原始页面](https://www.nature.com/articles/s41597-025-06513-4)；DOI：`10.1038/s41597-025-06513-4`。
- 文件：[本地PDF](pdfs/D-PLANTSEG-2026.pdf)；SHA-256 `27d5d67a62405a38e054b232e830905c48b2513f41f24ea3071f4d54c041bdfa`。
- 项目用途：当前数据来源论文。只用作数据出处引用，不按出版页面更新本包冻结训练池或划分。
- 本次核对范围：本轮核对Nature正式条目、作者与公开数据描述；没有重新处理或替换实际研究数据。
- 版本说明：本地PDF为2024年arXiv作者预印本，不是2026年Scientific Data正式版的逐字节副本。预印本标题带PlantSeg:前缀，正式版省去此前缀；作者及作品身份一致，不声称全文逐字一致。本次文献整理未改变数据版本或原研究冻结划分。
- 项目依据：[README.md](../README.md)；[01_protocols_and_data/](../01_protocols_and_data/)

## 阅读与引用边界

GCP的优化分析已有CVPR2020/TPAMI2023直接先例。本研究不能声称此前只报告精度、首次研究协方差池化优化，当前切口限定到本管线的映射、有限拟合和读出验收。

QEGF、Hybrid Geometric-Entropy Gating、GM-GReFEL等历史讨论名称未核实唯一可靠原始身份，不进入正式BibTeX；详见机器清单unadmitted_names。

原数学附录、历史论文审查与实验记录只读保留。本目录是新增文献整理，不修改科学协议，不补写事前阅读或预注册时间。

## 本轮理论升级的直接近邻

<a id="alain2017probes"></a>
### alain2017probes · Understanding intermediate layers using linear classifier probes

Guillaume Alain; Yoshua Bengio. **2017**. International Conference on Learning Representations (ICLR). [arXiv](https://arxiv.org/abs/1610.01644)。

- 项目用途：线性 probe 作为冻结表示诊断工具的早期直接先例；本文不把 probe 准确率扩展成所有下游能力的证明。
- 当前理论差异：[RIGOROUS_AUDIT_THEORY_V2.md](../09_scientific_supplement_v1/math/RIGOROUS_AUDIT_THEORY_V2.md)进一步限定读出族、TRAIN、正则化和 solver gap。

<a id="hewittliang2019control"></a>
### hewittliang2019control · Designing and Interpreting Probes with Control Tasks

John Hewitt; Percy Liang. **2019**. EMNLP-IJCNLP, 2733–2743. [ACL](https://aclanthology.org/D19-1275/)。

- 项目用途：控制任务和 probe 选择性，说明 probe 可能自己记忆标签；本文把该边界扩展到固定 SPD 读出与可复核优化证书。

<a id="hewitt2021conditional"></a>
### hewitt2021conditional · Conditional probing: measuring usable information beyond a baseline

John Hewitt; Kawin Ethayarajh; Percy Liang; Christopher Manning. **2021**. EMNLP, 1626–1639. [ACL](https://aclanthology.org/2021.emnlp-main.122/)。

- 项目用途：条件 probing 和 baseline 可用信息；本文不把指定读出族的 TRAIN 最优风险等同于无条件表示质量。

<a id="dunner2016certificates"></a>
### dunner2016certificates · Primal-Dual Rates and Certificates

Celestine Dünner; Simone Forte; Martin Takáč; Martin Jaggi. **2016**. ICML, PMLR 48, 783–792. [PMLR](https://proceedings.mlr.press/v48/dunner16.html)。

- 项目用途：primal/dual gap 作为近似最优性证书的标准来源；本文的增量是把该类证书转成两个固定表示的风险差符号判定。

<a id="agarwala2020temperature"></a>
### agarwala2020temperature · Temperature Check: Theory and Practice for Training Models with Softmax-Cross-Entropy Losses

Atish Agarwala; Jeffrey Pennington; Yann Dauphin; Sam Schoenholz. **2020**. [arXiv](https://arxiv.org/abs/2010.07344)。

- 项目用途：逆温度影响 softmax 训练动力学的直接先例；本文不声称温度动力学本身首次被研究，只给出平方距离 softmax 的局部秩条件。

<a id="chou2026twospeeds"></a>
### chou2026twospeeds · Two Speeds of Learning: A Representation-Readout Decomposition of Grokking and Double Descent

Chi-Ning Chou; Oscar Uzdelewicz; Neng-Chun Chiu; Yao-Yuan Yang; SueYeon Chung. **2026**. arXiv:2605.27078. [arXiv](https://arxiv.org/abs/2605.27078)。

- 项目用途：直接近邻，已将编码器表示学习与分类器读出校准分解为两个学习过程，并用于解释 grokking 与 double descent。
- 当前理论差异：本文不把表示—读出分解本身作为原创；我们的增量是固定表示、指定读出和 TRAIN 风险上的确定性证书，以及对象不匹配时的拒绝分支。
- 核对范围：核对 arXiv 元数据和摘要，不声称完成全文复现。

<a id="barinpacela2026coding"></a>
### barinpacela2026coding · Stop Probing, Start Coding: Why Linear Probes and Sparse Autoencoders Fail at Compositional Generalisation

Vitória Barin-Pacela; Shruti Joshi; Isabela Camacho; Simon Lacoste-Julien; David Klindt. **2026**. Proceedings of UAI 2026, PMLR 337. [PMLR](https://proceedings.mlr.press/v337/barin-pacela26a.html)。

- 项目用途：区分线性表示与线性可访问性，并讨论非线性推断和摊销缺口；这直接限制了“高 probe 分数等于可组合泛化”的说法。
- 当前理论差异：本文不重新定义 accessibility gap；只对固定 SPD 表示的指定凸读出给出 solver gap、正则化偏差和范数条件下的审计证书。
- 核对范围：核对 PMLR/arXiv 元数据和摘要，不声称完成全文复现。

<a id="garg2026linearfeatures"></a>
### garg2026linearfeatures · How Many Features Can a Language Model Store Under the Linear Representation Hypothesis?

Nikhil Garg; Jon Kleinberg; Kenny Peng. **2026**. Proceedings of the 39th Conference on Learning Theory, PMLR 336, 5358–5376. [PMLR](https://proceedings.mlr.press/v336/garg26a.html)。

- 项目用途：在线性表示假设下对线性特征容量给出定量上下界；它是“表示与可访问性已有严格理论”的边界证据。
- 当前理论差异：本文不提出容量或组合泛化定理，而是针对给定数据集、读出族和预算认证两个固定表示的 TRAIN 风险差。
- 核对范围：核对 PMLR 正式条目和摘要，不声称完成全文复现。

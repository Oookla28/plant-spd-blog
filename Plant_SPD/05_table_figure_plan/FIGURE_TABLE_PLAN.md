# 当前论文图表计划

本版按证据对账后的叙事整理。[当前图件入口](../04_figures/CURRENT_PAPER_FIGURES.md)给出可直接引用的图与英文图注。先前计划已备份；科学快照、旧图及结果不改。

主线：**协方差几何表示的比较，必须先审计读出能力、优化完成度和评价指标；否则，有限训练配方的失败可能被误判为表示本身的失败。**

状态：**READY**＝实物存在，可排稿；**LAYOUT_ONLY**＝panel齐备，只需版心合版；**DEFERRED**＝缺合格事前判据或登记链，不作确证；**NOT_RUN**＝需新实验；**UNAVAILABLE**＝历史未记录，不能补造。图表整理不授权新实验。

## 1. 正文四组图

| 编号 / 图名 | 实物及状态 | 图注必须保留 |
|---|---|---|
| Figure 1. Low fit versus recoverable readout | READY：`04_figures/current_v1/F1_fit_separability_and_recipe_recovery.png/.pdf` | REC-F2-RAW/LOG、REC-A-SERIES。本轮两批固定特征认证100%，与成熟E08分代。seed3407 Log默认36.05%，不换成跨seed34.12%。A4是新联合路径；认证目标不同于AdamW。 |
| Figure 2. Distinct diagnostics, distinct limits | panels READY；合版LAYOUT_ONLY：`current_v1/F2_historical_diagnostics/` | REC-TS/FITPROGRESS/CLIP。温标、epoch进度、CE匹配、裁剪与采样真实更新分开。89.3%是NLL差距收缩，不是因果贡献；CE匹配是事后分析；采样更新不代表全程全部参数。 |
| Figure 3. Conditional source × readout interaction | panels READY；合版LAYOUT_ONLY：`current_v1/F3_five_source_seed_readout/` | REC-MATRIX-5S。20次新拟合、五来源训练seed，同反复开发1046HELD。保留3410/3411的F1方向例外，F1/NLL并列；source-seed SD不是独立数据集CI。 |
| Figure 4. Prespecified recovery interventions | panels READY；合版LAYOUT_ONLY：`current_v1/F4_prespecified_interventions/` | REC-A-SERIES/B-NONSUFFICIENT。端点、前瞻W/b/CE、实际行进与A4分栏。A2另列三seed。只把WD删除格称matched控制；不拟合跨参数化剂量曲线；MAF不计经验miss。 |

Figure 2–4建议正文各选2–3个panel，其他放附录。合版仅改版心、字母与字号，无需新训练、推理、重采样或温标拟合。

## 2. 协议图与正文表

| 项目 | 当前入口 | 写作要求 |
|---|---|---|
| Protocol diagram：四项检查 | READY：`04_figures/current_v1/S1_four_gate_audit_protocol.png/.pdf` | 数学准入→函数可达→数值收敛→充分TRAIN拟合；放正文，MAF/EPM分列。旧三查图保留历史。 |
| Table 1：设计与证据代次 | `12_evidence_reconciliation_v1/EVIDENCE_REGISTER_V1.json`及各protocol | task、FIT/HELD、source seed、头族、scaler、lambda、停止标准、终点、重复HELD情况；不能只列相同名义超参。 |
| Table 2：可达控制及认证读出 | `09_scientific_supplement_v1/native_pc10/`、`analysis/expanded_probe_final_v1/SUMMARY.json`；`11_f1_f4_A_forensics_v1/f2_convex_*/RESULT.json` | REC-NATIVE/RISK/MATRIX-5S/F2分代；函数包含、完整梯度/gap、TRAIN100%三栏，证书不是统计泛化保证。 |
| Table 3：五seed20格 | `09_scientific_supplement_v1/analysis/expanded_probe_final_v1/SUMMARY.json#/per_cell_distributions`与`/per_seed_effects` | 四组合F1均值±样本SD、NLL、逐seed简单效应；旧八格不混入。 |
| Table 4：A干预及实际终点 | READY转录：`03_results/current_v1/T_current_A_endpoints.csv/.md`；`11_f1_f4_A_forensics_v1/F1_F4_FORENSICS.json` | 默认、WD0、LR×10、60epoch、温度、A4、A2重复；原预测与实测分列；逐格标共变。 |
| Table 5：主张准入与边界 | `11_f1_f4_A_forensics_v1/DECISION_TREE_ADDENDUM_V1.md`及`12_evidence_reconciliation_v1/AUDIT_PROTOCOL_FOUR_GATES_V1.md` | q99×B和one-hot分类必要范数为MAF退役，不计EPM。有效逐坐标界仍成立，但唯一硬天花板机制未建立。 |

以上表均有已有元数据，可直接排稿；Table 1/2/5尚需按投稿模板压缩版心，不需要新实验。每数字给证据ID、文件键与SHA，沿用统一登记，不另外手填一套结果。

## 3. 两个必须显现的反例

**同B不同终点：** REC-B-NONSUFFICIENT。A0与A3的头LR总和均为 **1.3755**，F1差 **52.49675681pp**。正文一句话、附录给公式和指针；这否定B作为跨参数化充分剂量变量，不否定所有预算因素，不画异质干预统一对数拟合。

**seed与指标例外：** 不只展示平均热图。3410的Log来源F1偏Raw、3411的Raw来源F1偏Log；NLL偏好另列。因此只写本设置的条件性交互，不写原配必胜、刚性耦合或联合训练必需。

## 4. 附录分组

| 组别 | 已有资产 | 边界 |
|---|---|---|
| 读出工具演进 | E06/E07/E08；`09_scientific_supplement_v1/derived_figures_v2/D01*`及`D06*` | REC-UNDERFIT/PROBE-2S。旧八格为5接受端点+3授权恢复，另一代lambda，不混成28格。 |
| 数学和F取证 | `11_f1_f4_A_forensics_v1/math/`、`derived_actual_v1/`、`figures_F_v1/`；当前`supplement_current_forensics/` | 谱距离、Fréchet、固定CE需求、终端u等为标准工具/诊断；不把终端分位数当全程界。 |
| 前瞻轨迹与偏差记录 | 各A EPOCHS/step、启动拦截、注册与closeout | 只标本轮前瞻记录，原完整历史不可用；A3 τ(t)确证解释延期。 |
| 历史替代分支 | Sqrt逐seed、RMT/ANS、局部零通道、冲突审计、十组筛查 | 保留负结果；不塞进当前主贡献，不写Sqrt普适赢家。 |

## 5. 待办与不能补画的内容

| 项目 | 状态 | 当前处置 |
|---|---|---|
| Figure 2–4最终合版 | LAYOUT_ONLY | panel齐全，投稿模板确定后排版。 |
| A3 τ(t)事前定量预测 | DEFERRED | 字段存在，未找到对应判据；禁止先读轨迹再补先验预测。 |
| “曲线时代三预测/修订#3”历史链 | DEFERRED / 正文撤下 | 未定位原链，不补造，不计EPM；现登记被取代。 |
| 原完整W/b和encoder RMS历史 | UNAVAILABLE | 只能展示本轮前瞻或同图端点；不可伪恢复。 |
| 唯一机制：逐坐标预算/方向曲率/逐步动力学 | 未闭合 | 新因果判别须另立协议，本整理不启动。 |
| 本轮独立HELD/外来源泛化 | NOT_RUN | 新F/A仅FIT/TRAIN；旧反复开发HELD不称新盲测。 |
| epsilon剂量、有效背景反事实、专家病理复核 | NOT_RUN / HELD | 无结果可画，保留局限或未来工作。 |

## 6. 写稿与复核顺序

先写Audit Protocol及等头族/A干预，再写认证交叉读出，最后写引言和摘要。每图标证据ID、代次、source seed、分母、单位、重复HELD及描述性状态。来源清单见 `04_figures/current_v1/PROVENANCE_MANIFEST.json`；统一证据见 `12_evidence_reconciliation_v1/`。数学不替代独立确认与泛化证据。

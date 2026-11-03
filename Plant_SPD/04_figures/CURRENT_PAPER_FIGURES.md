# 当前论文图件入口

主线：**协方差几何表示的比较，必须先审计读出能力、优化完成度和评价指标；否则，有限训练配方的失败可能被误判为表示本身的失败。**

本页取代旧 `FIGURE_CATALOG.md` 的主文优先级；旧图和旧说明作为历史保留。当前资产在 [current_v1](current_v1/)。复制图字节不变；新增开篇图和四查流程图只读已有JSON标量，不训练、不读标签或预测数组。来源、JSON键及SHA见 [PROVENANCE_MANIFEST.json](current_v1/PROVENANCE_MANIFEST.json)。

## 四组正文图

| 论文编号 | 当前实物 | 证据ID / 图注意图 |
|---|---|---|
| Figure 1：低拟合与可读出信息分离 | [PNG](current_v1/F1_fit_separability_and_recipe_recovery.png) / [PDF](current_v1/F1_fit_separability_and_recipe_recovery.pdf) | REC-F2-RAW / REC-F2-LOG / REC-A-SERIES。本轮两批特征的默认、认证100%和预注册恢复分栏；认证目标不同于AdamW；A4为新联合路径。 |
| Figure 2：诊断量的解释边界 | [F2_historical_diagnostics](current_v1/F2_historical_diagnostics/)：温标、epoch动态、CE匹配、裁剪系数、采样更新 | REC-TS / REC-FITPROGRESS / REC-CLIP。不同指标不连成已识别因果链；CE匹配为事后分析，裁剪率不等于实际更新。 |
| Figure 3：认证读出的条件性交互 | [F3_five_source_seed_readout](current_v1/F3_five_source_seed_readout/)：五seed20格F1/NLL、simple effects/DID、拟合/gap | REC-MATRIX-5S。source seed非独立图像队列；保留3410/3411的F1例外和F1/NLL差异，不称原配必胜。 |
| Figure 4：预注册干预与机制边界 | [F4_prespecified_interventions](current_v1/F4_prespecified_interventions/)：全部端点、前瞻W/b/CE、实际行进与A4 | REC-A-SERIES / REC-B-NONSUFFICIENT。明确各臂共变；不拟合统一剂量曲线；两项判据MAF退役，不计经验miss。 |

Figure 1使用seed3407，Log默认端点为 **36.05%**；全文 **34.12%** 是跨seed汇总，不能用于此图同seed增幅。当前F2是本轮两批新认证，成熟E08为历史证书参考，必须分代。Raw A2与Log A4的来源/训练路径分开，不能当同一固定特征竞赛。

## 协议及附录

- 正文协议图：[四项审计PNG](current_v1/S1_four_gate_audit_protocol.png) / [PDF](current_v1/S1_four_gate_audit_protocol.pdf)：**数学准入→函数可达→求解收敛→充分TRAIN拟合**。MAF与EPM分列，旧三查图只作历史。
- [当前F取证附录](current_v1/supplement_current_forensics/)：固定CE需求区间、同4184FIT端点RMS。不把可行范数当分类必要范数、不把端点差写成历史增益轨迹。
- 旧8格位于 `09_scientific_supplement_v1/derived_figures_v2/D06_anchored_readout_f1_and_nll.*`，仅附录演进；不与20格合并为28格。
- Sqrt、RMT/ANS、局部零通道、冲突审计及早期十组保留原目录，按需补充，不承担本文中心贡献。

## 可直接改入稿件的图注

**Figure 1.** Default low TRAIN fit does not establish lost fixed-feature separability. Both current F2 fixed-feature references achieve complete TRAIN classification under an independently certified explicit-L2 affine objective. Prespecified finite-recipe interventions substantially recover fitting. Source encoders and evidence generations are separated; A4 follows a fresh joint feature path. All displayed outcomes are original/unflipped FIT diagnostics, not HELD generalization evidence.

**Figure 2.** Distinct diagnostics constrain distinct explanations. Temperature scaling, TRAIN-progress comparisons and clipping/update summaries are historical observations under their original protocols. TRAIN-CE matching is post hoc, clipping frequency is not an effective-update measurement, and the Adam-CV toy expression is not a fitted causal model.

**Figure 3.** Readout preference is conditional on encoder source and evaluation metric. Twenty new solves use five source-training seeds and the same already-viewed 1,046-image HELD cohort. Each cell passes the specified numerical objective-gap criterion and achieves complete TRAIN classification. Seed exceptions and differing F1/NLL preferences are retained.

**Figure 4.** Prespecified interventions recover finite TRAIN fitting without identifying a unique mechanism. WD deletion does not recover fitting in the matched control. A2prime changes visits, updates and cosine horizon; A3 changes parameterization; A4 changes head LR and warmup. Trajectories were prospectively recorded in this generation. A0 and A3 share B but differ in F1, so B is not a sufficient cross-parameterization dose variable.

## 重绘到新目录

```powershell
& 'C:\Users\lenovo\Documents\PlantSPD_plot_env_v1_20261026\Scripts\python.exe' -B `
  'F:\Plant_SPD\04_figures\current_v1\build_current_assets.py' `
  --output-root 'F:\Plant_SPD_paper_export_new'
```

显式输出目录须新建或为空。只读包内既有元数据，输出新图、复制panel与A表；不改源工件。本机绝对路径保留；该命令不启动科学实验。新两图已视觉核对，见 `current_v1/VISUAL_QA.json`。Figure 2–4的panel已完成，期刊模板确定后的合版/字号调整属于排版工作，见[图表计划](../05_table_figure_plan/FIGURE_TABLE_PLAN.md)。

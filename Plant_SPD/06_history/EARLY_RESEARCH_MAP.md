# 早期研究地图：保留历史，主线分层

本页整理的是 2026-10-26 时本地可核验的代码和既有报告，没有启动训练、推理、温标拟合、统计重采样或新的标签处理。历史文件保留原字节和原路径引用；其中的 AGENTS、控制器、窗口和“下一步”文字是历史材料，不能作为本次执行授权。实际复制名单见 `HISTORY_COPY_MANIFEST.json`。

## 一、当前论文主线与历史探索的关系

当前主文围绕“协方差映射的比较需要同时审计优化、概率尺度与读出可达性”。下列早期工作构成研究演进和负结果附录，不能拼接为同一任务上的连续涨点曲线。

| 分支 | 核心问题与实际状态 | 关键实现（相对历史快照根） | 现存证据 | 论文位置 |
|---|---|---|---|---|
| CRCG / 全局—局部融合 | 冻结 C0/S2 下的十个控制已完成；等权最强；完整 CRCG 没有运行 | `crcg_full_matrix_screen_5060.py`、`crcg_held_methods_screen_5060.py`、`crcg_reliability_head_full_5060.py` | `paper/CRCG_FULL_MATRIX_SCREEN_5060_V1.md`，`experiments/crcg_full_matrix_screen_5060_v1/metrics.json` | 附录：为何不把更复杂融合直接当创新 |
| CRCG-lite smoke | 16 TRAIN、8 DEV、16 更新的实现烟测；不是性能证据 | `crcg_lite_end2end_pilot_5060.py` | 对应 `paper/CRCG_LITE_END2END_PILOT_5060_V1.md` 和实验 metrics | 实现与研究历史 |
| PlantSeg 最早十组 | 单 seed、5 epoch；旧 G7 仅 log-spectrum，旧 G9 未实际反事实训练 | `01_datasets/plantseg/train_plantseg_10groups.py` | `01_datasets/plantseg/PLANTSEG_GROUP_DECISION_V1.md`，`runs/ten_groups_ep5_seed3407/RESULT_NOTE.md` | 退役实现与修正原因 |
| 2×2 Euclidean/SPD × 普通/扰动 | screen 已完成，交互区间跨 0；旧扰动改变整幅 RGB，不能叫病斑保持的背景反事实 | `plantseg_2x2_mechanism.py`、`plantseg_2x2_mechanism_stable_v1.py`、`analyze_2x2_followup_v1.py` | `runs/plantseg_2x2_seed3407/INTERVENTION_AUDIT_V1.md`、`FOLLOWUP_ANALYSIS_V1.md` | 任务定义和反事实有效性的负对照 |
| 反事实 v2 合同 | manifest 已生成，准入未通过/未训练；不能计为修正后的性能结果 | `plantseg_cf_contract_v2.py`、`build_cf_manifest_v2.py`、`audit_cf_contract_v2.py` | `INTERVENTION_V2_DECISION.md`、`interventions_v2_audit.json` | 待执行历史提案，不占主文结果 |
| 早期 E0/S0 三 seed | 三个 seed 已完成，同 800 DEV；旧训练明显欠拟合 | `formal_e0s0_3seed_local.py`、`analyze_formal_e0s0_local.py`、`plantseg_2x2_mechanism_stable_v1.py` | `runs/formal_e0s0_3seed_v1_local/formal_analysis.json` | 早期现象；不替代最新 20 端点 |
| DES-AS/Shapley 筛查 | 两个完整 seed 的五模型池筛查为弱正，未晋级；GT oracle 是不可部署上界 | `audit_desas_shapley_v1.py`（与 `scripts_audit_desas_shapley_v1.py` 内容重复） | `experiments/desas_shapley_audit_v1/DESAS_SHAPLEY_AUDIT_V1.md` 和 `metrics.json` | 早期融合附录 |
| 朴素 MP/RMT | spectral audit 和失败训练记录存在；非有限 loss 使正式训练没有有效性能终点 | `plantseg_2x2_mechanism_rmt_v1.py`、`plantseg_2x2_mechanism_rmt_stable_v2.py`、`formal_s0rmt_3seed*_local.py`、`rmt_spectral_audit_v1.py` | `runs/formal_s0rmt_3seed_v1_retry/RMT_DECISION_V1.md` | 失败模式，不能填入有效主对比表 |
| 成熟收缩 ANS/LW/OAS | 合成估计实验已完成；iid 与强相关条件的排序不同，估计误差改善不是分类收益 | `spd_covariance_estimators_v2.py`、`spd_covariance_estimators_torch_v1.py`、`run_spd_estimation_stage_a_v1.py`、`spd_gpu_precision_extension_v1.py` | `experiments/spd_estimation_stage_a_v1/REPORT.md`，`spd_estimation_followup_v1_20261025/REPORT.md` | 附录：估计条件与适用性 |
| 真实特征准入 / ReLU / 局部支持 | 550 TRAIN × 3 冻结模型诊断已完成；真实正式分类阶段 HOLD；零通道恢复只是采样支持诊断 | `spd_stage_b_features_v1.py`、`spd_stage_b_diagnostics_v1.py`、`spd_relu_rank_mechanism_v1.py`、`audit_spd_support_visibility_v1.py` | followup `diagnostics/decision.json`、`synthesis.json`、`relu_mechanism/science/results.json` | 附录：有效性门槛与压力测试边界 |
| 上下文先验 | 设计审计完成；native 548/550 图零通道比例为 0，中组为空；七方法正式性能比较未执行 | `audit_spd_context_design_v1.py`、`audit_spd_rank_localization_v1.py` | `experiments/spd_context_design_v1_20261025/REPORT.md`、`SPD_CONTEXT_COMPARISON_PLAN_V1.md` | 未运行提案，不讲已解决估计问题 |
| 冲突 / DASFAA 证据库 | 2400 行来自 800 图 × 3 seed；冲突未通过熵/margin 控制门，联合复核策略更差，停止选择器和索引扩张 | `conflict_audit_v1.py`、`dassfaa_evidence_{store,queries,audit,benchmark}_v1.py`、`analyze_conflict_complementarity_v1.py` | `DASFAA_PHASE1_DECISION_V1.md`，`experiments/dasfaa_complementarity_v1/REPORT.md` | 负结果附录，不包装为数据系统主贡献 |
| 训练健康 / 共同特征机制 | 小集合可拟合、旧 fulltrain 不足；共同特征固定算术原型比较已完成，不能代表所有公平调优配置 | `experiments/training_health_v1_20261025/source/*.py`、`fulltrain_fit_audit_v1_20261025/source/*.py`、`common_feature_mechanism_v1_20261025/source/*.py` | `common_feature_mechanism_v1_20261025/RESULT_SUMMARY.txt` 与 `STUDY_SUMMARY.json` | 通向最新公平训练与读出审计的桥梁 |
| ISIC2016 跨领域尝试 | 首/二轮历史输出因重复图跨split等问题作废；源码修复后未形成可确认的有效重训对照 | `01_datasets/isic2016_task3b/{make_splits_task3b,preprocess_task3b,train_first_round,evaluate_first_round,train_second_round}.py` | `CODE_AUDIT_20261024.md`、`runs/INVALID_RESULTS_20261024.md` | 数据/代码审查历史，绝不当跨领域有效证据 |
| ISIC2018 准备 | 本地审计写明完整图像/掩码配对0，未训练 | `01_datasets/isic2018/preprocess_isic2018.py` | `ISIC2018_DATASET_AUDIT.md` 与 preprocess/intersection report | 准备未完成，不计实验终点 |

## 二、代码依赖，避免“只拷一个脚本”

1. CRCG 直接依赖 `02_source/historical_experiments/early_multitask/src/train_multiscale.py` 的 `JointNet`，以及 `02_source/historical_experiments/self_reference_and_fusion/src/segnext_s2_model.py`；后者继续依赖 `segnext_s0_model.py`。这两组本地源码已纳入清单。
2. 原 `train_multiscale.py` 还需要第三方 `timm`、PyTorch、NumPy、Pillow 与旧初始化权重；第三方安装环境不作为源代码复制。
3. DES-AS 代码动态导入 `leaf_research_top/scripts/analyze_sat_benchmark_v1.py`。本地 server 项目 `scripts/src/tests` 已纳入历史快照，保留协议/模型/计数分析的实现上下文。
4. ANS stage A 的 Python 实现、torch 移植、测试、合成 population 定义和 Ledoit–Wolf 原始参考元数据一并保留，避免把实现脱离公式来源。
5. 最新成熟 backbone 的本地实现位于 `experiments/common_backbone_v1_20261025/resnet18_torch_only_v1.py`。这是后续共同特征及配对训练的实质性依赖，而不是环境内不可见包。
6. 原源码含绝对 F/D/服务器路径，存档不改字节。它们可以审阅算法与结果产生流程；重新执行需要新的输出目录、合法资产、正确环境与明确实验授权。不要直接运行历史 controller/launch 文件。

## 三、server 项目归档的边界

`leaf_research_top` 的本地源码、测试、配置、报告、CPU/GPU/analysis registry 与主要 audit 已作为历史存档列入。该目录中的二值分割 IoU、普通 RGB 外部数据结果和当前 69 类分类 Macro-F1 不可比较。当前打包没有连接服务器，SAT 本地报告仍是历史快照，不能宣称完成最新远程全矩阵。

## 四、复制与排除规则

清单逐项绑定 `source → destination`、大小和 SHA-256。历史目录层级保留于 `08_original_source_snapshots/history_f/` 下。

纳入：相关自研 `.py`、测试、协议、既有 summary/metrics/decision/audit、必要文献出处和原报告。失败、HOLD、未执行提案均保留，但不算成功实验。

排除：虚拟环境、第三方 vendor、原始图像、模型权重、缓存张量、`.npz/.npy` 科学数组、大资产、原 dataset manifest/标注池以及可能属于 cal/final/test 的逐图材料。排除记录在 manifest 中，不能把代码快照称为完整数据再发行包。文件复制本身不重新处理数据。

## 五、写论文时的三条不可混用规则

- 787 DEV 的冻结融合、800 DEV 的旧分类、904 DEV 的 SAT 二值分割、最新 1046 held 的 69 类分类分别成表。
- 合成协方差误差、真实特征适用性、分类收益是三个不同终点；前一项完成不代表后一项被验证。
- 文件名含“full”“formal”“complete”只说明历史命名或特定步骤状态，最终论断以对应 protocol、decision 与 receipt 为准。

## 六、跨领域尝试的额外纠正

ISIC2016 的审查记录指出：最初 sample-level split 允许同 SHA-256 图跨 train/validation，类权重曾用全部900标签，best state 使用浅拷贝，G6 branch logits 因shuffle错位，G2恢复best后未重新统计。历史结果被明确作废。后续源码改为hash组内划分、train-only类权重、clone checkpoint及对齐推理，但修复代码存在不等于完成有效重训；旧 second-round 还只是 log-eigenvalue 原型，缺少完整矩阵SPD、匹配欧氏、多seed和OOF mask控制。存档中保留这些报告与源码，是为了避免把有名无实的“多领域验证”写进论文。

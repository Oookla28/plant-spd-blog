# 证据块对账与论文准入登记

本次是**事后证据登记**，不是补做预注册。两个原封存包只读，原台账及结果不回写。每项数值、原始键、协议、run ID、代次及SHA见机器台账及三份子报告。

| 待对账块 | 结论 | 新证据ID | 处置 |
|---|---|---|---|
|Five-source-seed matrix|EXISTS|REC-MATRIX-5S|REGISTER_AND_ENABLE_CONDITIONAL_CONTRIBUTION2_AND_FIGURE3|
|Early eight cells|EXISTS_OLD_LEDGER_C07_C08_C09|REC-PROBE-2S|REGISTER_LINEAGE_APPENDIX_ONLY|
|Native controls / risk budget / underfit readout|EXISTS|REC-NATIVE, REC-RISK, REC-UNDERFIT|ENABLE_PROTOCOL_WITH_GENERATION_LABELS|
|Temperature / fit progress / clip versus update|EXISTS_OLD_LEDGER_C02_C04_C03|REC-TS, REC-FITPROGRESS, REC-CLIP|ENABLE_HISTORICAL_OBSERVATIONS_WITH_SCOPE|
|A interventions and current F2 references|EXISTS_CURRENT_SEALED_GENERATION|REC-A-SERIES, REC-F2-RAW, REC-F2-LOG, REC-B-NONSUFFICIENT|ENABLE_TRAIN_ONLY_WITH_COCHANGES|

## 登记结果与叙事边界

五种子20格真实存在；它未进入旧C07的两种子行，现登记REC-MATRIX-5S后可启用贡献2/图3。五种子是来源编码器训练seed，使用相同反复开发的HELD，不是五个独立数据集。新20格统一新lambda并全部重新拟合；旧八格属于另一代lambda，不能混成28格平均。原配偏好有例外，F1与NLL必须并列。

早期八格实际由五个已接受完成端点加三个另行授权恢复端点组成。旧未完成命名空间仍在，不能写原批次无中断完成。native控制、早期欠拟合及温标/更新等原包已有C05/C06/C09及C02/C03/C04；本次补齐工件级ID，并不声称此前完全没有记录。风险预算单列REC-RISK。

本轮新F2两批与成熟E08历史证书分代；对应来源、scaler、lambda与目标不同，不能借用或移植证书。

## 本轮必要的数学与术语修订

四项协议检查：**主张/判据数学准入 → 函数可达性 → 求解收敛 → 充分训练拟合**。MAF与EPM分列。q99预算盖帽和one-hot分类必要范数不通过准入，退休为MAF，不计经验预测miss。其审查已见A运行前冻结文件；不是今天新造的经验降级分支。

**B非充分性反例 REC-B-NONSUFFICIENT：** A0和A3实际头学习率总和均为1.3755；FIT Macro-F1差为52.49675681pp，公式100×(A3−A0)。来源：`D:\PlantSPD_forensics_F1F4_A_v1_20261026\cached_a0_s3407\COMPLETED.json#/actual_LR_budget_B/head`、`D:\PlantSPD_forensics_F1F4_A_v1_20261026\cached_a3_s3407\COMPLETED.json#/actual_LR_budget_B/head`及两文件`/train/macro_f1_fixed`。这说明B单独不能决定跨参数化终点，不证明预算因素完全无关。

总称“预注册干预”，逐格标明单因素与共变。WD用“删除头部WD未恢复拟合，当前配方下直接WD主导解释被削弱”；删除“WD出局”。不拟合或宣称跨异质干预的对数剂量—反应曲线。

## 待解决与撤下内容

τ(t)字段实际有保存，但未找到与其对应的事前定量判据；该确证评分显式延期。不读取现成轨迹后补写先验预测，也不由τ变化单独判定A3机制。

“曲线时代三预测/修订#3”的原始编号链未定位。按当前指令从正文撤下并登记为被取代，不计EPM；不能补造历史#3或三次miss。详见`PENDING_AND_RETIRED_ITEMS_V1.json`。

## 证据子报告

- [矩阵与早期八格](subreports/MATRIX_EVIDENCE_V1.md)
- [native、风险预算和欠拟合](subreports/PROBE_CONTROLS_EVIDENCE_V1.md)
- [E系列指标及优化诊断](subreports/E_SERIES_EVIDENCE_V1.md)

不存在“所有内容均尚未登记”的情况，也不存在“无实物仍启用”的准入。本次填补的是统一台账与工件ID之间的追踪缺口。

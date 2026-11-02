# E 系列证据对账登记（事后登记，不是新的预注册）

三块证据均存在；旧封存账本已分别记录 C02、C03、C04。本登记增加 REC 编号、代次、来源键路径和字节核验，不改原账本。

| 新登记 ID | 旧账本 | 处置 | 核心范围 |
|---|---|---|---|
| REC-TS | C02 | 启用，范围限定 | 四个冻结模型，p0、两个训练种子、既有1046张HELD、五折分组交叉拟合、事后探索 |
| REC-FITPROGRESS | C04 | 启用，范围限定 | 旧20个端点，2划分×5配对，TRAIN CE完整epoch首次过阈值、事后条件比较 |
| REC-CLIP | C03 | 启用，范围限定 | E02的16格含1个carryover+15个新端点；裁剪系数全步，实际参数更新仅136个采样步 |

## REC-TS

Raw/Log 的两seed平均 NLL：校准前 2.365193545332/1.177290708237；两者均交叉拟合温标后 1.285223892687/1.158665890173。
差距 1.187902837095 → 0.126558002514，描述性缩小 89.346098%。公式为 1−新Raw–Log差距/旧Raw–Log差距。
这不是Raw自身NLL降低89.3%，不是因果贡献；F1不变。完整四条件图可以使用，不能只比较Raw温标后与Log未温标。
结果与所有数字键路径：`F:\Plant_SPD\02_experiments\E03_calibration\temperature_crossfit_v1\RESULT.json` 的 `#/rows`、`#/contrasts`；新 JSON `#/evidence_entries/0`。

## REC-FITPROGRESS

主事后阈值 TRAIN CE≤0.1：Raw完整epoch首次达标在7–8，Log在18–19；全部10配对保留。p0/p1条件HELD F1差均值分别+6.290540/+6.136033个百分点。
敏感性阈值0.05下Log没有一个端点达到；不能删除未达标格或外推。相同平均CE不匹配margins、路径、表示、温度或预算。
逐数字来源：`F:\Plant_SPD\02_experiments\E04_fit_and_clip_diagnostics\MATCHED_TRAIN_CE.json` 的 `#/threshold_results`；新 JSON `#/evidence_entries/1`。

## REC-CLIP

standard_global两seed合并裁剪触发：Raw60.667939%、Log96.106870%；系数每个端点2620步完整记录。
实际更新采样在step1–5和每20步，共136个；均值排除前5步后用131个。该L2覆盖当步组内全部参数，包含解耦WD，不能外推完整训练路径。
历史optimizer m/v未保存；HEAD_CLIP_WINDOWS只能称裁剪系数窗口均值和总体标准差，不得称梯度方差或Adam二阶矩图。
逐数字来源：`F:\Plant_SPD\02_experiments\E04_fit_and_clip_diagnostics\CLIP_COEFFICIENT_DIAGNOSTICS.json` 的 `#/summaries_two_seed_pooled`，`F:\Plant_SPD\02_experiments\E02_optimizer_controls\analysis\FINAL_ANALYSIS.json` 的 `#/rows/*/diagnostics`；新 JSON `#/evidence_entries/2`。

## 完整性与语义边界

本次选择的149项元数据、源码和既有图字节全部匹配封存PACKAGE_MANIFEST。只读访问现有聚合指标；未读HELD标签/预测数组、未开模型、未训练。
本次输出登记的是既有证据，不能反向赋予旧探索分析预注册地位。新F/A代次只用FIT，旧E代次已经多次查看HELD，两者在正文和图注必须分开。

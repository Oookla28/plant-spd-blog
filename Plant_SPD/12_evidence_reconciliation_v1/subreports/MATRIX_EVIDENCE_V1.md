# 来源×读出证据对账

**结论：五source-seed20格与早期2source-seed8格均真实存在，代次不同。新20格应登记为REC-MATRIX-5S；旧8格已见原包C07/C08/C09，当前登记交叉引用REC-PROBE-2S。本次是事后证据登记，不是补做预注册。**

核验状态：PASS。选定元数据与预先存在PACKAGE_MANIFEST/SNAPSHOT_MANIFEST逐文件核对；全20格及旧8格的completion/protocol pin、TRAIN100%、完整梯度与gap条件逐项记录JSON。

## 新20格：可启用贡献2和图3，但必须保留范围

冻结协议使用source seeds3407–3411、partition0、4184FIT（两RGBflip共8368行）/1046反复开发HELD、69类。五seed指编码器训练随机性；读出全零初始化确定性求解，不是五套独立数据。
统一lambda=1.1659571544277561e-08，按10个完整native头的最大范数平方选择，20格全部重拟合。旧8格lambda=1.2515252525186259e-08，不能拼成同一批均值。

| 来源/读出 | HELD F1均值±样本SD(%) | 平均HELD NLL | TRAIN F1 |
|---|---:|---:|---:|
| raw/raw | 57.558589 ± 1.416484 | 1.77587426 | 100% |
| raw/log | 56.501324 ± 1.089977 | 1.70282162 | 100% |
| log/raw | 54.730982 ± 1.321645 | 2.49593184 | 100% |
| log/log | 56.982313 ± 1.311611 | 1.78227036 | 100% |

上表仅抄录既有SUMMARY#/per_cell_distributions，未打开HELD标签或重算预测。Macro-F1与NLL原始逐格键：COMPLETED.json#/held/macro_f1_fixed与#/held/nll。sampleSD=√[Σ(x−mean)²/(5−1)]，不是独立数据集置信区间。

简单效应=同来源F1(Log读出)−F1(Raw读出)；DID=Log来源简单效应−Raw来源简单效应，F1差乘100为pp。既有seed效应见SUMMARY#/per_seed_effects。
必须显示反例：3410的Log来源偏Raw、DID反向；3411的Raw来源偏Log。两来源NLL在5/5source-seed偏Log，这属于指标依赖而非原配必胜。

## 早期8格：附录流程演进

旧8格=五个被接受carryover＋三个授权恢复；全部TRAIN100%、完整梯度<1e−6、gap<1e−4。原包CLAIMS_LEDGER的C07/C08/C09已经登记其交互与读出失败案例；新的F/A账本没有引用，不等于原始证据不存在。

## 全部run IDs

| 证据代次 | run_id | source seed | 来源/读出 | TRAIN F1 | HELD F1(%) | gap |
|---|---|---:|---|---:|---:|---:|
| REC-MATRIX-5S | nlc5_p0_s3407_Eraw_Rraw | 3407 | raw/raw | 1.000 | 59.158728 | 3.87497947e-05 |
| REC-MATRIX-5S | nlc5_p0_s3407_Eraw_Rlog | 3407 | raw/log | 1.000 | 56.032861 | 3.05025453e-05 |
| REC-MATRIX-5S | nlc5_p0_s3407_Elog_Rraw | 3407 | log/raw | 1.000 | 53.793657 | 3.94478514e-05 |
| REC-MATRIX-5S | nlc5_p0_s3407_Elog_Rlog | 3407 | log/log | 1.000 | 58.003470 | 3.25575645e-05 |
| REC-MATRIX-5S | nlc5_p0_s3408_Eraw_Rraw | 3408 | raw/raw | 1.000 | 58.474070 | 4.23964593e-05 |
| REC-MATRIX-5S | nlc5_p0_s3408_Eraw_Rlog | 3408 | raw/log | 1.000 | 56.546408 | 3.53893709e-05 |
| REC-MATRIX-5S | nlc5_p0_s3408_Elog_Rraw | 3408 | log/raw | 1.000 | 56.000618 | 4.27678657e-05 |
| REC-MATRIX-5S | nlc5_p0_s3408_Elog_Rlog | 3408 | log/log | 1.000 | 56.920071 | 3.6482126e-05 |
| REC-MATRIX-5S | nlc5_p0_s3409_Eraw_Rraw | 3409 | raw/raw | 1.000 | 55.647888 | 3.20994864e-05 |
| REC-MATRIX-5S | nlc5_p0_s3409_Eraw_Rlog | 3409 | raw/log | 1.000 | 55.407358 | 4.04170265e-05 |
| REC-MATRIX-5S | nlc5_p0_s3409_Elog_Rraw | 3409 | log/raw | 1.000 | 53.031207 | 4.17572981e-05 |
| REC-MATRIX-5S | nlc5_p0_s3409_Elog_Rlog | 3409 | log/log | 1.000 | 56.802306 | 3.24577799e-05 |
| REC-MATRIX-5S | nlc5_p0_s3410_Eraw_Rraw | 3410 | raw/raw | 1.000 | 56.626281 | 3.9656026e-05 |
| REC-MATRIX-5S | nlc5_p0_s3410_Eraw_Rlog | 3410 | raw/log | 1.000 | 56.215300 | 4.24939649e-05 |
| REC-MATRIX-5S | nlc5_p0_s3410_Elog_Rraw | 3410 | log/raw | 1.000 | 55.994460 | 4.16738723e-05 |
| REC-MATRIX-5S | nlc5_p0_s3410_Elog_Rlog | 3410 | log/log | 1.000 | 54.934710 | 3.65835996e-05 |
| REC-MATRIX-5S | nlc5_p0_s3411_Eraw_Rraw | 3411 | raw/raw | 1.000 | 57.885977 | 3.10944968e-05 |
| REC-MATRIX-5S | nlc5_p0_s3411_Eraw_Rlog | 3411 | raw/log | 1.000 | 58.304692 | 4.1562923e-05 |
| REC-MATRIX-5S | nlc5_p0_s3411_Elog_Rraw | 3411 | log/raw | 1.000 | 54.834966 | 3.21136056e-05 |
| REC-MATRIX-5S | nlc5_p0_s3411_Elog_Rlog | 3411 | log/log | 1.000 | 58.251007 | 3.89803509e-05 |
| REC-PROBE-2S | nlc1_p0_s3407_Eraw_Rraw | 3407 | raw/raw | 1.000 | 58.229666 | 3.54295976e-05 |
| REC-PROBE-2S | nlc1_p0_s3407_Eraw_Rlog | 3407 | raw/log | 1.000 | 56.048796 | 3.1541865e-05 |
| REC-PROBE-2S | nlc1_p0_s3407_Elog_Rlog | 3407 | log/log | 1.000 | 57.907472 | 2.74580314e-05 |
| REC-PROBE-2S | nlc1_p0_s3407_Elog_Rraw | 3407 | log/raw | 1.000 | 53.793657 | 3.57479811e-05 |
| REC-PROBE-2S | nlc1_p0_s3408_Eraw_Rlog | 3408 | raw/log | 1.000 | 56.546408 | 3.67071239e-05 |
| REC-PROBE-2S | nlcr3_p0_s3408_Eraw_Rraw | 3408 | raw/raw | 1.000 | 58.544128 | 3.29647842e-05 |
| REC-PROBE-2S | nlcr3_p0_s3408_Elog_Rraw | 3408 | log/raw | 1.000 | 55.990727 | 3.40257401e-05 |
| REC-PROBE-2S | nlcr3_p0_s3408_Elog_Rlog | 3408 | log/log | 1.000 | 56.625489 | 3.46124705e-05 |

## 实物与表述边界

JSON逐格给出归档路径、protocol/completion SHA、cache binding/source encoder checkpoint/hash、数据划分SHA、每个数字文件+键指针及公式。旧绝对D盘路径仅作为历史执行身份保留，当前实际核验均指F盘归档路径。
未读图像/标签/预测数组，未导入归档代码，未计算新预测或新指标。只检查既有汇总。原目录只读；新20格并非本轮新增训练。
部分旧run_cell复用的limits文本仍写2seed/4encoder，补证SUMMARY已明确其为继承说明；核查实际协议为5seed/10encoder/20格。expanded_probe README也保留执行前notstarted说明，不能把旧设计文字当当前状态。
合理叙事：经充分拟合并通过指定凸目标数值证书后，来源×读出映射存在本设置下的条件性交互，且F1与NLL偏好不同。不能写原配必胜、不可替代刚性耦合、独立新域确认或联合训练因果必要性。

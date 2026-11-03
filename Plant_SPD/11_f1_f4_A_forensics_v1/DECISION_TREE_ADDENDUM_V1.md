# 原六条判决规则：逐项核对与数学准入边界

本附录保留用户的 (i)/(ii)/(iii)/(a)/(b)/(c) 标签，按当前直接指令作语义转写，**不是冒充历史文件中的逐字引文**。不改原冻结预测表，不新增实验或评价。数字仅从已完成 JSON 元数据读取或做明确的标量算术；机器版本提供每个数的实际来源键和 SHA。

| 原标签与规则简写 | 本轮状态 | 正确含义 |
|---|---|---|
| (i) 支持甲：B <= 2*r_min，并由 F3 复核。 | `NOT_ADMITTED_AS_FORMAL_TEST` | 100%严格分类的正r_min不存在：正缩放保持argmax，范数下确界为0。one-hot插值或未缩放theta_cert不是必要分类范数；同时B=sum LR单独并非硬参数预算。 |
| (ii) 支持甲：高需求坐标的 \|u\| 中位数 >0.5，说明方向未丢。 | `NOT_MET_DESCRIPTIVE_THRESHOLD` | 两个预选case的参考幅值前5%坐标中位数均不超过0.5；即使超过，绝对幅度也不证明有益方向。参考大系数坐标不等于必要高需求方向。 |
| (iii) 支持甲：W(t)线性增长后平台，高需求 \|W_i\| 停在qB附近且 \|theta_cert_i\|>=3B。 | `UNAVAILABLE_ORIGINAL_FULL_HISTORY` | 旧完整W/b及encoder RMS历史未存，不能从16个旧选中坐标或新A轨迹重建；q分位数不是全轨迹硬界，大参考坐标不是必要大小。 |
| (a) 否证/降级：B>=3*r_cert且W未平台或已达证书尺度仍低F1，归因方向/曲率。 | `NOT_MET_NUMERIC_PRECONDITION` | 按本轮完整73002参数RMS定义，两case均未满足B>=3*r_cert；旧完整历史仍不可用。即使满足该数值关系，r_cert也非必要范数，且不能唯一定位方向或曲率。 |
| (b) 否证/降级：高需求 \|u\| 中位数 <0.2，说明SNR接管。 | `MET_NUMERIC_THRESHOLD_BUT_CAUSAL_INFERENCE_NOT_ADMITTED` | Raw与Log对应末态中位数均小于0.2，数值条件确实成立；它只描述参考前5%坐标的终点更新幅度，未测方向/SNR/完整历史，不能据此宣称SNR接管。 |
| (c) 否证/降级：r_min远小于B，存在小解却未找到，因此预算次要。 | `NOT_ADMITTED_AS_STATED` | 分类r_min的下确界为0；对固定CE则只有必要下界和可行上界，不能把小下界当作存在小解。远小于也未给预冻结数值阈值；即使存在较小可行解，仍不唯一排除有限路径、参数化、方向或预算因素。 |

## 1. 原支持条件 (i)：不能用无效 r_min 确认预算叙事

严格可分分类器乘任意正 alpha 保持 argmax，范数可趋近0；因此“100%分类必须有正r_min”不成立。B只是实际LR之和；只有加入对每步u及衰减的有效界，才能形成参数上限。本轮有效的逐坐标及RMS上限是 weighted-Cauchy 的S，而不是q99×B。

| 同特征case | B | 有效S | 未缩放参考RMS（非必要大小） |
|---|---:|---:|---:|
| raw_frozen | 1.3755 | 6.6939215 | 7.0720664 |
| log_joint | 1.3755 | 6.6939215 | 3.9511917 |

固定CE可换成下表的必要下界L与射线可行上界U；两者不是所需最小范数的精确值。L没有超过S，不能据此证明资源预算导致不可达；反过来，L小也不能证明存在低范数解。

| case / 范围 | dual CE目标 | 必要RMS下界L | 射线可行RMS上界U | 此射线最大坐标绝对值 |
|---|---:|---:|---:|---:|
| raw_frozen / original_unflipped | 1 | 0.14190027 | 1.3355783 | 8.9213297 |
| raw_frozen / original_unflipped | 0.5 | 0.1794791 | 1.8552175 | 12.39239 |
| raw_frozen / original_unflipped | 0.1 | 0.24967019 | 3.1172764 | 20.822629 |
| raw_frozen / augmented_both_true_flips | 1 | 0.14204576 | 1.3354903 | 8.920742 |
| raw_frozen / augmented_both_true_flips | 0.5 | 0.17966311 | 1.8556057 | 12.394983 |
| raw_frozen / augmented_both_true_flips | 0.1 | 0.24992617 | 3.1187578 | 20.832524 |
| log_joint / original_unflipped | 1 | 0.030012968 | 0.63311945 | 3.8339675 |
| log_joint / original_unflipped | 0.5 | 0.03796117 | 0.88471478 | 5.3575478 |
| log_joint / original_unflipped | 0.1 | 0.052807111 | 1.4939591 | 9.0469351 |
| log_joint / augmented_both_true_flips | 1 | 0.030013095 | 0.63364467 | 3.8371481 |
| log_joint / augmented_both_true_flips | 0.5 | 0.03796133 | 0.88534979 | 5.3613932 |
| log_joint / augmented_both_true_flips | 0.1 | 0.052807334 | 1.4947911 | 9.0519736 |

**坐标上限与RMS上限不能混淆。** `U<S`只检查RMS这一个必要条件，不表示该射线每个坐标也都≤S。上表的最大坐标是`alpha*max_abs(theta_cert)`，来源为既有ray alpha和参考系数abs_max的元数据；即使全部坐标满足上限，也不证明AdamW在该有限路径可达。

实际来源：`derived_actual_v1/F1_F4_DERIVED_V1.json#/cells_5_by_3` 与 `#/principal_same_feature_cases`；`ray_witness_actual_v1/RESULT.json#/outcomes`。逐数精确索引见本附录 JSON。

## 2. 条件 (ii) 与分支 (b)：同一个幅度统计，不能偷换成方向/SNR

| case | 参考幅值前5%坐标末态 abs(u) 中位数 | 其中 abs(u)>0.5 占比 | >0.5中位数条件 | <0.2中位数条件 |
|---|---:|---:|---|---|
| raw_frozen | 0.18034339 | 7.45001% | 未满足 | 满足数值条件 |
| log_joint | 0.15946734 | 5.42317% | 未满足 | 满足数值条件 |

因此(ii)的描述阈值未满足，(b)的数值阈值满足；但两者的因果后半句均没有准入：`|u|`不包含更新是否朝有益方向的信息，参考大系数坐标也未被证明是所有好解必需的方向。没有由这些数值测出SNR接管。

实际来源：`derived_actual_v1/F1_F4_DERIVED_V1.json#/principal_same_feature_cases/0/terminal_u_on_same_feature_certificate_top5_abs_indices/abs_median`，case1同键；比例键为`fraction_abs_terminal_u_gt_point5_in_top5`。

## 3. 条件 (iii)、分支 (a)/(c)：历史缺失与竞争解释

- (iii)：原完整W/b与encoder RMS历史为`UNAVAILABLE`。原少量选中坐标、新A0/A4轨迹和F4终点不能补成原全轨迹，也不能由末期平台唯一证明范数天花板。
- (a)：按冻结的完整头RMS单位，两个case均不满足`B>=3*r_cert`；即使满足，未缩放参考系数不是必要大小，且不能唯一归因为方向或曲率。
- (c)：分类范数下确界0不能作为预算次要的机制证据；固定CE的“小下界”不等于“小解存在”。本轮报告了具体可行射线，但“远小于”的阈值未冻结，而且可行性不等于有限优化可达。

## 4. 受控干预实际支持什么

| 主臂seed3407 | 原始FIT Macro-F1 | 相对A0变化 | dual CE |
|---|---:|---:|---:|
| A0 | 24.178% | — | 2.790218 |
| A | 24.178% | 0pp | 2.790155 |
| A2 | 87.5436% | 63.3656pp | 0.8972282 |
| A2prime | 53.4716% | 29.2936pp | 1.867715 |
| A3 | 76.6747% | 52.4968pp | 1.061734 |

- A删除WD的Macro-F1变化为0pp，削弱当前配方中直接WD主导的解释；不否证所有噪声/方向解释。A2的LR×10、A2prime的时长/cosine共变、A3温度重参数化均有恢复，支持有限优化配方与参数化有实质影响，但不能唯一确认原甲的范数天花板。
- A2三个预定training seeds的最终FIT Macro-F1为 87.5436%, 87.8193%, 88.0291%，均值 87.7973%，样本SD 0.243461pp。样本SD分母为3−1；只衡量同一重复FIT上的训练种子变化，不是新独立数据或泛化置信区间。
- A4-Log最终FIT Macro-F1 89.1929%，较对应旧Log-joint提高 53.1427pp，达到预定10pp恢复条件；因此A4-Raw按预定条件跳过。没有观察到“Log干预失败、Raw干预成功”的分支，不支持Log特异失败机制。LR×5与warmup共同变化，也不能分开归因。
- 新A轨迹是前瞻记录；F4为同4184原图的三个终点，保留global RMS和mean-image RMS的区别，不证明统一标量缩放或历史演化。

实际来源：`F1_F4_FORENSICS.json#/A_primary_cached`、`#/conditional_results`、`#/A4_Log`、`#/F4_endpoint_RMS`。本附录JSON保留每个计算的value、formula、sourcefile、key与SHA。

## 5. 收束后的结论

Matched finite interventions support a substantial role of recipe/parameterization in low fitting. They do not identify a unique norm ceiling, lost direction, SNR takeover, curvature cause, or a geometry-specific failure. No new HELD/generalization evidence.

可以明确说：**原低拟合不能直接归咎固定表示不可分，有限训练配方与参数化具有实质影响。** 不能继续说：已经证明唯一行进上界、方向未丢、SNR接管或几何特异失效。所有新A结果仍是重复FIT诊断，没有新的HELD、田间或外部泛化结论。

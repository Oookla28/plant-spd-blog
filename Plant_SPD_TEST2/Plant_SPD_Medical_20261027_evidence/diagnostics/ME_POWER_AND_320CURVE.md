# 320-step 曲线与 E01 功效只读诊断

本诊断只读 F 盘已有产物，未训练、未调用 GPU、未修改训练源码或主报告。已读取历史 `AGENTS.md` 约束文件。

## 关键曲线读数

植物等头正式 `*log_joint` 五 seed 每 epoch 131 updates。320 steps 位于 epoch 2（step 262）与 epoch 3（step 393）之间：线性插值的 TRAIN Macro-F1 为 **2.96 ± 0.58%**，HELD 为 **2.53 ± 0.48%**；最近实际记录 step 262 为 1.97%/1.78%。到固定 20 epoch、step 2620 才达到 TRAIN **34.12 ± 2.20%**、HELD **25.74 ± 2.67%**。因此“320 steps 已约 34%”与日志不符，34%是最终预算点。曲线从 epoch 1 到 20 持续上升，HELD 峰值多在 epoch 19–20，终点相对峰值均值仅 −0.09pp，不能称为早停平台或晚期崩落。

作为命名交叉核对，植物 `raw_joint` 在 step 320 已为 TRAIN 54.33 ± 9.98%、HELD 36.89 ± 5.54%；E01 普通 `*_log` 管线在 step 320 为 TRAIN 28.19%、HELD 21.60%。这两组不是主读数，避免把 `raw_joint` 或普通 E01 log 与正式等头 `log_joint` 混称。

医学等头 `equal_*_log_joint` 的 20 epoch 终点正好是 step 320（16 updates/epoch），五 seed 均值为 TRAIN 60.00%、HELD 55.77%。同名 step 数对应的训练进度不同：植物 step 320 仅约 2.44 epoch。

## E01 配对功效

医学 E01 的逐配对 Log−Raw 差（pp）为 `[-6.69, 0.89, 0, -1.78, 14.10, 4.08, 2.98, 3.97, -7.21, -2.63]`。分划分统计：

- partition 0：均值 +1.30pp，SD **7.73pp**，SE **3.46pp**，paired t(4)=0.377，p=0.725，95% CI [−8.29,+10.90]pp；80% 功效的双侧 MDE 约 **13.00pp**。
- partition 1：均值 +0.24pp，SD **5.00pp**，SE **2.23pp**，paired t(4)=0.106，p=0.921，95% CI [−5.97,+6.44]pp；MDE 约 **8.41pp**。
- pooled n=10（仅描述性，两个 partition 重叠）：均值 +0.77pp，SD 6.16pp，SE 1.95pp，t(9)=0.395，p=0.702，95% CI [−3.64,+5.18]pp；MDE 约 **6.14pp**。

功效按双侧 α=0.05 的非中心 t 数值积分计算并以零效应功效 0.05 校验。对于预期 +2pp，partition 0/1 的功效约 **7.4%/10.8%**，pooled n=10 约 **15.1%**；因此 +0.77pp 与 +2pp 在现有 E01 规模下均不可分辨。用户给出的单配对 SD ±4–8pp 得到支持；SE 的 2–3pp 量级大体正确，但 partition 0 实测为 3.46pp，略超 3pp 上限。

完整逐 seed、曲线快照、公式和来源 SHA 见同目录 `ME_POWER_AND_320CURVE.json`。

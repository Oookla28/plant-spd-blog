# 审查执行偏差：意外触发一个真实读出格

本记录由独立审查执行者承担。原要求只读与合成审查；我采用内存 spy 检查 worker 路线时，未先核对两个模块别名，导致拦截对象不是实际调用对象。这是审查执行错误。

- 真实工件目录：`D:\PlantSPD_teacher_delivery_update_v1_20261026\independent_cross_probe_review\plan_Eraw_Rlog_s3409_v2\run`
- 实际格：`nlc5_p0_s3409_Eraw_Rlog`；状态 `COMPLETE`。
- 开始UTC：`2026-10-26T12:43:12.037074+00:00`；结束UTC：`2026-10-26T12:44:03.264273+00:00`。
- 原进程PID：42668；当前只读进程快照仅列出本次元数据记录脚本PID36656；意外进程PID42668不在列表中，已经退出。
- 实际读取4184张FIT的缓存及标签（8368真实翻转行），并读取和评分原已反复开发的1046张HELD；没有编码器训练、编码器前向或RGB读取。
- 没有修改F包。全部产物保留在D盘审查目录，禁止进入论文科学证据、复现成功结论或独立确认统计。

原因：`import_bound(anchored)` 生成 `manual_frozen_anchored`，实际 `Study.source(anchored)` 生成 `portable_frozen_bfca7316c99813c6`。更改前者的run_cell没有拦截后者。真实调用返回后spy次数断言失败，未生成计划的mock通过收据。

已经停止一切实验/worker调用。后续仅记录已有元数据与进程终态。交付说明中“本次没有真实拟合或HELD标签访问”的全局表述必须显式增加本偏差，不得将真实结果藏在合成验收名义下。

精确argv、协议/SHA、时间、原始产物SHA与访问范围依据见同目录 `REVIEW_EXECUTION_DEVIATION.json`。

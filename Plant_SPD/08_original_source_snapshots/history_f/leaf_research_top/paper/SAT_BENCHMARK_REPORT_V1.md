# SAT普通分割基线筛选 V1

生成时间：2026-10-19T15:04:41.982112+00:00。窗口阶段：**OPEN**。窗口阶段与科学完成分别记录：训练完成不会自动证明分析完成或窗口关闭，只有对应closer的真实closeout元数据可显示CLOSED。本writer未做实时PID、进程组或GPU身份检查。

本轮是普通模型的共同预算能力筛选，不是新算法贡献、官方训练配方复现、收敛SOTA或录用等级证明。5个模型各3个预定训练seed，固定20完整epoch、9800更新、78,340次图像访问，batch8且每epoch尾batch5保留。不同模型有预注册的初始化、参数量和学习率差异，因此不能把结果解释为只改变架构的因果实验。U-Net随机初始化；其余使用已有审计的ImageNet主干；新增任务头新初始化。DeepLab/U-Net为明确说明的重实现，SegFormer为经审阅源码适配的二值改头/单卡BN版本，EfficientViT两头为既有普通参考。Mask2Former/STAR-Net保持HELD，不用其他普通头替代其名称。

| 模型 | 计划参数量 | 初始化 | 预注册LR |
| --- | --- | --- | --- |
| deeplabv3plus_r50 | 26690993 | ImageNet backbone | 0.0001 |
| efficientvit_fpn | 4698977 | ImageNet backbone | 0.0002 |
| efficientvit_mlp | 4691489 | ImageNet backbone | 0.0002 |
| segformer_b2 | 27347393 | ImageNet backbone | 6e-05 |
| unet | 31384833 | random | 0.001 |

数据仅为冻结的3917训练图和反复使用的904开发图。输入与二值GT在各自原图上先处理EXIF，再按明确PIL规则缩放/letterbox到256；RGB bilinear、GT nearest。有效区仅排除填充，**不是叶mask**。所有本轮IoU、Dice和BoundaryF1均属**resized256 letterbox有效像素网格**，不等于原分辨率测量。原640输入/native160流程、69/70语义类别指标、官方116类mIoU及检测mAP需分别列示，不能直接混算或声称相同协议增益。

监督仅为既有二值前景，可能含叶片、果实及其他对象；病理/症状语义未获专家认证，专家审阅完成数仍为0。904仅作开发筛选。既往cal标签曾合法用于gain拟合；本轮不打开cal/final逐图标签、图像、掩码或作最终评价。旧协议final类别/宿主**聚合元数据曾暴露**，已有声明未用于模型/协议/选样；不能声称从未接触任何final相关标签信息，也不能把该暴露扩大成已读逐图final GT。本报告不重新读取或复制该聚合值。

## 运行与关闭元数据

| 字段 | 记录 / 限定 |
| --- | --- |
| window phase | OPEN |
| CPU end UTC | 2026-10-19T21:46:04Z |
| closer heartbeat UTC（非live验证） | 2026-10-19T15:04:31.121597+00:00 |
| closer outcome | MISSING |
| closeout record UTC | MISSING |
| analysis payload status | PLANNED |
| live PID/UUID/进程身份核查 | NOT_PERFORMED；本writer只投影登记元数据 |

原始dispatch的5个memory请求在guard登记前因spec中不支持的环境键被拒绝，15个formal因此被阻断；原attempt证据保留，这些不是20个科学训练失败。独立dispatch-only amendment仅删除该键，保留科学协议、run ID、argv与输出。报告同时保留实际payload状态和原/当前dispatch元数据状态；没有把GPU任务实际运行两遍，也不把预登记拒绝冒充已完成结果。

## 已登记执行故障（2026-10-19T14:00Z核查）

FPN seed3407在9,713步后因监督心跳超时被watchdog触发停止，之后出现DataLoader worker被SIGTERM终止；该载荷FAILED不代表已测出模型性能失败。MLP seed3407的command_go未放行，命令门返回125，随后监督器报告身份验证失败；没有该trainer已执行训练的证据，不能将其计为训练过的阴性模型。

静态审查发现心跳/登记元数据同步fsync及其他串行监控调用可能延长心跳与启动握手间隔，但缺少触发前阻塞栈与调用耗时，**尚未确认唯一根因**。现有温度、显存和磁盘观测未显示对应超温、OOM或满盘触发。证据与限制见audits/sat_execution_20261019/runtime_incident_20261019T1400_v1.json和GUARD_FAILURE_REVIEW_V1.md。

失败记录、部分checkpoint和已有输出原样保留；剩余固定任务继续使用原守护和原截止，不重试或恢复失败run、不修改运行源或阈值。完整15run分析及两项效率量测的前置条件未满足，继续HOLD；部分训练终点不进入正式性能主表，也不以缺失seed填充均值/区间。

## 各run的真实状态

| run_id | stage | 实际payload状态 | 科学状态 | 原dispatch | 当前dispatch元数据 |
| --- | --- | --- | --- | --- | --- |
| satv1_deeplabv3plus_r50_cpu_s3407 | CPU_SMOKE | COMPLETE | COMPLETE | NOT_RECORDED | NOT_RECORDED |
| satv1_deeplabv3plus_r50_mem_s3407 | GPU_MEMORY_SMOKE | COMPLETE | COMPLETE | LAUNCH_FAILED_NO_RETRY | COMPLETED |
| satv1_deeplabv3plus_r50_train_s3407 | GPU_SCREENING | COMPLETE | COMPLETE | BLOCKED_MEMORY_PROOF | COMPLETED |
| satv1_deeplabv3plus_r50_train_s3408 | GPU_SCREENING | COMPLETE | COMPLETE | BLOCKED_MEMORY_PROOF | COMPLETED |
| satv1_deeplabv3plus_r50_train_s3409 | GPU_SCREENING | NO_PAYLOAD_STATUS | PLANNED | BLOCKED_MEMORY_PROOF | PLANNED |
| satv1_efficientvit_fpn_cpu_s3407 | CPU_SMOKE | COMPLETE | COMPLETE | NOT_RECORDED | NOT_RECORDED |
| satv1_efficientvit_fpn_mem_s3407 | GPU_MEMORY_SMOKE | COMPLETE | COMPLETE | LAUNCH_FAILED_NO_RETRY | COMPLETED |
| satv1_efficientvit_fpn_train_s3407 | GPU_SCREENING | FAILED | FAILED | BLOCKED_MEMORY_PROOF | PAYLOAD_FAILED |
| satv1_efficientvit_fpn_train_s3408 | GPU_SCREENING | COMPLETE | COMPLETE | BLOCKED_MEMORY_PROOF | COMPLETED |
| satv1_efficientvit_fpn_train_s3409 | GPU_SCREENING | NO_PAYLOAD_STATUS | PLANNED | BLOCKED_MEMORY_PROOF | PLANNED |
| satv1_efficientvit_mlp_cpu_s3407 | CPU_SMOKE | COMPLETE | COMPLETE | NOT_RECORDED | NOT_RECORDED |
| satv1_efficientvit_mlp_mem_s3407 | GPU_MEMORY_SMOKE | COMPLETE | COMPLETE | LAUNCH_FAILED_NO_RETRY | COMPLETED |
| satv1_efficientvit_mlp_train_s3407 | GPU_SCREENING | NO_PAYLOAD_STATUS | PLANNED | BLOCKED_MEMORY_PROOF | GUARD_FAILURE |
| satv1_efficientvit_mlp_train_s3408 | GPU_SCREENING | RUNNING | RUNNING | BLOCKED_MEMORY_PROOF | RUNNING |
| satv1_efficientvit_mlp_train_s3409 | GPU_SCREENING | NO_PAYLOAD_STATUS | PLANNED | BLOCKED_MEMORY_PROOF | PLANNED |
| satv1_segformer_b2_cpu_s3407 | CPU_SMOKE | COMPLETE | COMPLETE | NOT_RECORDED | NOT_RECORDED |
| satv1_segformer_b2_mem_s3407 | GPU_MEMORY_SMOKE | COMPLETE | COMPLETE | LAUNCH_FAILED_NO_RETRY | COMPLETED |
| satv1_segformer_b2_train_s3407 | GPU_SCREENING | COMPLETE | COMPLETE | BLOCKED_MEMORY_PROOF | COMPLETED |
| satv1_segformer_b2_train_s3408 | GPU_SCREENING | RUNNING | RUNNING | BLOCKED_MEMORY_PROOF | RUNNING |
| satv1_segformer_b2_train_s3409 | GPU_SCREENING | NO_PAYLOAD_STATUS | PLANNED | BLOCKED_MEMORY_PROOF | PLANNED |
| satv1_unet_cpu_s3407 | CPU_SMOKE | COMPLETE | COMPLETE | NOT_RECORDED | NOT_RECORDED |
| satv1_unet_mem_s3407 | GPU_MEMORY_SMOKE | COMPLETE | COMPLETE | LAUNCH_FAILED_NO_RETRY | COMPLETED |
| satv1_unet_train_s3407 | GPU_SCREENING | COMPLETE | COMPLETE | BLOCKED_MEMORY_PROOF | COMPLETED |
| satv1_unet_train_s3408 | GPU_SCREENING | COMPLETE | COMPLETE | BLOCKED_MEMORY_PROOF | COMPLETED |
| satv1_unet_train_s3409 | GPU_SCREENING | NO_PAYLOAD_STATUS | PLANNED | BLOCKED_MEMORY_PROOF | PLANNED |

## 正式末步开发结果

只有同协议/源/配置指纹匹配、9800步/78,340访问且完整904图评价完成的run才显示数值；PLANNED、FAILED、STOPPED、partial或元数据不匹配均不产生主指标。

| 模型 | seed | 科学状态 | step | dev n | 前景IoU % | 二类mIoU % | Dice % | BoundaryF1 % | source-small n | small IoU % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| deeplabv3plus_r50 | 3407 | COMPLETE | 9800 | 904 | 64.62715 | 76.29928 | 78.51336 | 53.84720 | 19 | 10.81781 |
| deeplabv3plus_r50 | 3408 | COMPLETE | 9800 | 904 | 64.78542 | 76.38432 | 78.63004 | 53.91672 | 19 | 8.90045 |
| deeplabv3plus_r50 | 3409 | PLANNED | UNRECORDED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED |
| efficientvit_fpn | 3407 | FAILED | 9713 | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED |
| efficientvit_fpn | 3408 | COMPLETE | 9800 | 904 | 64.03603 | 75.86011 | 78.07557 | 51.66045 | 19 | 8.52928 |
| efficientvit_fpn | 3409 | PLANNED | UNRECORDED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED |
| efficientvit_mlp | 3407 | PLANNED | UNRECORDED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED |
| efficientvit_mlp | 3408 | RUNNING | 900 | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED |
| efficientvit_mlp | 3409 | PLANNED | UNRECORDED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED |
| segformer_b2 | 3407 | COMPLETE | 9800 | 904 | 68.13573 | 78.62698 | 81.04849 | 58.20397 | 19 | 9.51060 |
| segformer_b2 | 3408 | RUNNING | 9800 | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED |
| segformer_b2 | 3409 | PLANNED | UNRECORDED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED |
| unet | 3407 | COMPLETE | 9800 | 904 | 51.80434 | 67.25630 | 68.25146 | 40.52364 | 19 | 9.10155 |
| unet | 3408 | COMPLETE | 9800 | 904 | 51.82280 | 67.19333 | 68.26748 | 40.37413 | 19 | 9.83959 |
| unet | 3409 | PLANNED | UNRECORDED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED | UNMEASURED |

## 三seed汇总

UNMEASURED：只有完整且当前SHA匹配的分析器COMPLETE产物才能展示3seed均值/标准差；本writer不计算统计量。

配对组bootstrap若由另行授权的完整分析器产生，其区间条件于这3个训练实例，不是额外独立seed，不是独立最终验证。本writer不重新计算均值、标准差、CI或像素指标。

## CPU与显存smoke

以下仅为有限合约检查，2图开发smoke分数不是904正式性能，也不用于选模型或调参。

| run_id | stage | 状态 | step | dev n（非主结果） |
| --- | --- | --- | --- | --- |
| satv1_deeplabv3plus_r50_cpu_s3407 | CPU_SMOKE | COMPLETE | 4 | 2 |
| satv1_deeplabv3plus_r50_mem_s3407 | GPU_MEMORY_SMOKE | COMPLETE | 4 | 2 |
| satv1_efficientvit_fpn_cpu_s3407 | CPU_SMOKE | COMPLETE | 4 | 2 |
| satv1_efficientvit_fpn_mem_s3407 | GPU_MEMORY_SMOKE | COMPLETE | 4 | 2 |
| satv1_efficientvit_mlp_cpu_s3407 | CPU_SMOKE | COMPLETE | 4 | 2 |
| satv1_efficientvit_mlp_mem_s3407 | GPU_MEMORY_SMOKE | COMPLETE | 4 | 2 |
| satv1_segformer_b2_cpu_s3407 | CPU_SMOKE | COMPLETE | 4 | 2 |
| satv1_segformer_b2_mem_s3407 | GPU_MEMORY_SMOKE | COMPLETE | 4 | 2 |
| satv1_unet_cpu_s3407 | CPU_SMOKE | COMPLETE | 4 | 2 |
| satv1_unet_mem_s3407 | GPU_MEMORY_SMOKE | COMPLETE | 4 | 2 |

训练/导出总时间不等于孤立推理延迟；预训练成本未被本轮训练时间计入，不能按零成本计算。没有新增手机/田间、能耗、农艺收益或可靠性部署证据。普通基线筛选结果不构成复活路由、增添模型、seed、超参或延长窗口的授权。

## 本次读取的元数据与SHA

这些哈希只说明本次读到的JSON版本。预测/检查点等payload字节核验属于独立分析器的范围，不能归功于本writer；实时身份核验未执行。

```json
{
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/configs/sat_benchmark_v1.json": {
    "status": "READ",
    "sha256": "6b7ba0a06938511675bf887970aba498357a4aa137c05baf4cce37ce407a6db2"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/configs/sat_benchmark_jobs_v1.json": {
    "status": "READ",
    "sha256": "795ee830a2988be74b390ddf2f867eb54dd7ac746295c6fd6851f28f6d8ea3c3"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/.safe/windows/sat_benchmark_v1_20261019/queue_state.json": {
    "status": "READ",
    "sha256": "8586f7d311dea1b1f17b5b459ca73c5751a9be807b20325ff6a1ba85d966616f"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/.safe/windows/sat_benchmark_v1_20261019/closer.json": {
    "status": "READ",
    "sha256": "8ef42d0b95e5dd4f214f3a43dcb3fefa36f702d8aa7d653a1f96bd430b917990"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/.safe/windows/sat_benchmark_v1_20261019/closer_heartbeat.json": {
    "status": "READ",
    "sha256": "df4013ca5b85b235f72cd3cfd16e1339aa97b6bc65cd435ffc35c1717a88fe82"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/.safe/windows/sat_benchmark_v1_20261019/closeout.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/.safe/windows/sat_benchmark_v1_20261019/closer_outcome.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/audits/sat_execution_20261019/dispatch_environment_amendment_v1.json": {
    "status": "READ",
    "sha256": "8dabffe645dc49c2a8b9d954385caab29590cdd2328e209a4e88eb2d540d223a"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/.safe/windows/sat_benchmark_v1_20261019/dispatch_fix_v1/queue_state.json": {
    "status": "READ",
    "sha256": "6bfe84dac818ffff5f017da883259affcb7a02e2da5d7c271df3f21b8cb7fc66"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/.safe/windows/sat_benchmark_v1_20261019/dispatch_fix_v1/controller.json": {
    "status": "READ",
    "sha256": "dea424ee4cc052886c659aa3ac92a23671a545e55ab1daad3cb4c88022dd28de"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/configs/sat_benchmark_jobs_dispatch_fix_v1.json": {
    "status": "READ",
    "sha256": "d71b257f8f12f7321a1e435d6924a8672045348c66230dd8882df504eb15e37b"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_cpu_s3407/status.json": {
    "status": "READ",
    "sha256": "7ae9670edc473878ae3069c6abbbb2385adea2e916ba8e3d646788965e57a944"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_cpu_s3407/config.json": {
    "status": "READ",
    "sha256": "2563b3970535ae6ebf5d45d397d6adb1121a29325d10cf284663c16dc253fa13"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_cpu_s3407/metrics.json": {
    "status": "READ",
    "sha256": "1b2036807b11a91e793445bc4f62b57e4dde44ad492bed8a60174ea256963ddd"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_mem_s3407/status.json": {
    "status": "READ",
    "sha256": "44de3eccec88c889ab32e984389be9273f33a37d09b4db0925a7f4e1b1f5b7ea"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_mem_s3407/config.json": {
    "status": "READ",
    "sha256": "2b49ec27581837117b3c4147458450354df88a9175ecf40f0ec05abb39b4726a"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_mem_s3407/metrics.json": {
    "status": "READ",
    "sha256": "fa812308efbf62d7f612080ad9c8eff5bf27f39098af3c459fd9529cea0aebe9"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_train_s3407/status.json": {
    "status": "READ",
    "sha256": "378dd6f8505526af628ff89897fc0acdbe90f72b1e3123e08159f232138eeed8"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_train_s3407/config.json": {
    "status": "READ",
    "sha256": "bf97ad7e52e0333b9a20c3bc61e93ab52c11d07eadd85aad155fdd6d79e524c0"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_train_s3407/metrics.json": {
    "status": "READ",
    "sha256": "fd0385e932ad56eeaf52221db4e87388fe5d631f4436581d3f6d681f9c54f804"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_train_s3408/status.json": {
    "status": "READ",
    "sha256": "c0cbb46390f18130a45e060895f1e3cf777b2556c9cafa8c95468fc5ba616dc7"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_train_s3408/config.json": {
    "status": "READ",
    "sha256": "272ff95e9cf6b914c6ebe17ce865036082c95fbcbf6c29704f01899fc6d2bd89"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_train_s3408/metrics.json": {
    "status": "READ",
    "sha256": "bc0e4479eaaab5d7ea20dddedabc671e419a84f808346bead73db23587982122"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_train_s3409/status.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_deeplabv3plus_r50_train_s3409/config.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_cpu_s3407/status.json": {
    "status": "READ",
    "sha256": "1f6c93dcecae385c4b6381222e135e1a73a6df0cd72b646c2e2f3f9becfeb842"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_cpu_s3407/config.json": {
    "status": "READ",
    "sha256": "d37ec5c2da5148e84286750827f6b2518ba54d1644a2f21c246c107482e6b9b2"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_cpu_s3407/metrics.json": {
    "status": "READ",
    "sha256": "8458eae697c391e43f2de752635a41fa6b932ac5da4fb3f4ff8bffb7ad744526"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_mem_s3407/status.json": {
    "status": "READ",
    "sha256": "3f453edd21c5a41589229015b0f0b3dd7fc6810ab7f0f6ae7910e9887659cdae"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_mem_s3407/config.json": {
    "status": "READ",
    "sha256": "6733bd9cc4a5442a98e7625ba233cf823db48d534624d2e3a7f09d432e2ef304"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_mem_s3407/metrics.json": {
    "status": "READ",
    "sha256": "5d682e60a87676b7fe03b13cd20559e689a120ac1abe0183d0b9883678e8ef7d"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_train_s3407/status.json": {
    "status": "READ",
    "sha256": "b70ff551d5b9d530f7901144b6222c98a1caccf9cffeeb3768d4dbc2c283f34b"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_train_s3407/config.json": {
    "status": "READ",
    "sha256": "a795499775c002c56c0bd3b80f8104af1ced9bf1b8ab72940d2e20904c0e5566"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_train_s3408/status.json": {
    "status": "READ",
    "sha256": "f78e73e34186f88c23be25724529eea6a7732252da673a1e296f1e22345b6d7f"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_train_s3408/config.json": {
    "status": "READ",
    "sha256": "f7d8d0ef7d11e4b5be99909533b875040e3d11a8bc266b0a8139b8e5c51a60a4"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_train_s3408/metrics.json": {
    "status": "READ",
    "sha256": "f111b92c4c595cb0129b36579110a77a8a7685857452871f2f68ae3d61155c15"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_train_s3409/status.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_fpn_train_s3409/config.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_mlp_cpu_s3407/status.json": {
    "status": "READ",
    "sha256": "ae86fa0b86fd45ef5cf49756b2c58a7438bc897aeedaa95819e3936aedcfd57c"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_mlp_cpu_s3407/config.json": {
    "status": "READ",
    "sha256": "f2cd9400171dba37d7a9fb0003d0ccef937fc057f1027dc91b58e09d24061c91"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_mlp_cpu_s3407/metrics.json": {
    "status": "READ",
    "sha256": "0891c2f8b458bff3dcee9c0a4fb3e613a923aa17948ffc0243d4a29b24f18be1"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_mlp_mem_s3407/status.json": {
    "status": "READ",
    "sha256": "a12c4ec172fa8a00b3069023505509df78d5e55b262ec5ab3059679cad4ac480"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_mlp_mem_s3407/config.json": {
    "status": "READ",
    "sha256": "507a3bc1e60c6acaea53ae028b71f8c9d01042831520e66621a08eac08d9dba5"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_mlp_mem_s3407/metrics.json": {
    "status": "READ",
    "sha256": "d1d9a7753bc889a160d12b6d11550e6cb70aa9e3c24b2e40cd99beb49e535801"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_mlp_train_s3407/status.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_mlp_train_s3407/config.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_mlp_train_s3408/status.json": {
    "status": "READ",
    "sha256": "4293f151c01613d762910fb8f3f12c4271123cb1c24b5390f3451b23b87feffb"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_mlp_train_s3408/config.json": {
    "status": "READ",
    "sha256": "d716d66893ffd46be3dc9acc79a0a53f7b24bc363042f2390a1f6ee8e51691cd"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_mlp_train_s3409/status.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_efficientvit_mlp_train_s3409/config.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_cpu_s3407/status.json": {
    "status": "READ",
    "sha256": "1cf985a92d49a8384f12aeddf390b8e74490cfbc034555816ca488f5ac78b268"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_cpu_s3407/config.json": {
    "status": "READ",
    "sha256": "1bfc83a2981cb690bd60d6fce30952eb6635fb4db6820371268ec9934aa86d00"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_cpu_s3407/metrics.json": {
    "status": "READ",
    "sha256": "6cb0e8a5579ce0185603f14ca20380cf784a966893d434436ade067dc1fcbe08"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_mem_s3407/status.json": {
    "status": "READ",
    "sha256": "d9abce9ee43d9c110d77069dcd27293bf2cdfbb52c7434596eb6ccc03877c540"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_mem_s3407/config.json": {
    "status": "READ",
    "sha256": "aa96a7f8fda9406f8bae65edb19a797814911b74867e668fcc6d0347669a1139"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_mem_s3407/metrics.json": {
    "status": "READ",
    "sha256": "6eab54acfca6b42cf7e76119970ac0f2b96e988544686f138dd2ac8f83195634"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_train_s3407/status.json": {
    "status": "READ",
    "sha256": "393548793778af9c8fe3ceed38044f953843e239039458bd7ed0da0677d3c5aa"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_train_s3407/config.json": {
    "status": "READ",
    "sha256": "4d9232b8ab55b5d23dab0775ed2830517faafa6e1ca978c858c8371eddff886b"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_train_s3407/metrics.json": {
    "status": "READ",
    "sha256": "acfe976fc6728680f330c12423365ab2041c5adebf86be43ddf9c9bbf1070dff"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_train_s3408/status.json": {
    "status": "READ",
    "sha256": "ec6ad9dcb895fcca9412325b5a2cdec6dcde94ce0ce06bc504db06f403e6d60b"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_train_s3408/config.json": {
    "status": "READ",
    "sha256": "161aee787a4c9f444f00f2bc3e46f341fe97868ca5a7e49383eb0449da6c17ee"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_train_s3409/status.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_segformer_b2_train_s3409/config.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_cpu_s3407/status.json": {
    "status": "READ",
    "sha256": "bb0c77f795adb1b38052579d3474a404d489b7f667ca8d2576b396e02645f625"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_cpu_s3407/config.json": {
    "status": "READ",
    "sha256": "8fe5864612a41ea32b65ce071cd018e915b23da304ffcd389887749d51316cb1"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_cpu_s3407/metrics.json": {
    "status": "READ",
    "sha256": "d2ccb3f44677dd47727b0600d96301dad3c064f48759cc356ceeab11078ee879"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_mem_s3407/status.json": {
    "status": "READ",
    "sha256": "963880e4b8f23e7d7bd193bd55abdd98e1f6850bb5aca6c22319ef251f2dd9ff"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_mem_s3407/config.json": {
    "status": "READ",
    "sha256": "d8c177e2f4c6b0533596704747f48577434e2bf6768a774039ef9db89ecc4216"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_mem_s3407/metrics.json": {
    "status": "READ",
    "sha256": "931edd0e18971c82784ffc0c8b14907a8acf25afdbe37682f4a8df620c40cf62"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_train_s3407/status.json": {
    "status": "READ",
    "sha256": "153b1854aedfe1a44334d320ef0cafaab586b184e30fc21e073f30586a6b1e77"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_train_s3407/config.json": {
    "status": "READ",
    "sha256": "fb0f1f41fb91c0f087ebad477d8850c1a5c4426aa4a7145605c367a35a127075"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_train_s3407/metrics.json": {
    "status": "READ",
    "sha256": "a4a095bfd8a50e42adcf52e99bdec2cacfd131b1e447468598816aaffc59cdfb"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_train_s3408/status.json": {
    "status": "READ",
    "sha256": "a0cb5d3e166f854ee03f8ffa53c9bb95cc86569a8f523381b9c96e75bbc0ddcc"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_train_s3408/config.json": {
    "status": "READ",
    "sha256": "401373f9709f469ab1b0a549106446571b8f319194f6f01934b822926df40174"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_train_s3408/metrics.json": {
    "status": "READ",
    "sha256": "09dd9ceb14061470fad1952cda9becb5d3e1a6f5fc2babec706b0617362d92da"
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_train_s3409/status.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/satv1_unet_train_s3409/config.json": {
    "status": "MISSING",
    "sha256": null
  },
  "/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/sat_benchmark_analysis_v1/status.json": {
    "status": "MISSING",
    "sha256": null
  }
}
```

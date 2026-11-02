# BRACOL 普通 RGB 分割能力开发对照

生成时间：2026-10-19T11:57:23.353077+00:00。状态：COMPLETE — descriptive development results。

本报告是新研究的 metadata-only 汇总。只有两个正式作业完整结束、固定末步分析完整并绑定当前协议时，才列出效果数字。CPU 与实际 batch 显存 smoke 仅验证实现和资源，不作为主结果。writer 不运行模型、分析器或额外实验。

科学结果完整与父研究窗口关闭分别记录；两者不能互相替代。

| 父级元数据字段 | 记录 / 限定 |
| --- | --- |
| parent state phase | CLOSED |
| parent state active_gpu_jobs count | 0 |
| parent closeout phase | CLOSED |
| CLOSED state/closeout SHA binding | MATCHED_PARENT_RECORDS_ONLY |
| current live PID / registry verification | NOT_PERFORMED by this writer |
| external study CLOSED state emission | NOT_EMITTED; root must explicitly verify/close |

父状态/closeout 仅作为所读时刻的记录及 SHA 绑定证据。本 writer 不实时检查 PID，不执行 registry 审计、不发停止信号，也不自行生成新研究的 CLOSED state/closeout。现有父 closeout 不包含显式 registry_errors/registered_alive 字段或 closer 源码 SHA，因此由根任务依真实安全闭环再显式关闭新研究。父 state 可嵌入旧科学结果，读取后仅保留窗口关闭字段，不使用其中旧数字。

## 信息来源与实验边界

| 项目 | 冻结信息 / 限定 |
| --- | --- |
| 数据 | BRACOL admitted train=400, val=50; official test sealed |
| 输入 / 标签 | RGB-only 256 letterbox; exact red symptom only; valid is padding, green leaf is negative |
| 共同主干 | EfficientViT-B1, ImageNet initialization; trainable backbone; ordinary train/eval BN |
| 两种头 | ordinary GN FPN vs independently implemented SegFormer-style MLP; different parameter counts |
| 初始化资产 SHA256 | fcd84d10cb51762639cba7e5e3d936fb391777b654ab6e61701f14219d3d4a0f |
| 监督 / 预算 | train only; seed 3407; batch 8; fixed last 2000 updates / 16000 image visits |
| 状态 | COMPLETE — descriptive development results |

准入来源为作者固定 commit 的 BRACOL segmentation 数据；当前协议保留 400 train / 50 val，官方 50 test 的像素与标注封存。原 annotation 不修改。病斑仅精确红色，绿色叶片属于该二元任务的负类；padding validity 不是叶片掩码。人工标注过程及病理专家资质仍为 **UNVERIFIED**，项目没有完成独立专家复核。RGB 候选重复组和已开放旧 train/dev 原图 SHA 筛查不等于完整跨数据集去重或最终数据无重叠证明。

两臂主干结构、ImageNet 初值、训练输入和固定预算相同，主干正常可训，BN 训练更新、评价使用已保存统计。FPN 与 MLP 是不同结构、不同参数量的普通解码器；MLP 借用 SegFormer 的逐阶段线性映射、对齐及拼接定义，使用 GN、不同主干和二元标签，**不是官方 SegFormer 复现**。这里检验普通独立 RGB 学习能力，不构成新方法、路由方法或局部纠错机制创新。

## 正式作业与固定末步结果

| 臂 | 实际状态 | 实际 stage | step | formal directory |
| --- | --- | --- | --- | --- |
| FPN | COMPLETE | GPU_SCREENING | 2000 | experiments/exrgb_fpn_s3407_v1 |
| MLP | COMPLETE | GPU_SCREENING | 2000 | experiments/exrgb_mlp_s3407_v1 |

仅评价 fixed last 2000，训练损失为 pooled-valid BCE 加逐图 soft Dice loss（smooth=1，包含空病斑图）。无增强、阈值扫描、BN 扫描、预算扫描或中途 best 选优。所有数字的空间为 **256 letterbox 有效像素**，不等同于原图分辨率性能。source-small 使用原标注病斑像素 / 原图总像素，定义为 0 < 比例 < 1%；重采样后的分割分母仍为 256 网格。

| 臂 | split | n | IoU % | Dice % | NLL | soft Dice loss | total loss | source-small n | source-small IoU % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FPN | train | 400 | 89.1252 | 94.2500 | 0.0056 | 0.0489 | 0.0545 | 132 | 91.4231 |
| FPN | val | 50 | 77.4112 | 87.2675 | 0.0175 | 0.1037 | 0.1212 | 17 | 78.4097 |
| MLP | train | 400 | 88.4070 | 93.8469 | 0.0059 | 0.0515 | 0.0575 | 132 | 90.8256 |
| MLP | val | 50 | 79.3858 | 88.5085 | 0.0147 | 0.0890 | 0.1037 | 17 | 83.6853 |

| 臂 | split | TP | FP | FN | TN |
| --- | --- | --- | --- | --- | --- |
| FPN | train | 155438 | 8833 | 10133 | 12932796 |
| FPN | val | 17666 | 1901 | 3254 | 1615579 |
| MLP | train | 154875 | 9613 | 10696 | 12932016 |
| MLP | val | 18173 | 1972 | 2747 | 1615508 |

TP/FP/FN/TN 是单输出混淆计数，不是模型之间四向纠错或因果能力分解。权威二元预测为 raw logit > 0；零是背景，不用 rounded sigmoid 重新替换记录。

## 配对开发集比较

| split | 支持 | 状态 | n | groups | MLP−FPN IoU pp | paired 95% CI pp |
| --- | --- | --- | --- | --- | --- | --- |
| val | all | COMPLETE | 50 | 50 | 1.9747 | [0.3446, 4.4074] |
| val | source_small | COMPLETE | 17 | 17 | 5.2756 | [-0.5988, 15.9403] |
| train | all | COMPLETE | 400 | 399 | -0.7182 | [-0.8701, -0.5671] |
| train | source_small | COMPLETE | 132 | 132 | -0.5975 | [-0.8397, -0.3361] |

主要比较为 val MLP−FPN 的 micro foreground IoU。区间来自已有 RGB 候选组整体重采样的 2000 次 paired bootstrap，seed=3407，名义 95%。source-small 只作描述性分层；支持不足保持 NOT_ESTIMABLE。train 与 val 均为此轮已使用数据，50 val 是开发集，**不叫独立最终测试**。不把这里的数值与 PlantSeg 的不同任务、分辨率、标注和划分直接排榜；不从两个解码器的差异推导普适机制或自动批准后续训练。

分析器记录的限定：

- 400/50 admitted BRACOL development, not independent final; official test unopened
- Mask expert/manual provenance UNVERIFIED; RGB similarity grouping does not prove biological or cross-dataset independence
- 256 letterbox mask metrics, not original-resolution lesion IoU; source-small may vanish after resize
- One seed/fixed2000 and different heads/parameter counts; a negative training result alone does not identify cause or prove convergence
- Train readout uses final weights and saved-statistics eval mode; not the historical train-mode optimization loss
- No PlantSeg comparisons or old result/label reads; no imported author task weights
- Tensor/prediction hashes inherited from run metadata; no arrays/models/checkpoints independently verified here
- Payload wall includes setup/evaluation; download/intake and unknown upstream ImageNet resources are additional; not inference speed

## 资源与未测量项目


本轮的阶段判断是：普通、可训练的独立 RGB 模型在这份 BRACOL 开发协议上表现出分割能力，MLP 相对 FPN 的主要开发集差值区间为正；这只支持把它保留为后续能力对照。小病斑 17 图的 IoU 差值区间跨零，不宣称稳定小病斑优势。两臂训练集表现均高于开发集，仍有泛化差距。数据、整图输入和监督方式同时不同于先前 PlantSeg 局部纠错实验，因此不能把这次结果归因为某一个信息、上下文或归一化因素。


下一步应在原任务允许的 TRAIN/DEV 上冻结一个同数据、同初始化、同总监督与像素预算的整图／局部输入对照，并结合现有标注语义审查。该后续仅为待设计计划，未实现、未运行，本轮没有自动追加训练。当前没有新的独立方法贡献或投稿等级结论。

| 臂 | 参数 | body | head | train s | eval s | payload s | peak reserved MiB | GPU UUID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FPN | 4698977 | 4643936 | 55041 | 121.07 | 7.17 | 296.18 | 934.00 | GPU-57623a5e-e947-5d18-57c4-b58d99777bb3 |
| MLP | 4691489 | 4643936 | 47553 | 114.80 | 6.96 | 290.14 | 946.00 | GPU-ff32649a-a567-d2ad-c4aa-beff253050be |

参数量分别记录 body/head，两个 task head 不要求同参数或同初值。train/eval 时间是 trainer 对代码区间的记录，payload 时间包括 setup、评价和 I/O；均不是隔离、同步认证的单图推理延迟。ImageNet 外部预训练成本为 **UNKNOWN**，不能视为免费或与随机训练预算相等。FLOPs、隔离部署延迟、吞吐和能耗为 **UNMEASURED**。一随机种子、有限 2000 更新的 screen 不证明充分收敛，也不自动构成发表级证据。

## 本次读取的元数据与来源 SHA256

可追溯的先行方法与来源：[SegFormer 论文与作者实现](https://github.com/NVlabs/SegFormer)、[HRDA 作者实现](https://github.com/lhoyer/HRDA)、[PointRend 作者实现](https://github.com/facebookresearch/detectron2/tree/main/projects/PointRend)、[BRACOL 作者固定版本](https://github.com/esgario/lara2018/tree/a6c38b693094c2c4da4b82029fc8be7058506a16/segmentation)、[PSNC 数据记录](https://zenodo.org/records/14707857)。实际固定 commit、许可、依赖与差异见 `literature/external_sources_20261019/`；上游代码只作静态参考，未执行或导入。PSNC 的当前四对样本因灰度掩码编码尚未确认而暂缓准入，未阈值化或训练。

- `/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/configs/external_rgb_v1.json` — dec2b448dbb9cbbd85a8fd08c367a8b7923458b7bf29db6dbfee93dcaa570f95
- `/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/exrgb_fpn_s3407_v1/config.json` — b303596b4db902e59174bdac5aa6cd5b0250f5730d7d6de2f4077527af592f67
- `/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/exrgb_fpn_s3407_v1/status.json` — 4a34276748f30a956bfb8d7060aafd118b56ae15fa3968f2a41f8c701c99ace1
- `/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/exrgb_mlp_s3407_v1/config.json` — c4540857f1eb9c842b86ef3ad33717e2904a573e48963b5b58779ca82d87fe36
- `/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/exrgb_mlp_s3407_v1/status.json` — ada53917c3e9dbc668b37906444421884cd1ce33b81d6240f6bc00affa4bd0b2
- `/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/external_rgb_pair_analysis_v1/analysis.json` — 1117405c356062a5ff9856f86c0eeb7f039f2ddf8252721aab1bdc6571118bfa
- `/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/experiments/learning_path_v1_state.json` — b73921aafd77f51d27028b8807b2e0116deb8d47ed3576c713b8f418f95cb86e
- `/home/sdd_wangtao/ZhaoHaonan/leaf_research_top/audits/learning_path_v1_closeout.json` — a2e96970c28fd06943cd75b42f4d49118d260fd16673633d82335d576ea62d14
- writer SHA256: `fb1970711fd3e3a1588a65699d472d046f611eedf8d88b4010120d511a1d1caa`
- BASE SHA256: `2f183d9b81eed3cd1efe6cf287126a3e7789b49dfbb9c4af8d1c163e70d0fe26`

本 writer 不打开 dataset manifest、图像、mask、NPZ、检查点、旧研究结果、cal/final 或任何封存 test 数据。缺失或未完成结果保留未测量；不会调用 analyzer 或创建实验队列。

# 复现说明

这个目录同时保存原始实验工件与新的手工复现入口。原始 source、参数、数据数组、模型权重、训练/求解结果和失败记录用于核对论文证据；新入口用于在新输出目录重现当前主线的 FIT/TRAIN 实验。

所有示例保留本机绝对路径。先阅读根目录 README、`00_paper_story/` 和 `12_evidence_reconciliation_v1/`，再按本页执行。

## 1. 工作流与范围

| 工作 | 入口 | 是否训练 |
|---|---|---|
| 校验封存包与输入 | `tools/verify_package.py`、`RUN_REPRODUCTION.ps1 check` | 否 |
| 合成数值合同 | `RUN_REPRODUCTION.ps1 contracts` | 小型合成CPU单步，不读取真实数据 |
| 缓存特征A系列 | `RUN_REPRODUCTION.ps1 cached` / `cached-suite` | 只训练头 |
| 两批同特征认证凸读出 | `RUN_REPRODUCTION.ps1 convex` | 固定特征GPU F64凸求解 |
| 等头族 Raw/Log × frozen/joint | `RUN_REPRODUCTION.ps1 equal-head --recipe baseline` | 固定20 epoch |
| Log joint头LR×5＋100步warmup | `RUN_REPRODUCTION.ps1 equal-head --recipe A4` | 固定20 epoch |
| 五source-seed20格交叉读出 | `tools/reproduce_cross_readout.py`，见[专门说明](CROSS_READOUT_REPRODUCTION.md) | 冻结缓存上的CPU凸重求解；完成后重复评价原已见HELD |

新运行属于“手工复现”，不会替换为原预注册证据，也不自动构成独立确认。入口复用原冻结科学函数，新协议、输入SHA、日志、结果写入新目录，不延长旧窗口、不调用旧 controller。`run_reproduction.py`的训练入口只评价FIT；独立的交叉读出入口为复现历史20格，求解后会重复评价原已见HELD，不能作为独立泛化。

## 2. 环境与合成合同

```powershell
cd F:\Plant_SPD
.\RUN_REPRODUCTION.ps1 check
.\RUN_REPRODUCTION.ps1 contracts --output-root D:\PlantSPD_reproductions\synthetic_v1
```

`check` 核对核心source、特征缓存、FIT标签/索引的编码字节SHA与现有numpy/torch/scipy/threadpoolctl导入，不打开标签数组。`contracts` 只使用随机CPU张量检查双视图损失、AdamW更新、裁剪、温度等价、调度积分、翻转映射、凸求解解析梯度，并比较冻结等头族 `instrumented_step` 与手写同配方单步。

依赖与本机路径见 [ENVIRONMENTS.md](../01_protocols_and_data/ENVIRONMENTS.md)。直接Python命令等价：

```powershell
$Py = 'C:\Users\lenovo\AppData\Local\Programs\Python\Python311\python.exe'
& $Py -B F:\Plant_SPD\tools\run_reproduction.py check
```

## 3. 最快复现A系列

先跑默认冻结Raw臂A0：

```powershell
.\RUN_REPRODUCTION.ps1 cached --arm A0 --seed 3407 --device cuda:0 --output-root D:\PlantSPD_reproductions\A0_s3407
```

串行执行五项初始干预及A2两个追加种子：

```powershell
.\RUN_REPRODUCTION.ps1 cached-suite --device cuda:0 --output-root D:\PlantSPD_reproductions\cached_A_suite_v1
```

顺序为 `A0、A、A2、A2prime、A3`（seed3407），再运行 `A2`（seed3408、3409）。也可分开：

```powershell
.\RUN_REPRODUCTION.ps1 cached --arm A2 --seed 3408 --output-root D:\PlantSPD_reproductions\A2_s3408
.\RUN_REPRODUCTION.ps1 cached --arm A2prime --seed 3407 --output-root D:\PlantSPD_reproductions\A2prime_s3407
.\RUN_REPRODUCTION.ps1 cached --arm A3 --seed 3407 --output-root D:\PlantSPD_reproductions\A3_s3407
```

| 臂 | 固定设置 | 原记录TRAIN Macro-F1 |
|---|---|---:|
| A0 | LR .001，WD .0001，20 epoch | 24.18% |
| A | 仅头WD改0 | 24.18% |
| A2 | 头LR .01，20 epoch | 三种子87.80% ± 0.24pp |
| A2prime | LR .001，60 epoch，cosine同步拉伸至60 | 53.47% |
| A3 | 默认头配方＋可学逆温度，温度参数WD=0 | 76.67% |

共同设置：初始Raw特征缓存 `[8368,2,528]`，含4184张FIT的真实未翻转/翻转RGB状态；双视图独立仿射W/b共73,002参数、零初始化、F64；batch32；损失 `CE(mean logits)+0.25*(CE(view0)+CE(view1))`；AdamW β=(.9,.999)、eps=1e−8；合并头组裁剪 `5/sqrt(2)`。每完整epoch131步。A2prime按原协议重复同一20轮样本流三次，cosine T_max=60，不在20轮后保持零LR。

默认每臂外层610秒。CPU可显式选择 `--device cpu --timeout-sec 3600`，属于不同计算后端。本机历史用时为单臂约1分钟、60轮约3分钟、七臂约10分钟，作为参考。

## 4. 两批同特征认证凸读出

```powershell
.\RUN_REPRODUCTION.ps1 convex --features raw-frozen --output-root D:\PlantSPD_reproductions\certificate_raw_v1
.\RUN_REPRODUCTION.ps1 convex --features log-joint --output-root D:\PlantSPD_reproductions\certificate_log_v1
```

`raw-frozen` 为初始Raw冻结特征；`log-joint` 为旧低拟合Log joint seed3407最终编码器FIT特征。两者是F11本轮两个证书，与E08历史证书分代。

直接调用冻结 `F2_gpu_convex_demand_v1.py` 的 `run` 及解析目标/梯度：全W+b显式L2 `lambda=1.1659571544277561e−8`，SciPy L-BFGS-B、GPU F64，完整梯度证书 `||grad J||²/(2lambda) <= 1e−4`。终止依据是数值证书，不是F1或SciPy success。原两批均TRAIN100%；不代表泛化100%，显式L2不等于AdamW WD。

科学输出有 `COEFFICIENTS_AND_GRADIENT.npz`、`ITERATIONS.jsonl`、`RESULT.json`、`MANIFEST.json`。本机原用时约48/91秒。固定外层610秒，内层600秒及15秒收尾余量不改。

## 5. 从RGB复现等头族与A4

默认矩阵为 `Raw/Log × frozen/joint × 五种子`。固定20完整epoch、共同ImageNet初态、固定FIT统计量、对应种子样本/翻转流：

```powershell
.\RUN_REPRODUCTION.ps1 equal-head --mapping raw --encoder-mode frozen --seed 3407 --recipe baseline --output-root D:\PlantSPD_reproductions\equal_raw_frozen_s3407
.\RUN_REPRODUCTION.ps1 equal-head --mapping raw --encoder-mode joint --seed 3407 --recipe baseline --output-root D:\PlantSPD_reproductions\equal_raw_joint_s3407
.\RUN_REPRODUCTION.ps1 equal-head --mapping log --encoder-mode frozen --seed 3407 --recipe baseline --output-root D:\PlantSPD_reproductions\equal_log_frozen_s3407
.\RUN_REPRODUCTION.ps1 equal-head --mapping log --encoder-mode joint --seed 3407 --recipe baseline --output-root D:\PlantSPD_reproductions\equal_log_joint_s3407
```

seed可选3407–3411。默认头LR=.001，联合时编码器LR=.0001，WD=.0001；两组分别裁剪 `5/sqrt(2)`，epoch cosine T_max20；BN运行统计始终冻结，联合时编码器参数可训练。scaler来自共同初始编码器，仅FIT两个真实翻转状态的固定均值与标量能量，不重新拟合。

已记录的A4 Log joint：

```powershell
.\RUN_REPRODUCTION.ps1 equal-head --mapping log --encoder-mode joint --seed 3407 --recipe A4 --output-root D:\PlantSPD_reproductions\A4_log_joint_s3407
```

A4仅开放原已执行Log/joint/3407：头基准LR=.005＋100步线性warmup，其余科学设置不改；这是两个共变因素。原同种子TRAIN Macro-F1 36.05%→89.19%，不拿89.19%直接减五种子均值34.12%。端到端默认外层2700秒，F64头、F32编码器，无AMP/TF32。入口不读取HELD标签、不做HELD前向，因此不重算原20格HELD泛化指标。

整张TRAIN20格的显式串行循环：

```powershell
foreach ($Seed in 3407,3408,3409,3410,3411) {
    foreach ($Mapping in 'raw','log') {
        foreach ($Mode in 'frozen','joint') {
            .\RUN_REPRODUCTION.ps1 equal-head --mapping $Mapping --encoder-mode $Mode --seed $Seed --recipe baseline --output-root "D:\PlantSPD_reproductions\matrix20_v1\s${Seed}_${Mapping}_${Mode}"
            if ($LASTEXITCODE -ne 0) { throw 'A cell failed; inspect its preserved logs.' }
        }
    }
}
```

## 6. 输入、产物和实时进度

本机运行无需另外下载：

- E01 `input/rgb_views_uint8.npy` 为固定双视图RGB；`prepared/` 为原分组划分及样本流；`assets/` 为ResNet18实现和官方ImageNet权重。
- F10为等头族实现、共同FIT统计量和初始Raw头输入缓存。
- F11 `inputs/` 为FIT标签、索引、真实翻转行映射、3407–3409样本流；端到端五种子流从E01 `STREAMS.npz` 明确成员读取。
- F11还含Log末期FIT输入、证书、A终点和本轮前瞻轨迹。原历史完整轨迹缺失仍为unavailable，不用新运行冒充历史。

每个新目录有事前 `PROTOCOL.json`、`LAUNCH.json`、`stdout.log`、`stderr.log`、`EXECUTION.json`；科学输出在 `result/`。`RESULT.json` 记录TRAIN指标、原参考路径、SHA、F1差。按固定最终epoch报告，不挑最好分数。实时查看：

```powershell
Get-Content D:\PlantSPD_reproductions\A4_log_joint_s3407\stdout.log -Tail 10 -Wait
```

训练输出必须在 `F:\Plant_SPD` 外且目录未存在，避免覆盖封存结果。失败目录与日志保留。原实验全过程的source、预注册、合同、失败和结果也完整保留在对应代次目录；新入口负责当前论文主线的FIT训练与认证读出，不隐式重跑历史HELD分析。

## 7. 本次整理的验证范围

计划验收包括依赖/字节检查、CLI解析、小型合成CPU合同和plan-only。独立审查时有一次调用路径测试拦截失效，意外触发一格真实交叉读出及原已见HELD评价；该运行已退出，产物单独登记为执行偏差，不计论文证据、不计复现成功，没有改写原实验档案。本次没有重新训练编码器，也没有重跑完整科学矩阵。详见[交付验收记录](teacher_delivery_update_v1/)。

新入口复用原冻结模型、损失、优化器、裁剪、样本流及评估函数，记录新来源与结果；“合成合同通过”不等于“整套真实复现已经再次完成”。验收以更新后的交付QA与SHA清单为准。

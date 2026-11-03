# 本机环境与入口

本交付保留本机路径、历史协议和原始依赖记录。运行入口为项目根目录 `RUN_REPRODUCTION.ps1`，或 `tools/run_reproduction.py`。入口使用下列已存在的 Python 和包目录，不安装或修改环境。

| 用途 | 本机路径 / 版本 |
|---|---|
| Python 主程序 | `C:\Users\lenovo\AppData\Local\Programs\Python\Python311\python.exe`，Python 3.11 |
| GPU 数值包 | `D:\PlantSPD_work\paired_seed_training_v1_20261025_recovery1\gpu_env\Lib\site-packages` |
| CPU 求解依赖补充 | `D:\PlantSPD_work\linear_probe_cross_v1_20261025\cpu_env\Lib\site-packages` |
| 数值版本 | torch `2.11.0+cu128`；numpy `2.4.6`；scipy `1.17.1`；threadpoolctl `3.6.0` |
| 原 GPU | NVIDIA GeForce RTX 5060 Laptop GPU，CUDA 12.8 构建 |
| 绘图 | matplotlib `3.10.7`；独立绘图环境 `C:\Users\lenovo\Documents\PlantSPD_plot_env_v1_20261026` |

等头族原配方控制线程数为4；A系列缓存训练、A4与认证凸求解控制线程数为2。手工复现入口分别保留这些设置。模型自带 ResNet18 实现及官方 ImageNet 权重已在 E01 的 `assets/` 中，无需把 torchvision 当作隐含依赖。输入是包内固定的 uint8 RGB 双视图数组，训练入口不重新下载图像，也不重新划分数据。

依赖锁定表为 [requirements_reproduce.txt](requirements_reproduce.txt)。它记录科学内核所用版本；现有本机环境已经可用。只重建论文表格的代码使用 Python 标准库；绘图额外使用 matplotlib/numpy，见 [requirements_paper.txt](requirements_paper.txt)。

## 先做检查

```powershell
cd F:\Plant_SPD
.\RUN_REPRODUCTION.ps1 check
```

检查输出实际解释器、模块路径、版本与核心工件 SHA，不读取真实标签数组，不训练模型。合成合同另见 [复现说明](../07_reproducibility/REPRODUCIBILITY.md)。

历史 source 内仍保留原来的绝对路径、窗口、PID登记与SHA。论文历史证据以对应 `COMPLETED/RESULT/manifest` 为准；新复现入口写入独立输出目录，不重启旧 controller，也不覆盖历史证据。

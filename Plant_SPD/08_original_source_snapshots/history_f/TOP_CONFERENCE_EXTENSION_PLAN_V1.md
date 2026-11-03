# 顶会扩展路线规划 v1

状态：`PLANNED_NOT_IMPLEMENTED`

## 文献核对后的判断

GBWBN 确实把 SPD 度量参数做成可学习对象，并在 Bures-Wasserstein 几何下处理病态协方差；它的实验主要在动作和 EEG 信号上，因此可以作为“可学习 SPD 度量”的方法锚点，不能直接当作植物病害验证。[CVPR 2025 GBWBN](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_Learning_to_Normalize_on_the_SPD_Manifold_under_Bures-Wasserstein_Geometry_CVPR_2025_paper.html)

SPD-OT 已经被用于 SPD 流形上的跨域分布对齐，相关实验主要是跨会话脑机接口数据。它更适合支撑“跨来源/跨设备分布对齐”方向，而不是直接支撑当前的全局—局部病害融合。[Deep optimal transport on SPD manifolds](https://www.sciencedirect.com/science/article/pii/S0004370225000669)

Stackelberg-Riemannian 论文研究的是一般在线多智能体博弈，通过流形映射求解领导者—跟随者决策；它不是 SPD 协方差分类论文。直接把它包装成“SPD度量学习的 Stackelberg 理论”会留下很大的理论和实现缺口。[AAAI 2026 Stackelberg manifold](https://ojs.aaai.org/index.php/AAAI/article/view/39552)

Fisher-Rao 敏感性已经被用于 OOD 检测和不确定性解释，适合作为训练完成后的可靠性分析，不适合作为当前主网络的第四个模块。[ICLR 2026 Fisher-Rao sensitivity](https://proceedings.iclr.cc/paper_files/paper/2026/hash/029df12a9363313c3e41047844ecad94-Abstract-Conference.html)

## 主扩展：可学习 SPD 度量

只有在 S0 相对 E0 的三 seed 几何确认通过后，才进入本扩展。方法只增加一个核心变量：SPD 度量参数。

### 固定基线

- E0：欧氏协方差向量；
- S0：固定 Log-Euclidean；
- S-Metric：可学习 SPD 变换/度量；
- 可选 Bures-Wasserstein control：只有实现和预算允许时加入。

### 受控形式

对协方差 (C) 使用可学习的 SPD 变换 (M)：

\[
\tilde C=M^{1/2}CM^{1/2}
\]

再在 \\(\tilde C\\) 上计算 Log-Euclidean 距离或 Bures-Wasserstein 距离。(M) 需要使用 Cholesky 参数化，并加入 trace/determinant 归一化，防止模型通过整体放大距离获得虚假收益。

训练目标只保留：

```text
分类损失 + 类内几何紧致损失 + 类间几何间隔损失 + 度量正则
```

不要同时加入 OT、Fisher-Rao、Shapley 和反事实调度。

### 博弈论的正确位置

第一版不直接声称 Stackelberg 均衡。可以把它实现为受控的双层优化：

- follower：在当前度量下更新类别原型和分类头；
- leader：根据训练内交叉拟合的类间隔和跨来源稳定性更新 (M)；
- validation 只用于一次冻结选择，不能参与每步度量更新。

只有在能给出明确的 leader/follower 目标、更新顺序、收敛条件和反事实控制时，才考虑使用 Stackelberg 叙事。

## 实验顺序

1. 先完成 E0/S0 三 seed 几何确认；
2. 固定最优输入、OOF 掩码和训练预算；
3. 运行 fixed Log-Euclidean 与 learnable metric 的三 seed 对照；
4. 按 host、disease、病斑面积、来源簇做 paired bootstrap；
5. 测试跨来源稳定性、ECE/NLL、参数量和延迟；
6. 只有可学习度量有稳定收益时，才写博弈论解释；
7. OT 作为另一条独立后备实验，不与可学习度量同时加入。

## OT 后备路线

如果 S0 的收益主要出现在不同 host/source 分布之间，才考虑 SPD-OT。OT 的输入应是每个来源簇的 SPD 描述子分布，输出是跨来源对齐后的分类或融合结果。必须比较：

- 无对齐的 S0；
- 欧氏 OT；
- SPD-OT；
- 简单域归一化。

OT 不能只在同一随机验证集上做，因为它的科学问题是域偏移。

## 明确放弃的路线

- 不把 Stackelberg、OT、Fisher-Rao、Shapley 同时加入；
- 不把 Fisher-Rao 变成新的训练损失；
- 不加入热带几何分类头；
- 不在 SPD 三 seed 确认前扩展理论；
- 不把概念组合写成顶会创新。

## 顶会级贡献的最低条件

至少需要同时满足：

1. S0 的几何主效应在三 seed 上稳定；
2. 可学习度量相对固定 Log-Euclidean 有独立、可复现的收益；
3. 收益在 host/source 跨域和小病斑分层中仍存在；
4. 与 Euclidean、固定 Log-Euclidean、Bures-Wasserstein 或 SPD-OT 有公平对照；
5. 训练和测试不使用 GT 路由；
6. 有理论目标、数值稳定性和真实效率分析。

在这些条件满足前，论文应使用“learnable SPD metric”而不是“Stackelberg-Riemannian cooperative game”。


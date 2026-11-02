# K 阶梯协议缺口审计（只读）

**审计时间：** 2026-11-02

**结论：** 当前注册已经冻结了目标 K、两种标签构造、输出指标和方向预测，但没有冻结一个可执行的 K>2 runner，也没有冻结 (d_k^2) 的生成口径。因此本审计不启动阶梯，不把 K=2 读出代码外推为已注册的 K>2 实验。

## 已找到的持证内容

1. 注册文件冻结 `K={2,4,8,16,34,69}`、contiguous 主规则、support-balanced 备选规则、绝对 TRAIN F1、饱和标记、`CV(d²)`、加权 `S_beta` 以及方向预测。
2. `mechanism_zero_cost.py` 已实现并运行 K=69→2 的四种二分类标签构造：`merge_contiguous_half`、`merge_balanced_support`、`random_pair`、`one_vs_rest`。这是固定 K=69 特征上的二分类读出证据。
3. `readouts.py::fit_affine` 的实现固定为 `n_classes=2`，它不能直接执行 K=4/8/16/34/69 的阶梯。
4. 已有 K=69 初始冻结特征认证读出，Raw/Log TRAIN F1 均为 100%，但该证书不是阶梯 runner，也没有定义 K>2 的新原型集合。

## 缺失的协议字段

以下任一项未冻结，都不能把结果登记为 confirmatory：

- 每个目标 K 的原型/中心 (P_k) 如何由缓存特征生成；
- (d_k^2) 是 SPD/Frobenius 距离、svec 欧氏距离、类均值距离，还是原型头的 native 距离；
- Raw/Log 两个映射是否分别生成原型，还是共享同一原型后只改变特征映射；
- (eta=1/(uT)) 的来源、单位、按样本/按视图/按全局的聚合方式；
- (S_\beta=E_z\operatorname{Var}_{p_\beta}(d_k^2)) 的样本权重、视图处理和饱和处理；
- K=4/8/16/34 的 contiguous 分箱边界和 support-balanced 的确定性 tie-break 细节；
- affine readout 的类别数、正则、初始化、solver gap 阈值和绝对水平口径。

## 可执行结论

- K=2 的已运行结果可以继续作为 K=2 读出证据；
- K=69 的双侧认证可以继续作为 ceiling-censored 参照；
- K=4/8/16/34 的阶梯目前只能标记为 `REGISTERED_NOT_RUN / RUNNER_UNDEFINED`；
- 在协议负责人冻结上述字段之前，不创建临时 runner，不选择事后更有利的 (d_k^2) 定义，也不修改已有预测。

## 关联工件与 SHA256

- 注册：[MECHANISM_READOUT_STAIRCASE_REGISTRATION.json](../results/MECHANISM_READOUT_STAIRCASE_REGISTRATION.json)，`A7ED430F4F0C6C1F00779F2F4E71C03FC3D1847BDDC651534CA9E8ADF66BFEF1`。
- K=2 读出实现：[mechanism_zero_cost.py](../source/mechanism_zero_cost.py)，`0B44836E264AC56D1645E41BB88706441073EE283A2491AC8A98DA95D527B815`。
- affine solver：[readouts.py](../source/readouts.py)，`2266F2A65318D5E70233A7E4172E92633FB6378548D4DC60482556B7498F1576`。

本文件只记录协议缺口，不改动注册预测、不产生实验结果。

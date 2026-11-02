# SPD估计阶段A：无梯度合成验证

全部使用本地CPU/NumPy和已知真值合成数据，无病害图像、无模型前向或训练。

固定5种估计器、3种总体结构、3个样本量、2种行相关性、每类512次重复；含2个已知类别。

ANS为Ledoit–Wolf2020已发表算法，本轮验证其作为后续机制基线的适用性，不将其称为原创。

## 主检验：旋转spiked谱，独立样本，N=32

| 对照 | ANS相对log误差降低 | 多重比较调整区间 | ANS准确率变化 |
|---|---:|---|---:|
| fixed_005 | +37.45% | [+37.10%,+37.81%] | +0.00pp |
| ledoit_wolf | +9.82% | [+9.34%,+10.25%] | +0.00pp |
| oas_original | +9.22% | [+8.76%,+9.69%] | +0.00pp |

## 全场景均值

| 场景 | empirical | fixed.05 | LW | OAS | ANS |
|---|---:|---:|---:|---:|---:|
| isotropic_rho0.0_n256 | 1.0608 | 1.0036 | 0.1016 | 0.1023 | 0.2740 |
| isotropic_rho0.0_n64 | 2.3378 | 2.1726 | 0.2059 | 0.1976 | 0.5681 |
| isotropic_rho0.0_n32 | 3.8682 | 3.4435 | 0.3038 | 0.2721 | 0.9556 |
| isotropic_rho0.7_n256 | 1.8300 | 1.7213 | 1.1444 | 1.1365 | 1.2462 |
| isotropic_rho0.7_n64 | 3.9605 | 3.6057 | 2.1718 | 2.0844 | 2.4200 |
| isotropic_rho0.7_n32 | 6.0810 | 5.2391 | 2.8486 | 2.6239 | 3.2499 |
| rotated_spiked_rho0.0_n256 | 1.0122 | 0.9197 | 0.9380 | 0.9387 | 0.6564 |
| rotated_spiked_rho0.0_n64 | 2.2433 | 1.9040 | 1.6463 | 1.6440 | 1.2976 |
| rotated_spiked_rho0.0_n32 | 3.7121 | 2.9287 | 2.0313 | 2.0179 | 1.8319 |
| rotated_spiked_rho0.7_n256 | 1.7486 | 1.5133 | 1.5875 | 1.5874 | 1.3931 |
| rotated_spiked_rho0.7_n64 | 3.8053 | 3.0865 | 2.6030 | 2.5583 | 2.6299 |
| rotated_spiked_rho0.7_n32 | 5.9215 | 4.4244 | 3.0021 | 2.8494 | 3.4669 |
| toeplitz_channels_rho0.0_n256 | 0.9891 | 0.9473 | 0.9342 | 0.9334 | 0.9180 |
| toeplitz_channels_rho0.0_n64 | 2.1885 | 1.8124 | 1.7887 | 1.7886 | 1.7321 |
| toeplitz_channels_rho0.0_n32 | 3.6460 | 2.7430 | 2.4222 | 2.4386 | 2.3634 |
| toeplitz_channels_rho0.7_n256 | 1.7085 | 1.4630 | 1.4933 | 1.4927 | 1.5327 |
| toeplitz_channels_rho0.7_n64 | 3.7424 | 2.9051 | 2.4274 | 2.4002 | 2.7845 |
| toeplitz_channels_rho0.7_n32 | 5.8161 | 4.1410 | 2.9054 | 2.8323 | 3.5866 |

上表为矩阵对数误差Frobenius范数，越低越好；条件数降低不能替代此终点或分类判别。

## 准入决定

```json
{
  "all_numerical_checks": true,
  "primary_beats_all_strong_controls": true,
  "native_n256_noninferiority": true,
  "known_structure_preserved": true,
  "admitted": true,
  "decision": "ADMIT_SEPARATELY_FROZEN_TRAIN_ONLY_STAGE_B"
}
```

N=256对应原管线名义空间样本量；N=32/64是受控稀疏压力，不等价于天然小病斑。
rho=.7属于理论假设失配场景；正交去均值不会恢复行独立。重复数是Monte Carlo试验，不是病害图像数。
本次没有提出新谱估计器；一次ANS通过或失败都不能直接证明RMT普遍有效或无效。
失败则不扩展阶段B、不重启旧RMT训练、不扫描新带宽；通过也先单独冻结TRAIN特征诊断。

运行时间：13.024秒；总估计数：92160。

公式来源：作者官方analytical_shrinkage.m、Chen等原OAS Eq23（保留2/p）。
作者代码：https://www.econ.uzh.ch/en/people/faculty/wolf/publications.html
原OAS论文：https://arxiv.org/abs/0907.4698

复现入口为run_spd_estimation_stage_a_v1.py。已有运行禁止覆盖；protocol绑定源码与参考文件SHA。

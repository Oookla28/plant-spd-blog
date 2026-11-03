# E01 探索性原始病灶面积分组

固定K=2 Macro-F1，另列GT-present balanced accuracy；缺失类F1记0，空分组完全不可用。

| 分组/范围 | p0/p1图数（类别数） | 已有配对 | Raw F1 | Log F1 | Log−Raw F1 | BA-present差 |
|---|---|---:|---:|---:|---:|---:|
| small_native_0to1pct / 0 | 0（0类）/0（0类） | 5 | UNAVAILABLE_NO_IMAGES | UNAVAILABLE_NO_IMAGES | UNAVAILABLE_NO_IMAGES | UNAVAILABLE_NO_IMAGES |
| small_native_0to1pct / 1 | 0（0类）/0（0类） | 5 | UNAVAILABLE_NO_IMAGES | UNAVAILABLE_NO_IMAGES | UNAVAILABLE_NO_IMAGES | UNAVAILABLE_NO_IMAGES |
| small_native_0to1pct / both_descriptive | 0（0类）/0（0类） | 10 | UNAVAILABLE_NO_IMAGES | UNAVAILABLE_NO_IMAGES | UNAVAILABLE_NO_IMAGES | UNAVAILABLE_NO_IMAGES |
| medium_native_1to5pct / 0 | 11（2类）/11（2类） | 5 | 47.62% ± 0.00pp | 47.62% ± 0.00pp | +0.00pp | +0.00pp |
| medium_native_1to5pct / 1 | 11（2类）/11（2类） | 5 | 47.62% ± 0.00pp | 47.62% ± 0.00pp | +0.00pp | +0.00pp |
| medium_native_1to5pct / both_descriptive | 11（2类）/11（2类） | 10 | 47.62% ± 0.00pp | 47.62% ± 0.00pp | +0.00pp | +0.00pp |
| large_native_over5pct / 0 | 115（2类）/115（2类） | 5 | 68.14% ± 6.42pp | 69.55% ± 2.09pp | +1.41pp | +0.35pp |
| large_native_over5pct / 1 | 115（2类）/115（2类） | 5 | 56.20% ± 4.47pp | 56.60% ± 3.42pp | +0.40pp | +0.55pp |
| large_native_over5pct / both_descriptive | 115（2类）/115（2类） | 10 | 62.17% ± 8.17pp | 63.07% ± 7.33pp | +0.90pp | +0.45pp |

类别召回（所有HELD，按已配对端点均值）：

| 类别 | Raw recall | Log recall | Log−Raw |
|---|---:|---:|---:|
| benign | 93.96% ± 2.78pp | 97.03% ± 1.14pp | +3.07pp |
| malignant | 27.20% ± 11.75pp | 24.80% ± 9.94pp | -2.40pp |

- Original native mask area metadata defines posthoc slices; masks never enter classification inputs.
- Fixed-K2 Macro-F1 assigns absent classes zero; present-class balanced accuracy averages recall only over supported GT classes and is a different quantity.
- Empty subgroups have unavailable metrics, never zero or fabricated F1.
- Ten paired seed/partition endpoints reuse images; group support is not multiplied by seeds and overlapping partitions are descriptive.
- No predeclared subgroup interaction test or multiplicity-adjusted inference; this cannot establish a general tiny-lesion benefit.

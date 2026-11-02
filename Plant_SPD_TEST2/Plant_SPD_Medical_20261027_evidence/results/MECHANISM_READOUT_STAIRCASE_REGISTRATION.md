# Readout staircase registration

Frozen CPU-only readout design for target `K={2,4,8,16,34,69}` on the same Plant K=69 cached features. It is intended to separate class-count proxy from margin-spectrum structure without adding a domain or retraining an encoder.

Each target K uses two deterministic label constructions: contiguous class-ID blocks (primary) and support-balanced greedy bins (backup). Each cell reports absolute Raw/Log certified TRAIN F1, the difference, a saturation flag, and both unweighted `CV(d²)` and the primary weighted sensitivity

\[
S_\beta=\mathbb E_z\operatorname{Var}_{p_\beta}(d_k^2),\qquad p_k\propto e^{-\beta d_k^2}.
\]

The frozen direction prediction is: for the two locked constructions (contiguous and support-balanced), non-saturated cells have a Log−Raw difference that increases monotonically with `S_beta`, and `S_beta` predicts the difference better than raw K after construction and saturation are controlled. The previously observed `0.97–1.05pp` band is limited to the two K=2 locked constructions; `one_vs_rest` (`3.72pp`) is a known class-imbalance/construction outlier and cannot be used as a post-hoc falsifier. Saturated cells, including the K=69 dual-saturation reference, are marked ceiling-censored and carry no dose information. Any residual K effect after conditioning on `S_beta` is the readout evidence for a class-count component. This is registered and not yet run; it does not replace the Plant K=2 end-to-end window.

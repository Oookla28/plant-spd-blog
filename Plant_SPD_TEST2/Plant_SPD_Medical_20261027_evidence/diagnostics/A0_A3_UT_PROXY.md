# A0/A3 `uT` proxy read

The A0/A3 checkpoints contain a free affine `head_weight` and `head_bias`; they do not contain an explicit scalar `u`. The exact gauge invariant `kappa=uT` is therefore not directly observable from this model parameterization.

Using the class-difference head norm as a **proxy** for `u`:

- A0 inverse temperature: `1.0000`; proxy `u`: `2.5345406`; proxy `uT`: `2.5345406`.
- A3 inverse temperature: `1.2439877`; proxy `u`: `2.5444499`; proxy `uT`: `3.1652643`.
- A3/A0 inverse-temperature ratio: `1.24399`.
- A3/A0 proxy-`u` ratio: `1.00391`.
- A3/A0 proxy-`uT` ratio: `1.24884`.

This is a useful parameterization diagnostic, not an exact `uT` observation. It prevents registering an LR×κ arm with an undefined multiplier. The exact LR comparison must first define which free-head functional is the operational `u`.

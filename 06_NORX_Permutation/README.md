# Chapter 6. Analysis of the NORX Permutation

This folder contains several scripts for Chapter 6, which is about analysis of the NORX core permutation.
The code extensively uses the [cryptools](https://github.com/hellman/cryptools), a SageMath-based package of cryptanalytic tools.

There are two components:

1. [cycles/](cycles/): find all cycles and record tuples (value on the cycle, cycle length); results are in [cycles/cycles.out](cycles/cycles.out)
2. [low_degree_invariants/](low_degree_invariants/): compute dimensions of invariant spaces by the degree, based on cycle decomposition.

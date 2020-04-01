# Design and Cryptanalysis of Symmetric-Key Algorithms in Black and White-box Models
## Doctoral Thesis

This repository contains [my thesis](./thesis.pdf) (268 pages). It also contains various tools supporting some of the chapters, defense slides, and source code of the thesis and slides. Currently, there is code for the following chapters:

- [Chapter 3. Structural Cryptanalysis of Feistel Networks](./03_FeistelNetworks_Decomposition): implementations of decomposition attacks on Feistel Networks wrapped in secret affine layers.
- [Chapter 5. Decomposition of the 6-bit APN Permutation 79](./05_6bit_APN_Permutation_Decomposition): implemented decomposition process of the 6-bit APN permutation (the Butterfly structure).
- [Chapter 6. Analysis of the NORX Permutation](./06_NORX_Permutation): analysis of nonlinear invariants of a 32-bit permutation.
- [Chapters 8-9. White-box Cryptography: cryptolu/whitebox](https://github.com/cryptolu/whitebox): a framework for circuit-based white-box implementations, a nonlinear masking scheme and its verification, a sample nonlinear+linear masked AES implementation.
- [Chapter 11. The SPARKLE, ESCH and SCHWAEMM Algorithms](./11_SPARKLE): linearization of the ARX-box and generic truncated differential search. More supporting code for SPARKLE is available at the [main repository](https://github.com/cryptolu/sparkle).

For citation, please use the following bibtex:

```
@phdthesis{Udovenko19,
  author    = {Aleksei Udovenko},
  title     = {Design and Cryptanalysis of Symmetric-Key Algorithms in Black and
               White-box Models},
  school    = {University of Luxembourg, Luxembourg},
  year      = {2019},
  url       = "http://hdl.handle.net/10993/39350",
}
```

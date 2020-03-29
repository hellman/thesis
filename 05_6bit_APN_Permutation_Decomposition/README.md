# Chapter 5. Decomposition of the 6-bit APN Permutation

This folder contains several scripts for Chapter 5, which is about decomposition, analysis and generalization attempts of the 6-bit APN permutation.
The code extensively uses the [cryptools](https://github.com/hellman/cryptools), a SageMath-based package of cryptanalytic tools.

Currently, the decomposition process is documented:

1. [1info.py](1info.py): information gathering about the S-Box, aligning columns in the LAT.
2. [2tu.py](2tu.py): performing the TU-decomposition and finding relations between T and U.
3. [3decomposeT.py](3decomposeT.py): decomposing the T mini-block cipher.
4. [4decompose_full.py](4decompose_full.py): final decomposition.

**Bonus:** a very compact code for generating a 6-bit APN involution (in the CCZ-equivalence class of the analyzed APN permutation):
(python2 or python3)

```py
mul2 = lambda a: (a<<1) ^ (127 * (a//32))
s = list(range(64))
for a, b in (3, 54), (5, 57), (7, 41), (9, 58):
    for i in range(7):
        s[a], s[b] = b, a
        a, b = mul2(a), mul2(b)
print(s)
```
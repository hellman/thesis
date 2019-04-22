# Chapter 3. Structural Cryptanalysis of Feistel Networks

This folder contains several scripts for Chapter 3, which is about structural/decomposition attacks on Feistel Networks. The code extensively uses the [cryptools](https://github.com/hellman/cryptools), a SageMath-based package of cryptanalytic tools. In particular, the SBox2 class is used for generation and analysis of small Feistel Networks.

Note that some results are cached and saved in the [data/](data/) folder.

1. [walsh.py](walsh.py): verification of various Walsh equations
2. [lat_FN.py](lat_FN.py): generate random 4-,5-,6-round Feistel Networks with nice LAT % 8
3. [af4a.py](af4a.py): implementation of the (simplified) attack on AF<sup>4</sup>A' from Theorem 3.26 (based on Type-I HDIM distinguisher)
4. [af5a.py](af5a.py): implementation of the (simplified) attack on AF<sup>5</sup>A<sup>-1</sup> from Theorem 3.27 (based on Type-II HDIM distinguisher)
5. [empirical_typeII_nrounds.py](empirical_typeII_nrounds.py): determine the maximum number of rounds for type-II distinguisher for various (small) Feistel Network parameters; results are cached for next scripts (Table 3.3)
6. [empirical_impmono_list.py](empirical_impmono_list.py): list impossible monomials empirically
7. [empirical_impmono_rank.py](empirical_impmono_rank.py): compute rank of the impossible monomial attack empirically (Table 3.3)
8. [impmono.py](impmono.py): implementation of the impossible monomial attack, with empirical sampling of impossible monomial types

The implementations here are more like proofs-of-concept, even though some of them succeed quite often and recover secret functions. It would be interesting to:

1. combine attacks to have a full decomposition attack implementation on some AFA variants
2. harden them to solve cases when rank is not full, but close to full (i.e. add some bruteforce, may be some smart tricks)


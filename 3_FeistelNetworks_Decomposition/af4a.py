#-*- coding:utf-8 -*-

from sage.all import *
from cryptools.env import *
from utils import *

# implementation of the (simplified) attack on AF^4A'
# from Theorem 3.26 (based on Type-I HDIM distinguisher)

n = 4

nr = 4
perm = True
deg = n - 1

print "N", n, "NR", nr, "PERM", perm, "DEG", deg
print "pregen..."
FSPOOL = generate_functions(n, deg, perm)
print "done"
print

while True:
    fs, S = generate_FN(funcpool=FSPOOL, nr=nr)

    # attack constraint (for simplicity)
    HS = mat2blocks(S.hdim())
    if HS[0][0].rank() != n:
        continue

    print "S degrees"
    print S.degrees()
    print

    print "S hdim"
    print S.hdim()
    print

    # randomize linear encodings until
    # UL2-decompositions exist
    while True:
        mu = SBox2.gen.random_linear_permutation(2*n)
        eta = SBox2.gen.random_linear_permutation(2*n)
        try:
            a,b,c,d = UL2(mu.as_matrix())
            ap,bp,cp,dp = UL2((~eta).as_matrix())
            print "a"
            print a
            print
            print "ap"
            print ap
            print
            assert mu.as_matrix() == idup(c) * diag(b, d) * idlo(a)
            assert (~mu.as_matrix().transpose()) == idlo(c.transpose()) * diag(~b.transpose(), ~d.transpose()) * idup(a.transpose())

            assert ~eta.as_matrix() == idup(cp) * diag(bp, dp) * idlo(ap)
            assert eta.as_matrix() == idlo(ap) * diag(~bp, ~dp) * idup(cp)

            # "forget" secret
            del a,c,d
            del ap,cp,dp
            # b, bp are kept for assertion, not used
            break
        except ZeroDivisionError:
            continue

    T = eta * S * mu
    print "T hdim"
    print T.hdim()
    print

    HT = mat2blocks(T.hdim())
    assert T.hdim() == eta.as_matrix() * S.hdim() * (~mu.as_matrix().transpose())

    h = HT[0][0]
    print "h' rank", h.rank()
    print h

    # attack constraint (for simplicity)
    assert h.rank() == n, "guaranteed since b's are invertible by UL2-decompositions"

    assert h == (~bp) * HS[0][0] * (~b).transpose()

    # main part: recover a, ap
    hat = HT[0][1]
    aph = HT[1][0]

    a = ((~h) * hat).transpose()
    ap = aph * (~h)

    print "a recovered"
    print a
    print "ap recovered"
    print ap
    print "test quadratic", ap * h * a.transpose() == HT[1][1]
    print

    lina = SBox2.gen.from_matrix(a)
    linap = SBox2.gen.from_matrix(ap)
    Sp = [None] * 2**(2*n)

    # Feistel xor goes to the left, we need to the right
    fn_lina = SBox2.gen.feistel_round_xor(func=lina, swap=False).swap_halves()
    fn_linap = SBox2.gen.feistel_round_xor(func=linap, swap=False).swap_halves()
    Sp = fn_linap * T * fn_lina

    print "S' hdim"
    print Sp.hdim()
    print
    # should be of the form
    # ? 0
    # 0 0
    break

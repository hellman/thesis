#-*- coding:utf-8 -*-

from sage.all import *
from cryptools.env import *
from utils import *

# implementation of the (simplified) attack on AF^5A^{-1}
# from Theorem 3.27 (based on Type-II HDIM distinguisher)

n = 4

nr = 5
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
    if HS[0][1].rank() != n:
        continue

    print "S degrees"
    print S.degrees()
    print

    print "S hdim"
    print S.hdim()
    print

    while True:
        mu = SBox2.gen.random_linear_permutation(2*n)
        try:
            a,b,c,d = UL2(mu.as_matrix())
            print "a"
            print a
            print
            assert mu.as_matrix() == idup(c) * diag(b, d) * idlo(a)
            assert (~mu.as_matrix().transpose()) == idlo(c.transpose()) * diag(~b.transpose(), ~d.transpose()) * idup(a.transpose())
            break
        except ZeroDivisionError:
            continue

    T = (~mu) * S * mu
    print "T hdim"
    print T.hdim()
    print

    HT = mat2blocks(T.hdim())
    assert T.hdim() == (~mu.as_matrix()) * S.hdim() * (~mu.as_matrix().transpose())
    t11,t12,t21,t22 = sum(HT, [])

    if 1: # using secret (a) to verify the properties:
        lina = SBox2.gen.from_matrix(a)
        fn_lina = SBox2.gen.feistel_round_xor(func=lina, swap=False).swap_halves()
        Sp = fn_lina * T * fn_lina

        print "Sp hdim"
        print Sp.hdim()
        print

        assert Sp.hdim() == idlo(a) * T.hdim() * idup(a.transpose())

        HSp = mat2blocks(Sp.hdim())
        assert HSp[0][0] == (~b) * (HS[0][0] + c*HS[1][0] + HS[0][1]*c.transpose()) * (~b.transpose())
        assert HSp[0][1] == (~b) * HS[0][1] * (~d.transpose())
        assert HSp[1][0] == (~d) * HS[1][0] * (~b.transpose())
        assert HSp[1][1] == 0
        assert HSp[0][0] == t11
        assert HSp[0][1] == t12 + t11 * a.transpose()
        assert HSp[1][0] == t21 + a * t11
        assert HSp[1][1] == t22 + a*t12 + t21*a.transpose() + a*t11*a.transpose()

    # verify that secret (a) satisfies the generated public equation
    assert t22 + a*t12 + t21*a.transpose() + a*t11*a.transpose() == 0

    r = SBox2.gen.random_linear_permutation(n).as_matrix()
    my = SBox2.gen.from_matrix(diag(r, identity_matrix(GF(2), n)))
    TT = (~my) * T * my
    # print TT.hdim()
    HTT = mat2blocks(TT.hdim())
    tt11,tt12,tt21,tt22 = sum(HTT, [])
    assert TT.hdim() == (~my.as_matrix()) * (~mu.as_matrix()) * S.hdim() * (~mu.as_matrix().transpose()) * (~my.as_matrix().transpose())

    # print t11
    # print
    # print tt11
    # print
    assert tt11 == (~r) * t11 * (~r.transpose())

    print "verification done"
    break

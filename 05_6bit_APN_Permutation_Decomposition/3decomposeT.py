from sage.all import *
from cryptools.env import *

from common import *


# ----------------------------------
# 1. align zeroes in T
# ----------------------------------
# NOTE: T[k][fixed] is linear permutation
Ti = [~f for f in T]
t_after = SBox2(f[0] for f in Ti)
t_before = SBox2(f.preimage(0) for f in Ti)
print "after:", t_after, t_after.degrees(), t_after.anfs()
print "before:", t_before, t_before.degrees(), t_before.anfs()

t = [f[0] for f in T]
assert t == [0, 7, 4, 3, 1, 6, 5, 2]
t = SBox2(t)
print t, SBox2(t).is_linear(), SBox2(t).interpolation_polynomial(F3)
print

T_prime = [f ^ f[0] for f in T]
T_prime_inv = [~f for f in T_prime]

for k, x in product(range(8), repeat=2):
    test = T[k][x]
    x = T_prime[k][x]
    x ^= t[k]
    assert x == test
for k, x in product(range(8), repeat=2):
    test = Ti[k][x]
    x ^= t[k]
    x = T_prime_inv[k][x]
    assert x == test
t0 = t

# ----------------------------------
# 2a. interpolate
# ----------------------------------

extend = [ [texpoly(t.interpolation_polynomial(F3), no0=True)] for t in T_prime_inv]
for t in T_prime_inv:
    print t.interpolation_polynomial(F3)
print
print_latex_minicipher(T_prime_inv, "T'^{-1}", extend=extend)

# ----------------------------------
# 2b. separate nonlinear constant part
# ----------------------------------

x = PolynomialRing(F3, names='x').gen()
N = SBox2.gen.from_poly(w**3*x**6 + w**1*x**5 + w**6*x**3)

L = [T_prime_inv[k] ^ N for k in xrange(8)]
print "N = SBox2(%s)" % N
print "L = ["
for l in L:
    print l, ", #", l.interpolation_polynomial(F3)
print "]"

# ----------------------------------
# 3. simplify nonlinear constant part, and L
# ----------------------------------

if 0:
    for lin in GL(3, GF(2)):
        p = SBox2.gen.from_matrix(lin.matrix())
        poly = (p*N).interpolation_polynomial(F3)
        if len(str(poly)) < 10:
            print p, poly

p = SBox2((0, 4, 3, 7, 1, 5, 2, 6))
print "p = SBox2(%s) # %s" % (p, p.interpolation_polynomial(F3))

print "pL:"
l2 = []
l4 = []
for l in L:
    poly = (p * l).interpolation_polynomial(F3)
    print p*l, poly
    cs = [c.integer_representation() for c in poly] + [0] * 8
    l2.append(cs[2])
    l4.append(cs[4])

l2 = SBox2(l2)
l4 = SBox2(l4)
print "pre_l2 = SBox2(%s) # %s" % (l2, l2.interpolation_polynomial(F3))
print "pre_l4 = SBox2(%s) # %s" % (l4, l4.interpolation_polynomial(F3))

l2 = l2.xor(2, 0)
l4 = l4.xor(2, 0)
print "l2 = SBox2(%s) # %s" % (l2, l2.interpolation_polynomial(F3))
print "l4 = SBox2(%s) # %s" % (l4, l4.interpolation_polynomial(F3))

x = PolynomialRing(F3, names='x').gen()
inv = SBox2.gen.from_poly(x**6)

# verify current decomposition
def monomial(c, x, e):
    c = F3.fetch_int(c)
    x = F3.fetch_int(x)
    return (c*x**e).integer_representation()

pi = ~p
for k, x in product(range(8), repeat=2):
    test = Ti[k][x]
    x ^= t0[k]
    x = inv[x] ^ monomial(l2[k^2], x, 2) ^ monomial(l4[k^2], x, 4)
    x = pi[x]
    assert x == test, (x, test)

# ----------------------------------
# 4. simplify l2, l4
# ----------------------------------

print "simplify l2, l4:"
if 0:
    for lin in GL(3, GF(2)):
        q = SBox2.gen.from_matrix(lin.matrix())
        qpoly = q.interpolation_polynomial(F3)

        p2 = (l2*q).interpolation_polynomial(F3)
        p4 = (l4*q).interpolation_polynomial(F3)
        if len(str(p2)) < 10 and len(str(p4)) < 10:
            print q, "|", p2, p4, "|", texpoly(qpoly, linear=True, no0=True)

q = SBox2((0, 7, 6, 1, 5, 2, 3, 4))

# ----------------------------------
# 5. final
# ----------------------------------
z = t0*q ^ SBox2.gen.id(3)

for k, x in product(range(8), repeat=2):
    test = T[k][x]
    # outer affine
    x = p(x)
    k = q.preimage(k) ^ 5
    # main
    x ^= inv[k]
    x = inv[x]
    # inner affine
    x ^= k
    k ^= 5
    k = q(k)
    x ^= t0[k]
    assert x == test, (x, test)

for k, x in product(range(8), repeat=2):
    test = T[k][x]
    # outer affine (optional)
    x = p(x)
    k = q.preimage(k) ^ 5
    # main
    x ^= inv[k]
    x = inv[x]
    # inner affine
    x ^= z[k ^ 5] ^ 5
    assert x == test, (x, test)

print "q = SBox2(%s) # %s" % (q, q.interpolation_polynomial(F3))
print "z = SBox2(%s) # %s" % (z, z.interpolation_polynomial(F3))

#-*- coding:utf-8 -*-

from sage.all import *
from cryptools.env import *
from utils import generate_functions, generate_FN, generate_FN_two_last

"""
implementation of the
impossible monomials attack
(Algorithm 3.1 in the thesis)
"""

n = 6

if 1: # easy
    nr = 5
    deg = n - 1
    perm = True
else: # harder (a bit)
    nr = 7
    deg = 2
    perm = False

print "N", n, "NR", nr, "PERM", perm, "DEG", deg
print


# sampling impossible monomial classes
print "sampling..."
from empirical_impmono_list import get_impossible_monomials
num_imp, IMP_TYPES = get_impossible_monomials(nr-1, n, deg, perm)

def gettype(x):
    l, r = split_halves(x, h=n)
    return hw(l), hw(r)

IMP = [mono for mono in xrange(2**(2*n)) if gettype(mono) in IMP_TYPES]
imp2i = {}
for i, mono in enumerate(IMP):
    imp2i[mono] = i

UNK = [mono for mono in xrange(2**n) if hw(mono) <= deg]
unk2i = {}
for i, mono in enumerate(UNK):
    unk2i[mono] = i

print len(IMP), "impossible monomials"
print len(UNK), "unknown monomials"
print


print "generating random FN..."
FSPOOL = generate_functions(n, deg, perm)
fs, s, spre = generate_FN_two_last(funcpool=FSPOOL, nr=nr)
# secret FN (one round less)
print "hdim spre (secret)"
print spre.hdim()
print
# public FN
print "hdim s (public)"
print s.hdim()
print

print "precomputing submasks..."
by_y = []
for y in xrange(2**n):
    lst = []
    for x in xrange(y + 1):
        if x & y == x and hw(x) <= deg:
            lst.append(x)
    by_y.append(lst)
print "done"
print

print "precomputing by x..."
impmonos_by_x = []
for x in xrange(2**(2*n)):
    res = []
    for ix, impmono in enumerate(IMP):
        if x & impmono == x:
            res.append((ix, impmono))
    impmonos_by_x.append(res)
print "done"
print

m = matrix(GF(2), len(IMP), len(UNK))
targets = matrix(GF(2), len(IMP), n)

for x, y in s.graph():
    yl, yr = split_halves(y, h=n)
    ylbin = tobin(yl, n)
    for ix, impmono in impmonos_by_x[x]:
        for unkmono in by_y[yr]:
            iy = unk2i[unkmono]
            m[ix,iy] += 1
        for iy, ylbit in enumerate(ylbin):
            targets[ix,iy] += ylbit

print "Equation system:"
nullity = m.right_nullity()
print "Rank", m.rank(), "Nullity", nullity
print "2**%d" % (nullity * n), "solutions, if any"
print

print "Solving..."
# bit-sliced trickery
# mobius works on integers as well (each bit position is parallel)
anf_vecs = m.solve_right(targets)

print "Reconstructing..."
anfs = [0] * 2**n
for takes, unkmono in zip(anf_vecs, UNK):
    anfs[unkmono] = frombin(takes)
bf = mobius(anfs)
print
print "recovered         ", bf
print "original          ", fs[-1]
print "original up to xor", fs[-1] ^ fs[-1][0]

print "recovered correctly?", fs[-1] ^ fs[-1][0] == bf

real_anf = fs[-1].mobius()
sol = matrix(GF(2), len(UNK), n)
for i, unkmono in enumerate(UNK):
    sol[i] = tobin(real_anf[unkmono], n)

print "actual function satisfies the system?", m * sol == targets



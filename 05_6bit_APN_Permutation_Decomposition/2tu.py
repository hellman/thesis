from sage.all import *
from cryptools.env import *

from common import *

# ----------------------------------
# 1. T-U decomposition
# ----------------------------------
S = eta_S0

def halvenc(xl, xr):
    return split(S[(xl << 3) | xr], (3, 3))

def encrypt(xls, xrs):
    yls = []
    yrs = []
    for xl in xls:
        for xr in xrs:
            yl, yr = halvenc(xl, xr)
            yls.append(yl)
            yrs.append(yr)
    return set(yls), set(yrs)

p = range(8)
for c in xrange(8):
    l, r = encrypt(p, [c])
    res = {1: "c", 8: "p"}.get(len(l), "?")
    res += ","
    res += {1: "c", 8: "p"}.get(len(r), "?")
    print "c=%x: p,c ->" % c, res

for c in xrange(8):
    l, r = encrypt([c], p)
    res = {1: "c", 8: "p"}.get(len(l), "?")
    res += ","
    res += {1: "c", 8: "p"}.get(len(r), "?")
    print "c=%x: c,p ->" % c, res

# (p,c) -> (?,p)
# same as in GOST S-Box chapter

T = [
    SBox2(halvenc(x, k)[1] for x in xrange(8))
    for k in xrange(8)
]
Ti = [~t for t in T]

U = [
    SBox2(halvenc(Ti[x][k], x)[0] for x in xrange(8))
    for k in xrange(8)
]
print U
Ui = [~u for u in U]

for l, r in product(range(8), repeat=2):
    yl, yr = halvenc(l, r)

    l = T[r][l]
    l, r = r, l
    l = U[r][l]
    assert (l, r) == (yl, yr)

print "TU-decomposition OK"

res = [r""]
for x in xrange(8):
    res.append(r"$\hex{%1x}$" % x)
print " & ".join(res) + r"\\"
print

print_latex_minicipher(T, name="T")
print_latex_minicipher(U, name="U")

print "T = map(SBox2, ",
pprint(T)
print ")"
print "U = map(SBox2, ",
pprint(U)
print ")"

assert map(list, T) == [
    [0, 6, 4, 7, 3, 1, 5, 2] ,
    [7, 5, 1, 6, 4, 2, 0, 3] ,
    [4, 3, 2, 0, 5, 6, 1, 7] ,
    [3, 5, 2, 1, 4, 6, 7, 0] ,
    [1, 2, 0, 6, 4, 3, 7, 5] ,
    [6, 5, 2, 4, 7, 0, 1, 3] ,
    [5, 2, 6, 4, 0, 3, 1, 7] ,
    [2, 0, 1, 6, 5, 3, 4, 7] ,
]
assert map(list, U) == [
    [0, 3, 6, 4, 2, 7, 1, 5] ,
    [7, 4, 0, 2, 3, 6, 1, 5] ,
    [1, 4, 2, 6, 3, 0, 5, 7] ,
    [7, 2, 5, 1, 3, 0, 4, 6] ,
    [7, 3, 4, 1, 0, 2, 6, 5] ,
    [3, 7, 1, 4, 2, 0, 5, 6] ,
    [1, 3, 7, 4, 6, 2, 5, 0] ,
    [4, 6, 3, 0, 5, 1, 7, 2] ,
]

# ----------------------------------
# 2. Relation between T and U
# ----------------------------------
print "T_k degrees"
for f in T:
    print f.degrees(), (~f).degrees()
print "U_k degrees"
for f in U:
    print f.degrees(), (~f).degrees()

Tbox = SBox2((T[k][x] << 3) | k for x in xrange(8) for k in xrange(8))
Tinvbox = SBox2((T[k].preimage(x) << 3) | k for x in xrange(8) for k in xrange(8))
print "T degrees", Tbox.degrees(), (Tinvbox).degrees()
Ubox = SBox2((U[k][x] << 3) | k for x in xrange(8) for k in xrange(8))
Uinvbox = SBox2((U[k].preimage(x) << 3) | k for x in xrange(8) for k in xrange(8))
print "U degrees", Ubox.degrees(), (Uinvbox).degrees()

Mu, Mup = Tinvbox.is_linear_equivalent(Ubox)
assert Mup * Tinvbox * Mu == Ubox

print_latex_matrix(Mu.as_matrix(), r"M_U")
print_latex_matrix(Mup.as_matrix(), r"M_U'")

print "Mu = SBox2(%s)" % Mu
print "Mup = SBox2(%s)" % Mup


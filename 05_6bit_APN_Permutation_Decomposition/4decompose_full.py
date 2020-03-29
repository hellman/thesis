from sage.all import *
from cryptools.env import *

from common import *

M = []
for l, r in product(range(8), repeat=2):
    l ^= z[r]
    r = q[r]
    l, r = r, l
    lr = (l << 3) | r
    lr = Mu(lr)
    l, r = split(lr, (3, 3))
    r = q.preimage(r)
    l ^= z[r]
    lr = (l << 3) | r
    M.append(lr)

M = SBox2(M)
print M.as_matrix()
print M.as_matrix() * vector(GF(2), [1, 0, 1, 1, 0, 1])
quit()
print_latex_matrix(M.as_matrix(), "M")

# verify
s = []
for x, k in product(range(8), repeat=2):
    x ^= inv[k]
    x = inv[x]
    x ^= 5
    k ^= 5
    xk = (x << 3) | k
    xk = M[xk]
    x, k = split(xk, (3, 3))
    x ^= 5
    k ^= 5
    x = inv[x]
    x ^= inv[k]

    xk = (x << 3) | k
    s.append(xk)

s = SBox2(s)
print s.ddt_distrib()
assert s.is_APN()
assert s.is_permutation()


mat = M.as_matrix()
subs = [mat[3*i:3*i+3,3*j:3*j+3] for i in xrange(2) for j in xrange(2)]
for sub in subs:
    lin = SBox2.gen.from_matrix(sub)
    print lin.interpolation_polynomial(F3)

#-*- coding:utf-8 -*-

from sage.all import *
from ast import literal_eval

mats = [list() for _ in xrange(999)]
for line in open(sys.argv[1]):
    if line.strip():
        try:
            dim, offset, basis, eq = literal_eval(line.strip().strip(","))
        except Exception as err:
            print "broken equation:", repr(line)
            continue
        mats[dim].append(eq)

lst = []

for dim, mat in enumerate(mats):
    if dim == 0: continue
    elif not mat: break
    mat = matrix(GF(2), mat)
    rn = mat.right_nullity()
    if rn > 1:
        print "Invariant: subspace dimension", "%2d" % dim, "degree", "<=%2d" % (dim-1), " invariants dimension", rn
        ker = mat.right_kernel().matrix()
        for row in ker[:10]:
            print "   cycle subset:", [i for i, v in enumerate(row) if v]
        if ker.nrows() > 10:
            print "   ..."
        print
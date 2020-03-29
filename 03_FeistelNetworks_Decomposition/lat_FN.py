#-*- coding:utf-8 -*-

from sage.all import *
from cryptools.env import *

import ast

# generating some FN with nice LAT % 8

n = 3

# generate at random
# FS = [SBox2.gen.random_permutation(n) for _ in xrange(10)]
for nr in (4, 5, 6):
    while True:
        # generate at random
        # fs = FS[:nr]
        # or reuse saved one (used in the thesis)
        fs = ast.literal_eval(open("data/FNbij%d.txt" % nr).read())

        s = SBox2.gen.feistel_network_xor(funcs=fs)

        # filter out degenerate cases
        degs = s.degrees()
        if nr == 4 and degs != (5, 5, 5, 4, 4, 4): continue
        if nr == 5 and degs != (5, 5, 5, 5, 5, 5): continue
        if nr == 6 and degs != (5, 5, 5, 5, 5, 5): continue
        hdim = s.hdim()
        if nr >= 5 and any(max(row) == 0 for row in hdim): continue

        print "NR", nr, "fs", len(fs)
        print s.hdim()
        print

        # latex
        h = s.hdim()
        sh = [map(str, row) for row in s.hdim()]
        for i in xrange(2):
            for j in xrange(2):
                if max(h[i*n+ii][j*n+jj] for ii in xrange(n) for jj in xrange(n)) == 0:
                    for ii in xrange(n):
                        for jj in xrange(n):
                            sh[i*n+ii][j*n+jj] = r"\gzero"
        for row in sh:
            print " & ".join(row) + r" \\"
        print

        print "degrees", degs
        if 1:
            lat = s.lat() % 4
            with open("data/FNbij%d.txt" % nr, "w") as fd:
                fd.write(repr(fs))
            save_plot(lat, "data/lat%d.png" % nr, colorbar=False)
        print
        break

#-*- coding:utf-8 -*-

from sage.all import *
from cryptools.env import *
from utils import *

@sage_cache("data/typeII_nrounds")
def get_typeII_nrounds(n, deg, perm):
    for nr in xrange(3, 999):
        # MAX of hdims
        h = matrix(GF(2), 2*n, 2*n)
        """
        10 iterations should be enough, since n**2 bits are ORed
        we have the probability to get all-zeroes when they are actually not always so
        only about 2^{-10n**2}. Even for n=3 gives 2^-90.
        """
        funcpool = generate_functions(n, deg, perm)
        for i in xrange(10):
            fs, s = generate_FN(funcpool=funcpool, nr=nr)
            hi = s.hdim()
            for x in xrange(2*n):
                for y in xrange(2*n):
                    h[y,x] = max(h[y,x], hi[y,x])
        H = mat2blocks(h)

        # pattern
        pat = [max(m.list()) for row in H for m in row]
        assert pat != [1, 1, 1, 1],  "HDIM degraded completely???"

        if pat == [1, 1, 1, 0]:
            return nr
    assert False, "HDIM does not degrade???"

if __name__ == '__main__':
    for n in xrange(3, 12):
        for deg_data in sorted({2, 3, n-1, n, -1}):
            if deg_data > n: continue

            if deg_data == -1: # perm
                perm = True
                deg = n - 1
            else:
                perm = False
                deg = deg_data

            print "n %2d deg %2d" % (n, deg), "perm" if perm else "    ", ":",
            print "typeII at %d rounds" % get_typeII_nrounds(n, deg, perm)
        print

'''
n  3 deg  2 perm : typeII at 5 rounds
n  3 deg  2      : typeII at 5 rounds
n  3 deg  3      : typeII at 3 rounds

n  4 deg  3 perm : typeII at 5 rounds
n  4 deg  2      : typeII at 5 rounds
n  4 deg  3      : typeII at 4 rounds
n  4 deg  4      : typeII at 3 rounds

n  5 deg  4 perm : typeII at 5 rounds
n  5 deg  2      : typeII at 6 rounds
n  5 deg  3      : typeII at 5 rounds
n  5 deg  4      : typeII at 4 rounds
n  5 deg  5      : typeII at 3 rounds

n  6 deg  5 perm : typeII at 5 rounds
n  6 deg  2      : typeII at 7 rounds
n  6 deg  3      : typeII at 5 rounds
n  6 deg  5      : typeII at 4 rounds
n  6 deg  6      : typeII at 3 rounds

n  7 deg  6 perm : typeII at 5 rounds
n  7 deg  2      : typeII at 7 rounds
n  7 deg  3      : typeII at 5 rounds
n  7 deg  6      : typeII at 4 rounds
n  7 deg  7      : typeII at 3 rounds

n  8 deg  7 perm : typeII at 5 rounds
n  8 deg  2      : typeII at 7 rounds
n  8 deg  3      : typeII at 5 rounds
n  8 deg  7      : typeII at 4 rounds
n  8 deg  8      : typeII at 3 rounds

n  9 deg  8 perm : typeII at 5 rounds
n  9 deg  2      : typeII at 8 rounds
n  9 deg  3      : typeII at 5 rounds
n  9 deg  8      : typeII at 4 rounds
n  9 deg  9      : typeII at 3 rounds

n 10 deg  9 perm : typeII at 5 rounds
n 10 deg  2      : typeII at 8 rounds
n 10 deg  3      : typeII at 6 rounds
n 10 deg  9      : typeII at 4 rounds
n 10 deg 10      : typeII at 3 rounds
'''

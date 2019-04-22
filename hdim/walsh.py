#-*- coding:utf-8 -*-

# verification of various walsh equations

from sage.all import *
from cryptools.binary import scalar_bin

while True:
    n = randint(1, 7)

    f = [0] * 2**(n-1) + [1] * 2**(n-1)
    shuffle(f)

    w1 = [sum( (-1)**(scalar_bin(a, x)+f[x]) for x in xrange(2**n) ) for a in xrange(2**n)]
    w2 = [sum( f[x]*(-1)**scalar_bin(a, x) for x in xrange(2**n) ) for a in xrange(2**n)]

    for a in xrange(1, 2**n):
        assert w2[a] == -w1[a] / 2

    for dim in xrange(n+1):
        print "dim", dim
        mask = 2**dim - 1
        Vi = [a for a in xrange(2**n) if a & mask == 0]
        V = [b for b in xrange(2**n) if all(scalar_bin(a, b) == 0 for a in Vi)]
        print len(V), len(Vi)
        assert len(V) == 2**dim
        assert len(V) * len(Vi) == 2**n

        print "w1", sum(w1[a] for a in V), sum(w1[a] for a in Vi)
        print "w2", sum(w2[a] for a in V), sum(w2[a] for a in Vi)
        assert sum(w1[a] for a in V) == len(V) * sum((-1)**f[x] for x in Vi)
        assert sum(w1[a] for a in V) == len(V) * (len(Vi) - 2*sum(f[x] for x in Vi))
        assert sum(w1[a] for a in V) == 2**n - 2*len(V)*sum(f[x] for x in Vi)
        assert sum(w1[a] for a in V) == 2**n - 2**(dim+1) * sum(f[x] for x in Vi)
        assert (2**n - sum(w1[a] for a in V)) % 2**(dim+2) / 2**(dim+1) == sum(f[x] for x in Vi) % 2

        assert sum(w2[a] for a in V) == 2**dim * sum(f[x] for x in Vi)

        print

    if n >= 3:
        for j in xrange(n):
            assert (w1[1<<j] % 8) / 4 == sum(f[x] for x in xrange(2**n) if x & (1 << j) == 0) % 2

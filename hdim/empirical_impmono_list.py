#-*- coding:utf-8 -*-

from sage.all import *
from cryptools.env import *
from utils import *

from empirical_typeII_nrounds import get_typeII_nrounds

@sage_cache("data/impossible_monomials")
def get_impossible_monomials(nr, n, deg, perm):
    """
    impossible monomials on the right half of nr-round FN
    """
    seen = set()
    """
    10 iterations should be enough
    as there are several output bits
    """
    funcpool = generate_functions(n, deg, perm)
    for itr in xrange(10):
        fs, s = generate_FN(funcpool=funcpool, nr=nr)
        anf = s.mobius()
        for x, y in anf.graph():
            yl, yr = split_halves(y, h=n)
            if yr:
                xl, xr = split_halves(x, h=n)
                typ = hw(xl), hw(xr)
                seen.add(typ)

    types = set()
    num_imp = 0
    for typ in product(range(n+1), repeat=2):
        if typ not in seen:
            types.add(typ)
            num_imp += binomial(n, typ[0]) * binomial(n, typ[1])
    return num_imp, tuple(sorted(types))

if __name__ == '__main__':
    for n in xrange(3, 11):
        for deg_data in sorted({2, 3, n-1, n, -1}):
            if deg_data > n: continue

            if deg_data == -1: # perm
                perm = True
                deg = n - 1
            else:
                perm = False
                deg = deg_data

            print "n %2d deg %2d perm %5s" % (n, deg, "perm" if perm else ""), "|",
            nr = get_typeII_nrounds(n, deg, perm)
            print "typeII at %2d rounds" % nr, "|",

            if deg == n:
                todo_nr = nr
            else:
                todo_nr = nr - 1

            num_imp, types = get_impossible_monomials(todo_nr, n, deg, perm)
            print "%5d impossible monomials (%2d types) at %d rounds" % (num_imp, len(types), todo_nr), ":",
            print " ".join("%d:%d" % t for t in types)
        print



'''
n  3 deg  2 perm  perm | typeII at  5 rounds |    20 impossible monomials ( 6 types) at 4 rounds : 2:2 2:3 3:0 3:1 3:2 3:3
n  3 deg  2 perm       | typeII at  5 rounds |    10 impossible monomials ( 4 types) at 4 rounds : 2:3 3:1 3:2 3:3
n  3 deg  3 perm       | typeII at  3 rounds |     7 impossible monomials ( 3 types) at 3 rounds : 3:1 3:2 3:3

n  4 deg  3 perm  perm | typeII at  5 rounds |    36 impossible monomials ( 7 types) at 4 rounds : 3:3 3:4 4:0 4:1 4:2 4:3 4:4
n  4 deg  2 perm       | typeII at  5 rounds |    35 impossible monomials ( 6 types) at 4 rounds : 3:3 3:4 4:1 4:2 4:3 4:4
n  4 deg  3 perm       | typeII at  4 rounds |    82 impossible monomials (10 types) at 3 rounds : 2:4 3:1 3:2 3:3 3:4 4:0 4:1 4:2 4:3 4:4
n  4 deg  4 perm       | typeII at  3 rounds |    15 impossible monomials ( 4 types) at 3 rounds : 4:1 4:2 4:3 4:4

n  5 deg  4 perm  perm | typeII at  5 rounds |    62 impossible monomials ( 8 types) at 4 rounds : 4:4 4:5 5:0 5:1 5:2 5:3 5:4 5:5
n  5 deg  2 perm       | typeII at  6 rounds |    56 impossible monomials ( 6 types) at 5 rounds : 4:4 4:5 5:2 5:3 5:4 5:5
n  5 deg  3 perm       | typeII at  5 rounds |    31 impossible monomials ( 5 types) at 4 rounds : 4:5 5:2 5:3 5:4 5:5
n  5 deg  4 perm       | typeII at  4 rounds |   197 impossible monomials (12 types) at 3 rounds : 3:5 4:1 4:2 4:3 4:4 4:5 5:0 5:1 5:2 5:3 5:4 5:5
n  5 deg  5 perm       | typeII at  3 rounds |    31 impossible monomials ( 5 types) at 3 rounds : 5:1 5:2 5:3 5:4 5:5

n  6 deg  5 perm  perm | typeII at  5 rounds |   106 impossible monomials ( 9 types) at 4 rounds : 5:5 5:6 6:0 6:1 6:2 6:3 6:4 6:5 6:6
n  6 deg  2 perm       | typeII at  7 rounds |    28 impossible monomials ( 4 types) at 6 rounds : 5:6 6:4 6:5 6:6
n  6 deg  3 perm       | typeII at  5 rounds |    99 impossible monomials ( 7 types) at 4 rounds : 5:5 5:6 6:2 6:3 6:4 6:5 6:6
n  6 deg  5 perm       | typeII at  4 rounds |   457 impossible monomials (14 types) at 3 rounds : 4:6 5:1 5:2 5:3 5:4 5:5 5:6 6:0 6:1 6:2 6:3 6:4 6:5 6:6
n  6 deg  6 perm       | typeII at  3 rounds |    63 impossible monomials ( 6 types) at 3 rounds : 6:1 6:2 6:3 6:4 6:5 6:6

n  7 deg  6 perm  perm | typeII at  5 rounds |   184 impossible monomials (10 types) at 4 rounds : 6:6 6:7 7:0 7:1 7:2 7:3 7:4 7:5 7:6 7:7
n  7 deg  2 perm       | typeII at  7 rounds |   120 impossible monomials ( 6 types) at 6 rounds : 6:6 6:7 7:4 7:5 7:6 7:7
n  7 deg  3 perm       | typeII at  5 rounds |   596 impossible monomials (12 types) at 4 rounds : 5:7 6:4 6:5 6:6 6:7 7:1 7:2 7:3 7:4 7:5 7:6 7:7
n  7 deg  6 perm       | typeII at  4 rounds |  1038 impossible monomials (16 types) at 3 rounds : 5:7 6:1 6:2 6:3 6:4 6:5 6:6 6:7 7:0 7:1 7:2 7:3 7:4 7:5 7:6 7:7
n  7 deg  7 perm       | typeII at  3 rounds |   127 impossible monomials ( 7 types) at 3 rounds : 7:1 7:2 7:3 7:4 7:5 7:6 7:7

n  8 deg  7 perm  perm | typeII at  5 rounds |   328 impossible monomials (11 types) at 4 rounds : 7:7 7:8 8:0 8:1 8:2 8:3 8:4 8:5 8:6 8:7 8:8
n  8 deg  2 perm       | typeII at  7 rounds |   165 impossible monomials ( 6 types) at 6 rounds : 7:7 7:8 8:5 8:6 8:7 8:8
n  8 deg  3 perm       | typeII at  5 rounds |  1811 impossible monomials (15 types) at 4 rounds : 6:7 6:8 7:4 7:5 7:6 7:7 7:8 8:1 8:2 8:3 8:4 8:5 8:6 8:7 8:8
n  8 deg  7 perm       | typeII at  4 rounds |  2324 impossible monomials (18 types) at 3 rounds : 6:8 7:1 7:2 7:3 7:4 7:5 7:6 7:7 7:8 8:0 8:1 8:2 8:3 8:4 8:5 8:6 8:7 8:8
n  8 deg  8 perm       | typeII at  3 rounds |   255 impossible monomials ( 8 types) at 3 rounds : 8:1 8:2 8:3 8:4 8:5 8:6 8:7 8:8

n  9 deg  8 perm  perm | typeII at  5 rounds |   602 impossible monomials (12 types) at 4 rounds : 8:8 8:9 9:0 9:1 9:2 9:3 9:4 9:5 9:6 9:7 9:8 9:9
n  9 deg  2 perm       | typeII at  8 rounds |    55 impossible monomials ( 4 types) at 7 rounds : 8:9 9:7 9:8 9:9
n  9 deg  3 perm       | typeII at  5 rounds |  5605 impossible monomials (18 types) at 4 rounds : 7:7 7:8 7:9 8:4 8:5 8:6 8:7 8:8 8:9 9:1 9:2 9:3 9:4 9:5 9:6 9:7 9:8 9:9
n  9 deg  8 perm       | typeII at  4 rounds |  5147 impossible monomials (20 types) at 3 rounds : 7:9 8:1 8:2 8:3 8:4 8:5 8:6 8:7 8:8 8:9 9:0 9:1 9:2 9:3 9:4 9:5 9:6 9:7 9:8 9:9
n  9 deg  9 perm       | typeII at  3 rounds |   511 impossible monomials ( 9 types) at 3 rounds : 9:1 9:2 9:3 9:4 9:5 9:6 9:7 9:8 9:9

n 10 deg  9 perm  perm | typeII at  5 rounds |  1134 impossible monomials (13 types) at 4 rounds : 9:9 9:10 10:0 10:1 10:2 10:3 10:4 10:5 10:6 10:7 10:8 10:9 10:10
n 10 deg  2 perm       | typeII at  8 rounds |   286 impossible monomials ( 6 types) at 7 rounds : 9:9 9:10 10:7 10:8 10:9 10:10
n 10 deg  3 perm       | typeII at  6 rounds |   496 impossible monomials ( 7 types) at 5 rounds : 9:9 9:10 10:6 10:7 10:8 10:9 10:10
...
'''

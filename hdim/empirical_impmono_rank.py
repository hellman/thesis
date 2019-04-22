#-*- coding:utf-8 -*-

from sage.all import *
from cryptools.env import *
from utils import *

from empirical_typeII_nrounds import get_typeII_nrounds
from empirical_impmono_list import get_impossible_monomials

ITER = 1000


for n in xrange(3, 8):
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
        #print "typeII at %2d rounds" % nr, "|",

        # for checking type-II distinguishable structure
        if deg == n:
            todo_nr = nr
        else:
            todo_nr = nr - 1

        # for consistency with thesis Table 3.3
        # but actually todo_nr makes more sense for deg = n
        # todo_nr = nr - 1

        num_imp, IMP_TYPES = get_impossible_monomials(todo_nr, n, deg, perm)
        print "%5d impossible monos" % num_imp,
        #print "%5d impossible monomials (%2d types) at %d rounds" % (num_imp, len(IMP_TYPES), todo_nr), ":",
        #print " ".join("%d:%d" % t for t in IMP_TYPES)
        print "attack", todo_nr + 1, "rounds", "  |  ",

        def gettype(x):
            l, r = split_halves(x, h=n)
            return hw(l), hw(r)

        IMP = [mono for mono in xrange(2**(2*n)) if gettype(mono) in IMP_TYPES]
        imp2i = {}
        for i, mono in enumerate(IMP):
            imp2i[mono] = i

        UNK = [mono for mono in xrange(2**n) if 1 <= hw(mono) <= deg]
        unk2i = {}
        for i, mono in enumerate(UNK):
            unk2i[mono] = i

        # precomp
        by_y = []
        for y in xrange(2**n):
            lst = []
            for x in xrange(1, y + 1):
                if x & y == x and hw(x) <= deg:
                    lst.append(x)
            by_y.append(lst)

        impmonos_by_x = []
        for x in xrange(2**(2*n)):
            res = []
            for ix, impmono in enumerate(IMP):
                if x & impmono == x:
                    res.append((ix, impmono))
            impmonos_by_x.append(res)

        ranks = []
        FSPOOL = generate_functions(n, deg, perm, num=200)
        for i in xrange(ITER):
            fs, s, spre = generate_FN_two_last(funcpool=FSPOOL, nr=todo_nr + 1)

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

            ranks.append(m.rank())

            real_anf = fs[-1].mobius()
            sol = matrix(GF(2), len(UNK), n)
            for i, unkmono in enumerate(UNK):
                sol[i] = tobin(real_anf[unkmono], n)

            # actual function satisfies the system?
            assert m * sol == targets

        print "   ", "ranksum", sum(ranks), "iter", ITER, ":", "avg", float(sum(ranks)) / ITER, "/", len(UNK), "  |  ", ranks[:10]
    print



'''
n  3 deg  2 perm  perm |    20 impossible monos attack 5 rounds   |       ranksum 815 iter 200 : avg 4.075 / 6   |   [4, 3, 3, 5, 4, 4, 3, 4, 4, 4]
n  3 deg  2 perm       |    10 impossible monos attack 5 rounds   |       ranksum 781 iter 200 : avg 3.905 / 6   |   [4, 5, 4, 5, 5, 4, 2, 3, 2, 6]
n  3 deg  3 perm       |    53 impossible monos attack 3 rounds   |       ranksum 1320 iter 200 : avg 6.6 / 7   |   [7, 6, 6, 7, 5, 6, 7, 7, 7, 7]

n  4 deg  3 perm  perm |    36 impossible monos attack 5 rounds   |       ranksum 2789 iter 200 : avg 13.945 / 14   |   [14, 14, 14, 14, 14, 14, 14, 14, 14, 14]
n  4 deg  2 perm       |    35 impossible monos attack 5 rounds   |       ranksum 1534 iter 200 : avg 7.67 / 10   |   [8, 6, 7, 9, 9, 8, 8, 6, 7, 8]
n  4 deg  3 perm       |    82 impossible monos attack 4 rounds   |       ranksum 2796 iter 200 : avg 13.98 / 14   |   [14, 14, 14, 14, 14, 14, 14, 14, 14, 14]
n  4 deg  4 perm       |   236 impossible monos attack 3 rounds   |       ranksum 3000 iter 200 : avg 15.0 / 15   |   [15, 15, 15, 15, 15, 15, 15, 15, 15, 15]

n  5 deg  4 perm  perm |    62 impossible monos attack 5 rounds   |       ranksum 6000 iter 200 : avg 30.0 / 30   |   [30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
n  5 deg  2 perm       |    56 impossible monos attack 6 rounds   |       ranksum 3000 iter 200 : avg 15.0 / 15   |   [15, 15, 15, 15, 15, 15, 15, 15, 15, 15]
n  5 deg  3 perm       |    31 impossible monos attack 5 rounds   |       ranksum 4821 iter 200 : avg 24.105 / 25   |   [23, 23, 25, 23, 23, 24, 24, 24, 24, 24]
n  5 deg  4 perm       |   197 impossible monos attack 4 rounds   |       ranksum 6000 iter 200 : avg 30.0 / 30   |   [30, 30, 30, 30, 30, 30, 30, 30, 30, 30]

...

'''

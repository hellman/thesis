#-*- coding:utf-8 -*-

dp = [
    [(16, 2), (9, 10)],
    [(24, 2), (11, 11)],
    [(32, 2), (11, 12)],
    [(48, 2), (13, 13)],
    [(64, 2), (13, 14)],

    [(32, 5), (6, 6)],
    [(48, 5), (7, 7)],
    [(64, 5), (7, 7)],

    [(32, 7), (5, 5)],
    [(48, 7), (5, 6)],
    [(64, 7), (6, 6)],

    [(32, 31), (4, 5)],
    [(48, 47), (4, 5)],
    [(64, 63), (4, 5)],

    [(32, 32), (3, None)],
    [(48, 48), (3, None)],
    [(64, 64), (3, None)],
]

def getnbij(n, d):
    for r in xrange(1, 100):
        flo = (r-2)//2
        ceil = (r-2) - flo

        if pow(d, flo) + pow(d, ceil) >= 2*n:
            return r - 1
    assert 0

def getbij(n, d, di):
    for r in xrange(1, 100):
        flo = (r-5)//2
        ceil = (r-5) - flo

        if di * (pow(d, flo) + pow(d, ceil)) >= 2*n:
            return r - 1
    assert 0

for (n, d), (rn, rb) in dp:

    tn = getnbij(n, d)
    print "n %2d d %2d: dp %2d vs my %2d" % (n, d, rn, tn), "|", rb, getbij(n,d, d), getbij(n, d, n-1)

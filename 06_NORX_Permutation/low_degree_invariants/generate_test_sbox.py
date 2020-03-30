#-*- coding:utf-8 -*-

'''
Generate an S-Box with low-degree invariant,
to test the algorithm
'''

from sage.all import *

from cryptools.env import *

N = 16 # bits
T = 11 # invariant degree

TMASK = (1 << T) - 1

inv = SBox2( int(x & TMASK == TMASK) for x in xrange(2**N) )

vs = range(2**N)

x0 = [v for v in vs if inv[v] == 0]
x1 = [v for v in vs if inv[v] == 1]

y0 = [v for v in vs if inv[v] == 0]
y1 = [v for v in vs if inv[v] == 1]

shuffle(y0)
shuffle(y1)

s = [None] * 2**N
for x, y in zip(x0, y0):
    s[x] = y
for x, y in zip(x1, y1):
    s[x] = y

s = SBox2(s)

print inv.degrees()
print s.degrees()

cycles = sorted(s.cycles(), key=len, reverse=True)
print "invariant values on cycles:"
for c in cycles:
    print inv[c[0]],
print
with open("test16.h", "w") as f:
    f.write("const int BITS = %d;\n" % N)
    f.write("uint32_t sbox[%d] = {\n" % 2**N)
    f.write(",".join("0x%04x" % y for y in s) + "\n")
    f.write("};\n")

    f.write("vector<pair<uint32_t, uint32_t>> cycles = {\n")
    for c in cycles:
        f.write("{0x%04x, %d},\n" % (c[0], len(c)))
    f.write("};\n")



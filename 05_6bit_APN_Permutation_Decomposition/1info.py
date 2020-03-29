from sage.all import *
from cryptools.env import *

from common import S0


# print table for latex

if 1:
    T = [S0[i:i+16] for i in xrange(0, len(S0), 16)]
    res = [r""]
    for x in xrange(16):
        res.append(r"$\hex{.%1x}$" % x)
    print " & ".join(res) + r"\\"
    print

    for k in xrange(len(T)):
        res = [r"${\hex{%1x.}}$" % k]
        for x in xrange(16):
            res.append(r"$\hex{%02x}$" % T[k][x])
        print " & ".join(res) + r"\\"

# ----------------------------------
# 1. look at the LAT
# ----------------------------------
lat = 2*S0.lat(zero_zero=True, abs=True)
save_plot(lat, "0_Dillon_LAT.png", cmap="gray_r")

# ----------------------------------
# 2. align columns to get white square
# ----------------------------------
columns_coordinates = [4, 10, 14, 16, 20, 26, 30]

c = [4, 10, 16]
eta = matrix(GF(2), 6, 6)
for i in xrange(3):
    eta.set_column(5-i, tobin(c[i], 6))

for i in xrange(3):
    for vec in product(range(2), repeat=6):
        vec = vector(GF(2), vec)
        if vec not in eta.column_space():
            eta.set_column(2-i, vec)
            break
assert not eta.is_singular()

print "eta"
print eta.str()

etat = SBox2.gen.from_matrix(eta.transpose())
print "etat = SBox2(%s)" % etat

eta_S0 = etat * S0
print "eta_S0 = SBox2(%s)" % eta_S0

lat = 2*eta_S0.lat(zero_zero=True, abs=True)
save_plot(lat, "1_aligned_LAT.png", cmap="gray_r")

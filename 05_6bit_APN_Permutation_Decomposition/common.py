from sage.all import inverse_mod
from cryptools.env import *

def compress(mat):
    s = sorted(set(mat.list()))
    inv = {v: i for i, v in enumerate(s)}
    return mat.apply_map(inv.__getitem__)

def colfreq(mat):
    mat = mat[:,:]
    for x in xrange(0, mat.ncols()):
        col = mat.column(x)
        cnt = Counter(col)
        col = col.apply_map(cnt.__getitem__)
        mat.set_column(x, col)
    return mat

def rowfreq(mat):
    return colfreq(mat.transpose()).transpose()

def print_latex_minicipher(T, name, extend=None):
    for k in xrange(len(T)):
        res = [r"$" + name + r"_{\hex{%1X}}$" % k]
        for x in xrange(8):
            res.append(r"$\hex{%1x}$" % T[k][x])
        if extend:
            res += list(extend[k])
        print " & ".join(res) + r"\\"

def print_latex_func(f, name):
    print name, "~&~",
    res = []
    for y in f:
        res.append(r"$\hex{%1x}$" % y)
    print " & ".join(res) + r"\\"

def print_latex_lookup(f, name):
    res = []
    for y in f:
        res.append(r"\hex{%1x}" % y)
    print r"\lookup{%s} = (%s)" % (name, ",".join(res))

def print_latex_matrix(mat, name):
    print name + r" = \matb{"
    for row in mat:
        print " & ".join(map(str, row)), r"\\"
    print "}"

S0 = SBox2([
      0x00,  0x36,  0x30,  0x0d,  0x0f,  0x12,  0x35,  0x23,  0x19,  0x3f,  0x2d,  0x34,  0x03,  0x14,  0x29,  0x21,
      0x3b,  0x24,  0x02,  0x22,  0x0a,  0x08,  0x39,  0x25,  0x3c,  0x13,  0x2a,  0x0e,  0x32,  0x1a,  0x3a,  0x18,
      0x27,  0x1b,  0x15,  0x11,  0x10,  0x1d,  0x01,  0x3e,  0x2f,  0x28,  0x33,  0x38,  0x07,  0x2b,  0x2c,  0x26,
      0x1f,  0x0b,  0x04,  0x1c,  0x3d,  0x2e,  0x05,  0x31,  0x09,  0x06,  0x17,  0x20,  0x1e,  0x0c,  0x37,  0x16,
])

etat = SBox2((0, 8, 18, 26, 1, 9, 19, 27, 2, 10, 16, 24, 3, 11, 17, 25, 4, 12, 22, 30, 5, 13, 23, 31, 6, 14, 20, 28, 7, 15, 21, 29, 32, 40, 50, 58, 33, 41, 51, 59, 34, 42, 48, 56, 35, 43, 49, 57, 36, 44, 54, 62, 37, 45, 55, 63, 38, 46, 52, 60, 39, 47, 53, 61))
eta_S0 = SBox2((0, 55, 36, 11, 25, 22, 45, 58, 14, 61, 43, 37, 26, 5, 42, 40, 60, 33, 18, 50, 16, 2, 46, 41, 39, 30, 48, 17, 54, 20, 52, 6, 59, 28, 13, 12, 4, 15, 8, 53, 57, 34, 62, 38, 27, 56, 35, 51, 29, 24, 1, 7, 47, 49, 9, 44, 10, 19, 31, 32, 21, 3, 63, 23))

T = map(SBox2, [(0, 6, 4, 7, 3, 1, 5, 2),
 (7, 5, 1, 6, 4, 2, 0, 3),
 (4, 3, 2, 0, 5, 6, 1, 7),
 (3, 5, 2, 1, 4, 6, 7, 0),
 (1, 2, 0, 6, 4, 3, 7, 5),
 (6, 5, 2, 4, 7, 0, 1, 3),
 (5, 2, 6, 4, 0, 3, 1, 7),
 (2, 0, 1, 6, 5, 3, 4, 7)]
)
U = map(SBox2, [(0, 3, 6, 4, 2, 7, 1, 5),
 (7, 4, 0, 2, 3, 6, 1, 5),
 (1, 4, 2, 6, 3, 0, 5, 7),
 (7, 2, 5, 1, 3, 0, 4, 6),
 (7, 3, 4, 1, 0, 2, 6, 5),
 (3, 7, 1, 4, 2, 0, 5, 6),
 (1, 3, 7, 4, 6, 2, 5, 0),
 (4, 6, 3, 0, 5, 1, 7, 2)]
)

Mu = SBox2((0, 9, 59, 50, 4, 13, 63, 54, 40, 33, 19, 26, 44, 37, 23, 30, 32, 41, 27, 18, 36, 45, 31, 22, 8, 1, 51, 58, 12, 5, 55, 62, 16, 25, 43, 34, 20, 29, 47, 38, 56, 49, 3, 10, 60, 53, 7, 14, 48, 57, 11, 2, 52, 61, 15, 6, 24, 17, 35, 42, 28, 21, 39, 46))
Mup = SBox2((0, 9, 27, 18, 12, 5, 23, 30, 8, 1, 19, 26, 4, 13, 31, 22, 48, 57, 43, 34, 60, 53, 39, 46, 56, 49, 35, 42, 52, 61, 47, 38, 40, 33, 51, 58, 36, 45, 63, 54, 32, 41, 59, 50, 44, 37, 55, 62, 24, 17, 3, 10, 20, 29, 15, 6, 16, 25, 11, 2, 28, 21, 7, 14))


X = GF(2).polynomial_ring().gen()
F3 = GF(2**3, name='w', modulus=X**3 + X + 1)
fromF = lambda x: x.integer_representation()
toF = F3.fetch_int

F6 = GF(2**6, name='v')

x = PolynomialRing(F3, names='x').gen()
inv = SBox2.gen.from_poly(x**6)

w = F3.gen()
assert w**3 + w + 1 == 0

fexp = SBox2([0] + [(w**i).integer_representation() for i in xrange(1, 8)])
flog = ~fexp
# fexp (0, 2, 4, 3, 6, 7, 5, 1)
# flog (0, 7, 1, 3, 2, 6, 4, 5)


texlog_list = [r"{\WZ}"] + [r"\WW^%d" % flog[i] for  i in xrange(1, 8)]
def texlog(c):
    if not isinstance(c, int):
        c = c.integer_representation()
    return texlog_list[c]


def texpoly(poly, no7=True, no0=False, linear=False):
    coeffs = list(poly) + [0] * 8
    res = []
    for e in xrange(8):
        if linear and e in (3, 5, 6):
            assert coeffs[e] == 0
            continue
        if no0 and e == 0:
            assert coeffs[e] == 0
            continue
        if no7 and e == 7:
            assert coeffs[e] == 0
            continue
        if e == 0:
            res.append(texlog(coeffs[0]))
        elif e == 1:
            res.append(texlog(coeffs[e]) + "x")
        else:
            res.append(texlog(coeffs[e]) + "x^%d" % e)
    return "$" + " + ".join(res[::-1]) + "$"

q = SBox2((0, 7, 6, 1, 5, 2, 3, 4)) # (w + 1)*x^4 + (w^2 + w + 1)*x^2 + (w + 1)*x
z = SBox2((0, 3, 7, 4, 2, 1, 5, 6)) # x^4 + w^2*x^2 + (w^2 + w)*x


def openButterfly(e, alpha, n=3, sx=False, sy=False):
    F = GF(2**n, name='w')
    if n == 3:
        assert F == F3
    ei = inverse_mod(e, 2**n-1)
    alpha = F.fetch_int(alpha)
    s = []
    for x, k in product(range(2**n), range(2**n)):
        x = F.fetch_int(x)
        k = F.fetch_int(k)
        x += k**e
        x = x**ei
        if sx: x, k = k, x
        x += alpha*k
        x, k = k, x
        x += alpha*k
        if sy: x, k = k, x
        x = x**e
        x += k**e
        x = x.integer_representation()
        k = k.integer_representation()
        s.append((x << n) | k)
    return SBox2(s)

def closedButterfly(e, alpha, n=3):
    F = GF(2**n, name='w')
    if n == 3:
        assert F == F3
    alpha = F.fetch_int(alpha)
    s = []
    for x, y in product(range(2**n), range(2**n)):
        x = F.fetch_int(x)
        y = F.fetch_int(y)

        l = (x + alpha*y)**e + y**e
        r = (y + alpha*x)**e + x**e
        l = l.integer_representation()
        r = r.integer_representation()
        s.append((l << n) | r)
    return SBox2(s)

def interpolate2x2(mat):
    subs = [mat[3*i:3*i+3,3*j:3*j+3] for i in xrange(2) for j in xrange(2)]
    res = []
    for sub in subs:
        lin = SBox2.gen.from_matrix(sub)
        lin.n = 3
        res.append(lin.interpolation_polynomial(F3))
    return res

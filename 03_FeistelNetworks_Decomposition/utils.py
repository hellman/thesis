from cryptools.sagestuff import identity_matrix, GF, shuffle

# MATRIX 2x2
def mat2blocks(mat):
    assert mat.nrows() == mat.ncols()
    n = mat.nrows()/2
    res = [[None, None], [None, None]]
    for i in xrange(2):
        for j in xrange(2):
            res[i][j] = mat[i*n:i*n+n,j*n:j*n+n]
    return res

def UL2(mat):
    bs = mat2blocks(mat)
    d = bs[1][1]
    if d.is_singular():
        raise ZeroDivisionError("no UL2 decomposition")
    a = (~d)*bs[1][0]
    c = bs[0][1]*(~d)
    b = bs[0][0] + c * d * a
    return (a, b, c, d)

def idlo(mat):
    """
    I   0
    mat I
    """
    assert mat.nrows() == mat.ncols()
    n = mat.nrows()
    res = identity_matrix(GF(2), 2*n)
    res[n:,:n] = mat
    return res

def idup(mat):
    """
    I mat
    0  I
    """
    assert mat.nrows() == mat.ncols()
    n = mat.nrows()
    res = identity_matrix(GF(2), 2*n)
    res[:n,n:] = mat
    return res

def diag(a, b):
    """
    a 0
    0 b
    """
    assert a.nrows() == a.ncols() == b.nrows() == b.ncols()
    n = a.nrows()
    res = identity_matrix(GF(2), 2*n)
    res[:n,:n] = a
    res[n:,n:] = b
    return res

from cryptools.utils import sage_cache
from cryptools.sbox2 import SBox2

@sage_cache("data/functions")
def generate_functions(n, deg, perm, num=100):
    if perm:
        assert deg == n - 1
        return [SBox2.gen.random_permutation(n) for _ in xrange(num)]
    else:
        return [SBox2.gen.random_sbox_of_degree(n, n, deg) for _ in xrange(num)]

def generate_FN_two_last(funcpool, nr):
    shuffle(funcpool)
    fs = funcpool[:nr]
    s = SBox2.gen.feistel_network_xor(funcs=fs)
    spre = SBox2.gen.feistel_network_xor(funcs=fs[:-1])
    return fs, s, spre

def generate_FN(funcpool, nr):
    shuffle(funcpool)
    fs = funcpool[:nr]
    s = SBox2.gen.feistel_network_xor(funcs=fs)
    return fs, s

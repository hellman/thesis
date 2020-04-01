#include <bits/stdc++.h>

using namespace std;

// short loops...
#define CONCAT3_NX(x, y, z) x ## y ## z
#define CONCAT3(x, y, z) CONCAT3_NX(x, y, z)
#define VAR(name) CONCAT3(__tmpvar__, name, __LINE__)
#define TYPE(x) __typeof(x)

#define FOR(i, s, n)  for (TYPE(n) i=(s),   VAR(end)=(n);  i <  VAR(end);  i++)
#define RFOR(i, s, n) for (TYPE(n) i=(n)-1, VAR(end)=(s);  i >= VAR(end);  i--)
#define FORN(i, n)    FOR(i, 0, n)
#define RFORN(i, n)   RFOR(i, 0, n)
#define FOREACH(i, v) for (auto& i: v)

typedef uint8_t byte;
typedef long long LL;
typedef unsigned long long ULL;

// main code
const int ROTS[4] = {1, 3, 5, 7};

byte ROL(const byte value, int shift) {
    return (value << shift) | (value >> (8 - shift));
}

byte ROR(const byte value, int shift) {
    return (value >> shift) | (value << (8 - shift));
}

inline byte H(byte x, byte y) {
    return x ^ y ^ ((x & y) << 1);
}

#ifdef TEST_SBOX
#include "test16.h"
#endif

union Value {
    uint32_t as_int;
    byte as_bytes[4];
};

inline void applyG(Value &v) {
#ifdef TEST_SBOX
    v.as_int = sbox[v.as_int];
    return;
#endif

    byte *bytes = v.as_bytes;

    // 0xaabbccdd -> memory {0xdd, 0xcc, 0xbb, 0xaa}
    byte &a = bytes[3];
    byte &b = bytes[2];
    byte &c = bytes[1];
    byte &d = bytes[0];

    a = H(a, b);
    d = ROR(a ^ d, ROTS[0]);
    c = H(c, d);
    b = ROR(b ^ c, ROTS[1]);

    a = H(a, b);
    d = ROR(a ^ d, ROTS[2]);
    c = H(c, d);
    b = ROR(b ^ c, ROTS[3]);
}


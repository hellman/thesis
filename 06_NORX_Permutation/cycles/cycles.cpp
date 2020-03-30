#include "header.cpp"

int main() {
    vector<bool> visited(1ll << 32);

    printf("vector<pair<uint32_t, uint32_t>> cycles = {\n");
    Value t;
    FORN(val, 1ll << 32) {
        if (visited[val]) continue;
        visited[val] = 1;

        t.as_int = val;

        LL cyclen = 1;
        applyG(t);
        while (t.as_int != val) {
            assert(!visited[t.as_int]);
            visited[t.as_int] = 1;

            cyclen++;
            applyG(t);
        }

        printf("    {0x%08x, %lld},\n", (uint32_t)val, cyclen);
    }
    printf("};\n");
    return 0;
}

/*

g++ -O3 -std=c++11 cycles.cpp -o cycles && time ./cycles >cycles.out

real    2m13.381s

sorted manually

vector<pair<uint32_t, uint32_t>> cycles = {
    {0x00000001, 3294443807},
    {0x00000008, 621984749},
    {0x00000056, 212798071},
    {0x00000007, 56236016},
    {0x00000006, 55712043},
    {0x00000002, 21461014},
    {0x00000229, 9062510},
    {0x00000452, 7374122},
    {0x00000046, 7328319},
    {0x0000084e, 5608893},
    {0x000001f7, 2463170},
    {0x00002b65, 399843},
    {0x00021c06, 52972},
    {0x00005c28, 23344},
    {0x000000d5, 8301},
    {0x0000b8d2, 6339},
    {0x000594d3, 2124},
    {0x016626d2, 848},
    {0x004e63c1, 595},
    {0x009d2bc3, 137},
    {0x034f696c, 78},
    {0x00000000, 1},
};
*/

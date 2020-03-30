#ifdef TEST_SBOX
#include "header.cpp"
#else
#include "header.cpp"
const int BITS = 32;
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
#endif

const int MAX_CYCLE_POOL = 1 << 24;

vector<vector<uint32_t>> pool;

uint32_t sample(int id) {
    assert(id < pool.size());
    LL index = random() % pool[id].size();
    return pool[id][index];
}

int main(int argc, char *argv[]) {
    vector<uint16_t> val2id(1ll << BITS);
    assert(cycles.size() < 1<<16);

    vector<uint8_t> touched(1ll << BITS);
    LL ntouched = 0;

    int NR = atoi(argv[1]);
    fprintf(stderr, "Using %d rounds iterated version. Cycles:\n", NR);

    Value t;
    vector<pair<uint32_t, uint32_t>> cycles2;
    FORN(id, (int)cycles.size()) {
        t.as_int = cycles[id].first;
        LL cyclen = cycles[id].second;
        LL g = __gcd(cyclen, (LL)NR);
        FORN(i, g) {
            cycles2.push_back({t.as_int, cyclen/g});
            fprintf(stderr, "{0x%08x, %lld}\n", t.as_int, cyclen/g);
            applyG(t);
        }
    }
    fprintf(stderr, "\n");

    cycles = cycles2;
    pool.resize(cycles.size());
    assert(cycles.size() < 1<<16); // cycle id !!! uint16_t

    fprintf(stderr, "total: %lu cycles\n", cycles.size());
    FORN(id, (int)cycles.size()) {
        t.as_int = cycles[id].first;
        LL cyclen = cycles[id].second;
        fprintf(stderr, "cyclen %d: %08x (%08llx=%lld len)\n", id, t.as_int, cyclen, cyclen);

        FORN(j, (LL)cyclen) {
            val2id[t.as_int] = id;
            assert(touched[t.as_int] == 0);
            touched[t.as_int] = 1;
            ntouched++;

            if (pool[id].size() < MAX_CYCLE_POOL) {
                pool[id].push_back(t.as_int);
            }
            else {
                LL r = random() % cyclen;
                if (r <= MAX_CYCLE_POOL) {
                    LL index = random() % pool[id].size();
                    pool[id][index] = t.as_int;
                }
            }
            FORN(j, NR) applyG(t);
        }
    }
    fprintf(stderr, "precomputation done\n");

    assert(ntouched == 1ll << BITS);
    FORN(v, 1ll<<BITS) {
        assert(touched[v] == 1);
    }

    // a faster approach to obtain all results
    FORN(i, (int)cycles.size()+50) {
        vector<uint32_t> basis;
        vector<uint32_t> space = {0};
        space.reserve(1ll << BITS);
        vector<uint8_t> is_in_space(1ll << BITS, 0);
        is_in_space[0] = 1;

        vector<uint8_t> parity(cycles.size(), 0);

        uint32_t offset = sample(i % pool.size());
        parity[val2id[offset^0]] ^= 1;

        FOR(dim, 1, BITS+1) {
            // dim BITS is unique equation
            if (dim == BITS and i >= 2) break;

            fprintf(stderr, "eq %d dim %d\n", i, dim);

            uint32_t w;
            while (1) {
                w = sample(random() % pool.size()) ^ offset;
                if (is_in_space[w] == 0) break;
            }

            basis.push_back(w);
            auto space_old = space;
            FOREACH(u, space_old) {
                space.push_back(u ^ w);
                assert(is_in_space[u ^ w]  == 0);
                is_in_space[u ^ w] = 1;

                uint32_t v = u ^ w ^ offset;
                parity[val2id[v]] ^= 1;
            }

            // (dim, offset, [basis_vectors], [equation]),
            printf("(%d, 0x%08x, [", dim, offset);
            FOREACH(v, basis) printf("0x%08x,", v);
            printf("], [");
            int psum = 0;
            FOREACH(p, parity) {
                printf("%d,", p);
                psum ^= p;
            }
            assert(psum == 0);
            printf("]),\n");
        }
        fflush(stdout);
        fflush(stderr);
    }
    return 0;

    // an approach to obtain faster results for lower dimensions
    // FOR(dim, 1, BITS) {
    //     fprintf(stderr, "dim %d\n", dim);
    //     FORN(i, 100) {
    //         vector<uint8_t> parity(cycles.size());

    //         fprintf(stderr, "dim %d eq %d\n", dim, i);

    //         unordered_set<uint32_t> space = {0};
    //         vector<uint32_t> basis;
    //         uint32_t offset = sample(i % pool.size());
    //         while (1) {
    //             uint32_t w = sample(random() % pool.size()) ^ offset;
    //             if (space.find(w) != space.end()) continue;

    //             auto space_old = space;
    //             FOREACH(u, space_old)
    //                 space.insert(u ^ w);
    //             basis.push_back(w);

    //             if (space.size() >= (1ll << dim)) {
    //                 FOREACH(w, space) {
    //                     uint32_t v = offset ^ w;
    //                     parity[val2id[v]] ^= 1;
    //                 }
    //                 break;
    //             }
    //         }

    //         // (dim, offset, [basis_vectors], [equation]),
    //         printf("(%d, 0x%08x, [", dim, offset);
    //         FOREACH(v, basis) printf("0x%08x,", v);
    //         printf("], [");
    //         FOREACH(p, parity) printf("%d,", p);
    //         printf("]),\n");
    //     }
    // }

    // return 0;
}

/*

g++ -O3 -std=c++11 invariant_equations.cpp -o invariant_equations && time ./invariant_equations >invariant_equations.txt


*/

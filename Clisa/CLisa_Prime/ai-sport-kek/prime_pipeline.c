#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <pthread.h>
#include <sys/random.h>
#include <string.h>

//------------------------------------------------------------------------------
// Worker context for recursive random generation.
//------------------------------------------------------------------------------
typedef struct {
    unsigned char *buffer;   // Pointer to the target buffer region
    size_t length;           // Number of bytes to generate
    int depth;               // Current recursion depth
} WorkerCtx;

#define MAX_DEPTH   5       // Avoid unbounded thread creation
#define SMALL_CHUNK 32      // Threshold where recursion stops

//------------------------------------------------------------------------------
// Fetch a single random byte using getrandom.
//------------------------------------------------------------------------------
static unsigned char random_byte() {
    unsigned char b;
    if (getrandom(&b, 1, 0) != 1) {
        perror("getrandom");
        exit(EXIT_FAILURE);
    }
    return b;
}

//------------------------------------------------------------------------------
// Fill a buffer with random bytes sequentially.
//------------------------------------------------------------------------------
static void fill_random(unsigned char *buf, size_t len) {
    if (getrandom(buf, len, 0) != (ssize_t)len) {
        perror("getrandom");
        exit(EXIT_FAILURE);
    }
}

//------------------------------------------------------------------------------
// Thread entry that simply calls fill_random.
//------------------------------------------------------------------------------
static void *fill_random_thread(void *arg) {
    WorkerCtx ctx = *(WorkerCtx *)arg;
    fill_random(ctx.buffer, ctx.length);
    return NULL;
}

//------------------------------------------------------------------------------
// Recursive worker splitting the buffer and spawning two threads per call.
//------------------------------------------------------------------------------
static void *entropy_worker(void *arg) {
    WorkerCtx ctx = *(WorkerCtx *)arg;

    // Base case: small chunk or max depth reached.
    if (ctx.length <= SMALL_CHUNK || ctx.depth >= MAX_DEPTH) {
        fill_random(ctx.buffer, ctx.length);
        return NULL;
    }

    pthread_t t1, t2;
    size_t mid = ctx.length / 2;
    WorkerCtx left  = { ctx.buffer,        mid,           ctx.depth + 1 };
    WorkerCtx right = { ctx.buffer + mid,  ctx.length - mid, ctx.depth + 1 };

    pthread_create(&t1, NULL, entropy_worker, &left);
    pthread_create(&t2, NULL, entropy_worker, &right);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return NULL;
}

//------------------------------------------------------------------------------
// Convert a byte buffer to a 64-bit integer (little-endian).
//------------------------------------------------------------------------------
static uint64_t buf_to_u64(unsigned char *buf, size_t len) {
    uint64_t val = 0;
    size_t copy = len < sizeof(uint64_t) ? len : sizeof(uint64_t);
    memcpy(&val, buf, copy);
    return val;
}

//------------------------------------------------------------------------------
// Modular exponentiation (a^d mod n) using 128-bit intermediates.
//------------------------------------------------------------------------------
static uint64_t mod_pow(uint64_t a, uint64_t d, uint64_t n) {
    __uint128_t res = 1;
    __uint128_t base = a % n;
    while (d) {
        if (d & 1)
            res = (res * base) % n;
        base = (base * base) % n;
        d >>= 1;
    }
    return (uint64_t)res;
}

//------------------------------------------------------------------------------
// Deterministic Miller-Rabin for 64-bit integers.
//------------------------------------------------------------------------------
static int is_probably_prime(uint64_t n) {
    if (n < 2) return 0;
    if (n % 2 == 0) return n == 2;

    // Write n-1 as 2^r * d with d odd
    uint64_t d = n - 1;
    unsigned int r = 0;
    while ((d & 1) == 0) {
        d >>= 1;
        r++;
    }

    static const uint64_t bases[] = {2ULL, 3ULL, 5ULL, 7ULL, 11ULL};
    for (size_t i = 0; i < sizeof(bases)/sizeof(bases[0]); ++i) {
        uint64_t a = bases[i] % n;
        if (a == 0) return 1;
        uint64_t x = mod_pow(a, d, n);
        if (x == 1 || x == n - 1) continue;
        int witness = 1;
        for (unsigned int j = 1; j < r; ++j) {
            x = mod_pow(x, 2, n);
            if (x == n - 1) {
                witness = 0;
                break;
            }
        }
        if (witness) return 0;
    }
    return 1;
}

//------------------------------------------------------------------------------
// Worker that generates a random number, tests primality and prints result.
//------------------------------------------------------------------------------
static void *prime_worker(void *arg) {
    size_t bytes = *(size_t *)arg;
    unsigned char *buf = malloc(bytes);
    if (!buf) {
        perror("malloc");
        return NULL;
    }

    WorkerCtx root = { buf, bytes, 0 };
    entropy_worker(&root);

    uint64_t candidate = buf_to_u64(buf, bytes);
    printf("0x");
    for (size_t i = 0; i < bytes; ++i)
        printf("%02x", buf[i]);

    if (is_probably_prime(candidate))
        printf(" -> probable prime\n");
    else
        printf(" -> composite\n");

    free(buf);
    return NULL;
}

int main(int argc, char *argv[]) {
    size_t workers = 4;   // number of parallel prime jobs
    size_t bytes   = 8;   // bytes per number
    size_t count   = 10;  // how many numbers to generate

    if (argc > 1) count   = strtoull(argv[1], NULL, 10);
    if (argc > 2) workers = strtoull(argv[2], NULL, 10);
    if (argc > 3) bytes   = strtoull(argv[3], NULL, 10);

    for (size_t i = 0; i < count; i += workers) {
        pthread_t threads[workers];
        for (size_t w = 0; w < workers && i + w < count; ++w)
            pthread_create(&threads[w], NULL, prime_worker, &bytes);
        for (size_t w = 0; w < workers && i + w < count; ++w)
            pthread_join(threads[w], NULL);
    }
    return 0;
}


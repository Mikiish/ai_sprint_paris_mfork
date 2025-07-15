#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <pthread.h>
#include <sys/random.h>
#include <string.h>
#include <time.h>

/* -------------------------------------------------------------------------
 * Simple recursive worker structure for filling a buffer with random bytes.
 * Each worker knows the buffer segment it must fill and its recursion depth.
 * -------------------------------------------------------------------------*/
typedef struct {
    unsigned char *buffer; // start of the buffer
    size_t start;          // inclusive index
    size_t end;            // exclusive index
    int depth;             // recursion depth
} Worker;

#define MAX_DEPTH 7        // 2^7 = 128 threads max
#define MIN_CHUNK 1        // stop splitting below this size

/* Fill a region of memory with random bytes using getrandom(2). */
static void fill_random(unsigned char *buf, size_t len) {
    if (getrandom(buf, len, 0) != (ssize_t)len) {
        perror("getrandom");
        pthread_exit(NULL);
    }
}

/* Thread routine: recursively split the work until chunks are small enough. */
static void *worker_func(void *arg) {
    Worker ctx = *(Worker *)arg; // copy of the context
    size_t len = ctx.end - ctx.start;
    if (len <= MIN_CHUNK || ctx.depth >= MAX_DEPTH) {
        fill_random(ctx.buffer + ctx.start, len);
        return NULL;
    }

    size_t mid = ctx.start + len / 2;
    pthread_t t1, t2;
    Worker left  = { ctx.buffer, ctx.start, mid, ctx.depth + 1 };
    Worker right = { ctx.buffer, mid, ctx.end, ctx.depth + 1 };
    pthread_create(&t1, NULL, worker_func, &left);
    pthread_create(&t2, NULL, worker_func, &right);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return NULL;
}

/* -------------------------------------------------------------------------
 * Modular multiplication and exponentiation helpers for 64-bit numbers.
 * We use __uint128_t internally to avoid overflow when computing a*b mod m.
 * -------------------------------------------------------------------------*/
static uint64_t mod_mul(uint64_t a, uint64_t b, uint64_t m) {
    return ((unsigned __int128)a * b) % m;
}

static uint64_t mod_pow(uint64_t base, uint64_t exp, uint64_t mod) {
    uint64_t result = 1;
    while (exp) {
        if (exp & 1)
            result = mod_mul(result, base, mod);
        base = mod_mul(base, base, mod);
        exp >>= 1;
    }
    return result;
}

/* Deterministic Miller-Rabin test for 64-bit integers. */
static int is_probable_prime(uint64_t n) {
    if (n < 2) return 0;
    static const uint64_t small_primes[] = {2ULL,3ULL,5ULL,7ULL,11ULL,13ULL,17ULL,19ULL,23ULL,0};
    for (size_t i = 0; small_primes[i]; ++i) {
        if (n % small_primes[i] == 0)
            return n == small_primes[i];
    }

    int r = 0;
    uint64_t d = n - 1;
    while ((d & 1) == 0) { d >>= 1; r++; }

    static const uint64_t bases[] = {2ULL,325ULL,9375ULL,28178ULL,450775ULL,9780504ULL,1795265022ULL,0};
    for (size_t i = 0; bases[i]; ++i) {
        uint64_t a = bases[i] % n;
        if (a == 0) return 1;
        uint64_t x = mod_pow(a, d, n);
        if (x == 1 || x == n - 1) continue;
        int witness = 1;
        for (int j = 1; j < r; ++j) {
            x = mod_mul(x, x, n);
            if (x == n - 1) { witness = 0; break; }
        }
        if (witness) return 0;
    }
    return 1;
}

/* Convert a byte buffer to a hexadecimal string. */
static void to_hex(const unsigned char *buf, size_t len, char *out) {
    static const char hex[] = "0123456789abcdef";
    for (size_t i = 0; i < len; ++i) {
        out[i*2]     = hex[(buf[i] >> 4) & 0xF];
        out[i*2 + 1] = hex[buf[i] & 0xF];
    }
    out[len*2] = '\0';
}

/* Entry point: generate N primes using up to 128 threads per iteration. */
int main(int argc, char *argv[]) {
    size_t total = 5; // number of primes to find
    if (argc > 1) {
        total = strtoull(argv[1], NULL, 10);
        if (total == 0) {
            fprintf(stderr, "Invalid count\n");
            return EXIT_FAILURE;
        }
    }

    const size_t BYTES = 8; // 64-bit numbers
    unsigned char buffer[BYTES];
    char hexstr[BYTES*2 + 1];

    size_t found = 0;
    while (found < total) {
        Worker root = { buffer, 0, BYTES, 0 };
        worker_func(&root);

        uint64_t value = 0;
        for (size_t i = 0; i < BYTES; ++i)
            value = (value << 8) | buffer[i];

        // Ensure odd candidate
        value |= 1ULL;
        to_hex(buffer, BYTES, hexstr);
        printf("Candidate 0x%s\n", hexstr);

        if (is_probable_prime(value)) {
            printf(" -> prime!\n");
            found++;
        }
    }
    return 0;
}


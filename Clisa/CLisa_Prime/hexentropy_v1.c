#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/random.h>
#include <string.h>

/*-----------------------------------------------------------------------
 * Helper: print_binary
 *   Display a buffer in binary, grouping bits by nibble for readability.
 *   Each byte is printed MSB first with spaces between nibbles and bytes.
 *---------------------------------------------------------------------*/
static void print_binary(const unsigned char *buf, size_t len) {
    for (size_t i = 0; i < len; ++i) {
        unsigned char b = buf[i];
        for (int bit = 7; bit >= 0; --bit) {
            printf("%d", (b >> bit) & 1);
            if (bit % 4 == 0 && bit != 0)
                putchar(' ');  // separate nibbles
        }
        if (i != len - 1)
            putchar(' ');      // separate bytes
    }
    putchar('\n');
}

// Context passed to each thread
typedef struct {
    unsigned char *buffer;  // pointer to buffer region
    size_t length;          // bytes to generate
    int depth;              // recursion depth
} WorkerCtx;

#define MAX_DEPTH 4      // limit recursion to avoid CPU explosion
#define SMALL_CHUNK 32   // below this, just fill sequentially

// Return a random bit using getrandom
static int random_bit() {
    unsigned char b;
    if (getrandom(&b, 1, 0) != 1) {
        perror("getrandom");
        exit(EXIT_FAILURE);
    }
    return b & 1;
}

// Fill buffer with random bytes
static void fill_random(unsigned char *buf, size_t len) {
    if (getrandom(buf, len, 0) != (ssize_t)len) {
        perror("getrandom");
        exit(EXIT_FAILURE);
    }
}

// Wrapper to use fill_random as a thread routine
static void *fill_random_thread(void *arg) {
    WorkerCtx ctx = *(WorkerCtx *)arg;
    fill_random(ctx.buffer, ctx.length);
    return NULL;
}

/*-----------------------------------------------------------------------
 * hexentropy_worker
 *   Recursive worker implementing the parity-based strategy. The buffer is
 *   split in two halves and processed in parallel. Even segments recurse,
 *   odd segments spawn simple fill threads.
 *---------------------------------------------------------------------*/
static void *hexentropy_worker(void *arg) {
    WorkerCtx ctx = *(WorkerCtx *)arg; // copy context

    if (ctx.length == 0)
        return NULL;

    // Base case: small chunk or depth limit
    if (ctx.length <= SMALL_CHUNK || ctx.depth >= MAX_DEPTH) {
        fill_random(ctx.buffer, ctx.length);
        return NULL;
    }

    pthread_t t1, t2;
    size_t left_len, right_len, mid;

    if (ctx.length % 2 == 0) {
        // Even length: coin toss first, then recurse on both halves
        left_len = (ctx.length - 1) / 2;
        right_len = ctx.length - left_len - 1;
        mid = left_len;
        ctx.buffer[mid] = random_bit() ? 0x07 : 0x00;

        WorkerCtx left = { ctx.buffer, left_len, ctx.depth + 1 };
        WorkerCtx right = { ctx.buffer + mid + 1, right_len, ctx.depth + 1 };
        pthread_create(&t1, NULL, hexentropy_worker, &left);
        pthread_create(&t2, NULL, hexentropy_worker, &right);
    } else {
        // Odd length: coin toss and fill both halves without recursion
        left_len = ctx.length / 2;
        right_len = ctx.length - left_len - 1;
        mid = left_len;
        ctx.buffer[mid] = random_bit() ? 0x07 : 0x00;

        WorkerCtx left = { ctx.buffer, left_len, ctx.depth + 1 };
        WorkerCtx right = { ctx.buffer + mid + 1, right_len, ctx.depth + 1 };
        pthread_create(&t1, NULL, fill_random_thread, &left);
        pthread_create(&t2, NULL, fill_random_thread, &right);
    }

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return NULL;
}

int main(int argc, char *argv[]) {
    size_t n = 64;   // default length
    int binary = 0;  // output mode flag

    /* Parse command line arguments */
    for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], "--binary") == 0) {
            binary = 1;
        } else {
            n = strtoul(argv[i], NULL, 10);
            if (n == 0) {
                fprintf(stderr, "Invalid length\n");
                return EXIT_FAILURE;
            }
        }
    }

    /* Allocate output buffer */
    unsigned char *buffer = malloc(n);
    if (!buffer) {
        perror("malloc");
        return EXIT_FAILURE;
    }

    /* Launch recursive generation */
    WorkerCtx root = { buffer, n, 0 };
    hexentropy_worker(&root);

    /* Display final buffer */
    if (binary)
        print_binary(buffer, n);
    else {
        for (size_t i = 0; i < n; ++i)
            printf("%02x", buffer[i]);
        printf("\n");
    }

    free(buffer);
    return 0;
}

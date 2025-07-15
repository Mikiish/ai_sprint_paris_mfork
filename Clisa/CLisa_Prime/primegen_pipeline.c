#include <unistd.h>   // <-- sysconf(), _SC_NPROCESSORS_ONLN
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <pthread.h>
#include <sys/random.h>
#include <sys/time.h>
#include <stdatomic.h>
#include <gmp.h>

// Default ratio parts for generation, testing, overhead
static const int RATIO_GEN = 4;
static const int RATIO_TEST = 8;
static const int RATIO_OVERHEAD = 3;

// Shared queue for buffers awaiting primality test
typedef struct {
    unsigned char **buffers;  // array of pointers to byte buffers
    size_t capacity;
    size_t front;
    size_t count;
    pthread_mutex_t mutex;
    pthread_cond_t not_empty;
    pthread_cond_t not_full;
} BufferQueue;

// Global queue instance
static BufferQueue queue;

// Global flags/counters
static atomic_ullong next_index;    // atomic counter for number generation (to assign tasks)
static unsigned long long total_to_generate = 0;
static atomic_ullong primes_found;  // atomic counter for primes found

// Thread counts
static int num_gen_threads = 0;
static int num_test_threads = 0;

// Buffer parameters
static size_t number_length = 0;  // length of each number in bytes

// Initialize the queue
static void queue_init(BufferQueue *q, size_t capacity) {
    q->buffers = malloc(capacity * sizeof(unsigned char*));
    if (!q->buffers) {
        fprintf(stderr, "Queue buffer malloc failed\\n");
        exit(EXIT_FAILURE);
    }
    q->capacity = capacity;
    q->front = 0;
    q->count = 0;
    pthread_mutex_init(&q->mutex, NULL);
    pthread_cond_init(&q->not_empty, NULL);
    pthread_cond_init(&q->not_full, NULL);
}

// Destroy the queue
static void queue_destroy(BufferQueue *q) {
    free(q->buffers);
    pthread_mutex_destroy(&q->mutex);
    pthread_cond_destroy(&q->not_empty);
    pthread_cond_destroy(&q->not_full);
}

// Enqueue a buffer pointer (thread-safe)
static void queue_enqueue(BufferQueue *q, unsigned char *buffer) {
    pthread_mutex_lock(&q->mutex);
    // Wait until there is space
    while (q->count == q->capacity) {
        pthread_cond_wait(&q->not_full, &q->mutex);
    }
    // Compute insertion index (front + count mod capacity)
    size_t idx = (q->front + q->count) % q->capacity;
    q->buffers[idx] = buffer;
    q->count++;
    // Signal that queue is not empty
    pthread_cond_signal(&q->not_empty);
    pthread_mutex_unlock(&q->mutex);
}

// Dequeue a buffer pointer (thread-safe)
static unsigned char* queue_dequeue(BufferQueue *q) {
    pthread_mutex_lock(&q->mutex);
    // Wait until there is an item
    while (q->count == 0) {
        // If no more numbers will ever be produced (stop condition), break out
        // (We handle this via sentinel NULL pointers, so normally not needed to check here)
        pthread_cond_wait(&q->not_empty, &q->mutex);
    }
    // Remove item from front
    unsigned char *buffer = q->buffers[q->front];
    q->front = (q->front + 1) % q->capacity;
    q->count--;
    // Signal that queue has space
    pthread_cond_signal(&q->not_full);
    pthread_mutex_unlock(&q->mutex);
    return buffer;
}

// Generator thread function: produce random numbers and enqueue them
static void* generator_thread_func(void *arg) {
    (void)arg; // unused
    // Each thread uses its own buffer for each number to avoid contention
    // We allocate fresh buffers per number below for simplicity
    unsigned char *buffer;
    // Loop until we've generated all required numbers
    while (true) {
        // Atomically get the next index to generate
        unsigned long long idx = atomic_fetch_add(&next_index, 1);
        if (idx >= total_to_generate) {
            // All numbers assigned
            break;
        }
        // Allocate memory for the new number's bytes
        buffer = (unsigned char*)malloc(number_length);
        if (!buffer) {
            perror("malloc (number buffer)");
            break;
        }
        // Fill the buffer with cryptographically secure random bytes
        if (getrandom(buffer, number_length, 0) != (ssize_t)number_length) {
            perror("getrandom");
            free(buffer);
            // If getrandom fails, we abort the generation
            break;
        }
        // Enqueue the buffer for testing
        queue_enqueue(&queue, buffer);
    }
    return NULL;
}

// Tester thread function: consume numbers and test for primality
static void* tester_thread_func(void *arg) {
    (void)arg;
    // Initialize a big integer for reuse in this thread
    mpz_t n;
    mpz_init(n);
    // Continuously dequeue buffers and test them
    while (true) {
        unsigned char *buffer = queue_dequeue(&queue);
        if (buffer == NULL) {
            // NULL buffer is a signal to terminate
            break;
        }
        // Import the bytes into a big integer (treat buffer as big-endian)
        mpz_import(n, number_length, 1, 1, 1, 0, buffer);
        // Perform Miller-Rabin primality test with a given number of rounds
        int result = mpz_probab_prime_p(n, 25);
        if (result >= 1) {
            // Probably prime (or definitely prime)
            atomic_fetch_add(&primes_found, 1);
            // (Optionally, we could output or log the prime here, 
            // but that is omitted for performance.)
        }
        // Free the buffer memory
        free(buffer);
    }
    // Clear big integer
    mpz_clear(n);
    return NULL;
}

int main(int argc, char *argv[]) {
    // Parse command-line arguments
    // Usage: ./primegen [count] [length]
    // If only one argument, treat it as the byte length (for one number); 
    // if two arguments, first is count of numbers, second is byte length.
    total_to_generate = 1;
    number_length = 64; // default 64 bytes (~512 bits)
    if (argc >= 2) {
        // If two arguments provided, use first as count, second as length
        char *endptr = NULL;
        unsigned long long maybeCount = strtoull(argv[1], &endptr, 10);
        if (argc >= 3) {
            if (maybeCount == 0) {
                fprintf(stderr, "Invalid count\\n");
                return EXIT_FAILURE;
            }
            total_to_generate = maybeCount;
            number_length = strtoul(argv[2], &endptr, 10);
        } else {
            // Only one arg: interpret as length (keep count = 1)
            number_length = strtoul(argv[1], &endptr, 10);
        }
        if (number_length == 0) {
            fprintf(stderr, "Invalid length\\n");
            return EXIT_FAILURE;
        }
    }
    // Determine thread counts based on available CPUs
    long nproc = sysconf(_SC_NPROCESSORS_ONLN);
    if (nproc < 1) nproc = 1;
    // Calculate total ratio parts
    int total_ratio = RATIO_GEN + RATIO_TEST + RATIO_OVERHEAD;
    // Assign threads according to ratio, ensuring at least 1 in each category if possible
    num_gen_threads = (int)((RATIO_GEN * nproc) / total_ratio);
    num_test_threads = (int)((RATIO_TEST * nproc) / total_ratio);
    if (num_gen_threads < 1) num_gen_threads = 1;
    if (num_test_threads < 1) num_test_threads = 1;
    // Keep a few cores as overhead if possible (not creating threads for those)
    // (We don't explicitly use overhead threads in this implementation; they remain idle or for OS.)
    
    size_t queue_capacity = (size_t)(num_test_threads * 2);
    queue_init(&queue, queue_capacity);
    atomic_init(&next_index, 0);
    atomic_init(&primes_found, 0);
    
    // Allocate and launch generator threads
    pthread_t *gen_threads = malloc(num_gen_threads * sizeof(pthread_t));
    pthread_t *test_threads = malloc(num_test_threads * sizeof(pthread_t));
    if (!gen_threads || !test_threads) {
        fprintf(stderr, "Thread allocation failed\\n");
        return EXIT_FAILURE;
    }
    
    for (int i = 0; i < num_gen_threads; ++i) {
        if (pthread_create(&gen_threads[i], NULL, generator_thread_func, NULL) != 0) {
            fprintf(stderr, "Error creating generator thread %d\\n", i);
            return EXIT_FAILURE;
        }
    }
    for (int j = 0; j < num_test_threads; ++j) {
        if (pthread_create(&test_threads[j], NULL, tester_thread_func, NULL) != 0) {
            fprintf(stderr, "Error creating tester thread %d\\n", j);
            return EXIT_FAILURE;
        }
    }
    
    // Start timing
    struct timeval start, end;
    gettimeofday(&start, NULL);
    
    // Wait for all generator threads to finish producing
    for (int i = 0; i < num_gen_threads; ++i) {
        pthread_join(gen_threads[i], NULL);
    }
    // After generation is done, enqueue termination signals (NULL) for each tester thread
    for (int k = 0; k < num_test_threads; ++k) {
        queue_enqueue(&queue, NULL);
    }
    // Wait for all tester threads to finish
    for (int j = 0; j < num_test_threads; ++j) {
        pthread_join(test_threads[j], NULL);
    }
    
    gettimeofday(&end, NULL);
    // Compute elapsed time in seconds
    double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_usec - start.tv_usec) / 1000000.0;
    
    // Print benchmark results
    unsigned long long primes = atomic_load(&primes_found);
    printf("Generated %llu %zu-byte numbers in %.2f seconds. Primes found: %llu.\\n",
           total_to_generate, number_length, elapsed, primes);
    
    // Cleanup
    free(gen_threads);
    free(test_threads);
    queue_destroy(&queue);
    return 0;
}

#define _GNU_SOURCE
#include <stdio.h>   // printf, perror
#include <stdlib.h>  // malloc, free, atoi
#include <pthread.h> // gestion des threads POSIX
#include <sched.h>   // affinité CPU
#include <stdint.h>  // types entiers fixes
#include <string.h>  // memset & co
#include <unistd.h>  // sysconf
#include <sys/random.h> // getrandom

#define MAX_THREADS 256  // À adapter si besoin
#define BYTE_PAIR_SIZE 2 // 2 bytes par élément

typedef struct {
    uint8_t* buffer;
    size_t start_index;
    size_t size; // en paires de bytes
    int core_id;
} ThreadArgs;

/*
 * assign_thread_to_core
 * ---------------------
 * Force le thread appelant à s'exécuter sur un cœur spécifique.
 */

void assign_thread_to_core(int core_id) {
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(core_id, &cpuset);

    if (pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset) != 0) {
        perror("Erreur d'affinité CPU");
    }
}

void* fill_buffer_worker(void* arg) {
    /* Worker appelé par chaque thread pour remplir sa portion du buffer */
    ThreadArgs* args = (ThreadArgs*)arg;

    /* Placement du thread sur son cœur cible */
    assign_thread_to_core(args->core_id);

    for (size_t i = 0; i < args->size; ++i) {
        /* Récupère deux octets directement depuis le noyau */
        uint8_t a, b;
        if (getrandom(&a, 1, 0) != 1 || getrandom(&b, 1, 0) != 1) {
            perror("getrandom");
            pthread_exit(NULL);
        }

        size_t index = args->start_index + i * BYTE_PAIR_SIZE;
        args->buffer[index] = a;
        args->buffer[index + 1] = b;
    }

    pthread_exit(NULL); /* Fin du travail du thread */
}

/*
 * recursive_buffer_fill
 * --------------------
 * Crée de nouveaux threads pour remplir le buffer de manière diviser-pour-mieux-régner.
 */
void recursive_buffer_fill(uint8_t* buffer, size_t start_index, size_t n_pairs, int core_offset) {
    if (n_pairs <= 1) {
        /* Cas de base : un thread, une paire de bytes */
        ThreadArgs* args = malloc(sizeof(ThreadArgs));
        args->buffer = buffer;
        args->start_index = start_index;
        args->size = 1;
        args->core_id = core_offset % sysconf(_SC_NPROCESSORS_ONLN);

        pthread_t thread;
        pthread_create(&thread, NULL, fill_buffer_worker, args);
        pthread_join(thread, NULL);
        free(args);
        return;
    }

    size_t left_size = n_pairs / 2;
    size_t right_size = n_pairs - left_size;

    pthread_t left_thread, right_thread;
    /* Allocation des structures d'arguments pour les threads enfants */
    ThreadArgs* left_args = malloc(sizeof(ThreadArgs));
    ThreadArgs* right_args = malloc(sizeof(ThreadArgs));

    left_args->buffer = buffer;
    left_args->start_index = start_index;
    left_args->size = left_size;
    left_args->core_id = (core_offset + 0) % sysconf(_SC_NPROCESSORS_ONLN);

    right_args->buffer = buffer;
    right_args->start_index = start_index + left_size * BYTE_PAIR_SIZE;
    right_args->size = right_size;
    right_args->core_id = (core_offset + 1) % sysconf(_SC_NPROCESSORS_ONLN);

    /* Lancement des deux sous-threads */
    pthread_create(&left_thread, NULL, fill_buffer_worker, left_args);
    pthread_create(&right_thread, NULL, fill_buffer_worker, right_args);

    /* Attente de la fin des sous-threads */
    pthread_join(left_thread, NULL);
    pthread_join(right_thread, NULL);

    /* Nettoyage */
    free(left_args);
    free(right_args);
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage : %s <nombre_de_paires_de_bytes>\n", argv[0]);
        return 1;
    }



    /* Nombre de paires de bytes à générer */
    size_t n_pairs = atoi(argv[1]);
    size_t buffer_size = n_pairs * BYTE_PAIR_SIZE;

    /* Allocation du buffer principal */
    uint8_t* buffer = malloc(buffer_size);
    if (!buffer) {
        perror("Erreur malloc");
        return 1;
    }

    recursive_buffer_fill(buffer, 0, n_pairs, 0);

    /* Message final pour l'utilisateur */
    printf("[✔] Buffer rempli avec %zu paires de bytes.\n", n_pairs);
    free(buffer);
    return 0; /* Fin du programme */
}

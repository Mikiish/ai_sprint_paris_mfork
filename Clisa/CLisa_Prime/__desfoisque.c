#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

typedef struct {
    int value;
    int depth;
} Task;

void *fork_test(void *arg) {
    Task *task = (Task*) arg;
    int n = task->value;
    int depth = task->depth;

    if (n % 2 == 0 && n > 2) {
        int half = n / 2;
        printf("Dividing %d → %d + %d [depth %d]\n", n, half, half, depth);

        pthread_t t1, t2;

        Task *subtask1 = malloc(sizeof(Task));
        Task *subtask2 = malloc(sizeof(Task));
        *subtask1 = (Task){ .value = half, .depth = depth + 1 };
        *subtask2 = (Task){ .value = half, .depth = depth + 1 };

        pthread_create(&t1, NULL, fork_test, subtask1);
        pthread_create(&t2, NULL, fork_test, subtask2);

        pthread_join(t1, NULL);
        pthread_join(t2, NULL);

        free(subtask1);
        free(subtask2);
    } else {
        printf("Leaf: %d [depth %d]\n", n, depth);
    }

    free(task);
    return NULL;
}

int main() {
    int n = 128;  // point de départ
    pthread_t root;
    Task *root_task = malloc(sizeof(Task));
    *root_task = (Task){ .value = n, .depth = 0 };

    pthread_create(&root, NULL, fork_test, root_task);
    pthread_join(root, NULL);

    return 0;
}
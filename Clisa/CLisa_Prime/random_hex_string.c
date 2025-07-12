#include <stdio.h>
#include <stdlib.h>
#include <sys/random.h>

void print_random_hex(int n_bytes) {
    unsigned char *buffer = malloc(n_bytes);
    if (!buffer) {
        perror("malloc");
        exit(1);
    }

    if (getrandom(buffer, n_bytes, 0) != n_bytes) {
        perror("getrandom");
        exit(1);
    }

    for (int i = 0; i < n_bytes; i++) {
        printf("%02x", buffer[i]); // deux chiffres hex par byte
    }
    printf("\n");

    free(buffer);
}

int main() {
    print_random_hex(32);  // 32 bytes = 64 hex digits
    return 0;
}
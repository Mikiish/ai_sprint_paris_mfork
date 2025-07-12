#include <stdio.h>
#include <stdlib.h>
#include <sys/random.h>

static inline int pilouface() {
    unsigned char byte;
    getrandom(&byte, 1, GRND_NONBLOCK);
    return byte & 1;  // récupère le bit de poids faible
}

int main() {
    const long n = 10000000;  // dix millions de flips
    long pile = 0;
    
    for (long i = 0; i < n; ++i) {
        pile += pilouface();
    }

    printf("Pile: %ld | Face: %ld\n", pile, n - pile);
    return 0;
}
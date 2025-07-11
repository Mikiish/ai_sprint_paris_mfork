import numpy as np
import sympy
import time


def segmented_sieve(limit, segment_size=10 ** 8):
    """
    Génère tous les nombres premiers jusqu'à 'limit' en utilisant un crible segmenté.

    :param limit: La borne supérieure pour la génération des nombres premiers
    :param segment_size: Taille des segments de calcul (évite d'utiliser trop de RAM)
    :return: Liste des nombres premiers jusqu'à 'limit'
    """
    print(f"Génération des nombres premiers jusqu'à {limit} avec un crible segmenté...")
    start_time = time.time()

    # Étape 1 : Générer les petits nombres premiers jusqu'à sqrt(limit)
    sqrt_limit = int(np.sqrt(limit)) + 1
    small_primes = list(sympy.primerange(2, sqrt_limit))

    primes = []  # Liste finale des nombres premiers
    primes.extend(small_primes)  # Ajouter les petits nombres premiers directement

    # Étape 2 : Parcourir l'espace des nombres en segments
    for low in range(sqrt_limit, limit + 1, segment_size):
        high = min(low + segment_size - 1, limit)
        sieve = np.ones(high - low + 1, dtype=bool)

        # Marquer les multiples des petits nombres premiers
        for p in small_primes:
            start = max(p * p, low + (p - low % p) % p)  # Premier multiple de p dans ce segment
            sieve[start - low::p] = False  # Éliminer les multiples de p

        # Ajouter les nombres premiers du segment
        primes.extend(np.nonzero(sieve)[0] + low)

    end_time = time.time()
    print(f"Génération terminée en {end_time - start_time:.2f} secondes. {len(primes)} nombres premiers trouvés.")
    return primes


# Test rapide avec une limite de 10^10
LIMIT = 10 ** 11
prime_list = segmented_sieve(LIMIT)

# Exemple d'accès
print(f"Les 3 derniers nombres premiers générés: {prime_list[-3:]}")

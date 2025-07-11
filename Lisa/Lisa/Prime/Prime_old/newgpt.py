import sympy
import pandas as pd
import time
import multiprocessing


def algop(p):
    """ Exécution de Algo(p) si p est premier """
    if (16 % p == 1):
        return 1
    if sympy.isprime(p):
        n = 1
        while pow(16, n, p) != 1:
            n += 1
    else:
        n = None
    return n


def get_prime_cycle(k=16, p=61681):
    """ Calcul du cycle complet jusqu'à ce que la valeur revienne à 1 """
    cycle_values = [1]
    kmodp = k % p
    if kmodp == 1:
        cycle_values.append(kmodp)
        return cycle_values
    if kmodp == p - 1:
        cycle_values.append(-1)
        return cycle_values
    value = 1
    while True:
        value = (value * k) % p
        if value == 1:
            break
        cycle_values.append(value)
    return cycle_values


def analyze_cycle(p):
    """ Analyse du cycle dans un processus séparé """
    cycle = get_prime_cycle(16, p)
    df_cycle = pd.DataFrame({"n": range(len(cycle)), f"16^n % {p}": cycle})
    print(f"\nCycle des puissances de 16 modulo {p} :")
    print(df_cycle)
    return df_cycle


def find_prime_cycles(start, end, max_n):
    """ Recherche brute des nombres premiers respectant la condition et analyse en parallèle """
    prime_candidates = list(sympy.primerange(start, end))  # Liste des nombres premiers dans l'intervalle donné
    matching_pairs = []

    for p in prime_candidates:
        value = 1
        n = 0
        while n < p:
            value = (value * 16) % p
            n += 1
            if value == p - 1:
                if n <= max_n:
                    matching_pairs.append((p, n))
                    print(f"Appended :{(p, n)}")
                    process = multiprocessing.Process(target=analyze_cycle, args=(p,))
                    process.start()
                break

    df_matching = pd.DataFrame(matching_pairs, columns=["p", "n"])
    return df_matching


if __name__ == "__main__":
    p1 = 641
    p2 = 90289

    # Vérification de Primalité
    is_p1prime = sympy.isprime(p1)
    is_p2prime = sympy.isprime(p2)
    print(f"Is p1 Prime ? {is_p1prime}\nIs p2 Prime? {is_p2prime}")

    # Recherche des nombres premiers respectant la condition avec exécution parallèle
    df_result = find_prime_cycles(990000, 1110000, 99)
    print("\nNombres premiers trouvés respectant la condition :")
    print(df_result)

import sympy
import pandas as pd
import time

# Nombre à analyser
#p1 = 61681
#p2 = 65521
# Exécution de Algo(p) si p est premier
def algop(p):
    if (16%p == 1):
        return 1
    if sympy.isprime(p):
        n = 1
        while pow(16, n, p) != 1:
            n += 1
    else:
        n = None
    return n

# Calcul du cycle complet jusqu'à ce que la valeur revienne à 1
def get_prime_cycle(k=16,p=61681):
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

    return cycle_values  # 🔹 Ajout de ce return important !

def find_prime_cycles(start, end, max_n):
    """
    Recherche des nombres premiers p dans l'intervalle [start, end]
    pour lesquels il existe un n tel que 16^n ≡ p - 1 (mod p).
    Filtre les résultats pour ne garder que ceux avec n <= max_n.
    """
    prime_candidates = list(sympy.primerange(start, end))  # Liste des nombres premiers dans l'intervalle donné
    matching_pairs = []

    for p in prime_candidates:
        value = 1
        n = 0
        while n < p:  # On cherche jusqu'à trouver p-1 ou dépasser p
            value = (value * 16) % p
            n += 1
            if value == p - 1:
                if n <= max_n:  # Filtrage par max_n
                    matching_pairs.append((p, n))
                    print(f"Appended :{(p, n)}")
                break

    # Conversion en DataFrame pour affichage
    df_matching = pd.DataFrame(matching_pairs, columns=["p", "n"])
    return df_matching

# Affichage des résultats
if __name__ == "__main__":
    # Nombre à analyser
    p1 = 641
    p2 = 90289

    # Vérification de Primalité
    is_p1prime = sympy.isprime(p1)
    is_p2prime = sympy.isprime(p2)
    print(f"Is p1 Prime ?{is_p1prime}\nIs p2 Prime? {is_p2prime}")

    # Recherche des nombres premiers respectant la condition
    df_result = find_prime_cycles(990000, 1110000, 99)
    print("\nNombres premiers trouvés respectant la condition :")
    print(df_result)

    # Sauvegarde dans un fichier CSV (optionnel)
    #df_result.to_csv("prime_cycles.csv", index=False)
    #print("\nRésultats enregistrés dans 'prime_cycles.csv'.")

    # Calcul des cycles
    cycle_p1 = get_prime_cycle(16, p1)
    df_p1 = pd.DataFrame({"n": range(len(cycle_p1)), f"16^n % {p1}": cycle_p1})
    print(f"\nCycle des puissances de 16 modulo {p1} :")
    print(df_p1)

    cycle_p2 = get_prime_cycle(16, p2)
    df_p2 = pd.DataFrame({"n": range(len(cycle_p2)), f"16^n % {p2}": cycle_p2})
    print(f"\nCycle des puissances de 16 modulo {p2} :")
    print(df_p2)

    # Sauvegarde des cycles en CSV (optionnel)
    df_p1.to_csv(f"cycle_{p1}.csv", index=False)
    df_p2.to_csv(f"cycle_{p2}.csv", index=False)
    print("\nLes cycles ont été sauvegardés en fichiers CSV.")
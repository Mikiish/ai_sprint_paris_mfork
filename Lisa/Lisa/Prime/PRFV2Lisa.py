import random
import time
from sympy import isprime, factorint
from Crypto.Util import number


def is_hex_prime(hex_str):
    """Vérifie si un nombre hexadécimal est premier en le testant en base 10."""
    if not hex_str:
        return False
    try:
        decimal_value = int(hex_str, 16)
        return number.isPrime(decimal_value)
    except ValueError:
        return False


def pollards_rho(n, timeout=60):
    """Implémente l'algorithme de Pollard's Rho avec un timeout."""
    if n <= 1:
        return None

    start_time = time.time()
    if n % 2 == 0:
        return 2

    x = random.randint(1, max(2, n - 1))
    y = x
    c = random.randint(1, max(2, n - 1))
    f = lambda x: (x * x + c) % n
    d = 1
    while d == 1:
        if time.time() - start_time > timeout:
            print("Timeout atteint pour Pollard's Rho. Relance de la boucle principale.")
            return None
        x = f(x)
        y = f(f(y))
        d = number.GCD(abs(x - y), n)
        if d == n:
            return None
    return d


def evaluate_prime_range(cofactor, decrement=0):
    """Détermine la plage de nombres premiers pertinents pour factoriser un cofacteur, en décrémentant à chaque timeout."""
    cofactor_size = len(hex(cofactor)[2:])
    min_size = max(2, cofactor_size // 2 - 1 - decrement)
    max_size = max(2, cofactor_size // 2 + 1 - decrement)
    return min_size, max_size


def factorize_number(hex_number, pollard_timeout=60, max_iterations=200):
    """Effectue la factorisation avec une limite d'itérations sur la boucle principale."""
    decimal_number = int(hex_number, 16)
    factors = []
    decrement = 0  # Variable pour réduire min_size et max_size après chaque timeout

    for iteration in range(max_iterations):
        print(f"\n--- Début de l'itération {iteration + 1} de la boucle principale ---")
        if decimal_number <= 1:
            print("Le nombre est trivial (<=1).")
            break
        if number.isPrime(decimal_number):
            print("Le dernier cofacteur est premier.")
            break

        min_size, max_size = evaluate_prime_range(decimal_number, decrement)
        print(f"Recherche de facteurs dans la plage de taille : {min_size}-{max_size}")

        factor = pollards_rho(decimal_number, pollard_timeout)
        if factor is None:
            print("Aucun facteur trouvé avec Pollard's Rho, tentative avec sympy.factorint...")
            decrement += 1  # Réduire la plage de recherche après un timeout
            try:
                factors_dict = factorint(decimal_number, limit=pollard_timeout)
                if factors_dict:
                    for factor, count in factors_dict.items():
                        for _ in range(count):
                            if number.isPrime(factor):
                                factors.append(hex(factor).upper()[2:])
                            else:
                                decimal_number = factor  # Continuer la factorisation
                                break
                    continue
            except Exception:
                print("Timeout atteint pour sympy.factorint. Relance de la boucle principale.")
                continue  # Relance la boucle principale avec le dernier cofacteur

        if decimal_number == 1:
            break  # Sortie de la boucle si tout a été factorisé

        if number.isPrime(factor):
            hex_factor = hex(factor).upper()[2:]
            factors.append(hex_factor)
        else:
            decimal_number = factor  # Continuer la factorisation
            continue

        decimal_number //= factor
        print(f"Facteur trouvé : {hex_factor}")
        print(f"Nouveau cofacteur : {hex(decimal_number).upper()[2:]}")

    print(f"Facteurs finaux : {factors}, Cofacteur restant : {hex(decimal_number).upper()[2:]}")
    return factors


hex_number = "9E034D03DB45D5BDA40818BBCE5BAE245B72A000C80EA9C5F46D34BA5E05B6834430407B4E532640C80B06B310D80ED69EE465205570A03271550AFC2997997448DBA29A74E4BA098CC2EBBE9BB5CB5CFFE3B598A6325E9307D6A4365E61FF837357AC4518D2E08CC97A154395450256AA2DD755AC789F1AFCFEDD61E4B49FE8B52605874A0E9EDF4B03A2076F262F895E65F35E0050504CCDFAC88B4A88D02602E89424FBC4966EFC9FC42D7997CB6E1B4947C507F4E949B1526067A1C139394321D5F592BB3CB21DD473292818D868EB888922C72E81B8C69A21F5AD2A49093170DAB33BF54D6D880C479084211481109D8208A2BA256C77A76C41F17A4A7904690CFD1"

# Lancer la factorisation avec limite d'itérations
discovered_factors = factorize_number(hex_number, pollard_timeout=60, max_iterations=200)
print(f"Facteurs finaux : {discovered_factors}")

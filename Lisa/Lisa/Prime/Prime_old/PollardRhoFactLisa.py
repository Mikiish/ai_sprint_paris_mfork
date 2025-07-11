from sympy import isprime, factorint
import random
from decimal import Decimal
# Le script prend une entrée hex, directement test sa primalité
# puis execute un algorithme de factorisation en decimal pour produire les facteurs si le nombre n'est pas premier.

def hex_to_decimal(hex_str):
    """
    Convertit un nombre hexadécimal en décimal avec précision améliorée.
    :param hex_str: str, Nombre en base 16 sous forme de chaîne de caractères
    :return: str, Nombre en base 10 sous forme de chaîne de caractères
    """
    if not isinstance(hex_str, str) or not all(c in "0123456789ABCDEFabcdef" for c in hex_str):
        return "Erreur : Entrée non valide. Assurez-vous d'entrer un nombre hexadécimal valide."

    try:
        decimal_value = Decimal(int(hex_str, 16))  # Conversion avec Decimal pour éviter les pertes de précision
        return str(decimal_value)  # Retourner sous forme de chaîne pour éviter les dépassements
    except ValueError as e:
        return f"Erreur : Impossible de convertir. Détail : {e}"

    # Exemple d'utilisation


hex_number = ("82615181DE866BA8E04F829A670BB81496A2DDB386F72EEB009243F792A8E84653D5370340A74546EA72F633429FA68C72F0491C4")

# Validation avant conversion
if isprime(int(hex_number, 16)):
    print("Le nombre est premier.")
else:
    print("Le nombre n'est pas premier.")
    print("Factorisation en cours...")
    factors = factorint(int(hex_number, 16))
    print(f"Facteurs trouvés : {factors}")

if isinstance(hex_number, str) and all(c in "0123456789ABCDEFabcdef" for c in hex_number):
    decimal_value = hex_to_decimal(hex_number)
    print(f"Décimal: {decimal_value}")
else:
    print("Erreur : Entrée hexadécimale invalide.")


def pollards_rho(n, seed=2):
    """Implémente l'algorithme de Pollard's Rho pour la factorisation."""
    if n % 2 == 0:
        return 2  # Si divisible par 2, on retourne immédiatement

    x = seed
    y = seed
    c = random.randint(1, n - 1)
    f = lambda x: (x * x + c) % n

    d = 1
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = abs(x - y) % n
        if d == n:
            return None  # Échec, essayer une autre valeur de seed

    return d if isprime(d) else None


# Exécution de Pollard's Rho pour détecter un facteur
if decimal_value.isdigit():  # Vérifie que la conversion a réussi
    mutated_number = int(decimal_value)
    factor = pollards_rho(mutated_number)

    if factor:
        print(f"Facteur trouvé : {factor}")
    else:
        print("Aucun facteur trouvé avec cette méthode, essayer une autre valeur de seed ou un autre algorithme.")
else:
    print("Erreur : Impossible d'exécuter Pollard's Rho, la conversion en décimal a échoué.")

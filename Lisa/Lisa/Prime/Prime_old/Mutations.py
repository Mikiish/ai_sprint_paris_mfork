from sympy import isprime, factorint
import random
from decimal import Decimal


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

    # Nombre original et nombre muté


original_hex = "D4D35CA3432CF0B4992AF34519F2837E903A756EFD89780288F1E94F27D7FEB7F6CFACC93A688FA2439CFEFB3A083021A2F38CD6657F315393F27CF080FFBBE26C3722F48A36EA3F12FC1951D4F6B5E969FCE1FE74F123DC78B4F31CDED80CF13AD0FB7819AD8867D32A8113C783DAF545891B0B618C365ADDE806111E808CC91D8A1E9"
mutated_hex = "D4D35CA3432CF0B4992AF34519F2837E903A756EFD89780288F1E94F27D7FEB7F6CFACC93A688FA2439CFEFB3A083021A2F38CD6657F315393F27CF080FFBBE26C3022F48A36EA3F12FC1951D4F6B5E969FCE1FE74F123DC78B4F31CDED80CF13AD0FB7819AD8867D32A8113C783DAF545891B0B618C365ADDE806111E808CC91D8A1E9"

# Vérification de primalité
original_decimal = int(original_hex, 16)
mutated_decimal = int(mutated_hex, 16)

print("Analyse de la mutation :")
print(f"Nombre original : {original_hex}")
print(f"Nombre muté     : {mutated_hex}")

if isprime(original_decimal):
    print("✅ Le nombre original est premier.")
else:
    print("❌ Le nombre original n'est PAS premier. Problème détecté !")

if isprime(mutated_decimal):
    print("✅ Le nombre muté est toujours premier !")
else:
    print("❌ Le nombre muté n'est PAS premier. Facteurs en cours de recherche...")


    def factor_with_timeout(n, timeout_sec=30):
        """Essaye de factoriser un nombre sans utiliser multiprocessing."""
        try:
            factors = factorint(n)
            return factors
        except Exception as e:
            return f"Erreur lors de la factorisation : {e}"


    factors = factor_with_timeout(mutated_decimal)
    print(f"Facteurs trouvés pour le nombre muté : {factors}")

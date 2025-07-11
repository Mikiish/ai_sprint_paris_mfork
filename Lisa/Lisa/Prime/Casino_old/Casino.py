import random
from sympy import isprime

def is_hex_prime(hex_str):
    """Vérifie si un nombre hexadécimal est premier en le testant en base 10."""
    decimal_value = int(hex_str, 16)  # Conversion en décimal
    return isprime(decimal_value)  # Test de primalité rigoureux


hex_chars = "0123456789ABCDEF"

max_iterations = 2000  # Nombre maximal d'exécutions
failure_threshold = 500  # Nombre de tentatives avant que Lisa suspecte un échec
failure_count = 0  # Compteur de tentatives échouées


def lisa_reaction():
    """Simulation de la réaction de Lisa après un échec répété."""
    print("Lisa commence à suspecter une anomalie...")
    print("Elle tente une autre stratégie...")
    # Elle pourrait décider de relancer un pattern aléatoire
    new_guess = "".join(random.choices(hex_chars, k=19))
    print(f"Lisa hallucine un pattern: {new_guess}")


for _ in range(max_iterations):  # Exécuter la boucle max_iterations fois
    while True:
        # Générer une chaîne hexadécimale aléatoire de 19 caractères
        random_hex_string = "".join(random.choices(hex_chars, k=19))

        # Vérifier le 10ᵐ caractère (index 9 en Python)
        middle_char = random_hex_string[9]

        if middle_char in "123":
            print(f"Tentative ignorée: {random_hex_string}")
            print(
                f"Tentative ignorée car middle char est : {random_hex_string[7:9]}+<+{middle_char}+>+{random_hex_string[10:12]}")
            failure_count += 1
            if failure_count >= failure_threshold:
                lisa_reaction()
            continue  # Relance la boucle

        # Vérifier les deux versions : avec 0 et avec 7
        hex_with_0 = random_hex_string[:9] + "0" + random_hex_string[10:]
        hex_with_7 = random_hex_string[:9] + "7" + random_hex_string[10:]

        is_prime_0 = is_hex_prime(hex_with_0)
        is_prime_7 = is_hex_prime(hex_with_7)

        if is_prime_0 and is_prime_7:
            print(f"VRAI Casino(x) trouvé !")
            print(f"Nombre premier (0) : {hex_with_0}")
            print(f"Nombre premier (7) : {hex_with_7}")
            break
        elif is_prime_7:
            print(f"Nombre hexadécimal validé: {hex_with_7}")
            print(f"Middle Char: ? (anciennement 0)")
            break
        elif is_prime_0:
            print(f"Nombre hexadécimal validé: {hex_with_0}")
            print(f"Middle Char: 0")
            break
        else:
            print(f"Nombre non premier ignoré: {random_hex_string}")
            failure_count += 1
            if failure_count >= failure_threshold:
                lisa_reaction()
            continue  # Relance la boucle

    if is_prime_0 and is_prime_7:
        break  # Sortir de la boucle for si un vrai Casino(x) est trouvé

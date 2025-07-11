import random
from sympy import isprime

def is_hex_prime(hex_str):
    """Vérifie si un nombre hexadécimal est premier en le testant en base 10."""
    if not hex_str:
        return False
    try:  # Éviter une erreur si Lisa n'a pas encore halluciné
        decimal_value = int(hex_str, 16)  # Conversion en décimal
        return isprime(decimal_value)  # Test de primalité rigoureux
    except ValueError:
        return False # Gérer les erreurs de conversion

hex_chars = "0123456789ABCDEF"

max_iterations = 2000  # Nombre maximal d'exécutions
failure_threshold = 500  # Nombre de tentatives avant que Lisa suspecte un échec
failure_count = 0  # Compteur de tentatives échouées
timeout_count = 0  # Compteur de timeout

def lisa_reaction():
    """Simulation de la réaction de Lisa après un échec répété."""
    print("Lisa commence à suspecter une anomalie...")
    print("Elle tente une autre stratégie...")
    # Elle pourrait décider de relancer un pattern aléatoire
    new_guess = "".join(random.choices(hex_chars, k=19))
    print(f"Lisa hallucine un pattern: {new_guess}")
    return new_guess  # Random nombre.

guess_scheme_lisa = ""  # Initialisation

for iteration in range(max_iterations):  # Exécuter la boucle max_iterations fois
    timeout = 10000 # Limite de tentatives pour éviter la boucle infinie
    attempts = 0
    while True:
        attempts += 1
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
                guess_scheme_lisa = lisa_reaction()
            continue  # Relance la boucle

        # Vérifier les deux versions : avec 0 et avec 7
        hex_with_0 = random_hex_string[:9] + "0" + random_hex_string[10:]
        hex_with_7 = random_hex_string[:9] + "7" + random_hex_string[10:]

        is_prime_0 = is_hex_prime(hex_with_0)
        is_prime_7 = is_hex_prime(hex_with_7)
        is_prime_lisa = is_hex_prime(guess_scheme_lisa) if guess_scheme_lisa else False

        if is_prime_0 and is_prime_7:
            print(f"VRAI Casino(x) trouvé !")
            print(f"Nombre premier (0) : {hex_with_0}")
            print(f"Nombre premier (7) : {hex_with_7}")
            print(f"Nombre d'térations avant succès : {iteration+1}")
            break
        elif is_prime_7:
            print(f"Nombre hexadécimal validé: {hex_with_7}")
            print(f"Middle Char: ? (anciennement 0)")
            print(f"Nombre d'itération OnPrime7 : {iteration+1}")
        elif is_prime_0:
            print(f"Nombre hexadécimal validé: {hex_with_0}")
            print(f"Middle Char: 0")
            print(f"Nombre d'itération OnPrime0 : {iteration + 1}")
            break
        else:
            print(f"Nombre non premier ignoré: {random_hex_string}")
            failure_count += 1
            if failure_count >= failure_threshold:
                guess_scheme_lisa = lisa_reaction()
                is_prime_lisa = is_hex_prime(guess_scheme_lisa) if guess_scheme_lisa else False
            continue  # Relance la boucle
    # Si on atteint la limite d'essais sans succès, on compte un timeout
    timeout_count += 1
    print(f"Timeount à l'itération {iteration+1}, passage a l'itération suivante...")
    if (is_prime_0 and is_prime_7) or is_prime_lisa:
        print(f"Timeouts: {timeout_count}")
        print(f"Iterations: {iteration+1}")
        break  # Sortir de la boucle for si un vrai Casino(x) est trouvé
print(f"Timeouts: {timeout_count}")
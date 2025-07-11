import random
import numpy as np
import matplotlib.pyplot as plt
from sympy import isprime
from scipy.stats import linregress
import concurrent.futures


class QuantumState:
    def __init__(self, possible_states, hidden_variable=None):
        self.possible_states = possible_states  # Liste des états possibles
        self.state = None  # Indéterminé tant qu'aucune mesure
        self.hidden_variable = hidden_variable if hidden_variable is not None else random.random()
        self.measured = False

    def measure(self):
        """
        Simule l'effondrement de la fonction d'onde.
        L'état final est influencé par la variable cachée.
        """
        if not self.measured:
            weight = [abs(self.hidden_variable - i) for i in range(len(self.possible_states))]
            self.state = self.possible_states[
                weight.index(min(weight))]  # Choisit l'état le plus proche de la variable cachée
            self.measured = True
        return self.state

    def reset(self):
        """Remet l'état en superposition."""
        self.state = None
        self.measured = False


# Détection de nombres premiers robustes (mutants mathématiques) avec un score de stabilité
def mutate_number(hex_number, max_mutations=100000, tolerance=2084):
    decimal_number = int(hex_number, 16)
    original_prime = isprime(decimal_number)

    if not original_prime:
        return None, 0, 0  # Pas un mutant mathématique à l'origine

    stable_mutations = 0
    consecutive_fails = 0
    best_mutant = decimal_number  # Stocke le meilleur mutant
    mutation_history = []

    for i in range(max_mutations):
        # Mutation alternée entre poids fort et poids faible
        mutated_hex = list(hex_number.upper())
        if i % 2 == 0:
            mutation_index = random.randint(0, len(mutated_hex) // 2)  # Poids fort
        else:
            mutation_index = random.randint(len(mutated_hex) // 2, len(mutated_hex) - 1)  # Poids faible

        valid_hex_digits = "0123456789ABCDEF".replace(mutated_hex[mutation_index], "")
        mutated_hex[mutation_index] = random.choice(valid_hex_digits)

        mutated_number = int("".join(mutated_hex), 16)

        if isprime(mutated_number):
            stable_mutations += 1
            best_mutant = mutated_number  # Stocker le mutant réussi
            consecutive_fails = 0  # Réinitialiser l'échec
            mutation_history.append((i + 1, stable_mutations))
            print(f"Mutation réussie à l'itération {i + 1}: {hex(mutated_number)}")
        else:
            consecutive_fails += 1
            if consecutive_fails >= tolerance:
                break  # Arrêter si trop d'échecs consécutifs

    return best_mutant if stable_mutations > 0 else None, stable_mutations, i + 1, mutation_history


# Exécution sur Phi1 et Phi2 avec mesure de stabilité
Phi1 = "CAFFD366A99A307AE3B9860420B8F104AE39BA61361F5B05A42FE14EA984CC922A6D706E9C41BBE96246C38112B1521DD24E9554D069114F9FA8AEEE763614C247A8069AE40B9BE7CE0119A6EECAD6F01872F9A967F70417F20A22C6E8D2F039D5CB93F1D84BCF01B121A00F26CB5754263833DFBF043BF4A10243B771134B444BD70FF3355BB0AD7EC985D685FB34B9815A00AC2030CBD830E53AFFD21E6CDE01A995F8FC4C6E8F28D7EB54E980A51D2D721DD0106C0E18511E4CCB44B67B70F1A44A33369F00032DEDEDE570D54BAC9CC4397835D1168806BF7F79EC672023E1727E28978596694A4A8B38463F8AF10F3457A858539A2123385E3D3A564EDB36FF76AB1"
Phi2 = "CAFFD366A99A307AE3B9860420B8F104AE39BA61361F5B05A42FE14EA984CC922A6D706E9C41BBE96246C38112B1521DD24E9554D069114F9FA8AEEE763614C247A8069AE40B9BE7CE0119A6EECAD6F01872F9A967F70417F20A22C6E8D2F039D5CB93F1D84BCF01B121A00F26CB5754263833DFBF043BF4A10243B771134B444BD77FF3355BB0AD7EC985D685FB34B9815A00AC2030CBD830E53AFFD21E6CDE01A995F8FC4C6E8F28D7EB54E980A51D2D721DD0106C0E18511E4CCB44B67B70F1A44A33369F00032DEDEDE570D54BAC9CC4397835D1168806BF7F79EC672023E1727E28978596694A4A8B38463F8AF10F3457A858539A2123385E3D3A564EDB36FF76AB1"

mutant_Phi1, stability_Phi1, iter_Phi1, history_Phi1 = mutate_number(Phi1)
mutant_Phi2, stability_Phi2, iter_Phi2, history_Phi2 = mutate_number(Phi2)

# Affichage des résultats
print(f"Phi1 Mutant : {hex(mutant_Phi1) if mutant_Phi1 else 'None'}, Stabilité : {stability_Phi1}, Trouvé après {iter_Phi1} itérations")
print(f"Phi2 Mutant : {hex(mutant_Phi2) if mutant_Phi2 else 'None'}, Stabilité : {stability_Phi2}, Trouvé après {iter_Phi2} itérations")

# Analyse graphique
plt.figure(figsize=(10, 5))
if history_Phi1 and len(history_Phi1) > 1:
    iterations, stability_values = zip(*history_Phi1)
    plt.plot(iterations, stability_values, label="Phi1 Stabilité", marker='o')
    slope, intercept, _, _, _ = linregress(iterations, stability_values)
    plt.plot(iterations, np.array(iterations) * slope + intercept, 'r--', label="Phi1 Régression")
if history_Phi2 and len(history_Phi2) > 1:
    iterations, stability_values = zip(*history_Phi2)
    plt.plot(iterations, stability_values, label="Phi2 Stabilité", marker='s')
    slope, intercept, _, _, _ = linregress(iterations, stability_values)
    plt.plot(iterations, np.array(iterations) * slope + intercept, 'b--', label="Phi2 Régression")

plt.xlabel("Itérations")
plt.ylabel("Nombre de mutations stables")
plt.title("Évolution de la stabilité des mutations avec régression")
plt.legend()
plt.grid()
plt.show()

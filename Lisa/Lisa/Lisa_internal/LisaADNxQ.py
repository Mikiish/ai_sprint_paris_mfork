import os


class QuantumLisa:
    def __init__(self, hidden_variable=None):
        """
        Initialise un état quantique adversarial avec les états possibles 1 et 3.
        """
        self.possible_states = ['1', '3']

        self.state = None  # Indéterminé tant qu’aucune mesure
        if hidden_variable is None:
            self.hidden_variable = int.from_bytes(os.urandom(1), 'big')  # Assurer un entier
        else:
            self.hidden_variable = hidden_variable

        self.measured = False

    def measure(self):
        """Simule l'effondrement en choisissant un état basé sur `hidden_variable`."""
        if not self.measured:
            self.state = '1' if self.hidden_variable % 2 == 0 else '3'
            self.measured = True
        return self.state

    def reset(self):
        """Remet l’état en superposition."""
        self.state = None
        self.measured = False


class LisaQuantumADN(QuantumLisa):
    def __init__(self, hidden_variable=None):
        super().__init__(hidden_variable)

    def mutate_x(self):
        """Renvoie la mesure quantique pour x."""
        return self.measure()


def LisaParserADN(sequence, hidden_variable=None):
    """
    Fonction qui parse une séquence ADN et retourne les index des mutations quantiques.
    """
    possible_states = {'0', '1', '2', '3', 'x'}
    quantum_adn = LisaQuantumADN(hidden_variable)
    sequence = list(sequence)  # Stocke la séquence en tant que liste mutable
    mutation_indexes = []

    for i, char in enumerate(sequence):
        if char not in possible_states:
            raise ValueError(f"Caractère invalide détecté : {char}")
        if char == 'x':
            mutation_indexes.append(i)

    return sequence, mutation_indexes, quantum_adn


# Exemple d'utilisation
if __name__ == "__main__":
    adn_sequence = "0123xx23"
    sequence, mutations, quantum_adn = LisaParserADN(adn_sequence)
    print("Séquence originale:", ''.join(sequence))
    print("Indexes des mutations:", mutations)

    # Appliquer les mutations quantiques
    for index in mutations:
        sequence[index] = quantum_adn.mutate_x()

    print("Séquence après mutation:", ''.join(sequence))

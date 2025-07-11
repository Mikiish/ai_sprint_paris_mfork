class PheromoneType:
    def __init__(self, name, formula, function, volatility, persistence, diffusion, emoji_representation):
        self.name = name  # Nom scientifique
        self.formula = formula  # Formule chimique
        self.function = function  # Type de signal (alarme, nourriture, etc.)
        self.volatility = volatility  # Tendance à se disperser rapidement
        self.persistence = persistence  # Durée de vie dans l'environnement
        self.diffusion = diffusion  # Capacité à se propager
        self.emoji_representation = emoji_representation  # Symbole unique

    def __repr__(self):
        return f"{self.name} ({self.formula}) [{self.function}] {self.emoji_representation}"


# Définition des 5 phéromones principales
PHEROMONES = [
    PheromoneType("1,8-Cinéole", "C10H16O", "Alarme", volatility=0.9, persistence=0.3, diffusion=0.7,
                  emoji_representation="🚨💨🐜"),
    PheromoneType("Acide Formique", "CH2O2", "Défense", volatility=0.8, persistence=0.5, diffusion=0.6,
                  emoji_representation="🛡️🔥🐜"),
    PheromoneType("Décanoate", "C10H20O2", "Piste", volatility=0.2, persistence=0.9, diffusion=0.5,
                  emoji_representation="🛤️🐜📍"),
    PheromoneType("Saccharose", "C12H22O11", "Nourriture", volatility=0.3, persistence=0.8, diffusion=0.4,
                  emoji_representation="🍯🐜🍬"),
    PheromoneType("Héxanone", "C6H12O", "Sexuelle", volatility=0.5, persistence=1.0, diffusion=0.3,
                  emoji_representation="💕🐜🌿"),
]

# Définition des 5 phéromones secondaires
SECONDARY_PHEROMONES = [
    PheromoneType("N3H5", "N3H5", "Alerte", volatility=0.95, persistence=0.1, diffusion=0.9,
                  emoji_representation="⚠️💨🐜"),
    PheromoneType("Benzaldéhyde", "C7H6O", "Agression", volatility=0.7, persistence=0.4, diffusion=0.5,
                  emoji_representation="😡🔥🐜"),
    PheromoneType("Hexanoïque", "C6H12O2", "Regroupement", volatility=0.4, persistence=0.8, diffusion=0.6,
                  emoji_representation="📡🐜🔄"),
    PheromoneType("Octanol", "C8H18O", "Marquage", volatility=0.6, persistence=0.7, diffusion=0.5,
                  emoji_representation="📍🐜🖋️"),
    PheromoneType("Linalool", "C10H18O", "Orientation", volatility=0.5, persistence=0.6, diffusion=0.8,
                  emoji_representation="🧭🐜🌀"),
]

PHEROMONES.append(
    PheromoneType("Octopamine", "C8H11NO", "Sociale", volatility=0.6, persistence=0.7, diffusion=0.5,
                  emoji_representation="🤝🐜🔗")
)

def analyze_pheromone_interaction(pheromone_field):
    """Analyse les interactions entre phéromones dans un flux donné."""
    results = []

    for molecule in pheromone_field.molecules:
        for pheromone in PHEROMONES + SECONDARY_PHEROMONES:
            if pheromone.formula in molecule.formula:
                context = f"🧪 {pheromone.emoji_representation} détecté à {molecule.position} avec intensité {molecule.intensity:.2f}"

                # Adaptation dynamique
                if pheromone.function == "Alarme" and molecule.intensity > 0.8:
                    context += " ⚠️ Forte alerte ! Les fourmis réagissent rapidement."
                elif pheromone.function == "Piste" and molecule.intensity > 0.5:
                    context += " 📍 Formation d'une nouvelle route optimisée."
                elif pheromone.function == "Nourriture" and molecule.intensity > 0.6:
                    context += " 🍯 Signal fort, les ouvrières affluent."

                results.append(context)

    return results


# Exemple d'utilisation
if __name__ == "__main__":
    resultats = analyze_pheromone_interaction(PheromoneField.get_pheromon_field())
    for res in resultats:
        print(res)

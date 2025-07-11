import time
import unicodedata
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PheromoneAnalysis import PHEROMONES, SECONDARY_PHEROMONES, PheromoneType, analyze_pheromone_interaction

# 🚨 SUPPRIMER CETTE LIGNE 🚨
# Définition d'une molécule de phéromone avec son type et ses propriétés physiques
class PheromoneMolecule:
    def __init__(self, position, velocity, pheromone: PheromoneType):
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.intensity = 1.0
        self.pheromone = pheromone  # Stocker directement l'objet

        self.decay_rate = self.pheromone.persistence
        self.diffusion_rate = self.pheromone.diffusion
        self.gravity_effect = np.array([0, 0, -0.001])  # Ajustable



    def update(self, dt):
        """Met à jour la position et réduit l'intensité avec le temps."""
        self.velocity += self.gravity_effect * dt  # Applique la gravité
        self.position += self.velocity * dt
        self.intensity *= np.exp(-self.decay_rate * dt)  # Atténuation exponentielle


# Définition d'une fourmi
class Ant:
    def __init__(self, ant_type, position):
        """
        Initialise une fourmi avec un type et une position.
        - ant_type : "queen", "nourriciere", "ouvriere", "guerriere", "sexuee"
        - position : (x, y, z) position initiale
        """
        self.ant_type = ant_type
        self.position = np.array(position, dtype=np.float64)
        self.pheromone_emission = {
            "queen": 5.0,
            "nourriciere": 2.0,
            "ouvriere": 1.5,
            "guerriere": 2.5,
            "sexuee": 0.5
        }[ant_type]  # Quantité de phéromones émises

        # Vérifier que la direction n'est pas nulle
        self.direction = np.random.randn(3)
        norm = np.linalg.norm(self.direction)
        if norm > 0:
            self.direction /= norm
        else:
            self.direction = np.array([1, 0, 0])  # Direction par défaut

        self.emission_cycle = 50  # Nombre total d'itérations par cycle
        self.current_cycle = 0

    def emit_pheromone(self, pheromone_field):
        if 31 <= self.current_cycle < 50:  # Cycle d’émission actif (19 itérations)
            speed_factor = {
                "queen": 0.5, "nourriciere": 0.8, "ouvriere": 1.2, "guerriere": 1.5, "sexuee": 0.6
            }[self.ant_type]

            pheromone_type_map = {
                "queen": "Alarme",  # Correspondance avec PHEROMONES
                "nourriciere": "Nourriture",
                "ouvriere": "Piste",
                "guerriere": "Défense",
                "sexuee": "Sexuelle"
            }

            pheromone_function = next(
                (p for p in PHEROMONES if p.function.lower() == pheromone_type_map[self.ant_type].lower()), None)

            if pheromone_function is None:
                raise ValueError(f"Type de phéromone inconnu après mapping : {pheromone_type_map[self.ant_type]}")

            # ✅ Ajout du debug
            if self.current_cycle == 32:
                print(f"📡 [DEBUG] Fourmi {self.ant_type} a émis : {pheromone_function.name} {pheromone_function.emoji_representation} à {self.position}")

            for _ in range(int(self.pheromone_emission * 50)):
                velocity = self.direction * speed_factor + np.random.normal(0, 0.1, size=3)
                pheromone_field.add_pheromone(self.position, velocity, pheromone_function)  # ✅ On passe un objet PheromoneType

        self.current_cycle = (self.current_cycle + 1) % self.emission_cycle  # Boucle de cycle

# Simulation du flux de phéromones avec fourmis intégrées
class PheromoneField:
    def __init__(self, size=(100, 100, 100), diffusion_rate=0.01):
        self.size = size
        self.molecules = []
        self.diffusion_rate = diffusion_rate
        self.ants = []  # Liste des fourmis dans le champ

    def add_pheromone(self, position, velocity, pheromone: PheromoneType):
        self.molecules.append(PheromoneMolecule(position, velocity, pheromone))

    def add_ant(self, ant):
        """Ajoute une fourmi au champ de phéromones."""
        self.ants.append(ant)

    def update(self, dt, step):
        """Met à jour toutes les molécules de phéromones et les émissions des fourmis."""
        # ✅ Suppression des phéromones faibles avant l’update
        self.molecules = [m for m in self.molecules if m.intensity > 0.01]

        for molecule in self.molecules:
            molecule.update(dt)

        for ant in self.ants:
            ant.emit_pheromone(self)

    def visualize(self):
        """Affiche les molécules et les fourmis dans l'espace 3D."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Affichage des phéromones sous forme de nuage
        if self.molecules:
            positions = np.array([m.position for m in self.molecules])
            intensities = np.array([m.intensity for m in self.molecules])
            ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c=intensities, cmap='viridis', alpha=0.3, s=5)

        # Affichage des fourmis (différenciées par couleur)
        ant_colors = {"queen": "gold", "nourriciere": "yellow", "ouvriere": "brown", "guerriere": "red",
                      "sexuee": "blue"}
        for ant in self.ants:
            ax.scatter(*ant.position, color=ant_colors[ant.ant_type], s=300, edgecolor="black")

        ax.set_xlim(0, self.size[0])
        ax.set_ylim(0, self.size[1])
        ax.set_zlim(0, self.size[2])
        plt.show()


if __name__ == "__main__":
    # Initialisation du champ de phéromones
    pheromone_field = PheromoneField(size=(100, 100, 100))
    # Ajout de fourmis avec des rôles spécifiques
    pheromone_field.add_ant(Ant("queen", (50, 50, 50)))
    pheromone_field.add_ant(Ant("nourriciere", (52, 48, 50)))
    pheromone_field.add_ant(Ant("ouvriere", (30, 30, 40)))
    pheromone_field.add_ant(Ant("guerriere", (60, 60, 45)))
    pheromone_field.add_ant(Ant("sexuee", (70, 50, 50)))

    # Ajout de phéromones aléatoires dans l'environnement
    # Simulation dynamique
    time_init = time.time()
    for t in range(0xff):
        time_start_update = time.time()
        pheromone_field.update(0.1, t)
        time_end_update = time.time()
        if t % 20 == 0:
            print(f"📊 [DEBUG] Temps d'update : {time_end_update - time_start_update:.8f}s.")
            print(f"📊 [DEBUG] Temps d'update globale : {time_end_update - time_init:.2f}s.")
        # Affichage toutes les 10 itérations pour éviter de surcharger
        if t % 20 == 0:
            pheromone_field.visualize()
            print(f"\n📊 [DEBUG] États possibles avant mesure: {hex(t)}\n")
    time_end = time.time()
    time_total = time_end - time_init
    print(f"📊 [DEBUG] Temps total : {time_total:.2f}s.")

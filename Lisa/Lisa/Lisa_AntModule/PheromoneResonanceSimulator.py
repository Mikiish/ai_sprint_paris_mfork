import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class PheromoneResonanceSimulator:
    def __init__(self, size=(50, 50, 50), decay_rate=0.01, diffusion_rate=0.02, frequency_range=(0.1, 2.0)):
        self.size = size  # Taille de l'espace
        self.pheromone_field = np.zeros(size)  # Champ de phéromones 3D
        self.decay_rate = decay_rate  # Taux de décroissance des phéromones
        self.diffusion_rate = diffusion_rate  # Taux de diffusion
        self.frequency_range = frequency_range  # Fréquences des oscillations
        self.time = 0  # Temps simulé

    def add_pheromone(self, position, intensity, frequency):
        """Ajoute une molécule de phéromone avec une fréquence spécifique."""
        x, y, z = position
        if 0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2]:
            self.pheromone_field[x, y, z] += intensity * np.sin(2 * np.pi * frequency * self.time)

    def update(self, dt=1):
        """Met à jour la propagation et l'atténuation des phéromones."""
        diffusion = np.roll(self.pheromone_field, 1, axis=0) + np.roll(self.pheromone_field, -1, axis=0)
        diffusion += np.roll(self.pheromone_field, 1, axis=1) + np.roll(self.pheromone_field, -1, axis=1)
        diffusion += np.roll(self.pheromone_field, 1, axis=2) + np.roll(self.pheromone_field, -1, axis=2)
        diffusion /= 6  # Normalisation
        self.pheromone_field += self.diffusion_rate * (diffusion - self.pheromone_field)
        self.pheromone_field *= np.exp(-self.decay_rate * dt)  # Décroissance
        self.time += dt

    def visualize(self):
        """Affiche une coupe 3D du champ de phéromones."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x, y, z = np.where(self.pheromone_field > 0.01)
        c = self.pheromone_field[x, y, z]
        ax.scatter(x, y, z, c=c, cmap='inferno')
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Simulation de Résonance des Phéromones")
        plt.show()


# Test du simulateur
if __name__ == "__main__":
    simulator = PheromoneResonanceSimulator()
    simulator.add_pheromone((25, 25, 25), intensity=1.0, frequency=1.0)
    for _ in range(50):
        simulator.update()
    simulator.visualize()

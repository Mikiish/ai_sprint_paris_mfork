import numpy as np
import matplotlib.pyplot as plt
import random
from Visualization_old import draw_creature


# Définition des classes de neurones
class Neuron:
    def __init__(self, neuron_type):
        self.neuron_type = neuron_type
        self.input_connections = []  # connexions entrantes
        self.output_value = 0  # la sortie du neurone après activation
        self.name = f'{neuron_type}'

    def add_connection(self, target_neuron, weight):
        self.input_connections.append((target_neuron, weight))

    def compute_output(self, inputs):
        # Somme des entrées pondérées
        weighted_sum = np.sum(inputs)
        # Activation avec la fonction tanh
        self.output_value = np.tanh(weighted_sum)
        return self.output_value


class Creature:
    def __init__(self, genome_length=4):
        self.sensory_neurons = [Neuron('Sen') for _ in range(10)]  # Entrées sensorielles
        self.internal_neurons = [Neuron('N') for _ in range(3)]  # Neurones internes
        self.action_neurons = [Neuron('Out') for _ in range(5)]  # Neurones d'actions
        self.genome = self.generate_random_genome(genome_length)
        self.connections = self.create_connections_from_genome()

    def generate_random_genome(self, genome_length):
        # Génère un génome aléatoire, représenté ici par un tableau d'entiers
        return np.random.randint(0, 2, size=(genome_length, 5))

    def create_connections_from_genome(self):
        connections = []
        for gene in self.genome:
            source_type = gene[0]  # Le type de source (neurone sensoriel ou interne)
            sink_type = gene[2]  # Le type de cible (neurone interne ou action)
            weight = random.uniform(-4, 4)  # Poids de la connexion

            if source_type == 0:  # Si c'est une connexion d'un neurone sensoriel
                source_neuron = random.choice(self.sensory_neurons)
            else:  # Si c'est un neurone interne
                source_neuron = random.choice(self.internal_neurons)

            if sink_type == 0:  # Connexion vers un interne
                sink_neuron = random.choice(self.internal_neurons)
            else:  # Connexion vers une action
                sink_neuron = random.choice(self.action_neurons)

            connections.append((source_neuron, sink_neuron, weight))
        return connections

    def process_sensory_inputs(self, inputs):
        for i, input_value in enumerate(inputs):
            self.sensory_neurons[i].compute_output([input_value])

    def step(self):
        # Passe une étape de simulation
        for source, sink, weight in self.connections:
            sink.compute_output([source.output_value * weight])

    def get_actions(self):
        # Obtenir la sortie des neurones d'action
        return [neuron.output_value for neuron in self.action_neurons]


# Simulation de base
def run_simulation(num_creatures=1, steps=1):
    creatures = [Creature() for _ in range(num_creatures)]

    for step in range(steps):
        print(f"Step {step + 1}:")
        for i, creature in enumerate(creatures):
            # Entrée sensorielle aléatoire (exemple)
            sensory_inputs = np.random.rand(10)
            creature.process_sensory_inputs(sensory_inputs)
            creature.step()
            actions = creature.get_actions()
            print(f"  Creature {i + 1} actions: {actions}")

            draw_creature(creature)


# Lancer la simulation
run_simulation()

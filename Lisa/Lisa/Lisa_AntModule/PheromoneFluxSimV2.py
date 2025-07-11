import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
import PheromoneField

# Paramètres de la fourmilière
num_nodes = 50  # Nombre total de nœuds (salles + intersections)
num_layers = 5  # Nombre de couches de la fourmilière
radius = 10  # Rayon maximal d'expansion horizontale

# Création du graphe
G = nx.Graph()
positions = {}
node_types = {}

# Types de fourmis
ant_types = ["queen", "nourriciere", "ouvriere", "guerriere", "sexuee"]
probabilities = {"queen": 0.0, "nourriciere": 0.05, "ouvriere": 0.61, "guerriere": 0.3, "sexuee": 0.035}
colors = {"queen": "gold", "nourriciere": "yellow", "ouvriere": "brown", "guerriere": "red", "sexuee": "blue"}

# Génération de la pyramide inversée (fourmilière)
for layer in range(num_layers):
    num_nodes_layer = max(1, int(num_nodes * (1 - layer / num_layers)))  # Moins de nœuds en profondeur
    height = -layer * 5  # Profondeur croissante
    for i in range(num_nodes_layer):
        x = np.random.uniform(-radius * (1 - layer / num_layers), radius * (1 - layer / num_layers))
        y = np.random.uniform(-radius * (1 - layer / num_layers), radius * (1 - layer / num_layers))
        node_id = f"{layer}_{i}"
        G.add_node(node_id, pos=(x, y, height))
        positions[node_id] = (x, y, height)

# Connexions entre les nœuds avec densité de phéromones
nodes_list = list(G.nodes)
for i in range(len(nodes_list)):
    for j in range(i + 1, len(nodes_list)):
        if np.random.rand() < 0.1:  # Probabilité de connexion faible pour éviter trop de liens
            pheromone_density = np.random.rand()  # Densité aléatoire entre 0 et 1
            G.add_edge(nodes_list[i], nodes_list[j], pheromone_density=pheromone_density)

# Création de la figure
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Récupération des positions
pos_3d = nx.get_node_attributes(G, 'pos')

# Tracé des nœuds
for node, (x, y, z) in pos_3d.items():
    ax.scatter(x, y, z, color='brown', s=20)  # Salles en brun

# Tracé des arêtes avec coloration par densité de phéromones
norm = mcolors.Normalize(vmin=0, vmax=1)
cmap = plt.get_cmap("coolwarm")

for edge in G.edges:
    x_vals = [pos_3d[edge[0]][0], pos_3d[edge[1]][0]]
    y_vals = [pos_3d[edge[0]][1], pos_3d[edge[1]][1]]
    z_vals = [pos_3d[edge[0]][2], pos_3d[edge[1]][2]]
    density = G.edges[edge]['pheromone_density']
    ax.plot(x_vals, y_vals, z_vals, color=cmap(norm(density)), alpha=0.8, linewidth=2)  # Tunnels colorés

# Fonction pour extraire le champ de phéromones à une position donnée sur une arête
def get_pheromone_field(edge, position_factor):
    """
    Génère un champ local de phéromones à partir d'une arête donnée et d'un facteur de position (0 à 1).
    Intègre également l'effet des fourmis situées autour de cette arête.
    """
    node1, node2 = edge
    pos1, pos2 = np.array(pos_3d[node1]), np.array(pos_3d[node2])

    # Interpolation de la position
    local_position = pos1 + position_factor * (pos2 - pos1)

    # Récupération de la densité de phéromones sur l'arête
    density = G.edges[edge]['pheromone_density']

    # Création du champ local
    field = PheromoneField.PheromoneField(size=(20, 20, 20), diffusion_rate=0.02)

    # Ajout des phéromones de base liées à l'arête
    for _ in range(int(density * 100)):
        velocity = np.random.normal(0, 0.5, size=3)  # Vitesse aléatoire
        field.add_pheromone(local_position, velocity)

    # **Nouvelle partie : Influence des fourmis proches**
    for node in [node1, node2]:
        if node in node_types:
            ant_type = node_types[node]
            node_position = np.array(pos_3d[node])

            # Définition des effets des fourmis sur les phéromones
            pheromone_boost = 0
            if ant_type == "queen":
                pheromone_boost = 5.0  # Forte émission stabilisatrice
            elif ant_type == "nourriciere":
                pheromone_boost = 2.0  # Influence sur les zones maternales
            elif ant_type == "ouvriere":
                pheromone_boost = 1.5  # Marquage des chemins
            elif ant_type == "guerriere":
                pheromone_boost = 2.5  # Marquage agressif
            elif ant_type == "sexuee":
                pheromone_boost = 0.5  # Peu d’émission, réactivité accrue

            # Génération du champ de phéromones autour de la fourmi
            for _ in range(int(pheromone_boost * 50)):  # Ajustement du nombre de molécules générées
                velocity = np.random.normal(0, 0.3, size=3)  # Déplacement plus lent des phéromones des fourmis
                field.add_pheromone(node_position, velocity)

    return field


if __name__ == "__main__":
    # Affichage
    ax.set_title("Modélisation 3D d'une Fourmilière (Graphe) avec Densité de Phéromones")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Profondeur")

    plt.show()
    handles, labels = ax.get_legend_handles_labels()
    if labels:
        ax.legend()


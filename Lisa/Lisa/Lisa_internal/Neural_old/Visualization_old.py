import matplotlib.pyplot as plt
import networkx as nx


# Cette fonction dessine le réseau neuronal d'une créature
def draw_creature(creature):
    connections = creature.connections

    # Filtrons les neurones connectés seulement
    sensor_neurons = [n for n in creature.sensory_neurons if any(conn[0] == n or conn[1] == n for conn in connections)]
    action_neurons = [n for n in creature.action_neurons if any(conn[0] == n or conn[1] == n for conn in connections)]
    internal_neurons = [n for n in creature.internal_neurons if
                        any(conn[0] == n or conn[1] == n for conn in connections)]

    # Initialisation du Graphe
    G = nx.DiGraph()

    for neuron in sensor_neurons + internal_neurons + action_neurons:
        G.add_node(neuron.name, type=neuron.neuron_type)

    for conn in connections:
        if conn[0].name in G.nodes and conn[1].name in G.nodes:
            G.add_edge(conn[0].name, conn[1].name, weight=conn[2])

    # Positionnement des nœuds avec le layout spring (cercle restreint)
    pos = nx.spring_layout(G, center=(0.5, 0.5), scale=2)

    # Taille et couleur des neurones, augmentation de la taille des nœuds
    plt.figure(figsize=(8, 8))
    node_colors = [neuron_color(G.nodes[n]['type']) for n in G.nodes]

    # Récupération des poids pour colorer les flèches
    edge_colors = ['green' if G[u][v]['weight'] > 0 else 'red' for u, v in G.edges]
    edge_widths = [2 + abs(G[u][v]['weight']) for u, v in G.edges]  # Épaisseur basée sur le poids

    # Affichage des nœuds avec bordures plus épaisses
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=10000, font_size=20, font_color="black",
            edge_color=edge_colors, width=edge_widths, arrowsize=25, connectionstyle="arc3,rad=0.3", linewidths=2,
            edgecolors='black')

    # Ajouter les étiquettes de poids sur les connexions, y compris les boucles
    edge_labels = {(conn[0].name, conn[1].name): round(conn[2], 2) for conn in connections if
                   conn[0].name in G and conn[1].name in G}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Gestion des boucles (les arcs avec un radian élevé pour qu'ils soient visibles)
    for u, v in G.edges:
        if u == v:  # Cas d'une boucle
            plt.annotate('', xy=pos[v], xytext=pos[u],
                         arrowprops=dict(arrowstyle="->", color='green' if G[u][v]['weight'] > 0 else 'red',
                                         lw=2 + abs(G[u][v]['weight']),
                                         connectionstyle="arc3,rad=0.5"))  # Boucle plus prononcée

    # Fond gris
    plt.gca().set_facecolor('lightgray')

    plt.title('Visualisation du réseau de neurones')
    plt.show()


# Fonction pour gérer les couleurs des neurones
def neuron_color(neuron_type):
    if neuron_type == 'Sen':
        return 'blue'
    elif neuron_type == 'Out':
        return 'red'
    else:
        return 'darkgray'

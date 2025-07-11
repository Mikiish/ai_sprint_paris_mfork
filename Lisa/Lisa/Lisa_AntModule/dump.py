import time
import math
import random
from collections import defaultdict, deque


# =====================================================================
#                         GESTION DU GENOME / NN
# =====================================================================

class Genome:
    def __init__(self, connections=None, nb_inputs=0, nb_outputs=0):
        self.nb_inputs = nb_inputs
        self.nb_outputs = nb_outputs
        self.connections = connections if connections else []

    def mutate(self):
        if not self.connections:
            return
        idx = random.randrange(len(self.connections))
        src, tgt, w = self.connections[idx]
        self.connections[idx] = (src, tgt, w + random.uniform(-0.1, 0.1))


class NeuralNet:
    def __init__(self, genome: "Genome"):
        self.genome = genome
        self.nb_inputs = genome.nb_inputs
        self.nb_outputs = genome.nb_outputs

        # Identifions tous les neurones mentionnés
        self.all_neurons = set()
        for (s, t, w) in genome.connections:
            self.all_neurons.add(s)
            self.all_neurons.add(t)

        # Liste d'adjacence
        self.adj_list = defaultdict(list)
        for (s, t, w) in genome.connections:
            self.adj_list[s].append((t, w))

        max_id = max(self.all_neurons) if self.all_neurons else 0
        self.input_ids = list(range(self.nb_inputs))
        self.output_ids = list(range(max_id - self.nb_outputs + 1, max_id + 1))

        self.useful_neurons = self._find_useful_neurons()

    def _find_useful_neurons(self):
        reverse_adj = defaultdict(list)
        for src, targets in self.adj_list.items():
            for (tgt, _) in targets:
                reverse_adj[tgt].append(src)

        visited = set()
        queue = deque(self.output_ids)

        while queue:
            current = queue.popleft()
            visited.add(current)
            for ancestor in reverse_adj[current]:
                if ancestor not in visited:
                    visited.add(ancestor)
                    queue.append(ancestor)

        return visited

    def forward(self, inputs):
        neuron_values = {}

        # Initialisation entrées
        for i, val in enumerate(inputs):
            neuron_values[i] = val

        # Les autres à 0
        for n in self.all_neurons:
            if n not in neuron_values:
                neuron_values[n] = 0.0

        # Propagation naïve
        for _ in range(len(self.all_neurons)):
            for src in self.useful_neurons:
                val_src = neuron_values[src]
                for (tgt, w) in self.adj_list[src]:
                    if tgt in self.useful_neurons:
                        neuron_values[tgt] += val_src * w

        outputs = [neuron_values[out_n] for out_n in self.output_ids]
        return outputs


# =====================================================================
#                           ENVIRONNEMENT
# =====================================================================

class Environment:
    ###
    ### Gère le cycle jour/nuit + température +
    ### la "carte" 2D : anthill, fire spots, food spots.
    ###

    def __init__(self, width=200, height=200, current_day=1):
        self.current_day = current_day

        # Dimension du monde
        self.width = width
        self.height = height

        # Températures moyennes
        self.day_temperature = 25.0
        self.night_temperature = 15.0

        # On calcule la surface totale
        self.surface = width * height

        # ---- Définition de la fourmilière (anthill) ----
        # On veut que la fourmilière fasse ~1/42 de la surface.
        anthill_area = self.surface / 42.0
        self.anthill_radius = math.sqrt(anthill_area / math.pi)

        # On la place en haut à gauche : son centre sera
        # (anthill_radius, anthill_radius), pour qu'elle tienne dans le coin
        self.anthill_center = (self.anthill_radius, self.anthill_radius)

        # ---- Points de feu ----
        # On veut 7 spots de feu, total ~1/42 de la surface.
        # On va en faire 7 cercles, chacun occupant ~ (1/42)/7 => 1/294 de la surface
        fire_area_each = self.surface / 294.0
        fire_radius_each = math.sqrt(fire_area_each / math.pi)

        self.fire_spots = []
        for _ in range(7):
            # On place un spot loin de la fourmilière => par ex. en choisissant
            # random uniform sur [width*0.5 .. width], [height*0.5 .. height]
            fx = random.uniform(self.width * 0.6, self.width * 0.9)
            fy = random.uniform(self.height * 0.6, self.height * 0.9)
            self.fire_spots.append((fx, fy, fire_radius_each))

        # ---- Points de nourriture ----
        # 3 cercles de nourriture, on peut les placer un peu aléatoirement
        # mais pas trop près de la fourmilière
        food_area_each = self.surface / 600.0  # Par exemple plus petit
        food_radius_each = math.sqrt(food_area_each / math.pi)

        self.food_spots = []
        for _ in range(3):
            # random dans le quart "milieu" ?
            fx = random.uniform(self.width * 0.3, self.width * 0.7)
            fy = random.uniform(self.height * 0.3, self.height * 0.7)
            self.food_spots.append((fx, fy, food_radius_each))

    def get_temperature(self, hour):
        is_day = (7 <= hour < 19)
        base_temp = self.day_temperature if is_day else self.night_temperature

        # Variation saisonnière
        seasonal_factor = math.sin((self.current_day / 365.0) * 2 * math.pi)
        season_offset = 5.0 * seasonal_factor

        return base_temp + season_offset

    def in_anthill(self, x, y):
        """Vérifie si (x,y) est dans la fourmilière."""
        cx, cy = self.anthill_center
        r = self.anthill_radius
        return (x - cx) ** 2 + (y - cy) ** 2 <= r * r

    def in_fire(self, x, y):
        """Retourne True si (x,y) se trouve dans un des spots de feu."""
        for (fx, fy, fr) in self.fire_spots:
            if (x - fx) ** 2 + (y - fy) ** 2 <= fr * fr:
                return True
        return False

    def which_food_spot(self, x, y):
        """
        Retourne l'indice du spot de nourriture dans lequel (x,y) se trouve,
        ou None s'il n'est dans aucun.
        """
        for i, (fx, fy, fr) in enumerate(self.food_spots):
            if (x - fx) ** 2 + (y - fy) ** 2 <= fr * fr:
                return i
        return None

    def next_day(self):
        self.current_day += 1
        if self.current_day > 365:
            self.current_day = 1


# =====================================================================
#                           CREATURE
# =====================================================================

class Creature:
    """
    Fourmi :
     - âge en jours
     - énergie
     - inventaire
     - position (x,y)
     - genome -> brain
     - direction initiale aléatoire (0..pi/2)
     - peut manger 2 fois par jour pour récupérer la moitié de son énergie
     - meurt si energy <= 0
     - objectif : ramener de la "food" à la fourmilière
    """

    def __init__(self, environment: Environment, name="Antoinette", max_lifespan=365):
        self.name = name

        # On la place au hasard dans la fourmilière (ou au centre)
        self.x, self.y = environment.anthill_center

        self.age = 1
        self.energy = 100.0
        self.is_alive = True
        self.max_lifespan = max_lifespan

        self.inventory = {
            "food": 0,  # la fourmi peut transporter de la nourriture
            "sugar": 0,
            "pheromone": 0
        }

        # Génome par défaut : 4 entrées, 2 sorties, par ex.:
        # (0) = temp, (1) = energy, (2) = angleX, (3) = angleY
        # => (Xout, Yout)
        # On pourra complexifier plus tard
        default_genome = Genome(
            connections=[(0, 4, 0.5), (1, 5, 1.0), (2, 4, 0.2), (3, 5, 0.2)],
            nb_inputs=4,
            nb_outputs=2
        )
        self.genome = default_genome
        self.brain = NeuralNet(default_genome)

        # Comptage de repas par jour (max 2)
        self.meals_today = 0

        # Direction initiale aléatoire entre 0 et pi/2
        angle = random.uniform(0, math.pi / 2)
        # On stocke un vecteur direction (dx, dy)
        self.dir_x = math.cos(angle)
        self.dir_y = math.sin(angle)

    def new_day(self):
        """Appelé en début de chaque journée pour reset certains compteurs."""
        self.age += 1
        self.meals_today = 0

        if self.age > self.max_lifespan:
            print(f"{self.name} meurt de vieillesse (age={self.age}).")
            self.is_alive = False

    def live_one_day(self, environment: Environment, speed_factor=1.0):
        """
        Simule 24h. Chaque heure = 1s / speed_factor.
        - gère la température
        - meurt si energy <= 0
        - ramasse la nourriture (food_spot) si on est dessus
        - peut déposer la nourriture si on est dans la fourmilière
        - si on touche du feu, on perd de l'énergie
        - peut manger 2 fois par jour pour +50% d'énergie (limitée à 100)
        - déplace la fourmi selon le NN
        """
        if not self.is_alive:
            return

        self.new_day()  # Incrémente l'âge, reset meals_today
        if not self.is_alive:
            return  # Elle est morte de vieillesse

        for hour in range(24):
            # tempo
            time.sleep(1.0 / speed_factor)

            if self.energy <= 0:
                print(f"{self.name} est morte d'épuisement (energy=0).")
                self.is_alive = False
                return

            temp = environment.get_temperature(hour)

            # Sélection inputs pour le NN
            # 0 => temp / 50.0
            # 1 => energy / 100.0
            # 2 => dir_x
            # 3 => dir_y
            sensor_temp = temp / 50.0
            sensor_energy = self.energy / 100.0

            inputs = [sensor_temp, sensor_energy, self.dir_x, self.dir_y]
            outputs = self.brain.forward(inputs)

            # Sorties : dx, dy → on normalise un peu
            dx, dy = outputs
            # On peut envisager un petit facteur de vitesse
            speed = 1.0  # paramétrable
            self.x += dx * speed
            self.y += dy * speed

            # Mise à jour direction (optionnel, on la recalcule)
            norm = math.hypot(dx, dy)
            if norm > 1e-6:
                self.dir_x = dx / norm
                self.dir_y = dy / norm

            # On empêche de sortir du monde
            if self.x < 0: self.x = 0
            if self.x > environment.width: self.x = environment.width
            if self.y < 0: self.y = 0
            if self.y > environment.height: self.y = environment.height

            # Coût d'énergie (distance parcourue)
            dist = math.hypot(dx * speed, dy * speed)
            self.energy -= dist

            # FEU : si on est dans un spot de feu, on perd beaucoup d'énergie
            if environment.in_fire(self.x, self.y):
                self.energy -= 5.0  # p.ex. chaque heure où on est dans le feu

            # NOURRITURE : si on est dans un food_spot et qu'on n'en a pas déjà beaucoup
            spot_index = environment.which_food_spot(self.x, self.y)
            if spot_index is not None:
                # On ramasse un peu
                self.inventory["food"] += 1
                print(f"{self.name} ramasse de la nourriture au spot {spot_index}!")

            # DÉPÔT : si on est dans la fourmilière, on dépose la nourriture à la reine
            if environment.in_anthill(self.x, self.y) and self.inventory["food"] > 0:
                print(f"{self.name} rapporte {self.inventory['food']} de food à la reine!")
                self.inventory["food"] = 0

            # MANGER : on peut manger 2 fois par jour → si energy < 50, on peut décider de manger
            # (on suppose qu'on a besoin d'avoir de la nourriture sur soi → "food" > 0)
            if self.energy < 50 and self.meals_today < 2 and self.inventory["food"] > 0:
                self.meals_today += 1
                # On mange 1 unité de food
                self.inventory["food"] -= 1
                gained = self.energy * 0.5  # +50% de l'énergie courante
                self.energy += gained
                if self.energy > 100:
                    self.energy = 100
                print(f"{self.name} mange et récupère son énergie (-> {self.energy:.1f}).")

        # Fin de journée → rien de spécial ici, on passera au jour suivant
        # via environment.next_day()

    def __str__(self):
        status = "vivante" if self.is_alive else "morte"
        return (f"{self.name}({status}, age={self.age}, x={self.x:.2f}, "
                f"y={self.y:.2f}, energy={self.energy:.1f}, inv={self.inventory})")


# =====================================================================
#                           DEMO
# =====================================================================

if __name__ == "__main__":
    # On crée l'environnement
    env = Environment(width=200, height=200, current_day=1)

    # On crée une fourmi
    my_ant = Creature(environment=env, name="Antoinette", max_lifespan=365)

    # Paramètre de vitesse
    # 1h = 1s => 1j = 24s => 6j = ~144s
    # speed_factor=7 => 1j = ~3.4s
    SPEED_FACTOR = 3.0

    # On simule quelques jours
    nb_jours_simul = 6
    for day in range(nb_jours_simul):
        if not my_ant.is_alive:
            break

        print(f"\n=== Début Jour {env.current_day} ===")
        my_ant.live_one_day(env, speed_factor=SPEED_FACTOR)
        print(my_ant)

        env.next_day()

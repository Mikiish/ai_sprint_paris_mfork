import math, random
import GenomeNo
from collections import defaultdict, deque


ANT_SENSORS = [
    "Slr",  # Pheromon gradiant horizontal
    "Sfd",  # Pheromon gardiant forward
    "Sg",   # Pheromon density
    "Age",  # Age (used to incentivize ants to return to their queen before dying).
    "Rnd",  # Random input
    "Osc",  # Oscillator -- Based on temp
    "Blr",  # Blockage left/right
    "Bfd",  # Blockage forward
    "Pfd",  # Pop gradiant forward
    "Plr",  # Pop gardiant left/right
    "Pop",  # Pop density
    "LPf",  # Pop long-range forward
    "LBf",  # Blockage long-range forward
    "Lx",   # Grid location X
    "Ly",   # Grid location Y
    "LMx",  # Grid previous X
    "LMy",  # Grid previous Y
    "LTx",  # Grid tangente X -- Closest Grid cell to innate line
    "LTy",  # Grid tangente Y
    "Inn",  # Angle in [0, Pi/2] -- This determines an innate line from the queen (0,0). In practice, this is a constant the ant is born with.
    "BD",   # Distance to nearest grid border.
    "Idt",  # Distance to innate line.
    "Idp",  # Angle in [-Pi/2, Pi/2] -- This determines the angle the ant should take from tangente in order to reach innate line in one day. Negative = toward queen.
]

ANT_ACTIONS = [
    "Mfd",  # forward
    "Mrn",  # random
    "Mrv",  # reverse
    "Mgh",  # grid horizontal
    "Mgv",  # grid vertical
    "Mtn",  # tangente
    "Mvs",  # projection
    "SG",   # pheromone
    "OSC",  # oscillator period
    "LPD",  # long-probe distance
    "Kill", # plus tard
    # ... etc.
]


class AntGenome(Genome):
    ###
    ### Spécialisation possible de la classe Genome
    ### qui connaît nb_inputs, nb_outputs = len(ANT_SENSORS), len(ANT_ACTIONS).
    ### On peut y ajouter des règles de mutation particulières,
    ### ou un 'réseau minimal' comme point de départ.
    ###

    def __init__(self, connections=None):
        nb_inputs = len(ANT_SENSORS)
        nb_outputs = len(ANT_ACTIONS)
        super().__init__(connections=connections, nb_inputs=nb_inputs, nb_outputs=nb_outputs)

    def init_minimal(self):
        ###
        ### Exemple : on crée quelques connexions de base,
        ### par ex. Sg -> SG, ou Rnd -> Mrn, etc.
        ### pour avoir un comportement non-nul au début.
        ###
        self.connections = []
        # Par exemple, sensor #2 = 'Sg' => output #7 = 'SG'
        # Indice sensor = 2, indice output = (nb_inputs + nb_hidden) + 7
        # Sauf qu'on ne sait pas encore nb_hidden.
        # Pour faire simple, on suppose qu'il n'y a pas de neurone caché initial :
        # → Les sorties commencent à l'id = nb_inputs
        base_output_id = self.nb_inputs  # = len(ANT_SENSORS)

        # On mappe 'Sg' -> 'SG'
        i_sg = ANT_SENSORS.index("Sg")
        o_sg = base_output_id + ANT_ACTIONS.index("SG")
        self.connections.append((i_sg, o_sg, 1.0))

        # sensor 'Rnd' -> 'Mrn'
        i_rnd = ANT_SENSORS.index("Rnd")
        o_mrn = base_output_id + ANT_ACTIONS.index("Mrn")
        self.connections.append((i_rnd, o_mrn, 0.8))

        # etc. on peut en rajouter d'autres...

    def mutate(self):
        # soit on garde la mutation existante du parent :
        super().mutate()
        # soit on y ajoute des règles spécifiques


class AntNeuralNet(NeuralNet):
    ###
    ### Réseau spécialisé, si on veut surcharger la forward() pour y mettre
    ### un calcul plus complet (p. ex. tanh sur chaque neurone).
    ###
    def __init__(self, genome: AntGenome):
        super().__init__(genome)

    def forward(self, inputs):
        # On veut appliquer une activation (tanh) sur chaque neurone.
        # On peut donc faire un forward "en couches", ou l'approche naïve + activation au fur et à mesure.
        # Exemple : on stocke la somme pour chaque neurone, puis on applique tanh.
        neuron_values = {n: 0.0 for n in self.all_neurons}

        # init entrées directes (souvent sans activation)
        for i, val in enumerate(inputs):
            neuron_values[i] = val

        # on fait un certain nombre de passes
        for _ in range(len(self.all_neurons)):
            for src in self.useful_neurons:
                val_src = math.tanh(neuron_values[src])  # activation
                for (tgt, w) in self.adj_list[src]:
                    if tgt in self.useful_neurons:
                        neuron_values[tgt] += val_src * w

        # Valeur de sortie
        outputs = []
        for out_n in self.output_ids:
            outputs.append(math.tanh(neuron_values[out_n]))

        return outputs


import math, random, time
from creature import Creature  # On suppose que ta classe Creature est dans un fichier creature.py
from ant_genome import AntGenome, AntNeuralNet, ANT_SENSORS, ANT_ACTIONS


# (où ant_genome contient la définition de AntGenome, AntNeuralNet, etc.)
# Sinon, adapte l'import selon ta structure de fichiers

class AntCreature(Creature):
    ###
    ### Hérite de Creature.
    ### Spécialise la partie "cerveau" (AntGenome, AntNeuralNet),
    ### et gère les capteurs/actions propres aux fourmis.
    ###

    def __init__(self, environment, name="Antoinette", max_lifespan=365, genome=None):
        super().__init__(environment, name, max_lifespan)

        # Si aucun genome fourni, on en crée un "minimal".
        if genome is None:
            genome = AntGenome()
            genome.init_minimal()  # Par ex. on y définit quelques connexions de base

        self.genome = genome
        # On construit un AntNeuralNet, qui applique (par ex) une activation tanh
        self.brain = AntNeuralNet(genome)

        # Exemple : angle inné
        self.innate_angle = random.uniform(0, math.pi / 2)

        # On peut initialiser direction d'après l'angle inné
        self.dir_x = math.cos(self.innate_angle)
        self.dir_y = math.sin(self.innate_angle)

    def get_sensor_values(self, environment):
        ###
        ### Retourne un vecteur (liste) de float correspondant à l'ordre de ANT_SENSORS.
        ### Par ex. "Slr", "Sfd", "Sg", "Age", "Rnd", etc.
        ### Ici, on montre quelques exemples, à toi de compléter.
        ###
        values = []
        for sensor_name in ANT_SENSORS:
            if sensor_name == "Slr":
                val = self.compute_slr(environment)
            elif sensor_name == "Sfd":
                val = self.compute_sfd(environment)
            elif sensor_name == "Sg":
                val = self.compute_sg(environment)
            elif sensor_name == "Age":
                # Normalisation possible, ex. age / 365
                val = min(self.age / 365.0, 1.0)
            elif sensor_name == "Rnd":
                val = random.random()
            elif sensor_name == "Osc":
                # Ex: un oscillator couplé à la temp
                val = self.compute_osc(environment)
            elif sensor_name == "Lx":
                # Ex: normaliser x dans [0..1]
                val = self.x / environment.width
            elif sensor_name == "Ly":
                val = self.y / environment.height
            elif sensor_name == "Inn":
                # angle inné normalisé dans [0..1], en divisant par pi/2
                val = self.innate_angle / (math.pi / 2)
            else:
                # Par défaut
                val = 0.0
            values.append(val)
        return values

    # Exemple de méthodes "dummy" pour calculer certains senseurs
    def compute_slr(self, environment):
        # "slr" → pheromone gradient left-right
        # En attendant la vraie logique, on met un random
        return random.uniform(0, 1)

    def compute_sfd(self, environment):
        # "sfd" => pheromone gradient forward
        return random.uniform(0, 1)

    def compute_sg(self, environment):
        # "sg" => pheromone density
        return random.uniform(0, 5)

    def compute_osc(self, environment):
        # Ex: couplage avec la temperature de l'heure courante
        # on prend la temperature, la normalise, et fait un sin() par ex.
        hour = 12  # un placeholder si on n'a pas l'heure en param
        temp = environment.get_temperature(hour)
        return math.sin(temp * 0.1)

    def apply_actions(self, outputs, environment):
        ###
        ### Interprète la liste 'outputs' (même taille que ANT_ACTIONS),
        ### et exécute les actions correspondantes.
        ### On fait un winner-takes-all pour le mouvement
        ### (Mfd, Mrn, Mrv, Mgh, Mgv, Mtn, Mvs),
        ### et on active SG, OSC, LPD, Kill si leur valeur > 0, par ex.
        ###
        # 1) Mouvement
        move_names = ["Mfd", "Mrn", "Mrv", "Mgh", "Mgv", "Mtn", "Mvs"]
        move_indices = [ANT_ACTIONS.index(m) for m in move_names]
        move_vals = [outputs[i] for i in move_indices]

        best_idx = max(range(len(move_vals)), key=lambda i: move_vals[i])
        chosen_move = move_names[best_idx]

        if chosen_move == "Mfd":
            self.move_forward()
        elif chosen_move == "Mrn":
            self.move_random()
        elif chosen_move == "Mrv":
            self.move_reverse()
        elif chosen_move == "Mgh":
            self.move_grid_h()
        elif chosen_move == "Mgv":
            self.move_grid_v()
        elif chosen_move == "Mtn":
            self.move_tangente()
        elif chosen_move == "Mvs":
            self.move_projection()

        # 2) Autres actions
        # "SG" → emit pheromone
        i_sg = ANT_ACTIONS.index("SG")
        if outputs[i_sg] > 0:
            self.emit_pheromone()

        # "OSC" => set oscillator period
        i_osc = ANT_ACTIONS.index("OSC")
        if outputs[i_osc] > 0.5:
            self.set_oscillator_period()

        # "LPD" => long-probe distance
        i_lpd = ANT_ACTIONS.index("LPD")
        if outputs[i_lpd] > 0:
            self.do_long_probe()

        # "Kill"
        i_kill = ANT_ACTIONS.index("Kill")
        if outputs[i_kill] > 0.8:
            self.kill_forward_neighbor()

    # --- Implémentation des actions "dummy" ---

    def move_forward(self):
        # Ex. avance dans la direction courante self.dir_x, self.dir_y
        speed = 1.0
        self.x += self.dir_x * speed
        self.y += self.dir_y * speed

    def move_random(self):
        # ex. un déplacement aléatoire
        angle = random.uniform(0, 2 * math.pi)
        speed = 1.0
        self.x += math.cos(angle) * speed
        self.y += math.sin(angle) * speed

    def move_reverse(self):
        # recule (ou va vers la fourmilière)
        self.x -= self.dir_x
        self.y -= self.dir_y

    def move_grid_h(self):
        # Ex. se déplace horizontalement, + ou - selon le signe de self.dir_x
        # On peut imaginer un winner-takes-all sur la direction.
        pass

    def move_grid_v(self):
        # etc.
        pass

    def move_tangente(self):
        # va sur la tangente, on l'imagine comme un calcul +/-
        pass

    def move_projection(self):
        # se projette sur la ligne innée
        pass

    def emit_pheromone(self):
        # par ex. incrementer self.inventory["pheromone"] ?
        pass

    def set_oscillator_period(self):
        # pas implémenté pour l'instant
        pass

    def do_long_probe(self):
        pass

    def kill_forward_neighbor(self):
        pass

    # --- Surcharge possible de live_one_day pour utiliser get_sensor_values/apply_actions ---

    def live_one_day(self, environment, speed_factor=1.0):
        if not self.is_alive:
            return
        self.new_day()
        if not self.is_alive:
            return

        for hour in range(24):
            time.sleep(1.0 / speed_factor)
            if self.energy <= 0:
                print(f"{self.name} est morte d'épuisement (energy=0).")
                self.is_alive = False
                return

            # Au lieu d'utiliser un sensor "temp/dir_x/dir_y" direct,
            # on va récupérer l'ARRAY complet depuis get_sensor_values.
            inputs = self.get_sensor_values(environment)
            outputs = self.brain.forward(inputs)

            # On applique actions.
            self.apply_actions(outputs, environment)

            # On peut rajouter la logique "coût en énergie", "feu", "nourriture", etc.
            # → Soit on appelle super().live_one_day, soit on recopie la logique
            #    On recopie un peu pour l'exemple
            # Contrôle frontières.
            if self.x < 0: self.x = 0
            if self.x > environment.width: self.x = environment.width
            if self.y < 0: self.y = 0
            if self.y > environment.height: self.y = environment.height

            # Consommation d'énergie
            # (ici simplifiée : 1 point par heure, par ex.)
            self.energy -= 1.0

            if environment.in_fire(self.x, self.y):
                self.energy -= 5.0

            spot_index = environment.which_food_spot(self.x, self.y)
            if spot_index is not None:
                self.inventory["food"] += 1
                print(f"{self.name} ramasse de la nourriture (spot {spot_index}).")

            if environment.in_anthill(self.x, self.y) and self.inventory["food"] > 0:
                print(f"{self.name} rapporte {self.inventory['food']} food à la reine.")
                self.inventory["food"] = 0

            # Manger si < 50
            if self.energy < 50 and self.meals_today < 2 and self.inventory["food"] > 0:
                self.meals_today += 1
                self.inventory["food"] -= 1
                gained = self.energy * 0.5
                self.energy += gained
                if self.energy > 100:
                    self.energy = 100
                print(f"{self.name} mange (-> {self.energy:.1f} énergie).")


def pack_connection(source_type, source_id, sink_type, sink_id, weight, reserved=0):
    ###
    ### source_type : 1 bit (0=capteur, 1=neurone interne)
    ### source_id   : 14 bits
    ### sink_type   : 1 bit (0=neurone interne, 1=neurone de sortie)
    ### sink_id     : 14 bits
    ### weight      : int16 signés (plage -32768..32767)
    ### reserved    : 18 bits libres (par défaut 0)
    ### Retourne un entier 64 bits.
    ###
    # 1) On clamp source_type, sink_type
    st = (1 if source_type else 0) & 0x1
    si = source_id & 0x3FFF  # 14 bits
    tk = (1 if sink_type else 0) & 0x1
    ti = sink_id & 0x3FFF  # 14 bits

    # 2) Poids sur 16 bits signés
    #    En Python, pour s'assurer que weight tient dans [-32768..32767] :
    w = max(-32768, min(32767, weight))
    # On veut stocker ça en "2's complement" sur 16 bits.
    # Python peut aller au-delà, donc on force avec & 0xFFFF.
    w_16 = w & 0xFFFF

    # 3) Reserved sur 18 bits
    r = reserved & 0x3FFFF  # 18 bits

    # 4) On assemble (64 bits total)
    #    On choisit un layout (cf. schéma ci-dessus).
    packed = (
            (st & 0x1)
            | ((si & 0x3FFF) << 1)
            | ((tk & 0x1) << 15)
            | ((ti & 0x3FFF) << 16)
            | ((w_16 & 0xFFFF) << 30)
            | ((r & 0x3FFFF) << 46)
    )

    return packed


def unpack_connection(packed):
    # On lit les champs dans l'ordre inverse
    st = (packed & 0x1)
    si = (packed >> 1) & 0x3FFF
    tk = (packed >> 15) & 0x1
    ti = (packed >> 16) & 0x3FFF
    w_16 = (packed >> 30) & 0xFFFF
    r = (packed >> 46) & 0x3FFFF

    # Reconstruire weight signé
    # Si le bit 15 (0x8000) est set, c'est négatif
    if w_16 & 0x8000:
        w_int = -((~w_16 & 0xFFFF) + 1)
    else:
        w_int = w_16

    return st, si, tk, ti, w_int, r

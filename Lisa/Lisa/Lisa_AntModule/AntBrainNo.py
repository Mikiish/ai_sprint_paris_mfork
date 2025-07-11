#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import math


class Fourmi:
    def __init__(self, name="Anonyme"):
        # Données sensorielles (initialisées à 0 ou aléatoirement selon les besoins)
        self.name = name

        self.Slr = 0.0  # pheromone gradient left-right
        self.Sfd = 0.0  # pheromone gradient forward
        self.Sg = 0.0  # pheromone density

        self.Age = 0  # age
        self.Rnd = 0.0  # random input
        self.Blr = 0.0  # blockage left-right
        self.Bfd = 0.0  # blockage forward

        self.Osc = 0.0  # oscillator (peut servir d'horloge interne par ex.)

        self.Plr = 0.0  # population gradient left-right
        self.Pfd = 0.0  # population gradient forward
        self.Pop = 0.0  # population density

        self.LPf = 0.0  # population long-range forward
        self.LMy = 0.0  # last movement Y
        self.LMx = 0.0  # last movement X
        self.LBf = 0.0  # blockage long-range forward

        self.BDy = 0.0  # north/south border distance
        self.BDx = 0.0  # east/west border distance
        self.BD = 0.0  # nearest border distance

        self.Gen = 0.0  # genetic similarity of forward neighbor

        self.Lx = 0.0  # east/west world location
        self.Ly = 0.0  # north/south world location

    def percevoir_env(self):
        """
        Simule la mise à jour des données sensorielles.
        Dans un « vrai » projet, on irait chercher ces valeurs
        depuis un moteur de simulation ou d’autres modules.
        Ici, on joue avec des valeurs aléatoires ou arbitraires.
        """
        self.Slr = random.uniform(-1, 1)
        self.Sfd = random.uniform(-1, 1)
        self.Sg = random.uniform(0, 5)

        self.Age += 1
        self.Rnd = random.random()

        self.Blr = random.choice([0, 1])  # 0 = libre, 1 = bloqué à gauche/droite
        self.Bfd = random.choice([0, 1])

        # Oscillateur simple (par ex. sinusoïde dépendant de l'âge)
        self.Osc = math.sin(self.Age * 0.1)

        self.Plr = random.uniform(-2, 2)
        self.Pfd = random.uniform(-2, 2)
        self.Pop = random.randint(0, 100)

        self.LPf = random.randint(0, 50)
        self.LMy = random.choice([-1, 0, 1])
        self.LMx = random.choice([-1, 0, 1])
        self.LBf = random.choice([0, 1])

        self.BDy = random.uniform(0, 10)
        self.BDx = random.uniform(0, 10)
        self.BD = min(self.BDy, self.BDx)

        self.Gen = random.uniform(0, 1)

        # Position de la fourmi dans le monde
        self.Lx += self.LMx  # on se déplace un peu sur l'axe Est-Ouest
        self.Ly += self.LMy  # on se déplace un peu sur l'axe Nord-Sud

    def description_senseurs(self):
        """ Retourne une description texte des senseurs, façon mini-rapport. """
        desc = (
            f"----\n"
            f"Fourmi: {self.name}\n"
            f"Age: {self.Age}\n"
            f"Slr (grad pheromone gauche-droite): {self.Slr:.2f}\n"
            f"Sfd (grad pheromone avant): {self.Sfd:.2f}\n"
            f"Sg  (densité pheromone): {self.Sg:.2f}\n"
            f"Rnd (entrée aléatoire): {self.Rnd:.2f}\n"
            f"Blr (blocage gauche/droite): {self.Blr}\n"
            f"Bfd (blocage avant): {self.Bfd}\n"
            f"Osc (oscillateur interne): {self.Osc:.2f}\n"
            f"Plr (grad population g/d): {self.Plr:.2f}\n"
            f"Pfd (grad population avant): {self.Pfd:.2f}\n"
            f"Pop (densité population): {self.Pop}\n"
            f"LPf (pop. long-range devant): {self.LPf}\n"
            f"LMy (dernier déplacement Y): {self.LMy}\n"
            f"LMx (dernier déplacement X): {self.LMx}\n"
            f"LBf (blocage avant - longue portée): {self.LBf}\n"
            f"BDy (dist. bord nord/sud): {self.BDy:.2f}\n"
            f"BDx (dist. bord est/ouest): {self.BDx:.2f}\n"
            f"BD  (dist. plus proche bord): {self.BD:.2f}\n"
            f"Gen (similarité génétique voisin avant): {self.Gen:.2f}\n"
            f"Lx  (position E/O): {self.Lx:.2f}\n"
            f"Ly  (position N/S): {self.Ly:.2f}\n"
            f"----\n"
        )
        return desc


def lisa_parle(fourmi):
    """
    Lisa 'interprète' les senseurs de la fourmi et lui fait
    quelques remarques. On peut imaginer un moteur plus complexe,
    pour l'exemple, on reste léger.
    """
    msg = []
    msg.append(f"Lisa à {fourmi.name} :")

    # Exemples de règles simplifiées :
    if fourmi.Sg > 3:
        msg.append(" – Tu sens une forte odeur de phéromones, méfie-toi de la concurrence !")
    else:
        msg.append(" – Ça va, la piste de phéromones est encore légère.")

    if fourmi.BD < 2:
        msg.append(" – Attention, tu es proche d’un bord du monde… Prudence petit explorateur !")

    if fourmi.Gen > 0.8:
        msg.append(" – Tu sembles rencontrer une fourmi quasi-sœur devant toi, ça sent la famille !")
    elif fourmi.Gen < 0.2:
        msg.append(" – Devant toi, ce n’est pas la famille… reste sur tes gardes !")

    # Commentaire sur le déplacement récent
    direction = ""
    if fourmi.LMx > 0:
        direction += "Est"
    elif fourmi.LMx < 0:
        direction += "Ouest"
    if fourmi.LMy > 0:
        direction += (" et Nord" if direction else "Nord")
    elif fourmi.LMy < 0:
        direction += (" et Sud" if direction else "Sud")

    if direction:
        msg.append(f" – Tu t'es récemment déplacée vers le {direction}. Bon choix ?")
    else:
        msg.append(" – Tu es restée sur place dernièrement ? La patience a parfois du bon.")

    return "\n".join(msg)


# --- Exemple d'utilisation ---

if __name__ == "__main__":
    # Créons un petit groupe de fourmis
    fourmis = [Fourmi(name=f"Fourmi_{i}") for i in range(1, 4)]

    # À chaque "tour", on met à jour leurs senseurs, puis Lisa leur parle
    for tour in range(3):
        print(f"=== TOUR {tour + 1} ===")
        for f in fourmis:
            f.percevoir_env()
            print(f.description_senseurs())
            print(lisa_parle(f))
            print()

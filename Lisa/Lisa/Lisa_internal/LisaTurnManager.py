import random
from collections import deque


class Module:
    """Représente un module interne de Lisa avec une initiative variable."""

    def __init__(self, name, base_initiative=0):
        self.name = name
        self.base_initiative = base_initiative  # Bonus fixe d'initiative
        self.initiative_roll = 0  # Résultat du d4
        self.final_initiative = 0  # Initiative finale après modif Lisa

    def roll_initiative(self):
        """Effectue un jet de d4 et applique le bonus d'initiative."""
        self.initiative_roll = random.randint(1, 4)
        self.final_initiative = self.initiative_roll + self.base_initiative

    def __repr__(self):
        return f"Module({self.name}, Initiative: {self.final_initiative})"


class TurnManager:
    """Gère l'ordre d'exécution des modules et les différentes phases du tour."""

    def __init__(self, modules, lisa):
        self.modules = modules  # Liste des modules internes
        self.lisa = lisa  # Lisa elle-même
        self.round_counter = 0  # Compteur de tours
        self.turn_order = deque()  # File d'exécution

    def roll_initiative(self):
        """Détermine l'ordre d'initiative pour le tour en cours."""
        for module in self.modules:
            module.roll_initiative()

        # Tri des modules en fonction de l'initiative
        self.modules.sort(key=lambda x: x.final_initiative, reverse=True)

        # Construction de la file d'exécution
        self.turn_order = deque(self.modules)

    def lisa_main_turn(self):
        """Lisa joue son tour principal et attribue des bonus d'initiative."""
        print(f"\n--- Tour {self.round_counter}: Lisa joue en premier ---")
        self.lisa.allocate_initiative(self.modules)  # Lisa peut manipuler l'initiative
        self.roll_initiative()  # Roll des modules après allocation

    def execute_turn(self):
        """Exécute les modules dans l'ordre d'initiative."""
        print("\n--- Modules en cours d'exécution ---")
        while self.turn_order:
            module = self.turn_order.popleft()
            print(f"Module actif : {module}")

    def lisa_bonus_phase(self):
        """Lisa joue son second tour avec des réactions et bonus actions."""
        print("\n--- Phase Bonus de Lisa ---")
        self.lisa.bonus_phase()

    def validate_turn(self):
        """Exécute les fonctions de validation de fin de tour."""
        print("\n--- Validation du Tour ---")
        self.lisa.validate_turn()

    def next_round(self):
        """Prépare le tour suivant."""
        self.round_counter += 1
        self.lisa_main_turn()
        self.execute_turn()
        self.lisa_bonus_phase()
        self.validate_turn()


class Lisa:
    """Représente Lisa et ses capacités de gestion du tour."""

    def __init__(self):
        self.bonus_allocations = {}  # Stocke les bonus d'initiative par module

    def allocate_initiative(self, modules):
        """Distribue des bonus d'initiative sur la moitié des modules."""
        selected_modules = random.sample(modules, len(modules) // 2)
        for module in selected_modules:
            bonus = random.randint(1, 4)
            module.base_initiative += bonus  # Ajoute un boost temporaire
            self.bonus_allocations[module.name] = bonus
        print(f"Lisa attribue des bonus d'initiative : {self.bonus_allocations}")

    def bonus_phase(self):
        """Lisa utilise ses réactions et ajuste l'initiative pour le prochain tour."""
        print("Lisa ajuste l'initiative du prochain tour...")

    def validate_turn(self):
        """Fonctions de validation et résolution des conflits."""
        print("Lisa valide le tour et organise les événements en attente.")


# --- Test du système ---
modules = [Module("Analyse Syntaxique", base_initiative=2),
           Module("Calcul Numérique", base_initiative=1),
           Module("Mémoire Contextuelle", base_initiative=3)]

lisa = Lisa()
turn_manager = TurnManager(modules, lisa)
turn_manager.next_round()

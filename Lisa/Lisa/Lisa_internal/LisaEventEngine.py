from collections import deque
import heapq
import random
import math
import re

class Fact:
    """Représente un fait stocké dans la base de connaissances de Lisa."""
    def __init__(self, category, name, attributes):
        self.category = category  # Ex: "character", "location", "event"
        self.name = name  # Nom unique du fait
        self.attributes = attributes  # Dictionnaire d'attributs clés-valeurs

    def __repr__(self):
        return f"Fact({self.category}, {self.name}, {self.attributes})"


class Event:
    """Représente un événement dans le moteur événementiel de Lisa."""
    def __init__(self, event_type, source, condition, payload, priority=3):
        self.type = event_type  # Type d'événement (EVT_Sensoriel, EVT_Primaire...)
        self.source = source  # Origine de l'événement
        self.condition = condition  # Condition pour l'activation
        self.payload = payload  # Données attachées à l'événement
        self.priority = priority  # Priorité (1 = très urgent, 5 = faible)

    def __lt__(self, other):
        """Permet de comparer les événements pour la priority queue."""
        return self.priority < other.priority

    def __repr__(self):
        return f"Event({self.type}, {self.source}, {self.condition}, {self.payload}, priority={self.priority})"


class Trigger:
    """Représente un déclencheur qui agit comme une passerelle entre une source et un événement."""
    def __init__(self, name, source, event_type, conditions):
        self.name = name  # Nom du trigger
        self.source = source  # Objet ou entité déclenchant le trigger
        self.event_type = event_type  # Type d'événement qu'il déclenche
        self.conditions = conditions  # Conditions de déclenchement

    def check_conditions(self, context):
        """Vérifie si les conditions du trigger sont remplies en fonction du contexte."""
        return all(condition(context) for condition in self.conditions)

    def __repr__(self):
        return f"Trigger({self.name}, Source={self.source}, Event={self.event_type}, Conditions={self.conditions})"


class EmojiTrigger(Trigger):
    """Déclencheur basé sur un emoji, servant de pont entre un état et un événement."""
    def __init__(self, emoji, source, event_type, conditions):
        super().__init__(name=f"Trigger_{emoji}", source=source, event_type=event_type, conditions=conditions)
        self.emoji = emoji

    def __repr__(self):
        return f"EmojiTrigger({self.emoji}, Source={self.source}, Event={self.event_type}, Conditions={self.conditions})"


class EventQueue:
    """Gestionnaire de la file d'événements avec une queue FIFO et une queue de priorité."""
    def __init__(self):
        self.queue = deque()  # File FIFO pour les événements normaux
        self.priority_queue = []  # Heap (priority queue) pour les événements critiques

    def add_event(self, event):
        if event.priority == 1:
            heapq.heappush(self.priority_queue, event)  # Ajoute dans la queue prioritaire
        else:
            self.queue.append(event)  # Ajoute dans la queue normale

    def get_next_event(self):
        """Récupère l'événement le plus prioritaire disponible."""
        if self.priority_queue:
            return heapq.heappop(self.priority_queue)  # Récupère depuis la queue prioritaire
        elif self.queue:
            return self.queue.popleft()  # Récupère depuis la queue normale
        return None  # Aucun événement disponible

    def __repr__(self):
        return f"EventQueue(Priority={self.priority_queue}, Normal={list(self.queue)})"


class Context:
    """Gestion du contexte de Lisa (Mémoire immédiate, Court terme, Long terme)."""
    def __init__(self):
        self.immediate_memory = []  # Liste des événements actifs
        self.contextual_memory = {}  # Faits récents
        self.persistent_memory = {}  # Base de connaissances permanente

    def add_fact(self, fact):
        """Ajoute un fait en mémoire contextuelle."""
        self.contextual_memory[fact.name] = fact

    def store_persistent(self, key, value):
        """Ajoute un fait en mémoire permanente."""
        self.persistent_memory[key] = value

    def __repr__(self):
        return f"Context(Immediate={self.immediate_memory}, Contextual={self.contextual_memory}, Persistent={self.persistent_memory})"


class PipelineProcessor:
    """Pipeline de traitement des événements de Lisa avec filtres successifs."""
    transformations = {
        "🔍 Requête détectée": "🔍 Recherche approfondie en cours...",
        "📊 Analyse numérique détectée": "📊 Données mathématiques en traitement...",
        "🌀 Pattern non reconnu": "🌀 Tentative d'interprétation avancée..."
    }

    @staticmethod
    def process(input_data):
        if input_data in PipelineProcessor.transformations:
            return PipelineProcessor.transformations[input_data]
        return input_data


class TriggerManager:
    """Gère dynamiquement les triggers et leur activation."""
    def __init__(self):
        self.triggers = []

    def add_trigger(self, trigger):
        self.triggers.append(trigger)

    def check_and_trigger_events(self, context, event_queue):
        """Vérifie si les triggers doivent activer des événements."""
        for trigger in self.triggers:
            if trigger.check_conditions(context):
                new_event = Event(trigger.event_type, trigger.source, True, {}, priority=2)
                event_queue.add_event(new_event)
                print(f"✅ Trigger activé : {trigger} → {new_event}")

    def __repr__(self):
        return f"TriggerManager({self.triggers})"

import math
import numpy as np
import random
import re

# Fonctions d'activation pour les événements
def step_function(x, threshold=0.5):
    """Activation binaire : si x dépasse le seuil, retourne 1, sinon 0."""
    return 1 if x >= threshold else 0


def sigmoid(x):
    """Activation sigmoïde : utilisée pour les événements progressifs."""
    return 1 / (1 + math.exp(-x))


def relu(x):
    """Activation ReLU : utilisé pour les événements qui nécessitent un seuil minimum."""
    return max(0, x)


def leaky_relu(x, alpha=0.01):
    """Leaky ReLU : évite la saturation nulle en permettant une faible pente négative."""
    return x if x > 0 else alpha * x

# Hiérarchie des événements dans Lisa

def EVT_Sensoriel_AudioInput(unicode_char="🔊"):
    text = "🔊 Signal audio capté."
    activation = step_function(random.random())
    return text, unicode_char, activation


def EVT_Sensoriel_TextInput(unicode_char="⌨"):
    text = "⌨ Entrée texte détectée."
    activation = step_function(random.random())
    return text, unicode_char, activation


def EVT_Primaire_TextAnalyzed(unicode_char="📖"):
    text = "📖 Texte analysé."
    activation = sigmoid(random.random())
    return text, unicode_char, activation


def EVT_Primaire_PatternDetected(unicode_char="🧩"):
    text = "🧩 Pattern reconnu dans les données."
    activation = sigmoid(random.random())
    return text, unicode_char, activation


def EVT_Contextuel_ResearchStarted(unicode_char="🔍"):
    text = "🔍 Recherche en cours..."
    activation = relu(random.random())
    return text, unicode_char, activation


def EVT_Contextuel_CalculationStarted(unicode_char="📊"):
    text = "📊 Calcul en cours..."
    activation = sigmoid(random.random())
    return text, unicode_char, activation


def EVT_Critique_AnomalyDetected(unicode_char="⚠"):
    text = "⚠ Alerte : anomalie détectée."
    activation = step_function(random.random())
    return text, unicode_char, activation


def EVT_Critique_VerifiedConclusion(unicode_char="✅"):
    text = "✅ Conclusion validée."
    activation = step_function(random.random())
    return text, unicode_char, activation


def EVT_Systémique_MemoryUpdate(unicode_char="🔄"):
    text = "🔄 Mise à jour de la mémoire en cours..."
    activation = relu(random.random())
    return text, unicode_char, activation


def EVT_Systémique_OptimizationTriggered(unicode_char="♻"):
    text = "♻ Optimisation du système en cours..."
    activation = leaky_relu(random.random())
    return text, unicode_char, activation

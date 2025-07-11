import re
import unicodedata
import math
import Lisa_Tokenizer
from sympy import nextprime


# Classe de gestion du contexte dynamique
class ContextManager:
    def __init__(self):
        self.global_context = 0  # Valeur actuelle du contexte
        self.token_count = 0  # Nombre total de tokens traités
        self.event_triggers = []  # Liste des événements impactant le contexte

    def update_context(self, new_tokens, events=None):
        """Met à jour le contexte global en fonction des tokens lus et des événements."""
        self.token_count += new_tokens
        self.global_context = math.log(self.token_count + 1)  # Croissance logarithmique

        if events:
            for event in events:
                self.handle_event(event)

    def handle_event(self, event):
        """Applique les effets d’un événement sur le contexte."""
        if event == "SOFT_RESET":
            self.global_context /= 2  # Réduit le contexte de moitié
        elif event == "HARD_RESET":
            self.global_context = 0  # Réinitialise complètement le contexte
        elif event == "TRIGGER_ANOMALY":
            self.global_context *= 0.8  # Perturbation de 20%
        elif event == "FOCUS_MODE":
            self.global_context += 1  # Boost temporaire du contexte

    def get_context_value(self):
        """Retourne la valeur actuelle du contexte."""
        return self.global_context


# Fonction pour nettoyer et formater une énorme chaîne de texte
def clean_and_format_text(text):
    text = ''.join(c for c in text if c.isprintable())  # Suppression des caractères non imprimables
    text = re.sub(r'\s+', ' ', text)  # Remplacement des espaces multiples par un unique
    text = unicodedata.normalize('NFKC', text)  # Normalisation Unicode (NFKC pour uniformiser)
    return text.strip()


# Fonction pour générer un résumé à différentes échelles de compression
def generate_summary(text, tokens_count):
    words = text.split()
    if len(words) <= tokens_count:
        return text  # Si on a déjà un petit texte, on ne résume pas
    step = len(words) // tokens_count
    return ' '.join(words[i] for i in range(0, len(words), step))[:tokens_count]


# Simule un très grand corpus textuel
big_data_text = """
Dans un lointain futur, l'humanité explore les confins de l'univers à la recherche de connaissances infinies.
Chaque étoile est une bibliothèque de secrets, chaque trou noir une porte vers l'inconnu.
La science, la philosophie et la spiritualité convergent en une unique vérité fondamentale.
"""

# Initialisation du gestionnaire de contexte
context_manager = ContextManager()

# Nettoyage et normalisation
total_text = clean_and_format_text(big_data_text)

# Calcul des tailles des résumés
text_length = len(total_text)
summary_23 = generate_summary(total_text, 23)
summary_log3 = generate_summary(total_text, int(math.log(math.log(math.log(text_length + 1), 2), 2)))
summary_log2 = generate_summary(total_text, int(math.log(math.log(text_length + 1), 2)))
summary_ln = generate_summary(total_text, int(math.log(text_length + 1)))

# Construction de la chaîne enrichie
enhanced_text = f"""
SUMMARY_23: {summary_23}
SUMMARY_LOG3: {summary_log3}
SUMMARY_LOG2: {summary_log2}
SUMMARY_LN: {summary_ln}

{total_text}
"""

# Calcul du premier nombre premier suivant la taille de la chaîne
prime_index = nextprime(len(enhanced_text))

# Mise à jour du contexte avec le nombre de tokens traités
context_manager.update_context(len(enhanced_text.split()))

# Affichage des résultats
print(f"Nombre premier associé : {prime_index}")
print(f"Valeur du contexte après traitement : {context_manager.get_context_value()}")
print(f"Chaîne formatée et enrichie:\n{enhanced_text[:500]}...")

# Lisa_Tokenizer.bijective_tokenize(enhanced_text)  # Lancement de la tokenisation (commenté pour test)
# Le contexte sera mis à jour directement dans Lisa_Tokenizer.bijective_tokenize, intégrant la gestion des événements

import re
import unicodedata
import math
import Lisa_Tokenizer
from sympy import nextprime


# Fonction pour nettoyer et formater une énorme chaîne de texte
def clean_and_format_text(text):
    # Suppression des caractères non imprimables
    text = ''.join(c for c in text if c.isprintable())

    # Remplacement des espaces multiples par un unique
    text = re.sub(r'\s+', ' ', text)

    # Normalisation Unicode (NFKC pour uniformiser)
    text = unicodedata.normalize('NFKC', text)

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

# Affichage des résultats
print(f"Nombre premier associé : {prime_index}")
print(f"Chaîne formatée et enrichie:\n{enhanced_text[:500]}...")

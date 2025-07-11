import re
import random
import unicodedata
from sympy import prime


# Fonction pour générer une liste de nombres premiers
def generate_prime_list(n):
    return [prime(i) for i in range(1, n + 1)]


# Fonction pour déterminer la taille du token
def determine_token_size(i):
    prime_value = prime(i)
    size = prime_value % 7
    if size == 0 or size == 6:
        return random.choice([3, 4])  # Choix aléatoire entre 3 et 4
    return size


# Fonction pour récupérer la valeur Unicode d'un caractère
def get_unicode_value(char):
    return ord(char)


# Définition des voyelles et consonnes
VOWELS = set("AEIOUYaeiouy")
CONSONANTS = set("BCDFGHJKLMNPQRSTVWXZbcdfghjklmnpqrstvwxz")

# Liste temporaire de mots anglais courants qui suivent la segmentation normale
ENGLISH_WORDS = {"Proof", "Time", "Technology", "Science"}

# Liste de noms propres courants (prénoms, villes, entités)
PROPER_NAMES = {"Lisa", "Paris", "Tesla", "Google", "Elon"}

# Définition des types de séparateurs spéciaux
BRACKETS_MAP = {
    "(": "FØ_OPEN", ")": "FØ_CLOSE",
    "{": "Ø_OPEN", "}": "Ø_CLOSE",
    "[": "Ø_OPEN", "]": "Ø_CLOSE",
    "\"": "Ø_OPEN"
}

# Liste des opérateurs mathématiques fondamentaux
OPERATORS = {"+", "-", "=", "*", "/", "%", "^", "_"}  # Ajout de l'underscore comme opérateur d'indice

# Liste des plage d'emoji unicode
EMOJI_PATTERN = (
    "[\U0001F600-\U0001F64F"  # Emoticônes (smiley, émotions)
    "\U0001F300-\U0001F5FF"  # Symboles divers (météo, flèches, objets)
    "\U0001F680-\U0001F6FF"  # Moyens de transport et cartes
    "\U0001F700-\U0001F77F"  # Symboles alchimiques
    "\U0001F780-\U0001F7FF"  # Supplément flèches, symboles géométriques
    "\U0001F800-\U0001F8FF"  # Divers symboles techniques
    "\U0001F900-\U0001F9FF"  # Extensions (gestes, animaux, objets)
    "\U0001FA00-\U0001FA6F"  # Symboles supplémentaires (mains, personnes)
    "\U0001FA70-\U0001FAFF"  # Objets divers (outils, armes, instruments)
    "\U00002700-\U000027BF"  # Dingbats (⚔️ inclus ici)
    "\U00002B50-\U00002B59"  # Étoiles et symboles géométriques
    "\U00002600-\U000026FF"  # Divers symboles (soleil, nuages, parapluies, ⚔️ inclus ici)
    "]"
)

# Fonction principale de scanning et tokenisation
def bijective_tokenize(text):

    words = re.findall(r'\n+|\s+|\w+|[:.!?(){}\[\]"\'\d+]|[+\-*/%^=_]|' + EMOJI_PATTERN, text, re.UNICODE)
    tokens = []
    index = 1  # Pour suivre le i-ème nombre premier

    for i, word in enumerate(words):
        if "\n" in word:  # Si c'est un saut de ligne, marquer un segment plus fort
            token = {
                "word": "HARD_NEW_SEG",  # Marquer comme un segment structurant
                "prime_id": prime(index),
                "size": len(word)
            }
            tokens.append(token)
            index += 1
            continue

        if word.isspace():  # Si c'est un espace, le traiter comme un token séparé
            token = {
                "word": "SPACE",
                "prime_id": prime(index),
                "size": len(word)
            }
            tokens.append(token)
            index += 1
            continue

        if word in BRACKETS_MAP:  # Gérer les parenthèses et autres délimiteurs
            token = {
                "word": BRACKETS_MAP[word],
                "prime_id": prime(index),
                "size": 1
            }
            tokens.append(token)
            index += 1
            continue

        if word in OPERATORS:  # Détecter les opérateurs mathématiques
            token = {
                "word": "OPERATOR_" + word,
                "prime_id": prime(index),
                "size": 1
            }
            tokens.append(token)
            index += 1
            continue

        # Gestion spécifique du caractère '
        if "'" in word:
            if i > 0 and words[i - 1][-1].isalpha() and word[0].isalpha():
                tokens.append({"word": "GRAMMATICAL_CONTRACTION", "prime_id": prime(index), "size": 0})
                index += 1
            else:
                tokens.append({"word": "IMPLICIT_BREAK", "prime_id": prime(index), "size": 0})
                index += 1
            continue

        # Vérifier les transitions structurelles (Cas 2 - Séparations implicites)
        if i > 0:
            prev_word = words[i - 1]
            if (prev_word[-1].isalpha() and word[0].isdigit()) or (prev_word[-1].isdigit() and word[0].isalpha()):
                tokens.append({"word": "IMPLICIT_BREAK", "prime_id": prime(index), "size": 0})
                index += 1
            elif prev_word[-1].islower() and word[0].isupper():
                tokens.append({"word": "IMPLICIT_BREAK", "prime_id": prime(index), "size": 0})
                index += 1

        if word in ENGLISH_WORDS:  # Si c'est un mot anglais connu, appliquer la segmentation normale
            j = 0
            while j < len(word):
                size = determine_token_size(index)  # Déterminer la taille du token
                token_text = word[j:j + size]  # Extraire la portion du texte

                token = {
                    "word": token_text,
                    "prime_id": prime(index),
                    "size": size
                }
                tokens.append(token)

                j += size  # Avancer dans le mot
                index += 1  # Passer au nombre premier suivant
        elif word in PROPER_NAMES:  # Ne pas découper un nom propre établi
            token = {
                "word": word,
                "prime_id": prime(index),
                "size": len(word)
            }
            tokens.append(token)
            index += 1  # Passer au nombre premier suivant
        else:
            # Cas standard de segmentation
            j = 0
            while j < len(word):
                size = determine_token_size(index)
                token_text = word[j:j + size]

                token = {
                    "word": token_text,
                    "prime_id": prime(index),
                    "size": size
                }
                tokens.append(token)

                j += size
                index += 1

    return tokens


# Test avec une phrase exemple
text = "Quel est le rôle de la gravité dans la formation des galaxies?"
tokens = bijective_tokenize(text)


# Résultat
def print_tokens(tokens):
    print(" - ".join([f'[{token["word"]}]({token["size"]})' for token in tokens]))


print_tokens(tokens)

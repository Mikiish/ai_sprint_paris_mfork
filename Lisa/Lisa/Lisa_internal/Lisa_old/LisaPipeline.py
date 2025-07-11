import random
import math
import re

# import EventHandler

# Liste des fonctions événementielles de Lisa
# def HasProcessedToken(unicode_char="⚡"):
# def HasValidatedModule(unicode_char="🔍"):
# def HasBlockedLeak(unicode_char="🔒"):
# def HasMappedTokenToCurve(unicode_char="🌀"):
# def HasAppliedQuadForm(unicode_char="📊"):
# def HasReachedThreshold(unicode_char="📈"):
# def HasFoundInformation(unicode_char="🤖"):
# def IsComputing(unicode_char="🏗️"):
# def IsTrying(unicode_char="🚀"):
# def IsFailing(unicode_char="❓"):
# from Lisa_Tokenizer import bijective_tokenize

def lisa_internal(input_data):
    """Simule un module interne spécialisé dans l'analyse brute."""
    if "🌀" in input_data:
        return random.choice(
            ["🔍 Requête détectée: Recherche en cours...", "🌀 Pattern non reconnu, analyse symbolique requise."])
    elif "?" in input_data:
        return "🔍 Requête détectée: Recherche en cours..."
    elif re.match(r'\[.*\]\(\d+\)', input_data):  # Détecte le format [valeur](X)
        value = re.search(r'\[(.*?)\]', input_data).group(1)
        bias_factor = int(re.search(r'\((\d+)\)', input_data).group(1))  # Extrait X
        probability = math.sin(2 * (bias_factor * math.pi) / 3)  # Biais sinusoïdal entre 0 et 1

        # On encode la valeur pour être traitée dans lisa()
        return f"<<BIASED:{bias_factor}:{value}>>"

    elif input_data.isnumeric():
        return f"📊 Analyse numérique détectée: {int(input_data) * 42}"  # Exemple bidon
    else:
        return "🌀 Pattern non reconnu, analyse symbolique requise."


def lisa_only(intermediate_result):
    """Reformate et optimise les résultats avant qu'ils ne soient envoyés à Lisa."""
    # Vérifier si la réponse est déjà encodée en "<<BIASED:X:text>>", si oui ne pas toucher
    if "<<BIASED:" in intermediate_result:
        return intermediate_result

    transformations = {
        "🔍 Requête détectée": "🔍 Recherche approfondie en cours...",
        "📊 Analyse numérique détectée": "📊 Données mathématiques en traitement...",
        "🌀 Pattern non reconnu": "🌀 Tentative d'interprétation avancée..."
    }
    for key in transformations:
        if key in intermediate_result:
            return transformations[key]
    return "⚠ Résultat non catégorisé."


def lisa(final_stage):
    """Prend la décision finale sur ce qui doit être affiché."""
    if "🔍" in final_stage:
        return "🤖 Lisa a trouvé une information pertinente et continue la recherche."
    elif "📊" in final_stage:
        return "🏗️ Lisa a effectué un calcul basé sur la structure des données."
    elif "🌀" in final_stage or "🚀" in final_stage:
        return "🚀 Lisa tente une approche logique sur des données inconnues."
    elif "🤖" in final_stage:
        return "🤖 Lisa a trouvé une information pertinente."

    # Vérifier si un token biaisé est présent dans la structure correcte
    if "<<BIASED:" in final_stage:
        match = re.search(r"<<BIASED:(\d+):(.*?)>>", final_stage)
        if match:
            bias_factor = int(match.group(1))
            value = match.group(2).strip()
            probability = (math.sin(bias_factor * math.pi) + 1) / 2  # Biais sinusoïdal basé sur X * π

            return random.choices(
                [f"{value} 🚀", "❓ Lisa n'a pas pu catégoriser la demande."],
                weights=[probability, 1 - probability]
            )[0]

    return "🚀 Lisa tente une approche logique avec des fragments incomplets."


def extract_first_character(text):
    """Retourne le premier caractère d'une chaîne de caractères."""
    return text[0] if text else ""


def user_visible(final_output):
    """Affiche uniquement ce que l'utilisateur doit voir."""
    return f"🎯 Réponse de Lisa: {final_output}"

emoji_mapping = {
    "🤖": "HasFoundInformation",
    "🏗️": "IsComputing",
    "🚀": "IsTrying",
    "❓": "IsFailing"
}

emoji_mapping.update({
    "🌀": "HasMappedTokenToCurve",
    "📊": "HasAppliedQuadForm",
    "⚡": "HasProcessedToken",
    "🔍": "HasValidatedModule",
    "🔒": "HasBlockedLeak",
    "📈": "HasReachedThreshold"
})


# Simulation d'une requête utilisateur
user_input = random.choice(
    ["[42](2)", "[Pourquoi le ciel est bleu?](26)", "[&*%$](4)", "[Qu](2)", "[el](3)", "[🌀](1)", "[est](4)", "[🌀](1)", "[le](3)",
     "[🌀](1)", "[rôle](5)", "[🌀](1)", "[d](1)", "[e](3)", "[🌀](1)", "[la](3)", "[🌀](1)", "[gravi](5)", "[té](4)",
     "[🌀](1)", "[dans](5)", "[🌀](1)", "[l](1)", "[a](3)", "[🌀](1)", "[form](4)", "[ation](5)", "[🌀](1)", "[des](3)",
     "[🌀](1)", "[ga](2)", "[laxi](4)", "[e](1)", "[s](1)", "[?](5)"])
# Simulation enrichie

# Passage dans le pipeline
temp1 = lisa_internal(user_input)
temp2 = lisa_only(temp1)
temp3 = lisa(temp2)
final_response = user_visible(temp3)

# Extraction du premier caractère
first_character = extract_first_character(temp3)

# Affichage du résultat
print("Utilisateur: ", user_input)
print(final_response)
print("Premier caractère extrait: ", first_character)

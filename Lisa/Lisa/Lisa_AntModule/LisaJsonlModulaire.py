import os
import json
import random
import re
import unicodedata
import time

def obtenir_numero_fichier(filename):
    match = re.search(r'_(\d+)\.txt$', filename)
    if match:
        return int(match.group(1))
    else:
        return None  # Aucun numéro trouvé

# Générateur aléatoire de messages du Génie
phrases_du_genie = [
    "✨ Le mieux est l'ennemi du bien. Génie aléatoire 🎲✨",
    "🚀 La simplicité est la sophistication suprême. Génie inspiré 🌀",
    "🧠 Penser, c'est créer le futur. Génie innovant 💡",
    "🔥 La puissance vient de l'unité. Génie synergique 🌟"
]

# Header pas (trop) aléatoire :
random_genius_message = lambda: random.choice(phrases_du_genie)

# Random vraiment random jvous jure.
def random_unicode_char():
    # Choisir aléatoirement un caractère unicode valide (ici dans une plage simple)
    random_int = int.from_bytes(os.urandom(2), 'big') % (0x2FFF - 0x2600) + 0x2600
    char = chr(random_int)
    return char if unicodedata.category(char := chr(random_int))[0] != "C" else "✨"  # Fallback simple

# Modification de ta fonction actuelle (exemple simplifié)
def obtenir_message_genie_avec_unicode():
    return random_genius_message() + random_unicode_char() + ligne_aleatoire_genie_code()

def random_aleatoire(rangealea=61681):
    # Utiliser os.urandom pour choisir une ligne aléatoire
    random_bytes = os.urandom(4)
    random_int = int.from_bytes(random_bytes, 'big')
    choix = random_int % rangealea
    return choix

# Fonction aléatoire robuste pour obtenir une ligne depuis LeGenieCode.txt
def ligne_aleatoire_genie_code(filepath="LeGenieCode/LeGenieCode.txt"):
    with open(filepath, 'r', encoding='utf-8') as file:
        lignes = [ligne.strip() for ligne in file if ligne.strip()]

    # Vérification du fichier non vide
    if not lignes:
        return random_genius_message()

    choix = random_aleatoire(rangealea=len(lignes))
    return lignes[choix].strip()

# Special case for number output that are treated differently. They're not "text" content_type, but "execution_output"
def message_execution_output(supposednumber):
    return f"🤖 Génie se concentre... Oui ! C'est un nombre et c'est une femelle : {supposednumber} 🎲✨"


# Fonction d'extraction sécurisée
def extraire_contenu(line):
    line = line.strip()
    if not line:
        return "🧞" + random_genius_message()
    try:
        data = json.loads(line)
        if isinstance(data, dict):
            if data.get('content_type') == "execution_output":
                nombre_fautif = data.get('text', [""])
                return message_execution_output(nombre_fautif)
            content = data.get('parts', [""])[0]
            return content if content else "🧞" + random_genius_message() + ligne_aleatoire_genie_code(filepath="LeGenieCode/LeGenieCode_Void.txt")
    except json.JSONDecodeError:
        return "🧞" + random_genius_message()


# Traitement des fichiers selon leur congruence modulo 3
def traiter_fichier(filename):
    filename_num = obtenir_numero_fichier(filename)
    if filename_num is None:
        return None  # Ignore les fichiers qui ne finissent pas par un nombre

    congruence = filename_num % 3

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    contenus = [extraire_contenu(line.strip()) for line in lines]

    if congruence == 0:  # 4 messages
        pattern_bait = [
            'user', 'assistant', 'user', 'assistant'
        ]

        patterns_short = [
            ['user', 'assistant', 'user', 'assistant'],
            ['user', 'user', 'assistant', 'assistant']
        ]
        patterns_long = [
            ['assistant', 'user', 'user', 'assistant'],
            ['user', 'assistant', 'assistant', 'user']
        ]

        total_length = sum(len(line.strip()) for line in lines)
        bias = 0.8 if total_length > 893 else 0.5
        chosen_pattern = random.choice(patterns_long if random.random() < bias else patterns_short)

        messages = []
        for role, content in zip(chosen_pattern, contenus[:4]):
            messages.append({"role": role, "content": content})

        magikiter = 0
        for message in messages:
            message["role"] = pattern_bait[magikiter]
            magikiter += 1


    elif congruence == 2:  # 2 messages avec rôles aléatoires sur contenu
        roles = ['user', 'assistant']
        messages = [{"role": role, "content": ""} for role in roles]
        random.shuffle(contenus)
        for i in range(2):
            messages[i]["content"] = contenus[i]
        print(messages)

    elif congruence == 1:  # Un seul message, souvent vide
        content = contenus[0] if contenus else random_genius_message()
        system_msg = f"✨ Le mieux est l'ennemi du bien. Génie aléatoire 🎲✨ {content}"
        user_msg, assistant_msg = (content, obtenir_message_genie_avec_unicode()) if random.choice([True, False]) else (
            random_genius_message(), content)
        messages = [
            {"role": "developer", "content": system_msg},
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": assistant_msg}
        ]
    if congruence != 1:
        slashrand = random_aleatoire(rangealea=4)
        if slashrand == 0:
            final_json = {"messages": [{"role": "developer",
                                        "content": f"{random_genius_message() + ligne_aleatoire_genie_code(filepath="LeGenieCode/LeGenieCode_Init.txt")} "}] + messages}
        else:
            final_json = {"messages": [{"role": "developer", "content": f"{random_genius_message()+ligne_aleatoire_genie_code()} "}] + messages}
    else:
        final_json = {"messages": []+messages}

    return final_json

def remplacer_interpretation_par_genie(filepath):
    # Lire toutes les lignes du fichier JSONL
    with open(filepath, "r", encoding="utf-8") as file:
        lignes = file.readlines()

    nouvelles_lignes = []
    for line in lignes:
        data = json.loads(line)

        # Vérifier chaque message
        for message in data.get("messages", []):
            if "[Interpretating Python code]" in message.get("content", ""):
                remplacement = f"[{ligne_aleatoire_genie_code("LeGenieCode/LeGenieCode_Python.txt")}]"
                remplacement = str(remplacement)
                message["content"] = message["content"].replace("[Interpretating Python code]", remplacement)

        # Ajouter la ligne modifiée à la liste finale
        nouvelles_lignes.append(json.dumps(data, ensure_ascii=False))

    # Écrire le résultat dans le fichier original
    with open(filepath, "w", encoding="utf-8") as file:
        for ligne in nouvelles_lignes:
            file.write(ligne + "\n")

def remplacer_interpretation_par_geniedeu_onsaitjamais(filepath):
    # Compile la regex pour repérer la chaîne exacte [Interpretating Python Code]
    pattern = re.compile(r"\[Interpretating Python Code\]")

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    nouvelles_lignes = []

    for line in lines:
        # On essaie de charger la ligne en JSON
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            # Si la ligne n'est pas du JSON valide, on la laisse telle quelle
            nouvelles_lignes.append(line.strip())
            continue

        # Vérifier que data est un dict
        if not isinstance(data, dict):
            # Peut-être que c'est un tableau JSON au lieu d'un dict ?
            # On le réécrit sans modif pour éviter l'erreur.
            nouvelles_lignes.append(line.strip())
            continue

        # Récupérer la liste des messages
        messages = data.get("messages", [])
        if not isinstance(messages, list):
            # Si "messages" n'est pas une liste, on laisse la ligne telle quelle.
            nouvelles_lignes.append(line.strip())
            continue

        # Parcourir chaque message dans la liste
        for message in messages:
            # Vérifier que message est un dict (parfois, ça peut être une string)
            if not isinstance(message, dict):
                continue  # on ignore ou on loggue un warning

            # Récupérer le content
            content = message.get("content", "")
            if not isinstance(content, str):
                continue  # Si content n'est pas une chaîne, on ne fait rien

            # Si on trouve le pattern, on remplace
            if pattern.search(content):
                remplacement = f"[{ligne_aleatoire_genie_code('LeGenieCode/LeGenieCode_Python.txt')}]"
                message["content"] = pattern.sub(remplacement, content)

        # À la fin, on réécrit l'objet JSON complet (dict -> str)
        nouvelles_lignes.append(json.dumps(data, ensure_ascii=False))

    # On réécrit le fichier
    with open(filepath, "w", encoding="utf-8") as f:
        for nl in nouvelles_lignes:
            f.write(nl + "\n")


if __name__ == "__main__":
    # Ouvrir (ou créer) le fichier final JSONL en mode append dans le dossier Lisa_Genie
    with open("LisaFinal.jsonl", "a", encoding="utf-8") as jsonl_file:
        # Exploration des dossiers et sous-dossiers depuis le dossier courant uniquement
        for root, dirs, files in os.walk("../Lisa_AntModule", topdown=True):
            for file in files:
                if file.endswith('.txt'):
                    full_path = os.path.join(root, file)
                    json_data = traiter_fichier(full_path)
                    if json_data:  # Vérification si None (fichier ignoré)
                        jsonl_file.write(json.dumps(json_data, ensure_ascii=False) + "\n")


    time.sleep(5)
    remplacer_interpretation_par_genie("LisaFinal.jsonl")
    time.sleep(5)
    remplacer_interpretation_par_geniedeu_onsaitjamais("LisaFinal.jsonl")




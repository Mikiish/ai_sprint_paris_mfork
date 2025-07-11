import math
import json
import re
import os


def load_messages(filepath):
    """Charge les messages en JSON et retourne une liste d'objets"""
    with open(filepath, "r", encoding="utf-8") as file:
        raw_text = file.read()
        messages = raw_text.split("\n\n")  # Séparer chaque bloc {}
        return [json.loads(msg) for msg in messages if msg.strip()]  # Charger en JSON


def detect_python_code(message):
    """Détecte précisément la présence de code Python, sans faux positif dû aux caractères fréquents."""
    python_keywords = [
        r"\bclass\b", r"\bimport\b", r"\breturn\b",
        r"\bfrom\b", r"\bfor\b", r"\bwhile\b", r"\bself\b",
        r"if __name__ =="
    ]
    keyword_count = sum(bool(re.search(pattern, message)) for pattern in python_keywords)

    # Seuil de mots-clés : ≥2 keywords distincts trouvés pour déclencher la détection
    return keyword_count >= 2 or "if __name__ ==" in message


def sanitize_message_part(part):
    if not isinstance(part, str):
        return "[Interpretating Quantum Type]"

    # Patterns explicites Canvas / Updates / Textdoc
    canvas_pattern = r'{"name":.*?"type": ?"code/python".*?}'
    updates_pattern = r'{"updates":.*?"replacement":.*?}'
    textdoc_pattern = r'{"textdoc_id":'

    # Traitement précis des blocs Python explicites
    if re.search(canvas_pattern, part) or re.search(updates_pattern, part) or re.search(textdoc_pattern, part):
        return "[Interpretating Python Code]"

    # Traitement des blocs explicites ```python```
    if "```python" in part:
        return re.sub(r"```python[\s\S]*?```", "\n[Interpretating Python code]\n", part)

    # Traitement général basé sur la détection de code Python avec double vérification
    user_code_pattern = r'(\"{1,3})?import\s|(\"{1,3})?class\s'
    match = re.search(user_code_pattern, part)

    if match:
        code_start = match.start()
        subsequent_text = part[code_start:]
        if detect_python_code(subsequent_text):
            return part[:code_start] + "[Interpretating Python Code]"

    return part


def sanitize_jsonl_file(input_file, output_file):
    """Charge un fichier JSONL, détecte et remplace le code Python dans les messages."""
    sanitized_entries = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line.strip())
            if "parts" in entry and isinstance(entry["parts"], list):
                entry["parts"] = [sanitize_message_part(part) for part in entry["parts"]]
            sanitized_entries.append(entry)

    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in sanitized_entries:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')


def save_messages(messages, filepath):
    """Sauvegarde une liste d'objets JSON sous forme de texte structuré."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write("\n\n".join(json.dumps(msg, ensure_ascii=False) for msg in messages))


def apply_condensation(block, factor):
    """Condense une liste de messages selon un facteur spécifique."""
    reduced_size = max(1, int(len(block) * factor))
    indices = sorted(math.floor(i * len(block) / reduced_size) for i in range(reduced_size))
    return [block[i] for i in indices]


def segment_and_condense(messages):
    """ Segmente les messages en 3 actes et applique la condensation exponentielle. """
    total_msgs = len(messages)

    # Définition des actes (segmentation en messages)
    acts = [
        messages[:total_msgs // 3],
        messages[total_msgs // 3: 2 * total_msgs // 3],
        messages[2 * total_msgs // 3:]
    ]

    # Appliquer charge → décharge → charge à chaque acte
    acts_condensed = []
    for act, charge_factor, discharge_factor in zip(acts, [0.5, 0.6, 0.7], [0.8, 0.9, 1.0]):
        part1 = apply_condensation(act[:len(act) // 3], 1 - math.exp(-charge_factor))  # Charge
        part2 = apply_condensation(act[len(act) // 3: 2 * len(act) // 3], math.exp(-discharge_factor))  # Décharge
        part3 = apply_condensation(act[2 * len(act) // 3:], 1 - math.exp(-charge_factor + 0.2))  # Charge
        acts_condensed.append([part1, part2, part3])

    return acts, acts_condensed


def segment_final_parts(messages, segment_length):
    """Segment chaque sous-partie d'un acte en fichiers de 1 à 7 messages"""
    segmented_messages = []
    idx = 0
    while idx < len(messages):
        batch_size = segment_length[idx % len(segment_length)]
        segment = messages[idx:idx + batch_size]
        segmented_messages.append(segment)
        idx += batch_size
    return segmented_messages


def sanitize_messages(messages):
    for msg in messages:
        if "parts" in msg and isinstance(msg["parts"], list) and msg["parts"]:
            msg["parts"] = [sanitize_message_part(part) for part in msg["parts"]]
    return messages


# Chargement du fichier brut en JSON
messages = load_messages("export_conversation.txt")

# Nettoyage des messages pour retirer le code Python
messages = sanitize_messages(messages)

# Segmentation et condensation
acts, acts_condensed = segment_and_condense(messages)

# Sauvegarde des actes bruts
for i, act in enumerate(acts, start=1):
    save_messages(act, f"Act{i}_ChatToAPI/Act{i}_ChatToAPI_Raw.txt")
    for j, part in enumerate(acts_condensed[i - 1], start=1):
        part_path = f"Act{i}_ChatToAPI/Act{i}_ChatToAPI_Part{j}/Act{i}_ChatToAPI_Part{j}_Raw.txt"
        save_messages(part, part_path)

        # Segmentation en fichiers plus petits et enregistrement
        segmented_parts = segment_final_parts(part, [1, 2, 3, 4, 5, 6, 7])
        for k, segment in enumerate(segmented_parts, start=1):
            save_messages(segment,
                          f"Act{i}_ChatToAPI/Act{i}_ChatToAPI_Part{j}/Act{i}_ChatToAPI_Part{j}_{i}{j}_{k}.txt")

print(f"✅ Condensation terminée : {len(messages)} messages segmentés et enregistrés.")

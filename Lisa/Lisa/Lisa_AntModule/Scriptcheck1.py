import json
import re


def compter_long_hex_majuscule(filepath, longueur_min=10):
    """
    Compte dans tout le fichier .jsonl le nombre total de séquences
    hexadécimales (A-F0-9) d'au moins `longueur_min` caractères.
    On se limite aux "role" = user ou assistant.
    """
    # Regex pour cibler uniquement des suites en MAJUSCULES (A-F et 0-9),
    # par ex. "EA123F0F1", entre délimiteurs de mots (\b).
    pattern_upper_hex = re.compile(rf"\b[A-F0-9]{{{longueur_min},}}\b")

    total_count = 0

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Tente de charger le JSON
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                # Ligne hors-format JSON, on passe
                continue

            # On s'attend à ce que data soit un dict avec "messages"
            if not isinstance(data, dict):
                continue

            messages = data.get("messages", [])
            if not isinstance(messages, list):
                continue

            # On cible seulement les "role" user ou assistant
            for msg in messages:
                if not isinstance(msg, dict):
                    continue
                role = msg.get("role")
                if role in ("user", "assistant"):
                    content = msg.get("content", "")
                    if isinstance(content, str):
                        # On recherche toutes les occurrences en majuscules
                        matches = pattern_upper_hex.findall(content)
                        total_count += len(matches)

    print(f"Nombre total de nombres hexadécimaux en majuscules : {total_count}")

# Exemple d’utilisation :
# Compter uniquement celles de 20+ caractères :
compter_long_hex_majuscule("LisaFinal.jsonl", longueur_min=20)


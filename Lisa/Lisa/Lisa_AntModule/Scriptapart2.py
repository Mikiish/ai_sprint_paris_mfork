import json
import re
import LisaJsonlModulaire
from LisaJsonlModulaire import ligne_aleatoire_genie_code

# Regex qui va capturer soit :
# - 0x suivi de [a-f0-9]+ (en minuscule), ou
# - [A-F0-9]+ (en majuscule, sans préfixe)
# \b est optionnel si tu veux vraiment des "mots" hex distincts,
# sinon tu peux l'enlever si tes hex peuvent être collés à d'autres caractères.
pattern_hex = re.compile(r"\b(0x[a-f0-9]+|[A-F0-9]+)\b")


def insertion_bracket_au_milieu(m):
    """
    Fonction de substitution qui reçoit un objet Match (m).
    On insère [RimeDuGénie] au milieu du nombre hex.
    """
    original_hex = m.group(0)

    # Vérifie si ça commence par '0x'
    if original_hex.startswith("0x"):
        prefix = "0x"
        # On isole la partie hex (après 0x)
        valeur_hex = original_hex[2:]
    else:
        prefix = ""
        valeur_hex = original_hex

    # Split en deux moitiés
    longueur = len(valeur_hex)
    milieu = longueur // 2  # arbitraire si c'est pair

    partie1 = valeur_hex[:milieu]
    partie2 = valeur_hex[milieu:]

    return f"{prefix}{partie1}[{ligne_aleatoire_genie_code(filepath="LeGenieCode/LeGenieCode.txt")}]{partie2}"


def parse_and_insert_rime(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    result_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            # Ligne vide => on skip ou on réécrit telle quelle
            result_lines.append(line)
            continue

        # On tente de charger le JSON
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            # Pas du JSON valide => on réécrit la ligne telle quelle
            result_lines.append(line)
            continue

        # On s'attend à ce que data soit un dict avec une clé "messages"
        if not isinstance(data, dict):
            result_lines.append(line)
            continue

        messages = data.get("messages")
        if not isinstance(messages, list):
            result_lines.append(line)
            continue

        # Pour chaque message, on check role et si c'est "user" ou "assistant",
        # on applique la substitution sur son content
        for msg in messages:
            if not isinstance(msg, dict):
                continue

            role = msg.get("role")
            # On se focalise sur "user" ou "assistant"
            if role in ("user", "assistant"):
                content = msg.get("content", "")
                if isinstance(content, str):
                    # On applique la regex + fonction de remplacement
                    new_content = pattern_hex.sub(insertion_bracket_au_milieu, content)
                    msg["content"] = new_content

        # On reconvertit l'objet en chaîne JSON
        result_json = json.dumps(data, ensure_ascii=False)
        result_lines.append(result_json)

    # Écriture finale
    with open(filepath, "w", encoding="utf-8") as f:
        for rl in result_lines:
            f.write(rl + "\n")


if __name__ == "__main__":
    # Ouvrir (ou créer) le fichier final JSONL en mode append dans le dossier Lisa_Genie
    parse_and_insert_rime("LisaFinal.jsonl")

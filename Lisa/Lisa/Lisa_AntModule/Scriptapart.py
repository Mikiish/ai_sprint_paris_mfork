import os
import json
import random
import re
import unicodedata
import LisaJsonlModulaire

def remplacer_interpretation_par_genie(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    nouvelle_liste_jsonl = []

    # Regex pour détecter la chaîne exacte [Interpretating Python Code]
    pattern = re.compile(r"\[Interpretating Python Code\]")

    for line in lines:
        # On s'attend à ce que chaque "line" soit un tableau JSON
        # (liste d'objets) et non un seul objet avec "messages".
        liste_messages = json.loads(line)

        # On parcourt chaque élément du tableau (chaque "message" dict)
        for message in liste_messages:
            content = message.get("content", "")
            # Si la chaîne [Interpretating Python Code] est trouvée
            if pattern.search(content):
                # Exemple de remplacement :
                # on insère [...] avec du code aléatoire récupéré via ligne_aleatoire_genie_code
                remplacement = f"[{ligne_aleatoire_genie_code('LeGenieCode/LeGenieCode_Python.txt')}]"
                message["content"] = pattern.sub(remplacement, content)

        # On réécrit la liste d'objets en JSON
        nouvelle_liste_jsonl.append(json.dumps(liste_messages, ensure_ascii=False))

    # On écrase le fichier avec les lignes modifiées
    with open(filepath, "w", encoding="utf-8") as file:
        for ligne in nouvelle_liste_jsonl:
            file.write(ligne + "\n")


if __name__ == "__main__":
    # Ouvrir (ou créer) le fichier final JSONL en mode append dans le dossier Lisa_Genie
    remplacer_interpretation_par_genie("LisaFinal.jsonl")
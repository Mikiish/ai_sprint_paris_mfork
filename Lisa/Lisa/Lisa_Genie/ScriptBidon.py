import os
import json
import random


def nettoyer_fichier(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    lignes_non_vides = [line.strip() for line in lines if line.strip()]

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lignes_non_vides))

if __name__ == "__main__":
    with open("Act1_ChatToAPI_Part1_11_3.txt", "r", encoding="utf-8") as file:
        # On lit chaque ligne, on enlève les espaces/sauts de ligne, et on ignore les lignes vides
        lignes_nettoyees = [line.strip() for line in file if line.strip()]

    # Affichage du résultat
    print("\n".join(lignes_nettoyees))

    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith('.txt'):
                fichier = os.path.join(root, name)
                nettoyer_fichier(fichier)


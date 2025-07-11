import os
import json
import random

if __name__ == "__main__":
    with open("Act1_ChatToAPI_Part1_11_3.txt", "r", encoding="utf-8") as file:
        # On lit chaque ligne, on enlève les espaces/sauts de ligne, et on ignore les lignes vides
        lignes_nettoyees = [line.strip() for line in file if line.strip()]

    # Affichage du résultat
    print("\n".join(lignes_nettoyees))

    

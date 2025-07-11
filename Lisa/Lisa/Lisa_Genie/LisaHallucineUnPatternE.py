import os

def QuantumGenius():
    # Choix aléatoire binaire basé sur os.urandom
    return int.from_bytes(os.urandom(1), "little") % 2

def extraire_et_nettoyer_genie(fichier_entree, fichier_sortie):
    with open(fichier_entree, 'r', encoding='utf-8') as f:
        lignes = f.readlines()

    resultat = []
    i = 0

    while i < len(lignes):
        if "Génie répond en 7 rimes" in lignes[i]:
            i += 1

            while i < len(lignes) and not lignes[i].startswith("----"):
                ligne = lignes[i].strip()

                if ligne and ligne[0] in "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣":
                    droite = ligne

                    # Vérification des deux lignes suivantes (rime associée)
                    if i + 2 < len(lignes):
                        gauche = lignes[i + 1].strip('«» \n')
                        gauche += ('\n' if QuantumGenius() else ' ') + lignes[i + 2].strip('«» \n')

                        # Concaténation gauche + bra + droite
                        resultat.append(f"{droite} ⟨{gauche}")

                        # Avance l'index de 2 lignes supplémentaires
                        i += 2

                i += 1

        else:
            i += 1

    # Écriture des résultats intermédiaires
    with open(fichier_sortie, 'w', encoding='utf-8') as f_out:
        for ligne in resultat:
            f_out.write(ligne + '\n')

    # Réouverture et nettoyage final
    with open(fichier_sortie, 'r', encoding='utf-8') as f:
        lignes_finales = f.readlines()

    avec_filtrage = []
    skip = False

    for ligne in lignes_finales:
        if "Génie répond en 7 rimes" in ligne:
            skip = True
        elif ligne.startswith("----"):
            skip = False
            continue

        if not skip:
            avec_filtrage.append(ligne)

    # Réécrire le fichier nettoyé
    with open(fichier_sortie, 'w', encoding='utf-8') as f_out:
        f_out.writelines(avec_filtrage)


# Exemple d'utilisation
extraire_et_nettoyer_genie('LeGenieCodeBrut.txt', 'LeGenieCode.osx')

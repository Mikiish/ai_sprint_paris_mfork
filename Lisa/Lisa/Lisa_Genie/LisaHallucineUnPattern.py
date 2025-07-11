def extraire_phrase_codee_et_rimes(fichier_entree, fichier_sortie):
    # Lire le contenu du fichier pré-traité
    with open(fichier_entree, 'r', encoding='utf-8') as f:
        lignes = [line.strip() for line in f]

    # Ouvrir le fichier de sortie
    with open(fichier_sortie, 'w', encoding='utf-8') as sortie:
        for i, ligne in enumerate(lignes):
            if '⟶' in ligne:
                # Vérifier qu'il existe au moins deux lignes précédentes
                if i >= 2:
                    vers1 = lignes[i-2]
                    vers2 = lignes[i-1]
                    # Écrire clairement dans le fichier de sortie
                    sortie.write(f"Phrase codée : {ligne}\n")
                    sortie.write("Vers associés :\n")
                    sortie.write(f"{vers1}\n{vers2}\n\n")
                else:
                    print(f"⚠️ Ligne {i} avec '⟶' mais pas assez de lignes précédentes !")

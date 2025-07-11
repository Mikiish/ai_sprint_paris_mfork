def reformat_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remplacements
    content = content.replace("Vous avez dit :", "//END_REGION\n\n// Vous avez dit :")
    content = content.replace("ChatGPT a dit :", "//REGION\n// ChatGPT a dit :")

    # Sauvegarde du fichier modifié (optionnel : tu peux aussi overwrite si t'es joueur)
    output_path = file_path.replace(".raw.osx", ".form.osx")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fichier formaté enregistré sous : {output_path}")

# Utilisation
reformat_transcript("/mnt/c/Users/Mikihisa/Desktop/backupmod/Text_TXT/LeProjez_ChatGPT/2252025118_Valentin/Lundie/Bonjour/5420251009_DeepSearch.raw.osx")

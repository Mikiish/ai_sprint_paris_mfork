import json

# Charger les conversations exportées
with open("conversations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extraire uniquement les messages du projet "Jeu Videoz"
messages = []
print(type(data))  # Vérifie si c'est une liste ou un dictionnaire
print(data[:2])  # Affiche les 2 premiers éléments pour voir la structure

# Vérifier la structure
for conv in data:
    if "mapping" in conv:
        for msg in conv["mapping"].values():
            if isinstance(msg, dict) and isinstance(msg.get("message"), dict):  # Vérifie que msg["message"] est bien un dictionnaire
                message_content = msg["message"].get("content", "")

                if isinstance(message_content, dict):
                    message_content = json.dumps(message_content, ensure_ascii=False)  # Convertir en texte lisible si c'est un dictionnaire

                messages.append(str(message_content))  # Forcer en chaîne de caractères

# Enregistrer dans un fichier texte
output_file = "export_conversation.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n\n".join(messages))  # Séparation par deux sauts de ligne pour mieux structurer

print(f"✅ Export terminé ! Tous les messages sont dans '{output_file}'")
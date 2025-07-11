import json

def json_to_jsonl(input_json_file, output_jsonl_file):
    # Charger l'OBJET JSON principal
    with open(input_json_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # Récupérer la liste des messages
    messages = data["messages"]

    # Écrire chaque message sur une ligne dans un fichier JSONL
    with open(output_jsonl_file, 'w', encoding='utf-8') as outfile:
        for msg in messages:
            # msg est un dict : {"role": "...", "content": "..."}
            json.dump(msg, outfile, ensure_ascii=False)
            outfile.write('\n')

if __name__ == "__main__":
    # Exemple d'utilisation
    json_to_jsonl("input.json", "output.jsonl")
    print("Conversion terminée !")

import re
import json

# --- REGEX pour capturer "content": f" ... " ---
#  1) ("content"\s*:\s*f")  => repère le préfixe
#  2) ((\\.|[^"\\])*)       => capture tout ce qui n'est pas un " non-échappé
#  3) (")                   => guillemet de fin
content_pattern = re.compile(r'("content"\s*:\s*f")((\\.|[^"\\])*)(")')


def escape_fstring_content(text: str) -> str:
    """
    Échappe les caractères spéciaux dans le contenu de la f-string :
      - \  => \\
      - "  => \"
      - {  => \{
      - }  => \}
    """
    # D’abord on double tous les backslash existants,
    # pour éviter qu'ils ne "mangent" le caractère suivant.
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    return text


def verify_and_fix_jsonlg_line(line: str) -> str:
    """
    - Repère les occurrences de "content": f" ... " dans 'line'.
    - Échappe les caractères spéciaux dans le contenu de la f-string.
    - Renvoie une version "corrigée" de la ligne (toujours avec f"").
    - Vérifie qu'elle correspond bien à la structure attendue (developer, user, assistant).

    Si la structure n'est pas correcte, lève une exception ou renvoie une erreur.
    """
    original_line = line.rstrip('\n')

    # 1) Échapper les caractères spéciaux dans chaque f-string
    def replace_fstring(m):
        prefix = m.group(1)  # "content": f"
        content_in_f = m.group(2)  # le texte brut à l'intérieur des ""
        # group(3) = le guillemet fermant (non capturé en param)

        escaped_content = escape_fstring_content(content_in_f)
        return f'{prefix}{escaped_content}"'  # on reconstruit : "content": f"XXX"

    fixed_line = content_pattern.sub(replace_fstring, original_line)

    # 2) Vérification de la structure => on remplace f"..." par "..." (sans le f)
    #    juste pour parser en JSON standard et checker la structure.
    #    On parse un "fichier" JSON en mémoire.
    #    Si la structure n'est pas bonne, on renvoie une erreur.

    # Remplacer "content": f" par "content": "
    line_for_parsing = re.sub(r'("content"\s*:\s*)f"', r'\1"', fixed_line)
    print("DEBUG line_for_parsing=", repr(line_for_parsing))
    try:
        data = json.loads(line_for_parsing)
    except json.JSONDecodeError as e:
        raise ValueError(f"Impossible de parser la ligne en JSON : {e}\nLigne : {fixed_line}")

    # 3) Checker qu'on a bien { "messages": [ {role, content}, ... ] }
    if "messages" not in data or not isinstance(data["messages"], list):
        raise ValueError(f"Structure invalide (pas de 'messages' ou pas une liste)\nLigne : {fixed_line}")

    messages = data["messages"]
    roles = [m.get("role") for m in messages]

    required = {"developer", "user", "assistant"}
    if not required.issubset(set(roles)):
        raise ValueError(f"Les rôles {required} ne sont pas tous présents.\nLigne : {fixed_line}")

    # Tout est OK, on renvoie la ligne corrigée
    return fixed_line


def verify_and_fix_jsonlg_file(input_path: str, output_path: str = None):
    """
    - Parcourt chaque ligne du fichier .jsonlg (ou .txt).
    - Vérifie/corrige (échappe) le contenu de la f-string.
    - S'assure que la structure est correcte (developer, user, assistant).
    - Écrit dans un fichier output_path si fourni, sinon fait un check "à blanc".
    """
    with open(input_path, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()

    fixed_lines = []
    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            # Ligne vide, on l'ignore ou on la recopie telle quelle
            fixed_lines.append(line)
            continue

        try:
            fixed_line = verify_and_fix_jsonlg_line(line)
            fixed_lines.append(fixed_line)
        except ValueError as e:
            print(f"Erreur à la ligne {i} : {e}")
            return  # on stoppe ou on continue selon ton besoin

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as fout:
            for fl in fixed_lines:
                fout.write(fl + '\n')
        print(f"Fichier corrigé écrit dans : {output_path}")
    else:
        print("Aucune sortie spécifiée, vérification terminée sans sauvegarde.")


if __name__ == "__main__":
    # EXEMPLE
    input_file = "input.jsonlg"
    output_file = "output.jsonlg"
    verify_and_fix_jsonlg_file(input_file, output_file)

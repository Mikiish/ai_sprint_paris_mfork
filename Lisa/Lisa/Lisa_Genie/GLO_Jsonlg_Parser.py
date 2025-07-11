import re
import sys

# Regex pour trouver: "content": f" ... "
# 1) ("content"\s*:\s*f") => repère la séquence littérale
# 2) ((?:\\.|[^"\\])*)    => capture tout ce qu'il y a jusqu'au prochain guillemet,
#                            en autorisant les séquences échappées \.
# 3) (")                  => le guillemet fermant
content_pattern = re.compile(r'("content"\s*:\s*f")((?:\\.|[^"\\])*)(")')

def escape_minimal_fstring(text: str) -> str:
    ###
    ### Remplace uniquement :
    ### - " => \"
    ### - { => \{
    ### - } => \}
    ### Laisse tout le reste tel quel (y compris \).
    ###
    text = text.replace('"', '\\"')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    return text

def fix_line(line: str) -> str:
    ###
    ### Cherche toutes les occurrences de "content": f" ... " et applique escape_minimal_fstring
    ### au contenu de la f-string, puis reconstruit la ligne.

    def replacer(match):
        prefix = match.group(1)       # "content": f"
        inner_text = match.group(2)   # le contenu entre guillemets
        # match.group(3) = le guillemet fermant

        escaped_inner = escape_minimal_fstring(inner_text)
        return f'{prefix}{escaped_inner}"'

    return content_pattern.sub(replacer, line)

def process_file(input_path: str, output_path: str = None):
    ###
    ### Lit le fichier ligne par ligne, applique fix_line() et écrit le résultat
    ### dans output_path ou sur la console.
    ###
    with open(input_path, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()

    fixed_lines = []
    for i, line in enumerate(lines, start=1):
        line_stripped = line.rstrip('\n')
        if not line_stripped:
            # Ligne vide => on la garde telle quelle
            fixed_lines.append(line_stripped)
            continue

        new_line = fix_line(line_stripped)
        fixed_lines.append(new_line)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as fout:
            for fl in fixed_lines:
                fout.write(fl + '\n')
        print(f"Fichier corrigé écrit : {output_path}")
    else:
        # Affiche juste le résultat
        for fl in fixed_lines:
            print(fl)

if __name__ == "__main__":
    # Exemple d'utilisation
    # python GLO_Jsonlg_Parser.py input.jsonlg output.jsonlg
    """
    if len(sys.argv) < 2:
        print("Usage: GLO_Jsonlg_Parser.py <input_file> [output_file]")
        sys.exit(1)

    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None"""
    inp = "input.jsonlg"
    out = "output.jsonlg"
    process_file(inp, out)

def check_brackets_and_quotes(line: str) -> None:
    ###
    ### Vérifie la cohérence des paires de ()[]{} et des guillemets "
    ### dans 'line'. Si tout va bien, ne renvoie rien.
    ### Si un problème est détecté, lève ValueError avec un message et l'index fautif.
    ###

    stack = []  # va contenir des tuples (symbole, index)
    in_string = False
    escaped = False  # pour savoir si le caractère précédent est un backslash

    # On parcourt chaque caractère de la ligne
    for i, ch in enumerate(line):
        if in_string:
            # On est dans une chaîne
            if escaped:
                # Le caractère précédent était un backslash, donc on ignore
                # la signification spéciale du char courant
                escaped = False
            else:
                if ch == '\\':
                    # Le prochain char sera échappé
                    escaped = True
                elif ch == '"':
                    # fin de la chaîne
                    in_string = False
        else:
            # On n'est pas dans une chaîne
            if ch == '"':
                # On entre dans une chaîne
                in_string = True
            elif ch in ['(', '[', '{']:
                # On empile
                stack.append((ch, i))
            elif ch in [')', ']', '}']:
                # On dépile et on vérifie
                if not stack:
                    raise ValueError(f"Symbole fermant '{ch}' à l'index {i} sans ouvrant correspondant.")
                top, idx_open = stack.pop()
                # Vérifier la correspondance
                if top == '(' and ch != ')':
                    raise ValueError(f"Attendu ')' mais trouvé '{ch}' à l'index {i}.")
                if top == '[' and ch != ']':
                    raise ValueError(f"Attendu ']' mais trouvé '{ch}' à l'index {i}.")
                if top == '{' and ch != '}':
                    raise ValueError(f"Attendu '}}' mais trouvé '{ch}' à l'index {i}.")

        # Fin du else: in_string
        # On remet escaped à False si on n'a pas rencontré un backslash
        if ch != '\\':
            escaped = False

    # Fin de la boucle
    if in_string:
        # on est encore dans une chaîne
        raise ValueError(f"Guillemet ouvrant sans fermant. La chaîne commence mais ne se termine pas.")

    if stack:
        # Il reste des ouvrants non fermés
        top, idx_open = stack[-1]
        raise ValueError(f"Ouvrant '{top}' (index {idx_open}) non fermé.")


def check_file(input_path: str):
    ###
    ### Lit 'input_path' ligne par ligne, vérifie l'équilibrage et affiche le résultat.
    ###
    with open(input_path, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()

    for i, line in enumerate(lines, start=1):
        line_stripped = line.rstrip('\n')
        try:
            check_brackets_and_quotes(line_stripped)
            print(f"Ligne {i}: OK - balanced")
        except ValueError as e:
            print(f"Ligne {i}: ERREUR - {e}")

if __name__ == "__main__":
    # Exemple d'utilisation :
    # Remplace "mon_fichier.txt" par le chemin réel vers ton fichier à vérifier.
    check_file("output.jsonlg")

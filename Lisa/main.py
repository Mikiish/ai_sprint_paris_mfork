import subprocess
import signal
import sys
import os
import Casino1031

# Liste pour stocker les résultats
resultsForPS = []


def open_powershell():
    """ Ouvre une fenêtre PowerShell pour afficher les résultats en live. """
    if os.name == 'nt':  # Windows
        return subprocess.Popen(
            ["powershell.exe", "-NoExit", "-Command", "while ($true) { Get-Content -Path results_ps.txt -Wait }"],
            creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:  # Linux/Mac
        return subprocess.Popen(["xterm", "-e", "tail -f results_ps.txt"])


# Ouvrir la console externe
ps_process = open_powershell()

while True:
    currentValue = casino_hex_prime()
    resultsForPS.append(currentValue)

    # Écrire la dernière valeur dans un fichier texte pour que PowerShell puisse l'afficher
    with open("results_ps.txt", "w") as f:
        f.write(str(currentValue) + "\n")

    print(f"Dernière valeur trouvée : {currentValue}")
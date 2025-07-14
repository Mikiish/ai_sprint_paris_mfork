#!/bin/bash
set -e

# 🧠 Configuration
VENV_DIR="Lisa/.venv"
REQ_FILE="requirements.txt"

# 🔥 Suppression ancienne version si elle existe
if [ -d "$VENV_DIR" ]; then
    echo "[⚠] Ancien environnement détecté, suppression..."
    rm -rf "$VENV_DIR"
fi

# 🏗️ Création d'un nouvel environnement virtuel
echo "[+] Création d’un nouvel environnement virtuel dans $VENV_DIR..."
python3 -m venv "$VENV_DIR" --prompt pylisa

# 🧬 Activation de l’environnement
echo "[+] Activation..."
source "$VENV_DIR/bin/activate"

# 📦 Mise à jour des outils de base
echo "[+] Mise à jour de pip, setuptools, wheel..."
pip install --upgrade pip setuptools wheel

# 📄 Installation des dépendances si le fichier existe
if [ -f "$REQ_FILE" ]; then
    echo "[+] Installation depuis $REQ_FILE..."
    pip install -r "$REQ_FILE"
else
    echo "[!] Aucun $REQ_FILE trouvé. Dépendances non installées."
fi

# 🧾 Affiche le contenu du fichier pyvenv.cfg
echo "[+] Configuration actuelle de l’environnement :"
cat "$VENV_DIR/pyvenv.cfg"

# ✅ Terminé
echo "[✔] Environnement virtuel prêt à l’emploi !"

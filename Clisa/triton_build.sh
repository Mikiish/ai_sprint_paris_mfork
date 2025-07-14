#!/bin/bash
set -e
export TRITON_BUILD_WITH_CLANG_LLD=true
export TRITON_BUILD_WITH_CCACHE=true
export TRITON_HOME="$PWD/.triton_home"          # évite de polluer ton $HOME
export MAX_JOBS=4                               # (ou 2 si t’as peu de RAM)

rm -rf triton
git clone https://github.com/triton-lang/triton.git
cd triton

python3 -m venv .venv --prompt triton
python3 -m pip install --upgrade pip setuptools wheel
source .venv/bin/activate
pip install -r python/requirements.txt 		# build-time dependencies
pip install -e . --no-build-isolation

# Localisation du compile_commands.json
echo "\n[+] Recherche du fichier compile_commands.json..."
readlink -f $(find ./build -name 'compile_commands.json') || echo "[!] Aucun fichier compile_commands.json trouvé."

echo "\n[✔] Triton reconstruit proprement. À toi de jouer."

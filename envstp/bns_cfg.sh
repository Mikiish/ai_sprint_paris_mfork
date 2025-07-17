#!/bin/bash

set -e

echo "[+] Mise à jour des paquets..."
sudo apt update -y && sudo apt upgrade -y

echo "[+] Installation des outils de développement essentiels..."
sudo apt install -y \
    build-essential \
    cmake \
    make \
    g++ \
    gcc \
    clang \
    lldb \
    lcov \
    valgrind

echo "[+] Installation des bibliothèques système de base..."
sudo apt install -y \
    zlib1g-dev \
    libreadline-dev \
    libssl-dev \
    libffi-dev

echo "[+] Installation des bibliothèques de nombres entiers arbitraires et crypto..."
sudo apt install -y \
    libgmp-dev \
    libmpfr-dev \
    libmpc-dev \
    libboost-all-dev \
    libcrypto++-dev \
    libsodium-dev \
    libtommath-dev \
    libntl-dev \
    libgcrypt20-dev

echo "[+] Installation des outils de développement et de débogage pratiques..."
sudo apt install -y \
    git \
    curl \
    wget \
    nano \
    unzip \
    htop \
    jq

echo "[+] Installation des outils Python (pip, venv, setuptools)..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-setuptools \
    python3-dev \
    python3-wheel

echo "[✔] Environnement C/C++/Python prêt. Tu n'as maintenant plus que ta propre incompétence à blâmer."



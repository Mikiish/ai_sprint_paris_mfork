#!/bin/bash
set -e

sudo apt update
sudo apt install quickemu

git clone https://github.com/quickemu-project/quickemu
cd quickemu
sudo ./quickemu --install
echo "[+] Quickemu installed. Preparing env..."
quickget ubuntu
ech "[+] Env is ready. Run command `quickemu --vm ubuntu.conf` to start VM."

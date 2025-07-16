#!/bin/bash
# This script is used to set up the vLLM development environment.
set -e
cd scripts
git clone https://github.com/vllm-project/vllm.git
echo "[+] vLLM repository cloned successfully. Apply devpatch..."
chmod +x ./0_container.sh
./0_container.sh
echo "[+] vLLM development environment is set up. Pulling latest changes..."
pip uninstall vllm -y
cd /vllm-dev
python setup.py develop
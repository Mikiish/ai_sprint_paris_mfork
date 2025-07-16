#!/bin/bash
set -e
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
echo "[+] Docker is working properly. Pulling docker immage..."
docker pull rocm/vllm:latest
echo "[+] Docker image pulled. Starting container..."
docker run -it --rm \
  --network=host \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add=video \
  --ipc=host \
  --cap-add=SYS_PTRACE \
  --security-opt seccomp=unconfined \
  --shm-size 8G \
  -v $(pwd):/workspace \
  -w /workspace/notebooks \
  rocm/vllm:latest
echo "[+] Docker contained started."
pip install jupyter
echo "[+] Jupyter installed. Run [jupyter-lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root] command to start Jupyter server."

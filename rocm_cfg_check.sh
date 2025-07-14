#!/bin/bash
set -e

# Make the directory if it doesn't exist yet.
# This location is recommended by the distribution maintainers.
sudo mkdir --parents --mode=0755 /etc/apt/keyrings

# Download the key, convert the signing-key to a full
# keyring required by apt and store in the keyring directory
wget https://repo.radeon.com/rocm/rocm.gpg.key -O - | \
    gpg --dearmor | sudo tee /etc/apt/keyrings/rocm.gpg > /dev/null

# Register ROCm packages
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/6.4.1 noble main" \
    | sudo tee --append /etc/apt/sources.list.d/rocm.list
echo -e 'Package: *\nPin: release o=repo.radeon.com\nPin-Priority: 600' \
    | sudo tee /etc/apt/preferences.d/rocm-pin-600
sudo apt update
sudo apt install rocm

# Post-installation instructions
sudo apt install python3-setuptools python3-wheel
sudo apt install environment-modules
sudo usermod -a -G video,render $LOGNAME
sudo usermod -a -G video,render root

echo 'ADD_EXTRA_GROUPS=1' | sudo tee -a /etc/adduser.conf
echo 'EXTRA_GROUPS=video' | sudo tee -a /etc/adduser.conf
echo 'EXTRA_GROUPS=render' | sudo tee -a /etc/adduser.conf

sudo tee --append /etc/ld.so.conf.d/rocm.conf <<EOF
/opt/rocm/lib
/opt/rocm/lib64
EOF
sudo ldconfig

sudo mv 70-amdgpu.rules /etc/udev/rules.d/70-amdgpu.rules
sudo udevadm control --reload-rules && sudo udevadm trigger

source /etc/profile.d/modules.sh
module load rocm/6.4.1
export LD_LIBRARY_PATH=/opt/rocm-6.4.1/lib

rocminfo
clinfo

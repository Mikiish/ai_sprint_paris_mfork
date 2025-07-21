#!/bin/bash
set -e

# Desired ROCm version
ROCM_VERSION="6.4.1"

# Check if ROCm is already installed and matches desired version
if ls /opt | grep -q "rocm-"; then
    INSTALLED_VERSION=$(ls -d /opt/rocm-* 2>/dev/null | head -n1 | sed 's|/opt/rocm-||')
    if [ "$INSTALLED_VERSION" = "$ROCM_VERSION" ]; then
        echo "ROCm $ROCM_VERSION already installed. Nothing to do."
        exit 0
    else
        echo "ROCm $INSTALLED_VERSION detected, but version $ROCM_VERSION requested."
        echo "Continuing with installation of ROCm $ROCM_VERSION..."
    fi
else
    echo "No existing ROCm installation detected. Installing ROCm $ROCM_VERSION..."
fi

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
sudo apt update -qq
sudo apt install -qq rocm

# Post-installation instructions
sudo apt install -qq python3-setuptools python3-wheel
sudo apt install -qq environment-modules
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

#!/bin/bash
set -e

############################################################
# WinForge Secure Builder
# Environment Setup & Configuration Script
#
# Author: Marcos Hernandez (Einjunge)
# Version: 1.0.0
# Purpose: Full Wine + Python (Windows) build environment
############################################################

# -------------------- GLOBAL CONFIG -----------------------
export WINEARCH=win64
export WINEPREFIX="$HOME/.wine-winforge"

PYTHON_VERSION="3.10.11"
PYTHON_EXE="python-${PYTHON_VERSION}-amd64.exe"
PYTHON_URL="https://www.python.org/ftp/python/${PYTHON_VERSION}/${PYTHON_EXE}"
PYTHON_WIN_DIR="C:\\Python310"

LOGFILE="$HOME/.winforge_setup.log"
exec > >(tee -a "$LOGFILE") 2>&1

echo "========================================================"
echo " WinForge Secure Builder :: Environment Setup"
echo " Author : Marcos Hernandez (Einjunge)"
echo "========================================================"
echo "[+] Log file: $LOGFILE"
echo

# -------------------- CHECK ROOT --------------------------
if [[ "$EUID" -ne 0 ]]; then
  echo "[ERROR] This script must be run as root (sudo)."
  exit 1
fi

# -------------------- STEP 1 ------------------------------
echo "[*] Installing Linux dependencies..."
apt update
apt install -y \
  wine64 \
  wine32 \
  wget \
  winbind \
  cabextract \
  unzip \
  fonts-wine

# -------------------- STEP 2 ------------------------------
echo "[*] Initializing Wine prefix: $WINEPREFIX"
mkdir -p "$WINEPREFIX"
wineboot --init
sleep 5

# -------------------- STEP 3 ------------------------------
echo "[*] Downloading Python ${PYTHON_VERSION} (Windows x64)..."
if [ ! -f "$PYTHON_EXE" ]; then
  wget -q --show-progress "$PYTHON_URL"
else
  echo "[*] Python installer already exists."
fi

# -------------------- STEP 4 ------------------------------
echo "[*] Installing Python inside Wine..."
wine "$PYTHON_EXE" /quiet \
  InstallAllUsers=1 \
  PrependPath=1 \
  TargetDir="$PYTHON_WIN_DIR"

# -------------------- STEP 5 ------------------------------
echo "[*] Restarting Wine services..."
wineserver -k
sleep 5

# -------------------- STEP 6 ------------------------------
echo "[*] Verifying Python installation..."
wine python --version || {
  echo "[FATAL] Python installation failed."
  exit 1
}

# -------------------- STEP 7 ------------------------------
echo "[*] Installing Python packages inside Wine..."
wine python -m pip install --upgrade pip setuptools wheel

wine python -m pip install \
  pyinstaller \
  requests \
  psutil \
  pillow

# -------------------- STEP 8 ------------------------------
echo "[*] Validating Python runtime..."
wine python - <<EOF
import sys
import requests
import psutil
from PIL import Image

print("Python OK:", sys.version)
print("requests OK:", requests.__version__)
print("psutil OK")
print("pillow OK")
EOF

# -------------------- STEP 9 ------------------------------
echo "[*] Validating PyInstaller..."
wine python -m PyInstaller --version || {
  echo "[FATAL] PyInstaller validation failed."
  exit 1
}

# -------------------- FINAL -------------------------------
echo
echo "========================================================"
echo " [✔] WinForge Environment READY"
echo " [✔] Wine Prefix : $WINEPREFIX"
echo " [✔] Python      : $PYTHON_VERSION (Windows)"
echo " [✔] PyInstaller : Operational"
echo "========================================================"
echo
echo "[+] You can now compile Windows executables safely."

#!/bin/bash
set -e

command -v python3 >/dev/null 2>&1 || { echo >&2 "Python3 is not installed."; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo >&2 "pip3 is not installed."; exit 1; }

if ! command -v python3-venv >/dev/null 2>&1; then
    echo "Installing python3-venv..."
    sudo apt-get update && sudo apt-get install -y python3-venv
fi

if [ ! -d venv ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "All dependencies installed."

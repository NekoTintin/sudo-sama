#!/bin/bash
set -e

# Check python installation
if ! command -v python3 &> /dev/null
then
	echo "Python3 not found."
exit
fi

# Venv
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source ".venv/bin/activate"

# Check deps
pip install --upgrade pip
pip install -r requirements.txt

# Compiling translations
bash compile_translations.sh

# Start
python3 sudo-sama.py
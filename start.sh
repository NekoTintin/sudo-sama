#!/bin/bash

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
pip install -r --r requirements.txt

# Compiling translations
msgfmt locale/en/LC_MESSAGES/en.po -o locale/en/LC_MESSAGES/en.mo
msgfmt locale/fr/LC_MESSAGES/fr.po -o locale/fr/LC_MESSAGES/fr.mo

# Start
python3 sudo-sama.py
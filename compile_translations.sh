#!/bin/bash
set -e

# Compiling translations
msgfmt locale/en/LC_MESSAGES/en.po -o locale/en/LC_MESSAGES/en.mo
msgfmt locale/fr/LC_MESSAGES/fr.po -o locale/fr/LC_MESSAGES/fr.mo
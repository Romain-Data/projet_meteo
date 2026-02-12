#!/bin/bash

echo "--- 📋 Rapport Pylint ---"
pylint run.py || true

echo -e "\n--- 🧪 Rapport Pytest ---"
pytest || true

echo -e "\n--- 🚀 Démarrage de l'application ---"
exec python run.py run

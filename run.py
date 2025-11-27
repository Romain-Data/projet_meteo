#!/usr/bin/env python3
"""Script de gestion du projet compatible Mac/Windows/Linux"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def run():
    """Lance l'application Streamlit"""
    # Chemins absolus
    script_dir = Path(__file__).parent.absolute()
    app_path = script_dir / "projet" / "app.py"

    # Changer vers le répertoire racine
    os.chdir(script_dir)

    # Configurer l'environnement PYTHONPATH
    env = os.environ.copy()
    pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{script_dir}{os.pathsep}{pythonpath}"

    # Lancer Streamlit
    print("🚀 Lancement de l'application...")
    print(f"📁 Répertoire: {script_dir}")
    print(f"📄 App: {app_path}")

    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)], env=env)


def install():
    """Installe les dépendances"""
    print("📦 Installation des dépendances...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✓ Installation terminée")


def clean():
    """Nettoie les fichiers cache"""
    project_root = Path(".")

    print("🧹 Nettoyage en cours...")

    # Supprime __pycache__
    for pycache in project_root.rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
        print(f"✓ Supprimé {pycache}")

    # Supprime .pyc
    for pyc in project_root.rglob("*.pyc"):
        pyc.unlink(missing_ok=True)

    # Supprime .log
    for log in project_root.rglob("*.log"):
        log.unlink(missing_ok=True)
        print(f"✓ Supprimé {log}")

    print("✓ Nettoyage terminé")


def test():
    """Lance les tests"""
    print("🧪 Lancement des tests...")

    # Ajouter la racine au PYTHONPATH pour les tests aussi
    script_dir = Path(__file__).parent.absolute()
    env = os.environ.copy()
    pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{script_dir}{os.pathsep}{pythonpath}"

    subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], env=env)


def help_menu():
    """Affiche l'aide"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║          Gestionnaire de projet Weather App              ║
╚═══════════════════════════════════════════════════════════╝

Commandes disponibles:
  python run.py install  - Installe les dépendances
  python run.py run      - Lance l'application Streamlit
  python run.py clean    - Nettoie les fichiers temporaires
  python run.py test     - Lance les tests avec pytest
  python run.py help     - Affiche cette aide

Exemples:
  python run.py install && python run.py run
  python run.py clean && python run.py test
    """)


if __name__ == "__main__":
    commands = {
        "run": run,
        "install": install,
        "clean": clean,
        "test": test,
        "help": help_menu,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        help_menu()
        sys.exit(1)
    else:
        commands[sys.argv[1]]()

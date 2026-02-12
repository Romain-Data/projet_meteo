"""
Ce script est le point d'entrée de l'application.
Il permet de lancer l'application, de lancer les tests,
d'installer les dépendances et de nettoyer les fichiers temporaires.
"""

import os
import shutil
import sys
import subprocess
from pathlib import Path


def run():
    """Lance l'application Streamlit"""
    app_path = Path(__file__).parent / "projet" / "app.py"

    if not app_path.exists():
        print(f"❌ Erreur: {app_path} n'existe pas")
        sys.exit(1)

    # Configuration de l'environnement
    env = {
        **dict(os.environ),
        "PYTHONPATH": str(Path(__file__).parent)
    }

    try:
        print("🚀 Démarrage de l'application Streamlit...")
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(app_path)],
            env=env,
            check=True  # Lève une exception si le code de retour n'est pas 0
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt de l'application demandé...")
        print("✅ Application arrêtée proprement")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors de l'exécution: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)


def test():
    """Lance les tests"""
    try:
        print("🧪 Lancement des tests...")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v"],
            check=False
        )
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrompus")
        sys.exit(130)  # Code standard pour interruption

def clean():
    """Nettoie les fichiers temporaires"""

    print("🧹 Nettoyage des fichiers temporaires...")

    patterns_to_clean = [
        "__pycache__",
        "*.pyc",
        ".pytest_cache",
        ".coverage",
        "htmlcov",
        "*.egg-info"
    ]

    cleaned = 0
    root = Path(__file__).parent

    for pattern in patterns_to_clean:
        if "*" in pattern:
            # Fichiers avec wildcard
            for file in root.rglob(pattern):
                try:
                    file.unlink()
                    cleaned += 1
                    print(f"  🗑️  {file.relative_to(root)}")
                except Exception as e:
                    print(f"  ⚠️  Impossible de supprimer {file}: {e}")
        else:
            # Dossiers
            for folder in root.rglob(pattern):
                try:
                    shutil.rmtree(folder)
                    cleaned += 1
                    print(f"  🗑️  {folder.relative_to(root)}/")
                except Exception as e:
                    print(f"  ⚠️  Impossible de supprimer {folder}: {e}")

    print(f"✅ Nettoyage terminé ({cleaned} éléments supprimés)")


def help_cmd():
    """Affiche l'aide"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           🌡️  PROJET MÉTÉO - COMMANDES DISPONIBLES          ║
╚══════════════════════════════════════════════════════════════╝

📌 Commandes principales:

    python run.py run        🚀 Lance l'application Streamlit
    python run.py test       🧪 Lance les tests avec pytest
    python run.py install    📦 Installe les dépendances
    python run.py clean      🧹 Nettoie les fichiers temporaires
    python run.py help       ❓ Affiche cette aide

💡 Exemples:

    python run.py run                    # Lance l'app
    python run.py test                   # Lance tous les tests
    python run.py clean && python run.py run   # Nettoie puis lance

🛑 Pour arrêter l'application: Ctrl+C (ou Cmd+C sur Mac)
""")


# Mapping des commandes
commands = {
    "run": run,
    "test": test,
    "clean": clean,
    "help": help_cmd,
}


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print("❌ Commande invalide\n")
        help_cmd()
        sys.exit(1)

    try:
        commands[sys.argv[1]]()
    except KeyboardInterrupt:
        print("\n\n🛑 Commande interrompue par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

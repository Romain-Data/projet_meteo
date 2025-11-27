"""Configuration centralisée du système de logging"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging(log_level: str = "INFO", log_file: str = "app.log"):
    """
    Configure le système de logging avec sortie fichier + console

    Args:
        log_level: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Chemin du fichier de log
    """
    # Créer le dossier logs/ s'il n'existe pas
    log_dir = Path("projet/logs")
    log_dir.mkdir(exist_ok=True)

    log_path = log_dir / log_file

    # Format des logs
    log_format = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler pour le fichier (rotation automatique)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,              # Garde 3 anciennes versions
        encoding='utf-8'
    )
    file_handler.setLevel(getattr(logging, log_level.upper()))
    file_handler.setFormatter(log_format)

    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(log_format)

    # Configuration du logger racine
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Supprimer les handlers existants (évite les doublons)
    root_logger.handlers.clear()

    # Ajouter les nouveaux handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Log de confirmation
    logging.info(f"📝 Logging configuré - Fichier: {log_path}")

    return log_path

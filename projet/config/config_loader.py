import json
import logging
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ConfigLoader:
    """
    Singleton
    Handles loading and providing access to the application configuration.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._config = None
        return cls._instance

    def __init__(self, fichier_config: str = "projet/config/config.json"):
        if self._config is None:
            self._load(fichier_config)

    def _load(self, fichier_config: str) -> None:
        """
        Loads the configuration from a JSON configuration file.

        Args:
            fichier_config (str): The path to the JSON configuration file.

        Raises:
            FileNotFoundError: If the configuration file is not found at the specified path.
        """
        path = Path(fichier_config)

        if not path.exists():
            logger.error(f"Le fichier de configuration n'a pas été trouvé : {fichier_config}")
            raise FileNotFoundError(f"Config not found: {fichier_config}")

        with open(path, 'r', encoding='utf-8') as file:
            self._config = json.load(file)

        logger.info(f"Configuration chargée depuis {fichier_config}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a value from the configuration using dot notation.

        Args:
            key (str): A string representing the nested key (e.g., 'api.base_url').
            default (Any, optional): The default value to return if the key is not found. Defaults to None.

        Returns:
            Any: The requested configuration value, or the default value if not found.
        """
        if self._config is None:
            logger.warning("La configuration n'a pas été chargée. Appel de .get() sur une config vide.")
            return default

        keys = key.split('.')
        value = self._config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                logger.debug(f"Clé '{key}' non trouvée. Retour de la valeur par défaut.")
                return default

        return value

    def get_required(self, key: str) -> Any:
        """
        Retrieves a required value from the configuration.

        Args:
            key (str): A string representing the nested key (e.g., 'api.base_url').

        Raises:
            ValueError: If the key is not found.
        """
        value = self.get(key)
        if value is None:
            raise ValueError(f"Configuration requise manquante: '{key}'")
        return value

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Retrieves an entire configuration section as a dictionary.

        Args:
            section (str): The top-level key of the section to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing the configuration for the section,
                            or an empty dictionary if the section is not found.
        """
        return self.get(section, {})

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ConfigLoader:
    """
    Handles loading and providing access to the application configuration.

    This class is intended to be used as a singleton, managed by the
    `get_config` factory function.
    """
<<<<<<< Updated upstream
    def __init__(self):
        self._config: Dict[str, Any] | None = None
=======

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._config = None
        return cls._instance

    def __init__(self, config_path: str = "projet/config/config.json"):
        if self._config is None:
            self._load(config_path)
>>>>>>> Stashed changes

    def _load(self, config_path: str) -> None:
        """
        Loads the configuration from a JSON configuration file.

        Args:
            config_path (str): The path to the JSON configuration file.

        Raises:
            FileNotFoundError: If the configuration file is not found
            at the specified path.
        """
        path = Path(config_path)

        if not path.exists():
            logger.error(f"Le fichier de configuration n'a pas été trouvé : {config_path}")
            raise FileNotFoundError(f"Config not found: {config_path}")

        with open(path, 'r', encoding='utf-8') as file:
            self._config = json.load(file)

        logger.info(f"Configuration chargée depuis {config_path}")

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Retrieves a value from the configuration using dot notation.

        Args:
            key_path (str): A string representing the nested key (e.g., 'api.base_url').
            default (Any, optional): The default value to return if the key is not found.
                                    Defaults to None.

        Returns:
            Any: The requested configuration value, or the default value if not found.
        """
        if self._config is None:
            logger.warning("La configuration n'a pas été chargée. Appel de .get() sur une config vide.")
            return default

        keys = key_path.split('.')
        value = self._config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                logger.debug(f"Clé '{key_path}' non trouvée. Retour de la valeur par défaut.")
                return default

        return value

    def get_required(self, key_path: str) -> Any:
        """
        Retrieves a required value from the configuration.

        Raises:
            ValueError: If the key is not found.
        """
        value = self.get(key_path)
        if value is None:
            raise ValueError(f"Configuration requise manquante: '{key_path}'")
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


@lru_cache(maxsize=1)
# J'ai découvert lru_cache avec Claude qui ne laisse exister
# qu'une seule instance de ConfigLoader
def get_config(config_path: str = "projet/config/config.json") -> ConfigLoader:
    """
    Factory function to get the singleton instance of ConfigLoader.

    This function ensures that the configuration is loaded only once. On the first call,
    it creates a `ConfigLoader` instance, loads the configuration file, and caches it.
    Subsequent calls return the cached instance.

    Args:
        config_path (str, optional): The path to the configuration file.
                                     Defaults to "config/config.yaml".

    Returns:
        ConfigLoader: The singleton instance of the configuration loader.
    """
    config_loader = ConfigLoader()
    config_loader.load(config_path)
    return config_loader

import pytest
import json
from unittest.mock import mock_open
from projet.config.config_loader import ConfigLoader

@pytest.fixture
def reset_singleton():
    """Reset the singleton instance before each test."""
    ConfigLoader._instance = None
    yield
    ConfigLoader._instance = None

def test_singleton_behavior(reset_singleton, mocker):
    """Test : ConfigLoader implémente bien le singleton pattern"""
    mocker.patch("builtins.open", mock_open(read_data='{}'))
    mocker.patch("projet.config.config_loader.Path.exists", return_value=True)
    
    loader1 = ConfigLoader()
    loader2 = ConfigLoader()
    
    assert loader1 is loader2

def test_load_valid_config(reset_singleton, mocker):
    """Test : Chargement d'un fichier de configuration valide"""
    config_data = {
        "api": {
            "key": "test_key",
            "url": "http://test.com"
        },
        "debug": True
    }
    json_content = json.dumps(config_data)
    
    mocker.patch("builtins.open", mock_open(read_data=json_content))
    mocker.patch("projet.config.config_loader.Path.exists", return_value=True)
    
    loader = ConfigLoader("dummy_path.json")
    
    assert loader.get("api.key") == "test_key"
    assert loader.get("api.url") == "http://test.com"
    assert loader.get("debug") is True

def test_file_not_found(reset_singleton, mocker):
    """Test : Lève FileNotFoundError si le fichier n'existe pas"""
    mocker.patch("projet.config.config_loader.Path.exists", return_value=False)
    
    with pytest.raises(FileNotFoundError):
        ConfigLoader("non_existent.json")

def test_get_nested_keys(reset_singleton, mocker):
    """Test : Récupération de clés imbriquées (dot notation)"""
    config_data = {"section": {"subsection": {"key": "value"}}}
    mocker.patch("builtins.open", mock_open(read_data=json.dumps(config_data)))
    mocker.patch("projet.config.config_loader.Path.exists", return_value=True)
    
    loader = ConfigLoader()
    
    assert loader.get("section.subsection.key") == "value"
    assert loader.get("section.subsection") == {"key": "value"}

def test_get_default_value(reset_singleton, mocker):
    """Test : Retourne la valeur par défaut si la clé n'existe pas"""
    mocker.patch("builtins.open", mock_open(read_data='{}'))
    mocker.patch("projet.config.config_loader.Path.exists", return_value=True)
    
    loader = ConfigLoader()
    
    assert loader.get("missing.key", "default") == "default"
    assert loader.get("missing.key") is None

def test_get_required_raises_error(reset_singleton, mocker):
    """Test : get_required lève ValueError si la clé est manquante"""
    mocker.patch("builtins.open", mock_open(read_data='{}'))
    mocker.patch("projet.config.config_loader.Path.exists", return_value=True)
    
    loader = ConfigLoader()
    
    with pytest.raises(ValueError, match="Configuration requise manquante"):
        loader.get_required("missing_key")

def test_get_section(reset_singleton, mocker):
    """Test : Récupération d'une section complète"""
    config_data = {"database": {"host": "localhost", "port": 5432}}
    mocker.patch("builtins.open", mock_open(read_data=json.dumps(config_data)))
    mocker.patch("projet.config.config_loader.Path.exists", return_value=True)
    
    loader = ConfigLoader()
    
    section = loader.get_section("database")
    assert section == {"host": "localhost", "port": 5432}
    assert loader.get_section("missing") == {}

def test_get_with_empty_config(reset_singleton, mocker):
    """Test : get() retourne default et log warning si config est None"""
    # Mock _load to do nothing so we can simulate empty config
    mocker.patch.object(ConfigLoader, '_load')
    
    loader = ConfigLoader()
    # Explicitly set to None to be sure (though __new__ sets it to None)
    loader._config = None
    
    # Validation
    assert loader.get("anything", "default") == "default"

def test_get_required_success(reset_singleton, mocker):
    """Test : get_required retourne la valeur si la clé existe"""
    config_data = {"my_key": "my_value"}
    mocker.patch("builtins.open", mock_open(read_data=json.dumps(config_data)))
    mocker.patch("projet.config.config_loader.Path.exists", return_value=True)
    
    loader = ConfigLoader()
    
    assert loader.get_required("my_key") == "my_value"

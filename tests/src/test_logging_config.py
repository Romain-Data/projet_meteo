import logging
import sys
import pytest
from projet.config import logging_config

@pytest.fixture
def mock_path(mocker):
    return mocker.patch('projet.config.logging_config.Path')

@pytest.fixture
def mock_rotating_handler(mocker):
    mock = mocker.patch('projet.config.logging_config.RotatingFileHandler')
    mock.return_value.level = logging.NOTSET 
    return mock

@pytest.fixture
def mock_stream_handler(mocker):
    mock = mocker.patch('logging.StreamHandler')
    mock.return_value.level = logging.NOTSET
    return mock

@pytest.fixture
def mock_get_logger(mocker):
    return mocker.patch('logging.getLogger')

@pytest.fixture
def mock_logging_info(mocker):
    return mocker.patch('logging.info')

def test_setup_logging_creates_directory(mock_path, mock_rotating_handler, mock_stream_handler, mock_logging_info):
    mock_dir = mock_path.return_value
    mock_log_file = mock_dir.__truediv__.return_value 
    
    log_path = logging_config.setup_logging()
    
    mock_path.assert_called_with("projet/logs")
    mock_dir.mkdir.assert_called_once_with(exist_ok=True)
    assert log_path == mock_log_file

def test_setup_logging_configures_handlers(mock_rotating_handler, mock_stream_handler, mock_logging_info):
    mock_file_handler_instance = mock_rotating_handler.return_value
    mock_console_handler_instance = mock_stream_handler.return_value
    
    logging_config.setup_logging(log_level="DEBUG", log_file="test.log")
    
    # Verify RotatingFileHandler
    mock_rotating_handler.assert_called_once()
    args, kwargs = mock_rotating_handler.call_args
    assert kwargs['maxBytes'] == 5 * 1024 * 1024
    assert kwargs['backupCount'] == 3
    assert kwargs['encoding'] == 'utf-8'
    
    # Verify levels and formatters
    mock_file_handler_instance.setLevel.assert_called_with(logging.DEBUG)
    assert mock_file_handler_instance.setFormatter.called
    
    # Verify StreamHandler
    mock_stream_handler.assert_called_with(sys.stdout)
    mock_console_handler_instance.setLevel.assert_called_with(logging.WARNING)
    assert mock_console_handler_instance.setFormatter.called

def test_setup_logging_configures_root_logger(mock_rotating_handler, mock_stream_handler, mock_get_logger, mock_logging_info):
    mock_root_logger = mock_get_logger.return_value
    mock_file_handler = mock_rotating_handler.return_value
    mock_console_handler = mock_stream_handler.return_value
    
    logging_config.setup_logging(log_level="ERROR")
    
    # Verify getLogger called with no args (root logger)
    mock_get_logger.assert_called_with()
    
    # Verify root logger configuration
    mock_root_logger.setLevel.assert_called_with(logging.ERROR)
    
    # Verify handlers clearing and adding
    mock_root_logger.handlers.clear.assert_called_once()
    
    # Pytest adds its own handler (LogCaptureHandler), so we can't assert count == 2
    mock_root_logger.addHandler.assert_any_call(mock_file_handler)
    mock_root_logger.addHandler.assert_any_call(mock_console_handler)

def test_setup_logging_logs_confirmation(mock_logging_info, mock_path, mock_rotating_handler, mock_stream_handler): # mock_path needed because setup_logging calls Path()
    logging_config.setup_logging()
    mock_logging_info.assert_called_once()
    args, _ = mock_logging_info.call_args
    assert "Logging configuré" in args[0]

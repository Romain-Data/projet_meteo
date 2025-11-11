import logging
import streamlit as st
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple

from config.config_loader import ConfigLoader, get_config
from src.api.extractor import APIExtractor
from src.entities.station import Station
from src.processing.transformer import DataTransformer
from src.processing.validator import DataValidator
from src.services.data_fetcher import DataFetcher
from src.services.loader import DataLoader
from src.storage.parquet_handler import ParquetHandler
from src.viz.chart import DataVizualiser

logger = logging.getLogger(__name__)


class AppInitializer:
    """
    Handles application initialization by loading configuration,
    setting up services, and preparing data sources.
    """
    
    def __init__(self, config: ConfigLoader):
        """
        Initializes the AppInitializer with the application configuration.

        Args:
            config (ConfigLoader): The application configuration loader.
        """
        self.config = config
    
    @st.cache_data(show_spinner=False)
    def load_stations(_self) -> List[Station]:
        """
        Load weather stations from CSV file.
        
        The '_self' parameter is used because this method is cached by Streamlit,
        and caching works better with instance methods.

        Returns:
            List[Station]: List of Station objects with id, name, and coordinates
        """
        stations_csv_path_str = _self.config.get("storage.stations_csv")
        stations_csv_path = Path(stations_csv_path_str)
        logger.info(f"Loading stations from {stations_csv_path}")
        
        if not stations_csv_path.exists():
            logger.error(f"Stations file not found: {stations_csv_path}")
            raise FileNotFoundError(f"Stations file not found: {stations_csv_path}")
        
        df = pd.read_csv(stations_csv_path, sep=';')
        
        stations = [
            Station(
                id=row['id_nom'],
                name=row['nom'],
                longitude=row['longitude'],
                latitude=row['latitude']
            )
            for _, row in df.iterrows()
        ]
        
        logger.info(f"Loaded {len(stations)} stations")
        return stations
    
    def create_station_lookup(self, stations: List[Station]) -> Dict[str, Station]:
        """
        Create a dictionary mapping station names to Station objects.
        
        Args:
            stations: List of Station objects
            
        Returns:
            Dict[str, Station]: Dictionary with station names as keys
        """
        return {station.name: station for station in stations}
    
    
    @staticmethod
    @st.cache_resource(show_spinner=False)
    def init_services() -> Tuple[ParquetHandler, DataFetcher, DataVizualiser]:
        """
        Initialize and cache all application services using settings from the config file.

        This method acts as a Dependency Injection container by creating and
        configuring services, then injecting them into higher-level services.
        
        Returns:
            Tuple of (ParquetHandler, DataFetcher, DataVizualiser)
        """
        logger.info("Initializing services from configuration...")
        config = get_config()

        # --- Build low-level services from config ---
        api_config = config.get_section('api')
        # Note: Assumes APIExtractor constructor accepts these arguments
        extractor = APIExtractor(base_url=api_config.get('url_base'), timeout=api_config.get('timeout'))

        validation_rules = config.get_section('validation')
        # Note: Assumes DataValidator constructor accepts rules
        validator = DataValidator(rules=validation_rules)

        storage_config = config.get_section('storage')
        # Note: Assumes ParquetHandler constructor accepts these arguments
        parquet_handler = ParquetHandler(
            base_path=storage_config.get('data_path'),
            compression=storage_config.get('parquet_compression')
        )

        # --- Build high-level services by injecting dependencies ---
        data_fetcher = DataFetcher(
            extractor=extractor,
            transformer=DataTransformer(), # Assuming no config needed
            validator=validator,
            loader=DataLoader(parquet_handler) # Loader might need the handler
        )

        weather_charts = DataVizualiser() # Assuming no config needed

        return parquet_handler, data_fetcher, weather_charts
    

    @staticmethod
    def configure_page():
        """Configure Streamlit page settings."""
        config = get_config()
        app_config = config.get_section('app')
        st.set_page_config(
            page_title=app_config.get('page_title', "Weather Dashboard"),
            page_icon=app_config.get('page_icon', "🌡️"),
            layout=app_config.get('layout', "wide")
        )
    

    @staticmethod
    def setup_logging():
        """Setup application logging based on the configuration file."""
        config = get_config()
        log_config = config.get_section('logging')
        logging.basicConfig(
            level=log_config.get('level', 'INFO').upper(),
            format=log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            # filename could also be added to config
        )

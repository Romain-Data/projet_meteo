import logging
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple
import streamlit as st

from projet.config.config_loader import ConfigLoader
from projet.src.api.extractor import APIExtractor
from projet.src.entities.station import Station
from projet.src.entities.station_builder import StationBuilder
from projet.src.processing.transformer import DataTransformer
from projet.src.processing.validator import DataValidator
from projet.src.services.data_fetcher import DataFetcher
from projet.src.services.loader import DataLoader
from projet.src.storage.parquet_handler import ParquetHandler
from projet.src.viz.chart import DataVizualiser

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

    @st.cache_data()
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
                StationBuilder()
                .set_id(row['id_nom'])
                .set_nom(row['nom'])
                .set_longitude(row['longitude'])
                .set_latitude(row['latitude'])
                .build()
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
        config = ConfigLoader()

        # --- Build low-level services from config ---
        extractor = APIExtractor(base_url=config.get_required('api.url_base'),
                                 timeout=config.get_required('api.timeout'))

        validation_rules = config.get_section('validation')
        validator = DataValidator(rules=validation_rules)

        parquet_handler = ParquetHandler(data_dir=Path(config.get_required('storage.data_path')),
                                         compression=config.get_required('storage.parquet_compression')
                                         )

        # --- Build high-level services by injecting dependencies ---
        data_fetcher = DataFetcher(
            extractor=extractor,
            transformer=DataTransformer(),
            validator=validator,
            loader=DataLoader(),
            parquet_handler=parquet_handler  # Injection de la dépendance
        )

        weather_charts = DataVizualiser()

        return parquet_handler, data_fetcher, weather_charts

    @staticmethod
    def configure_page():
        """Configure Streamlit page settings."""
        config = ConfigLoader()
        app_config = config.get_section('app')
        st.set_page_config(
            page_title=app_config.get('page_title', "Weather Dashboard"),
            page_icon=app_config.get('page_icon', "🌡️"),
            layout=app_config.get('layout', "wide")
        )

    @staticmethod
    def setup_logging():
        """Setup application logging based on the configuration file."""
        config = ConfigLoader()
        log_config = config.get_section('logging')
        logging.basicConfig(
            level=log_config.get('level', 'INFO').upper(),
            format=log_config.get('format',
                                  '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )

"""
Module for fetching and loading weather data into Station entities.
"""

import logging

from projet.src.api.extractor import APIExtractor
from projet.src.storage.parquet_handler import ParquetHandler
from projet.src.entities.station import Station
from projet.src.processing.transformer import DataTransformer
from projet.src.processing.validator import DataValidator
from projet.src.services.loader import DataLoader

logger = logging.getLogger(__name__)


class DataFetcher:
    """
    Service orchestrating the complete data pipeline for weather stations.

    Responsibilities:
    - Extract raw data from API
    - Transform data format
    - Validate data quality
    - Load validated data into Station entities
    """

    def __init__(
        self,
        extractor: APIExtractor,
        transformer: DataTransformer,
        validator: DataValidator,
        loader: DataLoader,
        parquet_handler: ParquetHandler
    ):
        # pylint: disable=too-many-arguments, too-many-positional-arguments
        self.extractor = extractor
        self.transformer = transformer
        self.validator = validator
        self.loader = loader
        self.parquet_handler = parquet_handler

    def fetch_and_load(self, station: Station) -> bool:
        """
        Fetch weather data for a station and load it into the entity.

        Args:
            station: The Station entity to update with fresh data

        Returns:
            bool: True if data was successfully fetched and loaded, False otherwise
        """
        # 1. Extract
        raw_data = self.extractor.extract(station)

        if raw_data.empty:
            logger.warning("Aucune donnée récupérée pour la station %s", station.name)
            return False

        # 2. Transform
        formatted_data = self.transformer.format_data(raw_data)
        formatted_data = self.transformer.normalize_columns(formatted_data)

        # 3. Validate
        if not self.validator.is_format_correct(formatted_data):
            logger.error("Format de données invalide pour la station %s", station.name)
            return False

        if not self.validator.are_values_valid(formatted_data):
            logger.warning(
                "Valeurs de données invalides détectées pour la station %s",
                station.name
            )
            return False

        # 4. Load
        self.loader.load_reports(station, formatted_data)
        logger.info("Chargement réussi de %d relevés pour %s", len(formatted_data), station.name)
        return True

    def refresh_and_save_station_data(self, station: Station) -> bool:
        """
        Orchestrates the full refresh and save pipeline for a single station.

        Args:
            station: The Station entity to refresh and save.

        Returns:
            bool: True if the entire process was successful, False otherwise.
        """
        logger.info("Starting full refresh and save for station %s", station.name)
        if self.fetch_and_load(station):
            return self.parquet_handler.save_station_reports(station)
        return False

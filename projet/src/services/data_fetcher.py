import logging

from projet.src.api.extractor import APIExtractor
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
        loader: DataLoader
    ):
        self.extractor = extractor
        self.transformer = transformer
        self.validator = validator
        self.loader = loader

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
            logger.warning(f"Aucune donnée récupérée pour la station {station.name}")
            return False

        # 2. Transform
        formatted_data = self.transformer.format_data(raw_data)
        formatted_data = self.transformer.normalize_columns(formatted_data)

        # 3. Validate
        if not self.validator.is_format_correct(formatted_data):
            logger.error(f"Format de données invalide pour la station {station.name}")
            return False

        if not self.validator.are_values_valid(formatted_data):
            logger.warning(f"Valeurs de données invalides détectées pour la station {station.name}")
            return False

        # 4. Load
        self.loader.load_reports(station, formatted_data)
        logger.info(f"Chargement réussi de {len(formatted_data)} relevés pour {station.name}")
        return True

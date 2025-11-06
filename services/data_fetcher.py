
from api.extractors import APIExtractor
from processing.transformers import DataTransformer
from processing.validators import DataValidator
from services.loaders import DataLoader
from domain.entities import Station
import pandas as pd


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
        extractor: APIExtractor = APIExtractor(),
        transformer: DataTransformer = DataTransformer(),
        validator: DataValidator = DataValidator(),
        loader: DataLoader = DataLoader()
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
            print(f"No data retrieved for station {station.name}")
            return False
        
        # 2. Transform
        formatted_data = self.transformer.format_data(raw_data)
        
        # 3. Validate
        if not self.validator.is_format_correct(formatted_data):
            print(f"Invalid data format for station {station.name}")
            return False
        
        if not self.validator.are_values_valid(formatted_data):
            print(f"Invalid data values for station {station.name}")
            return False
        
        # 4. Load
        self.loader.load_reports(station, formatted_data)
        
        print(f"Successfully loaded {len(formatted_data)} reports for {station.name}")
        return True

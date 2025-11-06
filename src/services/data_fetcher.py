from src.api.extractors import APIExtractor
from src.entities.station import Station
from src.processing.transformers import DataTransformer
from src.processing.validators import DataValidator
from src.services.loader import DataLoader


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
        formatted_data = self.transformer.normalize_columns(formatted_data)
        print(formatted_data.columns)
        
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

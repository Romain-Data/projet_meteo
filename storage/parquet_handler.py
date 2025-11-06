import logging
from pathlib import Path
import pandas as pd
from entities.station import Station
from services.loader import DataLoader

logger = logging.getLogger(__name__)


class ParquetHandler:
    """
    Manages the saving and loading of weather reports in Parquet format.
    """
    
    def __init__(self, data_dir: Path = Path("data/parquet")):
        """
        Args:
            data_dir: Parquet file storage directory
        """
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"ParquetHandler initialized with directory: {self.data_dir}")
    

    def save_station_reports(self, station: Station) -> None:
        """
        Saves weather reports from a station in Parquet.
        
        Args:
            station: Station with its weather reports
        """
        if not station.reports:
            logger.warning(f"No reports to save for station '{station.name}' (ID: {station.id})")
            return
        
        filepath = self._get_filepath(station)
        new_df = station.get_all_reports()

        # Merge with existing data if file exists
        if filepath.exists():
            try:
                existing_df = pd.read_parquet(filepath, engine='pyarrow')
                existing_df['date'] = pd.to_datetime(existing_df['date'])

                df = pd.concat([existing_df, new_df], ignore_index=True)

                df = df.drop_duplicates(subset=['date'], keep='last')

                df = df.sort_values('date').reset_index(drop=True)

                logger.info(f"Merged data for station '{station.name}': {len(existing_df)} existing + {len(new_df)} new = {len(df)} total records")
            
            except Exception as e:
                logger.error(f"Failed to read existing file for station '{station.name}': {type(e).__name__} - {str(e)}. Creating new file.")
                df = new_df
        else:
            df = new_df
            logger.info(f"Creating new file for station '{station.name}' with {len(df)} records")
        
        # Save to Parquet
        try:
            df.to_parquet(filepath, engine='pyarrow', compression='snappy', index=False)
            logger.info(f"Saved {len(df)} reports for station '{station.name}' to {filepath}")
        
        except Exception as e:
            logger.error(f"Failed to save reports for station '{station.name}': {type(e).__name__} - {str(e)}")
            raise
    

    def load_station_reports(self, station: Station, loader: DataLoader | None = None) -> None:
        """
        Loads weather reports from a station from Parquet.
        
        Args:
            station: Station to be filled with reports (modifies station.reports)
            loader: DataLoader instance to handle report conversion (default: new DataLoader)
        """
        if loader is None:
            loader = DataLoader()

        filepath = self._get_filepath(station)
        
        if not filepath.exists():
            logger.warning(f"No parquet file found for station '{station.name}' (ID: {station.id})")
            station.reports = []
            return 
        
        try:
            df = pd.read_parquet(filepath, engine='pyarrow')
            loader.load_reports(station, df)
            logger.info(f"Loaded {len(station.reports)} reports for station '{station.name}'")
        
        except Exception as e:
            logger.error(f"Failed to load reports for station '{station.name}': {type(e).__name__} - {str(e)}")
            station.reports = []
    

    def station_file_exists(self, station: Station) -> bool:
        """
        Checks whether a Parquet file exists for a station.
        
        Args:
            station: Station to check
            
        Returns:
            bool: True if the file exists, False otherwise
        """
        filepath = self._get_filepath(station)
        exists = filepath.exists()
        logger.debug(f"File check for station {station.name}: {exists}")
        return exists
    

    def _get_filepath(self, station: Station) -> Path:
        """
        Get the parquet filepath for a station.
        
        Args:
            station: Station to get filepath for
            
        Returns:
            Path to the parquet file
        """
        return self.data_dir / f"station_{station.id}.parquet"
from pathlib import Path
import pandas as pd
from entities.station import Station
from services.loader import DataLoader


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
    
    def save_station_reports(self, station: Station) -> None:
        """
        Saves weather reports from a station in Parquet.
        
        Args:
            station: Station with its weather reports
        """
        if not station.reports:
            print(f"⚠️  Station '{station.name}' has no reports to save")
            return
        
        # Get all reports
        df = station.get_all_reports()
        
        # Create the file name based on the station ID
        filepath = self.data_dir / f"station_{station.id}.parquet"
        
        # Save in Parquet
        df.to_parquet(filepath, engine='pyarrow', compression='snappy', index=False)

        print(f"✅ Saved {len(df)} reports for station '{station.name}' to {filepath}")
    

    def load_station_reports(self, station: Station, loader: DataLoader = DataLoader()) -> None:
        """
        Loads weather reports from a station from Parquet.
        
        Args:
            station: Station to be filled with reports (modifies station.reports)
            loader: DataLoader instance to handle report conversion (default: new DataLoader)
        """
        filepath = self.data_dir / f"station_{station.id}.parquet"
        
        if not filepath.exists():
            print(f"⚠️  No parquet file found for station '{station.name}' (ID: {station.id})")
            station.reports = []
            return
        
        # Read Parquet
        df = pd.read_parquet(filepath, engine='pyarrow')
        
        # Convert DataFrame to WeatherReport
        loader = DataLoader()
        loader.load_reports(station, df)
        
        print(f"✅ Loaded {len(df)} reports for station '{station.name}'")
    

    def station_file_exists(self, station: Station) -> bool:
        """
        Checks whether a Parquet file exists for a station.
        
        Args:
            station: Station to check
            
        Returns:
            bool: True if the file exists
        """
        filepath = self.data_dir / f"station_{station.id}.parquet"
        return filepath.exists()
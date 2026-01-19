"""
Module for handling Parquet files.
"""

import logging
from pathlib import Path
from typing import Optional
import pandas as pd

from projet.src.entities.station import Station
from projet.src.services.loader import DataLoader

logger = logging.getLogger(__name__)


class ParquetHandler:
    """
    Manages the saving and loading of weather reports in Parquet format.
    """

    def __init__(self, data_dir: Path | None = None, compression: Optional[str] = 'snappy'):
        """
        Args:
            data_dir: Parquet file storage directory
        """
        if data_dir is None:
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "data" / "parquet"

        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.compression = compression
        logger.info("ParquetHandler initialized with directory: %s", self.data_dir)

    def save_station_reports(self, station: Station) -> None:
        """
        Saves weather reports from a station in Parquet.

        Args:
            station: Station with its weather reports
        """
        if not station.reports:
            logger.warning("No reports to save for station '%s' (ID: %s)", station.name, station.id)
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

                logger.info("Merged data for station '%s': %s existing + %s new = %s total records",
                            station.name, len(existing_df), len(new_df), len(df))

            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error("Failed to read existing file for station '%s': %s - %s",
                             station.name, type(e).__name__, str(e))
                df = new_df
        else:
            df = new_df
            logger.info("Creating new file for station '%s' with %s records",
                        station.name, len(df))

        # Save to Parquet
        try:
            df.to_parquet(filepath, engine='pyarrow', compression='snappy', index=False)
            logger.info("Saved %s reports for station '%s' to %s", len(df), station.name, filepath)

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to save reports for station '%s': %s - %s",
                         station.name, type(e).__name__, str(e))
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
            logger.warning("No parquet file found for station '%s' (ID: %s)",
                           station.name, station.id)
            station.reports = []
            return

        try:
            df = pd.read_parquet(filepath, engine='pyarrow')
            loader.load_reports(station, df)
            logger.info("Loaded %s reports for station '%s'", len(station.reports), station.name)

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to load reports for station '%s': %s - %s",
                         station.name, type(e).__name__, str(e))
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
        logger.debug("File check for station '%s': %s", station.name, exists)
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

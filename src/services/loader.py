import pandas as pd
from src.entities.station import Station
from src.entities.weather_report import WeatherReport


class DataLoader:
    """
    Loads validated weather data into Station entities.
    
    Single Responsibility: Convert DataFrame rows to WeatherReport objects
    and attach them to a Station.
    """
    
    def load_reports(self, station: Station, data: pd.DataFrame) -> None:
        """
        Convert DataFrame rows to WeatherReport objects and add to station.
        
        Args:
            station: Target Station entity to populate
            data: Validated DataFrame with columns:
                - heure_de_paris (datetime)
                - temperature_en_degre_c (float)
                - humidite (int)
                - pression (int)
                - display_date (str)
                
        Side Effects:
            Replaces station.reports with new list of WeatherReport objects
        """
        reports = [
            self._create_report(row)
            for _, row in data.iterrows()
        ]
        
        station.reports = reports
    

    def _create_report(self, row: pd.Series) -> WeatherReport:
        """
        Create a single WeatherReport from a DataFrame row.
        
        Args:
            row: pandas Series with weather data
            
        Returns:
            WeatherReport: Initialized weather report object
        """
        return WeatherReport(
            date=row['date'],
            temperature=row['temperature'],
            humidity=row['humidity'],
            pressure=row['pressure'],
            display_date=row['display_date']
        )

from pathlib import Path
import pandas as pd
from typing import Optional

from domain.entities import Station, WeatherReport


class ParquetHandler:
    """
    Gère la sauvegarde et le chargement des rapports météo en format Parquet.
    """
    
    def __init__(self, data_dir: Path = Path("data/parquet")):
        """
        Args:
            data_dir: Répertoire de stockage des fichiers Parquet
        """
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save_station_reports(self, station: Station) -> None:
        """
        Sauvegarde les rapports météo d'une station en Parquet.
        
        Args:
            station: Station avec ses rapports météo
        """
        if not station.reports:
            print(f"⚠️  Station '{station.name}' has no reports to save")
            return
        
        # Convertir les rapports en DataFrame
        records = []
        for report in station.reports:
            records.append({
                'date': report.date,
                'temperature': report.temperature,
                'humidity': report.humidity,
                'pressure': report.pressure,
                'display_date': report.display_date
            })
        
        df = pd.DataFrame(records)
        
        # Créer le nom du fichier basé sur l'ID de la station
        filepath = self.data_dir / f"station_{station.id}.parquet"
        
        # Sauvegarder en Parquet
        df.to_parquet(filepath, engine='pyarrow', compression='snappy', index=False)
        
        print(f"✅ Saved {len(df)} reports for station '{station.name}' to {filepath}")
    
    def load_station_reports(self, station: Station) -> None:
        """
        Charge les rapports météo d'une station depuis Parquet.
        
        Args:
            station: Station à peupler avec les rapports (modifie station.reports)
        """
        filepath = self.data_dir / f"station_{station.id}.parquet"
        
        if not filepath.exists():
            print(f"⚠️  No parquet file found for station '{station.name}' (ID: {station.id})")
            station.reports = []
            return
        
        # Lire le Parquet
        df = pd.read_parquet(filepath, engine='pyarrow')
        
        # Convertir DataFrame en WeatherReport
        reports = []
        for _, row in df.iterrows():
            report = WeatherReport(
                date=row['date'],
                temperature=row['temperature'],
                humidity=row['humidity'],
                pressure=row['pressure'],
                display_date=row['display_date']
            )
            reports.append(report)
        
        station.reports = reports
        
        print(f"✅ Loaded {len(reports)} reports for station '{station.name}'")
    
    def station_file_exists(self, station: Station) -> bool:
        """
        Vérifie si un fichier Parquet existe pour une station.
        
        Args:
            station: Station à vérifier
            
        Returns:
            bool: True si le fichier existe
        """
        filepath = self.data_dir / f"station_{station.id}.parquet"
        return filepath.exists()
from dataclasses import dataclass
from datetime import datetime

# Dataclass découvert via le youtuber ArjanCodes
@dataclass
class WeatherReport:
    date: datetime
    temperature: float
    humidity: int
    pressure: int
    display_date: str
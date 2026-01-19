"""
Module for representing a weather report.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeatherReport:
    """
    Represents a single weather report.
    """
    date: datetime
    temperature: float
    humidity: int
    pressure: int
    display_date: str

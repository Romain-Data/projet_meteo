from datetime import datetime

class WeatherReport:
    def __init__(self, date: datetime, temperature: float, humidity: int, pressure: int, display_date: str) -> None:
        self.date: datetime = date
        self.temperature : float = temperature
        self.humidity: int = humidity
        self.pressure: int = pressure
        self.display_date: str = display_date
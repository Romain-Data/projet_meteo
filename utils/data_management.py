import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests

from utils.entity import Station, WeatherReport


class IDataExtractor:
    def extract(self):
        pass

class APIExtractor(IDataExtractor):

    def extract(
                self,
                station: Station,
                url_base: str = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/",
                select: str = 'heure_de_paris, temperature_en_degre_c, humidite, pression'
            )-> pd.DataFrame:
        """
        Fetches weather data records for a given station via API.

        Args:
            station (Station): Station object containing the target station's ID.
            url_base (str, optional): Base URL of the API endpoint. Defaults to Toulouse Métropole API.
            select (str, optional): Comma-separated list of fields to retrieve. Defaults to:
                - heure_de_paris (timestamp)
                - temperature_en_degre_c (temperature in °C)
                - humidite (humidity in %)
                - pression (pressure in Pa)

        Returns:
            pd.DataFrame: DataFrame containing the retrieved records with columns as specified in `select`.
                Rows are ordered by descending timestamp (most recent first).
                Returns empty DataFrame if no records match the criteria.

        API Query Details:
            - Time range: Last 4 days (heure_de_paris >= now(days=-4))
            - Temporal resolution: Hourly data (minute(heure_de_paris) = 0)
            - Data quality filters:
                - Temperature: -10°C to 50°C
                - Humidity: 50% to 99%
            - Limit: 100 most recent records matching criteria
            """

        station_id = station.id
        url_final = f"{url_base + station_id}/records"
        param = {
            'select': select,
            'where': """heure_de_paris >= now(days=-4)
                and minute(heure_de_paris) = 0
                and temperature_en_degre_c <= 50
                and temperature_en_degre_c >= -10
                and humidite >= 50
                and humidite < 100""",
            'order_by': 'heure_de_paris desc',
            'limit':'100'
        }
        
        data = requests.get(url_final, params=param)
        return pd.DataFrame(data.json()['results'])


class DataTransformer:
    def format_datime(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Formats datetime column in the DataFrame for display and processing.

        Args:
            data (pd.DataFrame): Input DataFrame containing a 'heure_de_paris' column
                with datetime values (as string or datetime objects).

        Returns:
            pd.DataFrame: Modified DataFrame with two datetime-related columns:
                - 'heure_de_paris': Original column converted to pandas datetime type
                (for calculations/filtering).
                - 'display_hour': Formatted string version (YYYY-MM-DD HH:MM)
                for display purposes.
        """

        data['heure_de_paris'] = pd.to_datetime(data['heure_de_paris'])
        data['display_date'] = data['heure_de_paris'].dt.strftime('%Y-%m-%d %H:%M')  
        return data 


class DataTester:
    def is_format_correct(self, data: pd.DataFrame) -> bool:
        pressure_is_int = data['pression'].dtype == np.int64
        humidity_is_int = data['humidite'].dtype == np.int64
        temperature_is_float = data['temperature_en_degre_c'].dtype == np.float64
        heure_is_datetime = pd.api.types.is_datetime64_any_dtype(data['heure_de_paris'])
        return pressure_is_int and humidity_is_int and temperature_is_float and heure_is_datetime
        
    def are_values_valid(self, data: pd.DataFrame) -> bool:
        aberrant_temperature = bool(len(data['temperature_en_degre_c'].between(50, -10, inclusive='both')))
        aberrant_humidity = bool(len(data['humidite'].between(95, 40, inclusive='both')))
        aberrant_pressure = bool(len(data['pression'].between(102000, 99500, inclusive='both')))
        return aberrant_temperature and aberrant_humidity and aberrant_pressure


class DataLoader:
    def add_reports(self, station: Station, data: pd.DataFrame)-> None:
        list_reports = []
        for _, row in data.iterrows():
            report = WeatherReport(
                date = row['heure_de_paris'],
                temperature = row['temperature_en_degre_c'],
                humidity = row['humidite'],
                pressure = row['pression'],
                display_date = row['display_date']
            )
            list_reports.append(report)
        station.reports=list_reports


class DataVizualiser:
    """
    Create an interactive line plot of temperature over time.
    
    Args:
        reports: DataFrame with 'date' (datetime) and 'temperature' (float) columns
        
    Returns:
        go.Figure: Plotly figure object with temperature timeline
    """
    def plot_temperature(self, reports: pd.DataFrame) -> go.Figure:
        # Créer la figure
        fig = go.Figure()

        # Ajouter la ligne de température
        fig.add_trace(go.Scatter(
            x=reports['date'],
            y=reports['temperature'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6, color='#1f77b4')
        ))

        # Détecter les changements de jour et créer les annotations
        annotations = []
        for i in range(1, len(reports)):
            if reports['date'].dt.date.iloc[i] != reports['date'].dt.date.iloc[i-1]:
                date_change = reports['date'].iloc[i]
                annotations.append(
                    dict(
                        x=date_change,
                        y=0,  # Position relative (sera ajustée avec yref)
                        yref="paper", 
                        yshift=-50,  # Décalage en pixels vers le bas
                        text=date_change.strftime('%d %B'),
                        showarrow=False,
                        font=dict(size=12, color='black'),
                        bgcolor='rgba(255, 255, 255, 0.7)',
                        borderpad=4,
                        xanchor='left'
                    )
                )

        # Configuration de la mise en page
        fig.update_layout(
            title=dict(
                text="Temperature Over Time",
                x=0.5,
                xanchor='center',
                font=dict(size=16)
            ),
            xaxis=dict(
                title=dict(
                    text="Hour",
                    standoff=25  # ✅ Décalage en pixels vers le bas
                ),
                tickformat='%Hh',  # Format des heures
                dtick=6*60*60*1000,  # Intervalle de 6 heures (en millisecondes)
                tickmode='linear',
                gridcolor='rgba(128, 128, 128, 0.3)',
                showgrid=True,
                tickangle=45
            ),
            yaxis=dict(
                title="Temperature (°C)",
                gridcolor='rgba(128, 128, 128, 0.3)',
                showgrid=True
            ),
            annotations=annotations,
            hovermode='x unified',
            plot_bgcolor='white',
            width=1200,
            height=600,
            margin=dict(b=100, t=80, l=60, r=40)  # Marges ajustées
        )

        return fig
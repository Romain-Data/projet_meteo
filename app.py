import streamlit as st
import pandas as pd
from pathlib import Path

from domain.entities import Station, City
from services.data_fetcher import DataFetcher
from storage.parquet_handler import ParquetHandler
from viz.charts import DataVizualiser

# Configuration de la page
st.set_page_config(
    page_title="Weather Station Dashboard",
    page_icon="🌡️",
    layout="wide"
)

# Initialisation des services
@st.cache_resource
def init_services():
    parquet_handler = ParquetHandler()
    data_fetcher = DataFetcher()
    weather_charts = DataVizualiser()
    return parquet_handler, data_fetcher, weather_charts

# Chargement des stations
@st.cache_data
def load_stations():
    csv_path = Path("data/stations/stations_meteo_transformees.csv")
    df = pd.read_csv(csv_path, sep=';')
    
    stations = []
    for _, row in df.iterrows():
        station = Station(
            id=row['id_nom'],
            name=row['nom'],
            longitude=row['longitude'],
            latitude=row['latitude']
        )
        stations.append(station)
    
    return stations

def main():
    parquet_handler, data_fetcher, weather_charts = init_services()
    
    # Titre de l'application
    st.title("🌡️ Weather Station Dashboard")
    st.markdown("---")
    
    # Chargement des stations
    stations = load_stations()
    station_names = {station.name: station for station in stations}
    
    # Sidebar pour la sélection
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Sélection de la station
        selected_name = st.selectbox(
            "Choose a station",
            options=list(station_names.keys()),
            index=0
        )
        
        selected_station = station_names[selected_name]
        
        st.markdown("---")
        
        # Bouton de rafraîchissement
        if st.button("🔄 Refresh Data", use_container_width=True):
            with st.spinner("Fetching new data..."):
                # Fetch les données via l'API
                data_fetcher.fetch_and_load(selected_station)
                # Sauvegarde en Parquet
                parquet_handler.save_station_reports(selected_station)
                st.success("Data refreshed!")
                st.rerun()
    
    # Chargement des données de la station depuis Parquet
    parquet_handler.load_station_reports(selected_station)
    
    if not selected_station.reports:
        st.warning(f"No data available for station '{selected_station.name}'")
        st.info("Click 'Refresh Data' to fetch initial data")
        return
    
    # Récupération du dernier rapport
    latest_report = selected_station.get_latest_report()
    
    # Section des métriques actuelles
    st.header(f"📍 {selected_station.name}")
    st.caption(f"Last update: {latest_report.display_date}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🌡️ Temperature",
            value=f"{latest_report.temperature}°C"
        )
    
    with col2:
        st.metric(
            label="💧 Humidity",
            value=f"{latest_report.humidity}%"
        )
    
    with col3:
        st.metric(
            label="🔽 Pressure",
            value=f"{latest_report.pressure} hPa"
        )
    
    st.markdown("---")
    
    # Section des graphiques
    st.header("📊 Temperature Timeline")
    
    # Conversion des rapports en DataFrame
    reports_data = []
    for report in selected_station.reports:
        reports_data.append({
            'date': report.date,
            'temperature': report.temperature,
            'humidity': report.humidity,
            'pressure': report.pressure
        })
    
    df_reports = pd.DataFrame(reports_data)
    
    # Affichage du graphique de température
    if not df_reports.empty:
        fig_temp = weather_charts.plot_temperature(df_reports)
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # Statistiques supplémentaires
        with st.expander("📈 Statistics"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Min Temperature", f"{df_reports['temperature'].min()}°C")
            with col2:
                st.metric("Max Temperature", f"{df_reports['temperature'].max()}°C")
            with col3:
                st.metric("Avg Temperature", f"{df_reports['temperature'].mean():.1f}°C")
    else:
        st.info("Not enough data to display chart")

if __name__ == "__main__":
    main()

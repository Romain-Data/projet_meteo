# Data Profiling - Projet Météo

Ce document décrit les données manipulées par l'application Weather Dashboard, provenant de l'API Open Data de Toulouse Métropole.

## 1. Description du Jeu de Données
Le jeu de données contient des relevés météorologiques périodiques (température, humidité, pression) pour différentes stations situées dans la métropole toulousaine.

## 2. Structure des Fichiers

### A. Stations (`stations_meteo_transformees.csv`)
Fichier de configuration statique listant les stations disponibles.
- **longitude** : Position est-ouest (coordonnées décimales).
- **latitude** : Position nord-sud (coordonnées décimales).
- **id_nom** : Identifiant unique de la station (utilisé pour les appels API).
- **nom** : Nom usuel de la station.

### B. Rapports Météo (`station_*.parquet`)
Données historiques stockées localement au format Parquet pour chaque station.
- **timestamp** : Date et heure du relevé (format datetime).
- **temperature** : Température mesurée en degrés Celsius (°C).
- **humidity** : Taux d'humidité relative en pourcentage (%).
- **pressure** : Pression atmosphérique en Pascals (Pa).

## 3. Plages de Valeurs Validées
L'application applique des filtres de validation lors de la récupération des données :
- **Température** : Entre -20°C et +60°C.
- **Humidité** : Entre 0% et 100%.
- **Pression** : Entre 80 000 Pa et 110 000 Pa.

Toute valeur en dehors de ces plages est considérée comme une anomalie et rejetée par le `DataValidator`.

## 4. Volume de Données
- **Stations** : Environ 5 stations configurées.
- **Historique** : Les visualisations se concentrent sur les 7 derniers jours par défaut.
- **Format de sortie** : Compression Snappy utilisée pour les fichiers Parquet.

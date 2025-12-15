# projet_meteo

Pitch client : société météo

- une appli pour suivre la météo toulousaine
- possibilité de choisir une station météo pour afficher données spécifiques
- voir un historique semaine

**Contraintes**
- utilisation de données ouvertes
- créer un modèle des classes en respectant les principes Clean Code
- création d'un dashboard **simple**


# Design patterns implémentés
- [x] Singleton sur [config_loader.py](projet/config/config_loader.py)
- [x] Builder sur [station_buider.py](projet/src/entities/station_builder.py)
- [x] Factory sur [data_vizualizer.py](projet/src/viz/data_vizualizer.py)
- [x] Decorator [station_display_decorator.py](projet/src/components/station_display_decorator.py)


# Installation et Lancement

## 1. Cloner le dépôt
```bash
git clone https://github.com/Romain-Data/projet_meteo.git
cd projet_meteo
```

## 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

## 3. Lancer l'application
```bash
python run.py run
```

# Architecture de fichiers
```text
.
├── projet
│   ├── components                      # Composant de l'application Streamlit
│   │   ├── metrics_display.py
│   │   ├── navigation_header.py
│   │   └── sidebar.py
│   ├── config                          # Configuration
│   │   ├── config.json
│   │   ├── config_loader.py
│   │   └── logging_config.py
│   ├── data                            # Données brutes et stockage
│   │   ├── parquet
│   │   └── stations
│   ├── logs                            # Logs de l'application
│   │   └── weather_app.log
│   ├── src                             # Source code
│   │   ├── api                         # API
│   │   │   ├── extractor.py
│   │   │   └── request_queue.py
│   │   ├── data_structures             # Structures de données
│   │   │   ├── linked_list_navigator.py
│   │   │   └── linked_list_node.py
│   │   ├── entities                    # Entités et builder
│   │   │   ├── city.py
│   │   │   ├── station.py
│   │   │   ├── station_builder.py
│   │   │   └── weather_report.py
│   │   ├── interfaces                  # Interfaces
│   │   │   └── station_navigator.py
│   │   ├── processing                  # Transformation et validation des données
│   │   │   ├── transformer.py
│   │   │   └── validator.py
│   │   ├── services                    # Services
│   │   │   ├── data_fetcher.py
│   │   │   └── loader.py
│   │   ├── storage                     # Gestion du stockage
│   │   │   └── parquet_handler.py
│   │   └── viz                         # Visualisation des données
│   │       ├── data_vizualizer_factory.py
│   │       ├── humidity_vizualizer.py
│   │       ├── pressure_vizualizer.py
│   │       └── temperature_vizualizer.py
│   ├── app.py
│   └── app_init.py
├── README.md
├── requirements.txt
└── run.py                              # Point d'entrée
```

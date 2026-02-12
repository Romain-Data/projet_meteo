# Projet Meteo

**Pitch client**

- une appli pour suivre la météo toulousaine
- possibilité de choisir une station météo pour afficher données spécifiques
- voir un historique semaine

**Contraintes**
- utilisation de données ouvertes
- créer un modèle des classes en respectant les principes Clean Code
- création d'un dashboard **simple**


# Design patterns implémentés
- [x] **Singleton** : [config_loader.py](projet/config/config_loader.py) et [app_init.py](projet/app_init.py)
- [x] **Builder** : [station_builder.py](projet/src/entities/station_builder.py)
- [x] **Factory** : [data_vizualizer_factory.py](projet/src/viz/data_vizualizer_factory.py)
- [x] **Decorator** : [station_display_decorator.py](projet/src/entities/station_display_decorator.py)
- [x] **File** (Queue): [request_queue.py](projet/src/api/request_queue.py)

# Conformité Barême
- [x] **Structures de données** : Liste chaînée (`LinkedListNavigator`), File (`ApiRequestQueue`), Dictionnaire (Configuration JSON).
- [x] **Qualité** : Score PyLint 10/10, Tests unitaires (146 tests, >99% couv).
- [x] **Documentation** : [DATA_PROFILING.md](projet/docs/DATA_PROFILING.md), Docstrings et Type Hinting.
- [x] **Architecture** : Lancement du code via une commande Docker

# Installation et Lancement

```bash
docker compose up
```

# Architecture de fichiers
```text
.
├── projet
│   ├── components                      # Composants UI Streamlit
│   │   ├── metrics_display.py
│   │   ├── navigation_header.py
│   │   └── sidebar.py
│   ├── config                          # Configuration et Singleton
│   │   ├── config.json
│   │   ├── config_loader.py
│   │   └── logging_config.py
│   ├── data                            # Données et Stockage Parquet
│   ├── docs                            # Documentation (Data Profiling)
│   │   └── DATA_PROFILING.md
│   ├── src                             # Core Logic
│   │   ├── api                         # API et File (Queue)
│   │   │   ├── extractor.py
│   │   │   └── request_queue.py
│   │   ├── data_structures             # Liste Chaînée
│   │   │   ├── linked_list_navigator.py
│   │   │   └── linked_list_node.py
│   │   ├── entities                    # Entités, Builder et Decorator
│   │   │   ├── city.py
│   │   │   ├── station.py
│   │   │   ├── station_builder.py
│   │   │   ├── station_display_decorator.py
│   │   │   └── weather_report.py
│   │   ├── interfaces
│   │   ├── processing                  # Transformation et Validation
│   │   ├── services                    # Services (Data Fetcher)
│   │   ├── storage                     # Parquet Handler
│   │   └── viz                         # Factory et Visualisations
│   ├── __init__.py
│   ├── __main__.py                     # Point d'entrée package
│   ├── app.py
│   └── app_init.py
├── tests                               # 146 tests unitaires
├── README.md
├── requirements.txt
├── Dockerfile
└── run.py
```


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
[x] Singleton sur [config_loader.py](projet/config/config_loader.py)
[x] Builder sur [station_buider.py](projet/src/entities/station_builder.py)
[x] Factory sur [data_vizualizer.py](projet/src/viz/data_vizualizer.py)



```text
./
├── components/        # Composants de l'application 
│   
├── data/
│   ├── parquet/        # Données météos sauvegardées
│   └── stations/       # Stations disponibles
│
├── src/
│   ├── api/            # Requête données météo
│   ├── entities/       # Classes métier
│   ├── processing/     # Traitement et transformation des données
│   ├── services/       # Logique métier et services
│   ├── storage/        # Gestion du stockage et persistance
│   └── viz/            # Visualisations et graphiques
│
├── README.md
├── app.py              # Point d'entrée de l'application
└── requirements        # Dépendances Python (pip)
```
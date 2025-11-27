# projet_meteo

Pitch client : société météo

- une appli pour suivre la météo toulousaine
- possibilité de choisir une station météo pour afficher données spécifiques
- voir un historique semaine

**Contraintes**
- utilisation de données ouvertes
- créer un modèle des classes en respectant les principes Clean Code
- création d'un dashboard **simple**

# A faire
[x] Structurer le code python (main, init, sous-dossier)
[ ] Implémenter une liste chaînée pour l'affichage station par station
[ ] Implémenter une file pour les extractions
[x] Implémenter un dictionnaire pour la configuration


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
# Projet Python Avancé, Analyse des Top Joueurs Euro

Ce projet est un projet scolaire pour un Bachelor 3 IA & DATA à Paris Ynov Campus. Il a pour objectif d'analyser les joueurs de football du top Euro en utilisant les données extraites de la page https://www.footmercato.net/joueur/. Les données sont extraites à l'aide de BeautifulSoup et Selenium, puis stockées dans une base de données MongoDB. L'analyse est effectuée à l'aide de Streamlit, qui permet de créer une interface web interactive.

## Installation des dépendances

Assurez-vous d'avoir Python 3.x installé. Clonez ensuite le dépôt et installez les dépendances requises en exécutant les commandes suivantes dans votre terminal :

```bash
git clone https://github.com/raphacarr/Python-avancee
python requirements.py
```

Assurez vous également d'avoir mongoDB qui est activé sur votre machine et modifiez la ligne suivante en fonction de votre mongo : 
```
url = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.2"
```

## Structure du projet

Le projet est constitué de trois fichiers principaux :

1. `scraper.py` : Ce fichier contient le code pour extraire les données des joueurs à l'aide de BeautifulSoup et Selenium, puis les stocker dans une base de données MongoDB.
2. `main.py` : Ce fichier contient le code pour créer l'interface web interactive à l'aide de Streamlit. Il permet d'afficher les données extraites et de générer des graphiques pour analyser les joueurs.
3. `config.py` : Ce fichier contient les informations de configuration pour se connecter à la base de données MongoDB.

## Utilisation

Pour lancer l'application Streamlit, exécutez la commande suivante dans votre terminal :

```bash
streamlit run main.py
```
Une fois l'application lancée, ouvrez votre navigateur et accédez à l'URL indiquée

## Fonctionnalités

L'interface web permet de :

    - Afficher les données des joueurs dans un tableau interactif.
    - Filtrer les données par équipe.
    - Ajouter de nouveaux joueurs à la base de données.
    - Générer différents graphiques pour analyser les joueurs
    
## Licence

Ce projet est sous licence MIT. Pour plus d'informations, veuillez consulter le fichier LICENSE.

# Auteur 
Raphaël CARRILHO @raphacarr

# website_diff
Permet de comparer visuellement une page de deux sites web différents avec un automate de https://fr.wikipedia.org/wiki/Distance_de_Bhattacharyya

# Utilisation

## Récupération du dépôt
On récupère le dépôt avec:
```
git clone git@github.com:epfl-sdf/website_diff.git
```

## Installation des outils nécessaires
Simplement avec la commande:
```
./install.sh
```

Pour préparer les données, il faut lancer:
```
./make_data.py
```

Ceci nécessite la présance d'un fichier `../credentials/credentials.csv`.

## Lancer le vérificateur
Simplement avec la commande:
```
./start.sh
```

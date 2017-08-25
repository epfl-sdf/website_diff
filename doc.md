# website_diff
Permet de comparer visuellement une page de deux sites web différents avec un 
automate de la [distance de Bhattacharyya](https://fr.wikipedia.org/wiki/Distance_de_Bhattacharyya)

# Utilisation

## Récupération du dépôt
On récupère le dépôt avec:
```
git clone git@github.com:epfl-sdf/website_diff.git
```
(cette commande nécessite la présence de `git` sur l'ordinateur)

Pour executer les commandes des sections suivantes, il faut se mettre dans
le dossier du dépôt.

## Installation des outils nécessaires
Simplement avec la commande:
```
./install.sh
```
Pour que cette commande marche, il faut être sous Ubuntu ou une autre
distribution utilisant `apt-get` comme gestionnaire de paquets et qui a les
mêmes noms de packets que sur les dépôts Ubuntu.

Cette commande va créer la structure de dossier nécessaire pour le bon
fonctionnement du code à l'état actuel. Cette structure est la suivante:

```
data_web_diff
└─copy_screen
web_diff
```
Où `web_diff` est le dossier du dépôt.

Ensuite, il faut lancer la commande suivante:
```
./make_data
```

Qui va créer un fichier `sites.csv` qui va contenir les sites a comparer
par le programme. Pour cela, nous avons besoin d'un fichier d'où tirer ces
sites. Dans l'état actuel, il faut avoir un fichier `credentials.csv`
dans la structure de dossier suivante:
```
data_web_diff
└─copy_screen
credentials
└─ credentials.csv
web_diff
```
`credentials.csv` est un fichier au format `.csv` dont les colonnes sont 
séparés par des virgules. Les colonnes nécessaires pour le bon fonctionnement 
du filtre:
* La deuxième colonne est l'URL du premier site de la comparaison
* La troisème colonne est l'URL du deuxième site de la comparaison
* La quatrième colonne doit être le titre du site

Ce fichier sera un fichier `.csv` dont les colonnes sont séparés par des virgules et
elles sont les suivantes:
* `name` qui est le nom du test, obtenu içi à partir du nom du site du
  fichier source
* `url1` le premier URL de la comparaison
* `url2` le deuxième site de la comparaison

## Lancer le programme
Simplement avec la commande:
```
./start.sh
```
Cette commande nécessite la présance du fichier `sites.csv` placé au bon
endroit comme l'explique la section précedante de ce document.

# Expliquation du logiciel

Ce logiciel sert a faire des comparaisons chromatique entre des pages WEB. Pour
cela, il crée un histograme des pixels présents sur la page et il calcule la
distance entre ces deux histogrammes selon la [distance de Bhattacharyya](https://fr.wikipedia.org/wiki/Distance_de_Bhattacharyya).
Le coefficient retournée dans le résultat est plus grand si les sites sont similaires
et plus petit sinon.

Le logiciel utilise selenium pour automatiser un navigateur web (Firefox) pour
charger les pages a comparer et faire 2 copies d'écrans de ces pages a comparer.
Ensuite, la librairie Pillow est utilisé pour charger ces deux images dans le code
et calculer l'histogramme des pixels dans la copie-d'écran. Ensuite, on utilise Numpy
pour effectuer les calculs nécessaires pour la distance de Bhattacharyya.

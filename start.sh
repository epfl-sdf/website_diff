#!/bin/bash

date

virtFold="venv"

if (( $# < 1 ))
then
    echo "Erreur: pas assez d'arguments
    usage: ./start.sh fichier_des_sites"
    exit
fi

credFile=$1

source $virtFold/bin/activate
PATH="$PATH:$(pwd)"
python3 website_diff.py $credFile
deactivate

date


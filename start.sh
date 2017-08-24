#!/bin/bash
# petit script pour démarrer la comparaison visuelle de pages WEB
#170824.1452

#source:



date

pkill firefox
pkill Xvfb
virtFold="venv"
credFile="../data_web_diff/sites.csv"

source $virtFold/bin/activate
PATH="$PATH:$(pwd)"
python3 website_diff.py $credFile
deactivate

date


#!/bin/bash
virtFold="venv"
credFile="../data_web_diff/sites.csv"

source $virtFold/bin/activate
PATH="$PATH:$(pwd)"
python3 website_diff.py $credFile
deactivate


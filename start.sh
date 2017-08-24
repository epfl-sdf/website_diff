#!/bin/bash
pkill firefox
pkill Xvfb
virtFold="venv"
credFile="../credentials/test-credentials.csv"

source $virtFold/bin/activate
PATH="$PATH:$(pwd)"
python3 website_diff.py $credFile
deactivate


#!/bin/bash
virtFold="venv"
credFile="../credentials/credentials.csv"

source $virtFold/bin/activate
PATH="$PATH:$(pwd)"
./website_diff.py $credFile
deactivate


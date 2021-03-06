#!/bin/bash
virtFold="venv"

sudo apt-get update
sudo apt-get install python3-dev python3-pip
sudo apt-get install xvfb
sudo apt-get install firefox
sudo apt install virtualenv

wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
tar xf geckodriver-v0.18.0-linux64.tar.gz

if [ -d $virtFold ];
then
    rm -rf $virtFold    
fi

virtualenv -p /usr/bin/python3 $virtFold
source $virtFold/bin/activate
pip install pillow
pip install numpy 
pip install selenium 
pip install pyvirtualdisplay
deactivate

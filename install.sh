#!/bin/bash
virtFold="venv"
dataFold="../data_web_diff"
screenFold="copy_screen"

sudo apt-get update
sudo apt-get -y install python3-dev python3-pip
sudo apt-get -y install xvfb
sudo apt-get -y install firefox
sudo apt-get -y install virtualenv

wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
tar xf geckodriver-v0.18.0-linux64.tar.gz

if [ -d $virtFold ];
then
    rm -rf $virtFold    
fi

if [ ! -d $dataFold ];
then
    mkdir $dataFold
    mkdir $dataFold/$screenFold
fi

virtualenv -p /usr/bin/python3 $virtFold
source $virtFold/bin/activate
pip install pillow
pip install numpy 
pip install selenium 
pip install pyvirtualdisplay
deactivate

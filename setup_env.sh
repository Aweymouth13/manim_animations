#!/bin/bash

#upgrade pip
python3 -m pip install --upgrade pip

#irrelvant if using ghub codespaces
sudo apt-get install -y git
sudo apt-get update

#ffmpeg install
sudo apt-get install -y ffmpeg

#latex download
sudo apt-get install -y texlive texlive-latex-extra texlive-fonts-recommended dvipng dvisvgm

#cairo for graphics
sudo apt-get install -y libcairo2-dev libgirepository1.0-dev

#need for pangocairo
sudo apt-get install -y libpango1.0-dev

#cmake dependancies 
sudo apt-get install -y software-properties-common

#cmake update
sudo apt-add-repository -y ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y cmake

#libpangocairo
sudo apt-get install -y libpangocairo-1.0-0

#pycairo
pip install pycairo

#clone 3b1b manim
git clone https://github.com/ManimCommunity/manim.git
cd manim

#install dependancies
pip install -r docs/requirements.txt

#editible mode
pip install -e .

#install his old video lib
git clone https://github.com/3b1b/videos.git 3b1bv
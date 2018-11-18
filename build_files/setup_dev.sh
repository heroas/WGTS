#!/bin/bash

#clone repos needed
git clone https://gitlab.com/kivymd/KivyMD

virtualenv -p python3 wgts
#source wgts/bin/activate
wgts/bin/pip install -r WGTS/build_files/requirements.txt
wgts/bin/pip install kivy

cd KivyMD
../wgts/bin/python ./setup.py install

cd ..

cp WGTS/build_files/kivy.py wgts/lib/python3.6/site-packages/async_gui/toolkits/
cp WGTS/build_files/hook-kivymd.py wgts/lib/python3.6/site-packages/PyInstaller/hooks/

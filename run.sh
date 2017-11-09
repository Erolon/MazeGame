#!/bin/bash

pip3 show colorama
if ! [ $? == 0 ]; then
   pip3 install colorama --user
fi


resize -s 30 60
(cd src && exec python3 main.py)

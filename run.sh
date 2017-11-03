#!/bin/sh

pip3 show colorama
if ! [ $? == 0 ]; then
   pip3 install colorama --user
fi

(cd src && exec python3 main.py)

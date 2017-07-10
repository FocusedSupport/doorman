#!/bin/bash

PYTHON=python3
DIR=/home/pi/thedoorman

[ -f /home/pi/.doorman.env ] && . /home/pi/.doorman.env

screen -L -S doorman_screen -d -m $PYTHON $DIR/thedoorman/run.py

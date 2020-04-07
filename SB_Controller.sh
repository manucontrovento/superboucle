#!/bin/bash

# SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
# cd $SCRIPTPATH
# export PYTHONPATH=$(pwd):$PYTHONPATH
# python3 superboucle/boucle.py

# python3 /home/manu/Applicazioni/SuperBoucle-Manu/superboucle/boucle.py &

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
cd $SCRIPTPATH
export PYTHONPATH=$(pwd):$PYTHONPATH
python3 superboucle/boucle.py &
a2jmidid -e &
jack_midi_clock &
carla /home/manu/Produzione/Carla_Sessions/SuperBoucle_AkaiAPCkey25.carxp

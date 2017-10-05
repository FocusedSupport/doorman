#!/bin/bash

DIR=/home/pi/festival/cmu_us_bdl_arctic

cd $DIR

echo "(voice_cmu_us_bdl_arctic_clunits)" > /tmp/festival.scm
echo "(SayText \"$*\")" >> /tmp/festival.scm

festival -b festvox/cmu_us_bdl_arctic_clunits.scm /tmp/festival.scm

rm /tmp/festival.scm

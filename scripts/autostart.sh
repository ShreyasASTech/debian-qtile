#!/bin/bash

lxpolkit &
picom --config ~/.config/picom/picom.conf -b
# killall volumeicon &
# volumeicon &
# nm-applet &
nitrogen --set-zoom-fill /usr/share/backgrounds/garden.jpg --save
xset dpms 600

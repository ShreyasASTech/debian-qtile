#!/bin/bash

lxpolkit &
picom --config ~/.config/picom/picom.conf -b
# killall volumeicon &
# volumeicon &
# nm-applet &
nitrogen --restore &
xset dpms 600

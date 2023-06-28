#!/bin/bash
sed -i "/--set-zoom-fill/ c\nitrogen --restore &" ~/.config/qtile/autostart.sh
sed -i "/wall/ c\\" ~/.config/qtile/config.py
rm ~/wall-set.sh

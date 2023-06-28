#!/bin/bash
sed -i "/nitrogen/ c\nitrogen --restore &" ~/.config/qtile/autostart.sh
sed -i "/wall/ c\\" ~/.config/qtile/config.py
rm ~/wall-set.sh

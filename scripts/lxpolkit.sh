#!/bin/bash

echo ""; echo "Checking whether to install lxpolkit or not..."
if [ "$distroname" == "Antix" ]; then
	echo "Not installing lxpolkit coz it won't work properly in antix..."
	sed -i "/lxpolkit/ c\\" /home/"$username"/.config/i3/config
else
	echo "Installing lxpolkit..."
	sudo apt install lxpolkit -y
fi

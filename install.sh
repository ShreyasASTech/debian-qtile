#!/bin/bash

# Check if script is run as root
if [[ $EUID == 0 ]]; then
  echo "You must NOT be a root user to run this script, please run ./install.sh as a normal user" 2>&1
  exit 1
fi

# Get username, working directory, i3 vsersion, distro name & debian version
username=$(id -u -n 1000)
builddir=$(pwd)
debianversion=$(cat /etc/debian_version) && debianversion=${debianversion%.*}

# Updating system & installing programs
echo ""; echo "Doing a system update & Installing the required programs..."
sudo apt update && sudo apt upgrade -y
sudo apt install fonts-powerline x11-utils x11-xserver-utils curl imagemagick pulseaudio pavucontrol lightdm slick-greeter xfce4-terminal wget nitrogen dmenu xserver-xorg-video-intel xserver-xorg-input-libinput alsa-utils python-is-python3 python3-psutil python3-cairocffi python3-cffi python3-xcffib git picom -y

# Change the current working directory
cd "$builddir" || exit

# Installing qtile
echo ""; echo "Installing Qtile..."
git clone https://github.com/qtile/qtile.git
cd qtile || exit
sudo python setup.py install
cd "$builddir" || exit
rm -r qtile

# Creating necessary directories
echo ""; echo "Making necessary directories..."
mkdir -p /home/"$username"/.config/qtile/
mkdir -p /home/"$username"/.config/picom/
mkdir -p /home/"$username"/Screenshots/
mkdir -p /home/"$username"/.config/screencapture/
sudo mkdir -p /usr/share/backgrounds/

# Copy config files
echo ""; echo "Copying config files..."
cp dotfiles/config.py /home/"$username"/.config/qtile/ # qtile wm customizations
cp scripts/autostart.sh /home/"$username"/.config/qtile/ # Autostart apps
sudo cp qtile.desktop /usr/share/xsessions/ # For qtile to be lauched by lightdm
cp qtile.png /usr/share/slick-greeter/badges/ # For qtile to have an icon in slick-greeter login page
cp dotfiles/picom.conf /home/"$username"/.config/picom/ # Picom Compositor config file
cp scripts/screenshooter.sh /home/"$username"/.config/screencapture/ # script to take screenshots
sed -i "s/user-name/""$username""/g" /home/"$username"/.config/qtile/config.py

# i3 tweaks
. ./scripts/reboot-poweroff.sh # For configuring reboot-poweroff commands in i3 config
. ./scripts/j4-i3scripts.sh # Installing j4-dmenu-desktop and dependencies of i3scripts

# Done
echo "Installation is now complete. Reboot your system for the changes to take place.
Remember, upon reboot no wallpaper will be set. Use the app Nitrogen > Preferences to set a wallpaper."

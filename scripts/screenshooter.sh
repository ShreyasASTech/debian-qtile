#!/bin/bash
import ~/Screenshots/screen.png
timestamp=$(date +"_%d_%m_%y_%H_%M_%S")
mv ~/Screenshots/screen.png ~/Screenshots/screen"$timestamp".png

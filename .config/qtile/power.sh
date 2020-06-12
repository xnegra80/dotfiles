#!/bin/bash

# Simple script to handle a DIY shutdown menu. When run you should see a bunch of options (shutdown, reboot etc.)
#
# Requirements:
# - rofi
# - systemd, but you can replace the commands for OpenRC or anything else
#
# Instructions:
# - Save this file as power.sh or anything
# - Give it exec priviledge, or chmod +x /path/to/power.sh
# - Run it

chosen=$(echo -e "Lock\nLogout\nShutdown\nReboot\nSuspend" | rofi -dmenu -i)
# Info about some states are available here:
# https://www.freedesktop.org/software/systemd/man/systemd-sleep.conf.html#Description

if [[ $chosen = "Logout" ]]; then
  qtile-cmd -o cmd -f shutdown
elif [[ $chosen = "Lock" ]]; then
  xset dpms force off
elif [[ $chosen = "Shutdown" ]]; then
  systemctl poweroff
elif [[ $chosen = "Reboot" ]]; then
  sudo reboot now
elif [[ $chosen = "Suspend" ]]; then
  systemctl suspend
fi

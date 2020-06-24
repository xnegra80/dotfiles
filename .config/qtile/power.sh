#!/bin/bash

chosen=$(echo -e "Lock\nLogout\nShutdown\nReboot\nSuspend" | rofi -dmenu -p 'Power Menu' -i)

if [[ $chosen = "Logout" ]]; then
  qtile-cmd -o cmd -f shutdown
elif [[ $chosen = "Lock" ]]; then
  xset dpms force suspend; slock
elif [[ $chosen = "Shutdown" ]]; then
  systemctl poweroff
elif [[ $chosen = "Reboot" ]]; then
  sudo reboot now
elif [[ $chosen = "Suspend" ]]; then
  systemctl suspend
fi

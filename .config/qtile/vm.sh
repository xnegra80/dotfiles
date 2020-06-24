#!/bin/bash

chosen=$(echo -e "Connect\nSuspend" | rofi -dmenu -p 'Windows 10 VM' -i)

if [[ $chosen = "Connect" ]]; then
  virsh start win10
  virt-viewer --domain-name win10
  notify-send 'Windows 10 VM connected'
elif [[ $chosen = "Suspend" ]]; then
  virsh managedsave win10
  notify-send 'Windows 10 VM suspended'
fi
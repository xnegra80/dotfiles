#!/bin/bash

power_on() {
    if bluetoothctl show | grep -q "Powered: yes"; then
        return 0
    else
        return 1
    fi
}

if power_on; then
  devices=$(bluetoothctl info | grep Name: | sed 1q | awk '{$1 = ""; print $0}'| paste -sd "," -)
  echo "${devices}"
else
  echo "No devices"
fi

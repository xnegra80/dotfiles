#! /bin/bash
picom -b &
feh --bg-fill ~/Pictures/wallpaper.jpg &
killall blueman-applet &
blueman-applet &
xss-lock -- i3lock -n -i ~/Pictures/wallpaper.jpg &
dunst &

#! /bin/bash

picom --experimental-backends --backend glx&
feh --bg-fill ~/Pictures/wallpaper.png&
dunst&
ferdi&
evolution&
fusuma -d&
fcitx5&
discord --start-minimized&
~/.config/scripts/wait.sh&
/usr/bin/lxpolkit&
sudo tzupdate&
redshift -l geoclue2&
emacs --daemon&
echo "enabled" > ~/.keyboard&

#!/bin/sh

B='#00000000'  # blank
C='#ffffff22'  # clear ish
D='#bd93f9'  # default
T='#f8f8f2'  # text
W='#ff79c6'  # wrong
V='#50fa7b'  # verifying

i3lock -e \
--insidevercolor=$C   \
--ringvercolor=$V     \
\
--insidewrongcolor=$C \
--ringwrongcolor=$W   \
\
--insidecolor=$B      \
--ringcolor=$D        \
--linecolor=$B        \
--separatorcolor=$D   \
\
--verifcolor=$T        \
--wrongcolor=$T        \
--timecolor=$T        \
--datecolor=$T        \
--layoutcolor=$T      \
--keyhlcolor=$W       \
--bshlcolor=$W        \
\
--blur 5              \
--clock               \
--indicator           \
--timestr="%l:%M %P"  \
--datestr="%b %d %a" \

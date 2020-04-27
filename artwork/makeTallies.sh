#!/bin/bash

if [ ! -d "img" ]; then mkdir img; fi

F1="./tally/tally.ttf"

for glyph in 1 2 3 4 5 51 52 53 54 55 551 552 553 554 555; do
ix=0
for color in black; do
file="tally_${glyph}_${color}".png
convert -background none \
    -fill $color \
    -stroke none \
    -strokewidth 0 \
    -font "$F1" \
    -pointsize 96 \
    label:"$glyph" \
    -trim \
    "$file"
    
#mogrify -background none -gravity center -resize x100  img/"$file"
ix=$(($ix+1))
done
done

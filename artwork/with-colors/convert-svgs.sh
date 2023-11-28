#!/bin/bash
set -e
cd "$(dirname "$0")" || exit 1

export OMP_NUM_THREADS=4

cwd="$(pwd)"

echo "Creating pngs"
if [ -d "pngs" ]; then rm -rf "pngs"; fi
mkdir "pngs"
for svg in *.svg; do
  if [ ! -f "$svg" ]; then continue; fi
  png="$(echo "$svg" | sed 's/.svg$/.png/')"
  if [ -f "pngs/$png" ]; then rm "pngs/$png"; fi
  inkscape -o "pngs/${png}" -C --export-background=white --export-background-opacity=1.0 \
    --export-png-color-mode=RGB_16 --export-area-page "${svg}"
done

echo "Creating jpgs"
if [ -d "jpgs" ]; then rm -rf "jpgs"; fi
mkdir "jpgs"
p=0
for png in pngs/*.png; do
  if [ ! -f "$png" ]; then continue; fi
  p=$(($p + 1))
  jpg="$(basename "$png" | sed 's/.png$/.jpg/')"
  gm convert -background white -flatten $T -quality 90 "$png" "jpgs/$jpg"
done

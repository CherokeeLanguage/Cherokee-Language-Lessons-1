#!/bin/bash
set -e

trap "echo; echo ERROR; read a; exit -1" ERR

cd "$(dirname "$0")" || exit 1

export OMP_NUM_THREADS=4

bksize="1325x2050" #200dpi: 6.625x10.25
pgsize="2650x4100" #400dpi: 6.625x10.25
kindlesize="1600x2560"

echo "Creating pngs"
for svg in src.svg/*.svg; do
	png="$(echo "$svg"|sed 's/.svg$/.png/')"
	rm "$png" 2> /dev/null || true
done
for svg in src.svg/*.svg; do
	png="$(echo "$svg"|sed 's/.svg$/.png/')"
	inkscape -z -b=white -y=1.0 -e "${png}" -d 600 --export-area-page "${svg}"
	mv "${png}" "${png}.tmp"
	gm convert "${png}.tmp" -background white -flatten "${png}"
	rm "${png}.tmp"
done

if [ -d "pages.jpg" ]; then rm -rf "pages.jpg"; fi
mkdir "pages.jpg"
if [ -d "pages.jpg.lq" ]; then rm -rf "pages.jpg.lq"; fi
mkdir "pages.jpg.lq"

echo "Creating jpgs"
p=0
for png in src.svg/p*.png; do
	T="-trim"
	if [ "$p" = 0 ]; then
		unset T
	fi
	if [ ! -f "$png" ]; then continue; fi
	p=$(($p + 1))
	page="$(printf "%03d.jpg" $p)"
	gm convert -background white -flatten $T -quality 70 "$png" "pages.jpg"/"$page"
done

echo "Creating low quality jpgs"
for jpg in pages.jpg/*; do
	jpg2="pages.jpg.lq"/"$(basename "$jpg")"
	gm convert "$jpg" -resize 50% -quality 30 "$jpg2"
done

echo -n "Done"
sleep 1


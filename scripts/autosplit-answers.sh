#!/bin/bash

set -e
set -o pipefail

function die(){
	echo "ERROR!"
	echo "$0"
	echo "$1"
	echo "$2"
	echo "$3"
	read a
	exit -1
}
trap die ERR

if [ "$1"x = ""x ];then
	die "missing arg!"
fi

BaseName="$1"
Source="${BaseName}.pdf"

cd "$(dirname "$0")" || exit 1

pdftotext -r 300 -layout -nopgbrk -enc "UTF-8" "$Source"

export T="$(mktemp -d -t pdfsam-XXXXXXXXX)" # "/tmp/pdfsam-$$"
mkdir -p "$T"

#split PDF up into parts that should maintain UNICODE properly instead of doing it via print to pdf
#unfortunately the PDF's generated each time always have different md5sums ?
#work around is to convert PDF's into text, then md5sum the resulting text,
# this way we only do changed PDF's each time

pdfsam-console -bl 1 -f "$Source" -o "$T" -overwrite -p split_ -s BLEVEL split

c=0
ls -1tr "$T"/*split*.pdf | while read x; do
	d="$(printf "%02d" "$c")"
	TL=../$d
	DEST=../$d/"$BaseName-"$d.pdf
	TEXT=../$d/"$BaseName-"$d.txt
	mkdir -p ../"$d"/
	H1="$(pdftotext -raw -enc "UTF-8" "$x" - | md5sum)"
	H2=x
	if [ -f "$DEST" ]; then
		H2="$(pdftotext -raw -enc "UTF-8" "$DEST" - | md5sum)"
	fi
	if [ "$H1" != "$H2" ]; then
		rm "$DEST" 2> /dev/null || true
		cp -v "$x" "$DEST"
		if [ -f "$TEXT" ]; then mv "$TEXT" "$TEXT".prev; fi
		pdftotext -r 300 -layout -nopgbrk -enc "UTF-8" "$DEST"
		diff -t -N -E -Z -b -B -u "$TEXT".prev "$TEXT" > "$TEXT".diff || true
	fi
	rm "$x"
	touch --reference="$DEST" "$TL"
	c=$(($c+1))
	echo "$c" > count.txt
done

#remove any extra found
x="$(cat count.txt)"
for c in $(seq $x 99); do
	if [ "$c" -lt "$x" ]; then continue; fi
	d="$(printf "%02d" "$c")"
	TL=../$d
	if [ -d "$TL" ]; then rm -rfv "$TL"; fi
done

rm -rfv "$T"


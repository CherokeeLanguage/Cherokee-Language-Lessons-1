#!/bin/bash
set -e
set -o pipefail

exit 0

for p in $(seq 17 24); do
	dest="p0${p}.svg";
	cp "p045.svg" "$dest";
	sed -i "s/__dest__/p0${p}.png/g" "$dest";
	sed -i "s/__picture__/0${p}.png/g" "$dest";
done

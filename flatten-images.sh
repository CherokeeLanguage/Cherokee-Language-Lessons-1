#!/bin/bash

set -e
set -o pipefail

cd "$(dirname "$0")"

grep "\.jpg" "Cherokee Language Lessons-Volume I.lyx"|sed 's/.*filename //'|while read jpg; do
	echo "$jpg"
	png="$(echo "$jpg"|sed 's/.jpg$/.png/')"
	if [ ! -f "$png" ] || [ "$jpg" -nt "$png" ]; then
		printf "\t(skipped)\n"
		continue;
	fi
	printf "\t(recreating jpg from png)\n"
	gm convert "${png}" -background white -flatten "${jpg}"
done

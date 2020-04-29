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

wrkFile="Cherokee Language Lessons-Volume 1"
lyxFile="${wrkFile}.lyx"
lyxWithCoverFile="${wrkFile}-embedded-cover.lyx"
cd "$(dirname "$0")" || exit 1
DEST="/home/muksihs/Sync/Cherokee/CherokeeLanguageLessons/Volume-01-3rd-edition/MASTER/"
mkdir -p "$DEST"
cp scripts/autosplit-answers.sh "$DEST"

lyx -e pdf4 "$lyxFile" -e pdf4 "$lyxFile"
lyx -e pdf4 "$lyxWithCoverFile" -e pdf4 "$lyxWithCoverFile"

cp "$wrkFile".pdf "$DEST"
cp "$wrkFile"-embedded-cover.pdf "$DEST"

cd "$DEST"
bash autosplit-answers.sh "$wrkFile" || exit 0

cd ..
xdg-open "$(pwd)" &

sleep 1


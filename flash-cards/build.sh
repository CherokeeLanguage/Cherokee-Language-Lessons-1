#!/bin/bash
FLD="cll1-flashcards"

set -e
set -o pipefail

trap 'echo; echo ERROR; echo; read a;' ERR

#run from the dir I am stored in
cd "$(dirname "$0")" 

rm -rfv "$FLD" || true
mkdir "$FLD" || true

#uses xelatex from the "texlive" (mostly unicode compliant) latex distribution
for x in *tex; do
	xelatex "$x" 
	rm *.aux
	rm *.log
	PDF="$(echo "$x"|sed 's/.tex$/.pdf/')"
	mv -v "$PDF" "$FLD"/.
done

zip "$FLD".zip -r "$FLD"/


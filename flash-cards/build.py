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

cp -v "$FLD".zip "../docs/Flash Cards/."

rm -v "../docs/Flash Cards/"*.pdf

dest_dir="../docs/Flash Cards"
md="$dest_dir/index.md"
(
  echo "# Flash Cards"
  echo
  echo "## ZIP Archive"
  echo
  echo "* Zip of all flashcards: [${FLD}.zip](${FLD}.zip)."
  echo
  echo "## Individual PDFs"
  echo

  for pdf in "$FLD"/*.pdf; do
    cp "$pdf" "$dest_dir"
    pdf_name=$(basename "$pdf")
    echo "* [$pdf_name]($pdf_name)"
  done
  echo
) > "$md"

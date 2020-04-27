#!/bin/bash

cd "$(dirname "$0")"
set -e
set -o pipefail
trap 'echo error; read a' ERR

FILE="Cherokee Language Lessons-Volume I"

cp "$FILE".tex "$FILE".tex.tmp
perl -p -i -e 's/\\uline\{/\\emph\{/g' "$FILE".tex.tmp
perl -p -i -e 's/\\label\{[^}]*?\}//g' "$FILE".tex.tmp
perl -p -i -e 's/\\begin\{multicols\}.*$//g' "$FILE".tex.tmp
perl -p -i -e 's/\\end\{multicols\}//g' "$FILE".tex.tmp
pandoc -o "$FILE".md --to=commonmark --from=latex "$FILE".tex.tmp
rm "$FILE".tex.tmp

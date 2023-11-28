#!/bin/bash

cd "$(dirname "$0")" || exit 1

unzip "${EPUB}".epub '*.jpg' -d "tmp.$$"

for x in "tmp.$$"/*/Images/*.jpg; do
	echo "$x"
	gm mogrify -quality 30 "$x"
done

cd "tmp.$$"
zip -9 -r  ../"${EPUB}".epub . -i "*.jpg"
zip -9 -r  ../"${EPUB}"-Kindle.epub . -i "*.jpg"
cd ..

rm -rfv "tmp.$$"

echo "DONE $(basename "$0") ... "



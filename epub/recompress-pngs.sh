#!/bin/bash

cd "$(dirname "$0")" || exit 1

unzip "${EPUB}".epub '*.png' -d "tmp.$$"

for x in "tmp.$$"/*/Images/*.png; do
	pngcrush "$x" "$x".tmp
	mv "$x".tmp "$x"
done

cd "tmp.$$"
zip -9 -r  ../"${EPUB}".epub . -i "*.png"
zip -9 -r  ../"${EPUB}"-Kindle.epub . -i "*.png"
cd ..

rm -rfv "tmp.$$"

echo "DONE $(basename "$0") ... "



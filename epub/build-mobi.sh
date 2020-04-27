#!/bin/bash

cd "$(dirname "$0")" || exit

if [ ! -f "${EPUB}"-Kindle.epub ]; then exit 0; fi

./bin/kindlegen_linux_2.6_i386_v2_9/kindlegen -dont_append_source -c0 -o "${EPUB}"-Kindle.mobi "${EPUB}"-Kindle.epub

rm "/home/mjoyner/Sync/Nook/${EPUB}"-Kindle.mobi
cp "${EPUB}"-Kindle.mobi "/home/mjoyner/Sync/Nook/."

echo "DONE $(basename "$0")"

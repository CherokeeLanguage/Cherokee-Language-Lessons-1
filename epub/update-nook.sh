#!/bin/bash

cd "$(dirname "$0")"||exit 1

if [ -d "/media/mjoyner/nook/my documents" ]; then
	rm -v "/media/mjoyner/nook/my documents/${EPUB}.epub"
	sync
	cp -v "${EPUB}.epub" "/media/mjoyner/nook/my documents/."
	sync
fi
echo "DONE $(basename "$0") ... "

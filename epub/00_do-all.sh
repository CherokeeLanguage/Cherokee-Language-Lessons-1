#!/bin/bash

set -e

cd "$(dirname "$0")"

for F in *.epub; do
	if [[ "$F" == *Kindle.epub ]]; then continue; fi
	export EPUB="$(basename "$F"|sed 's/.epub$//')"
	bash recompress-jpgs.sh
	bash recompress-pngs.sh
	#bash build-mobi.sh
	bash update-nook.sh
	bash copy-sync.sh
	break
done

echo -n "DONE $(basename "$0"): "
sleep 1

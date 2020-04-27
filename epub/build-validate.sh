#!/bin/bash

F="raven-dictionary"

cd "$(dirname "$0")" || exit 1

./bin/epubcheck-3.0.1/epubcheck-3.0.1.jar "$F"-Kindle.epub
./bin/epubcheck-3.0.1/epubcheck-3.0.1.jar "$F".epub

echo "DONE $(basename "$0") ... sleeping"
sleep 10

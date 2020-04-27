#!/bin/bash

set -e
set -o pipefail

cp /dev/null files.txt
echo -n 0 > counter.txt

find . -name '*.svg' | grep -v _backup.svg | while read f; do
	g="$(echo "$f"| sed 's/.svg/_backup.svg/g')"
   	if [ ! -f "$g" ]; then
   		c="$(cat counter.txt)"
		echo "$c: $f";
		inkscape "$f" --verb=FileSave --verb=FileQuit &
		echo -n "$(($c+1))" > counter.txt
       	if [ $c -gt 5 ]; then echo "==="; echo -n 0 > counter.txt; wait; fi
   	fi
done

echo "OK"

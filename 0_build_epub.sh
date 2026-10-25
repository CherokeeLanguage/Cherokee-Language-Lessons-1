#!/bin/bash

trap 'echo ERROR; read a' ERR
set -e
set -o pipefail

cd "$(dirname "$0")" || exit 1

Z="$(pwd)";
cd "${HOME}/git/Lyx2ePub/Lyx2ePub"
./gradlew clean build fatjar
cd "$Z"
lyx2epub="${HOME}/git/Lyx2ePub/Lyx2ePub/build/libs/lyx2epub.jar"
java -jar "${lyx2epub}"  --settings epub/settings.json
if [ $? != 0 ]; then
	echo "ERROR."
	read a;
	exit 1
fi

cd epub

bash 00_do-all.sh

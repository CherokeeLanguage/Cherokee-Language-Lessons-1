#!/bin/bash

set -e

cd "$(dirname "$0")"

DEST="/home/muksihs/Sync/Cherokee/CherokeeReferenceMaterial/ᎹᎦᎵ-MISC"
if [ ! -d "${DEST}" ]; then mkdir -p "${DEST}"; fi
cp *.epub "${DEST}"/.
cp *.mobi "${DEST}"/.

#!/bin/bash

OUTDIR="$HOME/Desktop/images"
if [ -n "$1" ]; then
  FILEPATH="$1"
else
  TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
  FILEPATH="$OUTDIR/snapshot_$TIMESTAMP.jpg"
fi

mkdir -p "$OUTDIR"

rpicam-still \
--awb custom \
--awbgains 1,1 \
-t 1 \
-o "$FILEPATH"

echo "$FILEPATH"

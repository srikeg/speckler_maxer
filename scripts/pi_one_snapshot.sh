#!/bin/bash

OUTDIR="$HOME/Desktop/images"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILEPATH="$OUTDIR/snapshot_$TIMESTAMP.jpg"

mkdir -p "$OUTDIR"

rpicam-still \
--awb custom \
--awbgains 1,1 \
-t 1 \
-o "$FILEPATH"

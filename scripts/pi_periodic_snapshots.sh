#!/bin/bash
# Capture 100 raw full-scale photos at 2‑second intervals and save them on the Desktop (snapshots folder)

# Ensure output directory on Desktop exists
mkdir -p "$HOME/Desktop/test pics"

rpicam-still \
--awb custom \
--roi 0.1,0.1,0.5,0.5 \
--width 256 \
--height 256 \
--awbgains 1,1 \
--timelapse 2000 \
-t 20000 \
-o "$HOME/Desktop/test pics/r4%03d.jpg"

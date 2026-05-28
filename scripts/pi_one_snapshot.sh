#!/bin/bash
# Take one raw full-scale snapshot without opening the GUI and save it on the Desktop (snapshots folder)

# Ensure output directory on Desktop exists
mkdir -p "$HOME/Desktop/test2"


rpicam-still \
--awb custom \
--roi 0.1,0.1,0.5,0.5 \
--width 256 \
--height 256 \
--awbgains 1,1 \
-t 1 \
-o "$HOME/Desktop/test2/test.jpg"
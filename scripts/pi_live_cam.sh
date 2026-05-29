#!/bin/bash
# See live recording of Raspberry Pi camera with a GUI at raw full-scale resolution

rpicam-still \
--roi 0.1,0.1,0.5,0.5 \
--width 256 \
--height 256 \
--awb custom \
--awbgains 1,1 \
-t 1000000000000

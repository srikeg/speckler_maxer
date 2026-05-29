#!/bin/bash
# See live recording of Raspberry Pi camera with a GUI at raw full-scale resolution

rpicam-still \
--awb custom \
--awbgains 1,1 \
-t 1000000000000

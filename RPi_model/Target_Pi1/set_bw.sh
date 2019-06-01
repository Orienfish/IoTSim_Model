#!/bin/bash
# Run bw power test
# Usage: sudo bash set_bw.sh 100 # 100kbps 
bw=$1

/home/pi/wondershaper/wondershaper -c -a wlan0
/home/pi/wondershaper/wondershaper -a wlan0 -u $bw -d $bw
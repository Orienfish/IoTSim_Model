#!/bin/bash
# Start perf measurement and start sending random data with iperf
# bw needs to be pre-set, and the info is included in $version
# Usage: bash ./run_test.sh 100k
version=$1

time=$(date +%H%M%S%m%d%Y)
file="./bw_measure/$version"
file+="_$time.txt"

bash ./get_cpu_usage.sh 0 > $file &
iperf -c 192.168.1.60 -t 30 # 30secs

pid=$(ps aux | grep get_cpu_usage | grep -v grep | awk '{print $2}')
kill -9 $pid
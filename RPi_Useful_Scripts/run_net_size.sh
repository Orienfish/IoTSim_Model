#!/bin/bash
# Start perf measurement and start sending diff data size with iperf
# The 1st coefficient is the size in bytes to send
# Usage: bash ./run_test.sh 100
len=$1

end=$((SECONDS+10))
file="/home/pi/Desktop/Target_Pi1/size_measure/perf_120_$len.txt"
bash /home/pi/Desktop/Target_Pi1/get_cpu_usage.sh 0 > $file &
sleep 3
iperf -c 192.168.1.60 -l $len -n 1 # send size bytes


while [ $SECONDS -lt $end ]; do
sleep 2
done

pid=$(ps aux | grep get_cpu_usage | grep -v grep | awk '{print $2}')
kill -9 $pid
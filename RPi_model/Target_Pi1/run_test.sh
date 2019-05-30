#!/bin/bash
# Start perf measurement and run the local workload
# Frequency needs to be pre-set, and the info is included in $version
# Usage: bash ./run_test.sh cpu_600
version=$1
time=$(date +%H%M%S%m%d%Y)
file="./cpu_measure/$version"
file+="_$time.txt"

bash ./get_cpu_usage.sh 0 > $file &
sleep 10 # idle test time
cd ./Raspberry_Pi_Benchmarks && bash ./run.sh

pid=$(ps aux | grep get_cpu_usage | grep -v grep | awk '{print $2}')
kill -9 $pid

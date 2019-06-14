#!/bin/bash
# Start perf measurement and run the local workload
# Frequency needs to be pre-set, and the info is included in $version
# Usage: bash ./run_test.sh cpu_600
version=$1

end=$((SECONDS+150))
file="./cpu_measure/$version.txt"

bash perf_script.sh > $file &
sleep 10 # idle test time
cd ./Raspberry_Pi_Benchmarks && bash ./run.sh
bash ./run.sh
while [ $SECONDS -lt $end ]; do
sleep 5
done

killall -9 bash

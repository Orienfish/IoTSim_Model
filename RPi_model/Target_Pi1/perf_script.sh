sudo perf stat -a -I 200 -x, -e instructions,cache-misses sleep infinity 2>&1
# redirect stderr to stdout

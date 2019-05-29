sudo perf stat -a -I 200 -x, -e instructions,cache-misses sleep infinity 2>&1
# sudo perf stat -a -I 200 -x, -e instructions,cache-misses,L1-dcache-loads,L1-dcache-stores,\
# branch-instructions,branch-misses,cache-references,cpu-cycles,r110,r13C,r1A2,r1C2 sleep infinity 2>&1
# redirect stderr to stdout

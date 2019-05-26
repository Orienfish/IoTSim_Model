#!/bin/bash
# A script to run all the benchmarks
# realease all the permission
find . -type f -exec chmod 777 {} \;
find . -type d -exec chmod 777 {} \;

# Dhrystone - single thread
bash -c "cd dhry && ./dhrystonePiA7 6" # default run secs
# Dhrystone - multi thread
bash -c "cd mpdhry && ./MP-DHRY"
bash -c "cd mpdhry && ./MP-DHRYPiA7"

# Whetstone - single thread
bash -c "cd whet && ./whetstonePiA7 1" # default loop cnt
# Whetstone - multi thread
bash -c "cd mpwhets && ./MP-WHETS"
bash -c "cd mpwhets && ./MP-WHETSPiA7"

# Linpack
bash -c "cd linpack && ./linpackPiA7 1" # default run secs

# MP-MFLOPS
bash -c "cd mpmflops && ./MP-MFLOPS"
bash -c "cd mpmflops && ./MP-MFLOPSPiA7"
bash -c "cd mpmflops && ./MP-MFLOPSDP"
bash -c "cd mpmflops && ./MP-MFLOPSPiNeon"
#!/bin/bash
# A script to compile all the benchmarks

# Dhrystone - single thread
bash -c "cd dhry && \
gcc dhry_1.c dhry_2.c cpuidc.c -lm -lrt -O3 -mcpu=cortex-a7 -o dhrystonePiA7"
# Dhrystone - multi thread
bash -c "cd mpdhry && \
gcc mpdhry.c dhry22.c cpuidc.c -lrt -lc -lm -O3 -lpthread -o MP-DHRY"
bash -c "cd mpdhry && \
gcc mpdhry.c dhry22.c cpuidc.c -lrt -lc -lm -O3 -mcpu=cortex-a7 -mfloat-abi=hard -mfpu=neon-vfpv4 -lpthread -o MP-DHRYPiA7"

# Whetstone - single thread
bash -c "cd whet && \
gcc  whets.c cpuidc.c -lm -lrt -O3 -mcpu=cortex-a7 -mfloat-abi=hard -mfpu=neon-vfpv4 -o whetstonePiA7"
# Whetstone - multi thread
bash -c "cd mpwhets && \
gcc mpwhets.c cpuidc.c -lrt -lc -lm -O3 -lpthread -o MP-WHETS"
bash -c "cd mpwhets && \
gcc mpwhets.c cpuidc.c -lrt -lc -lm -O3 -mcpu=cortex-a7 -mfloat-abi=hard -mfpu=neon-vfpv4 -funsafe-math-optimizations -lpthread -o MP-WHETSPiA7"

# Linpack
bash -c "cd linpack && \
gcc  linpack.c cpuidc.c -lm -lrt -O3 -mcpu=cortex-a7 -mfloat-abi=hard -mfpu=neon-vfpv4 -o linpackPiA7 " 

# MP-MFLOPS
bash -c "cd mpmflops && \
gcc  mpmflops.c cpuidc.c -lrt -lc -lm -O3 -lpthread -o MP-MFLOPS"
bash -c "cd mpmflops && \
gcc mpmflops.c cpuidc.c -lrt -lc -lm -O3 -mcpu=cortex-a7 -mfloat-abi=hard -mfpu=neon-vfpv4 -lpthread -o MP-MFLOPSPiA7"
bash -c "cd mpmflops && \
gcc mpmflopsdp.c cpuidc.c -lrt -lc -lm -O3 -mcpu=cortex-a7 -mfloat-abi=hard -mfpu=neon-vfpv4 -funsafe-math-optimizations -lpthread -o MP-MFLOPSDP "
bash -c "cd mpmflops && \
gcc mpmflops.c cpuidc.c -lrt -lc -lm -O3 -mcpu=cortex-a7 -mfloat-abi=hard -mfpu=neon-vfpv4 -funsafe-math-optimizations -lpthread -o MP-MFLOPSPiNeon"

The benchmarks were compiled using a Raspberry Pi Terminal command such as:

cc  mpmflops.c cpuidc.c -lrt -lc -lm -O3 -o MP-MFLOPS

Additional parameters were used for gcc 4.8 and Raspberry Pi 2 - see below.
The commands are provided at the start of each C source code. 

Execute using a Terminal command, for example, ./MP-MFLOPS
Results are displayed and saved in text log files - see Example Logs
in benchmark folders.

ARM-Intel folder contains executables to run on Intel CPUs via
Linux and are compiled from the same source codes. 

For details and example results on ARM and Intel processors see 
http://www.roylongbottom.org.uk/Raspberry Pi Multithreading Benchmarks.htm


NOTE - After unzipping, the benchmark execution file Properties,
Permissions needs a “Make the file executable” selection.   

New PiA7 versions are included to use Raspberry Pi 2 additional features. 
Example compilation command is:

gcc mpmflops.c cpuidc.c -lrt -lc -lm -O3 -mcpu=cortex-a7 -mfloat-abi=hard 
-mfpu=neon-vfpv4 -lpthread -o MP-MFLOPSPiA7. 

A second version MP-MFLOPSPiNeon uses the additional -funsafe-math-optimizations
parameter to force compilation of NEON instructions. MP-NeonMFLOPS carries 
out the same calculations using NEON intrinsic functions.


A second version of MP BusSpeed is included that avoids using RPi 2 
shared L2 cache, that previously lead to exaggerated performance.

linpackNeonMP is a demonstration of what not to use to demonstrate MP 
performance.

Benchmarks compiled to use OpenMP are now included. See Raspberry Pi 
Multithreading Benchmarks.htm.
   
Folder openmpmemspd new versions OpenMP-MemSpeed2, NotOpenMP-MemSpeed2

Folder mpmflops Doublr Precision version included MP-MFLOPSDP. Includes
assembly listing for 32 Ops/Word

Roy Longbottom
September 2016
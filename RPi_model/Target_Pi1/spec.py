# to run spec
def gen_spec_cpu2006(spec_benchname):
    return BenchInfo(
            bclass="spec_cpu2006",
            runpath=BENCHDIR_MAGIC + "/spec_cpu2006",
            envfile="./shrc",
            program_cmd="./bin/runspec --config yeseong_gcc48.cfg " \
                    "--iterations 1 --nobuild --noreportable " \
                    "--action onlyrun " + \
                    spec_benchname)

BENCHMARK_DICT["400_native.perlbench"] = gen_spec_cpu2006("400.perlbench")
BENCHMARK_DICT["401_native.bzip2"] = gen_spec_cpu2006("401.bzip2")
BENCHMARK_DICT["403_native.gcc"] = gen_spec_cpu2006("403.gcc")
BENCHMARK_DICT["429_native.mcf"] = gen_spec_cpu2006("429.mcf")
BENCHMARK_DICT["445_native.gobmk"] = gen_spec_cpu2006("445.gobmk")
BENCHMARK_DICT["456_native.hmmer"] = gen_spec_cpu2006("456.hmmer")
BENCHMARK_DICT["458_native.sjeng"] = gen_spec_cpu2006("458.sjeng")
BENCHMARK_DICT["462_native.libquantum"] = gen_spec_cpu2006("462.libquantum")
BENCHMARK_DICT["464_native.h264ref"] = gen_spec_cpu2006("464.h264ref")
BENCHMARK_DICT["471_native.omnetpp"] = gen_spec_cpu2006("471.omnetpp")
BENCHMARK_DICT["473_native.astar"] = gen_spec_cpu2006("473.astar")
BENCHMARK_DICT["483_native.xalancbmk"] = gen_spec_cpu2006("483.xalancbmk")
#BENCHMARK_DICT["999_native.specrand"] = gen_spec_cpu2006("999.specrand")
BENCHMARK_DICT["410_native.bwaves"] = gen_spec_cpu2006("410.bwaves")
BENCHMARK_DICT["416_native.gamess"] = gen_spec_cpu2006("416.gamess")
BENCHMARK_DICT["433_native.milc"] = gen_spec_cpu2006("433.milc")
BENCHMARK_DICT["434_native.zeusmp"] = gen_spec_cpu2006("434.zeusmp")
BENCHMARK_DICT["435_native.gromacs"] = gen_spec_cpu2006("435.gromacs")
BENCHMARK_DICT["436_native.cactusADM"] = gen_spec_cpu2006("436.cactusADM")
BENCHMARK_DICT["437_native.leslie3d"] = gen_spec_cpu2006("437.leslie3d")
BENCHMARK_DICT["444_native.namd"] = gen_spec_cpu2006("444.namd")
BENCHMARK_DICT["447_native.dealII"] = gen_spec_cpu2006("447.dealII")
BENCHMARK_DICT["450_native.soplex"] = gen_spec_cpu2006("450.soplex")
BENCHMARK_DICT["453_native.povray"] = gen_spec_cpu2006("453.povray")
BENCHMARK_DICT["454_native.calculix"] = gen_spec_cpu2006("454.calculix")
BENCHMARK_DICT["459_native.GemsFDTD"] = gen_spec_cpu2006("459.GemsFDTD")
BENCHMARK_DICT["465_native.tonto"] = gen_spec_cpu2006("465.tonto")
BENCHMARK_DICT["470_native.lbm"] = gen_spec_cpu2006("470.lbm")
BENCHMARK_DICT["481_native.wrf"] = gen_spec_cpu2006("481.wrf")
BENCHMARK_DICT["482_native.sphinx3"] = gen_spec_cpu2006("482.sphinx3")
#BENCHMARK_DICT["998_native.specrand"] = gen_spec_cpu2006("998.specrand")
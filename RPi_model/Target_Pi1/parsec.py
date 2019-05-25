# To run gen_parsec
def gen_parsec(benchname):
    return BenchInfo(
            bclass="parsec3_docker",
            docker_container="bm_parsec3",
            program_cmd="bash -c \"cd /root/parsec-3.0/; source env.sh; " \
                    "parsecmgmt -l -a run -i native -p " + \
                    benchname + "\"")

BENCHMARK_DICT["parsec.blackscholes"] = gen_parsec("parsec.blackscholes")
BENCHMARK_DICT["parsec.bodytrack"] = gen_parsec("parsec.bodytrack")
BENCHMARK_DICT["parsec.canneal"] = gen_parsec("parsec.canneal")
BENCHMARK_DICT["parsec.dedup"] = gen_parsec("parsec.dedup")
BENCHMARK_DICT["parsec.facesim"] = gen_parsec("parsec.facesim")
BENCHMARK_DICT["parsec.ferret"] = gen_parsec("parsec.ferret")
BENCHMARK_DICT["parsec.fluidanimate"] = gen_parsec("parsec.fluidanimate")
BENCHMARK_DICT["parsec.freqmine"] = gen_parsec("parsec.freqmine")
BENCHMARK_DICT["parsec.raytrace"] = gen_parsec("parsec.raytrace")
BENCHMARK_DICT["parsec.streamcluster"] = gen_parsec("parsec.streamcluster")
BENCHMARK_DICT["parsec.swaptions"] = gen_parsec("parsec.swaptions")
BENCHMARK_DICT["parsec.vips"] = gen_parsec("parsec.vips")
BENCHMARK_DICT["parsec.x264"] = gen_parsec("parsec.x264")
BENCHMARK_DICT["sp2x.barnes"] = gen_parsec("splash2x.barnes")
BENCHMARK_DICT["sp2x.cholesky"] = gen_parsec("splash2x.cholesky")
BENCHMARK_DICT["sp2x.fft"] = gen_parsec("splash2x.fft")
BENCHMARK_DICT["sp2x.fmm"] = gen_parsec("splash2x.fmm")
BENCHMARK_DICT["sp2x.lu_cb"] = gen_parsec("splash2x.lu_cb")
BENCHMARK_DICT["sp2x.lu_ncb"] = gen_parsec("splash2x.lu_ncb")
BENCHMARK_DICT["sp2x.ocean_cp"] = gen_parsec("splash2x.ocean_cp")
BENCHMARK_DICT["sp2x.ocean_ncp"] = gen_parsec("splash2x.ocean_ncp")
BENCHMARK_DICT["sp2x.radiosity"] = gen_parsec("splash2x.radiosity")
BENCHMARK_DICT["sp2x.radix"] = gen_parsec("splash2x.radix")
BENCHMARK_DICT["sp2x.raytrace"] = gen_parsec("splash2x.raytrace")
BENCHMARK_DICT["sp2x.volrend"] = gen_parsec("splash2x.volrend")
BENCHMARK_DICT["sp2x.water_nsquared"] = gen_parsec("splash2x.water_nsquared")
BENCHMARK_DICT["sp2x.water_spatial"] = gen_parsec("splash2x.water_spatial")
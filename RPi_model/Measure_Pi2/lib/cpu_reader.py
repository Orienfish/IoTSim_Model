import os
import signal
import subprocess
import threading
import time

#DEF_EXEC_CMD = "ssh shepherd@seelab-git.ucsd.edu " + \
#        "/media/shepherd/RabbitHole/intel_hpc/demo/perf_script.sh "
#DEF_KILL_CMD = "ssh shepherd@seelab-git.ucsd.edu \"bash -c 'sudo killall -9 sleep'\""

#DEF_EXEC_CMD = "ssh pietro@132.239.17.46 " + \
#        "/home/pietro/spec2006/perf_demo.sh"
#DEF_KILL_CMD = "ssh pietro@132.239.17.46 \"bash -c 'sudo killall -9 gcc'\""

DEF_EXEC_CMD = "ssh pi@132.239.17.47 " + \
        "/home/pi/Desktop/IoTSim_Model/RPi_model/Target_Pi1/get_cpu_usage.sh 0.05" # 0.2 sampling interval
DEF_KILL_CMD = "ssh pi@132.239.17.47 \"bash -c 'sudo kill -9 $(pgrep get_cpu_usage.sh)'\""


def sig_handler(signum, _):
    if sig_handler.kill_cmd is not None:
        print("End of procedure")
        os.system(sig_handler.kill_cmd)
        sig_handler.kill_cmd = None
 
def perf_runner(cmd, self):
    # exec the perf_script.sh
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    for line in iter(proc.stdout.readline, ''):
        line = line.strip()
        elems = line.split(",")

        self.digest(elems[0], elems[1]) # freq, util


class PerfOnlineReader(object):
    def __init__(self, cmd=DEF_EXEC_CMD, kill_cmd=DEF_KILL_CMD):
        self.cmd = cmd
        self.kill_cmd = kill_cmd
        self.pmu_dict = dict()

    def run(self, callback):
        self.callback = callback

        sig_handler.kill_cmd = self.kill_cmd
        signal.signal(signal.SIGINT, sig_handler)

        self.t = threading.Thread(target=perf_runner, args=(self.cmd, self))
        self.t.start()

    def finish(self):
        sig_handler(0, 0)
        if self.t is not None:
            self.t.join()

    def wait(self):
        self.t.join()
        self.t = None

    def digest(self, freq, util)
        self.pmu_dict["freq"] = freq
        self.pmu_dict["util"] = util
        self.callback(self.pmu_dict)
        
        self.pmu_dict = dict()
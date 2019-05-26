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
        "/home/pi/Desktop/IoTSim_Model/RPi_model/Target_Pi1/perf_script.sh"
DEF_KILL_CMD = "ssh pi@132.239.17.47 \"bash -c 'sudo kill -9 $(pgrep perf_script.sh)'\""


def sig_handler(signum, _):
    if sig_handler.kill_cmd is not None:
        print("End of procedure")
        os.system(sig_handler.kill_cmd)
        sig_handler.kill_cmd = None
 
def perf_runner(cmd, self):
    # exec the perf_script.sh
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    for line in iter(proc.stdout.readline, ''):
        if "Killed" in line:
            continue

        line = line.strip()
        elems = line.split(",")

        time = float(elems[0])
        if "not counted" in line:
            self.digest(time, -1, -1)
            return

        val = int(elems[1])
        evt = str(elems[3])
        self.digest(time, val, evt)


class PerfOnlineReader(object):
    def __init__(self, cmd=DEF_EXEC_CMD, kill_cmd=DEF_KILL_CMD):
        self.cmd = cmd
        self.kill_cmd = kill_cmd
        self.prev_time = None 
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

    def digest(self, time, val, evt):
        if self.prev_time != time:
            if self.prev_time is not None:
                if not any([self.pmu_dict[key] < 0 for key in self.pmu_dict]):
                    self.callback(self.pmu_dict)
            self.pmu_dict = dict()

        self.prev_time = time
        self.pmu_dict[evt] = val



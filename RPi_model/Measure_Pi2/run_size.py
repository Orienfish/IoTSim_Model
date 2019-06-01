import os
import sys
import datetime
import time
import threading

PWR_MEAS_CMD = "python ./pwr_measure.py %size_#"
RUN_CMD = "ssh pi@192.168.1.57 \"bash -c '/home/pi/Desktop/Target_Pi1/run_net_size.sh %size_#' \""
size = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000]

def cmd_runner(cmd):
    os.system(cmd)
    
def run(ssize, cnt):
    pwr_cmd = PWR_MEAS_CMD.replace("%size", str(ssize))
    pwr_cmd = pwr_cmd.replace("#", str(cnt))
    run_cmd = RUN_CMD.replace("%size", str(ssize))
    run_cmd = run_cmd.replace("#", str(cnt))
    print pwr_cmd, run_cmd
    pwr_t = threading.Thread(target=cmd_runner, args=(pwr_cmd,))
    run_t = threading.Thread(target=cmd_runner, args=(run_cmd,))
    
    run_t.start()
    pwr_t.start()
    pwr_t.join()
    run_t.join()
    
def main():
    MAX_CNT = 5
    for i in range(0, len(size)):
        for j in range(0, MAX_CNT):
            run(size[i], j)
	    time.sleep(5)
            
if __name__ == '__main__':
    main()
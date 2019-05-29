import os
import signal
import threading

BW_SET_CMD = "ssh pi@192.168.1.57 " + \
        "sudo /home/pi/wondershaper/wondershaper -a wlan0 -u %d -d %d"
BW_RESET_CMD = "ssh pi@192.168.1.57 " + \
        "sudo /home/pi/wondershaper/wondershaper -c -a wlan0"
PUB_EXEC_CMD = "ssh pi@192.168.1.57 " + \
        "python /home/pi/Desktop/IoTSim_Model/RPi_model/Target_Pi1/local_connecter.py > /dev/null 2>&1 &"
PUB_KILL_CMD = "ssh pi@192.168.1.57 \"bash -c 'sudo killall -9 python'\""

def sig_handler(signum, _):
    if sig_handler.reset_cmd is not None:
        print("Clear wondershaper setting")
        os.system(sig_handler.reset_cmd)
        sig_handler.reset_cmd = None
    if sig_handler.kill_cmd is not None:
        print("Kill pub script")
        os.system(sig_handler.kill_cmd)
        sig_handler.kill_cmd = None
 
def runner(set_cmd, exec_cmd):
    os.system(set_cmd)
    os.system(exec_cmd)

class NetTrigger(object):
    def __init__(self, set_cmd=BW_SET_CMD, reset_cmd=BW_RESET_CMD,
	exec_cmd = PUB_EXEC_CMD, kill_cmd = PUB_KILL_CMD):
        self.set_cmd = set_cmd
        self.reset_cmd = reset_cmd
        self.exec_cmd = exec_cmd
	self.kill_cmd = kill_cmd

    def runTest(self, bw):
	sig_handler.reset_cmd = self.reset_cmd
        sig_handler.kill_cmd = self.kill_cmd
        signal.signal(signal.SIGINT, sig_handler)

	self.set_cmd = self.set_cmd.replace("%d", str(bw), 2)
	# print self.set_cmd
        self.t = threading.Thread(target=runner, \
		args=(self.set_cmd, self.exec_cmd))
        self.t.start()

    def stop(self):
        sig_handler(0, 0)
        if self.t is not None:
            self.t.join()


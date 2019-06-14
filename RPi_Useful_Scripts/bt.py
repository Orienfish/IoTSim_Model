# Usage: python bluetooth.py 600 10 # run at 600MHz, send 10kB data
from bluedot.btcomm import BluetoothClient
from signal import pause
import time
import os
import sys

MAX_TIME = 10
PERF_CMD = "bash /home/pi/Desktop/Target_Pi1/get_cpu_usage.sh 0 >" + \
	"/home/pi/Desktop/Target_Pi1/bt_measure/%d_#.txt &"
KILL_CMD = "killall -9 bash"

# Start perf measurement
if (len(sys.argv) > 2):
    perf_cmd = PERF_CMD.replace("%d", sys.argv[1])
    perf_cmd = perf_cmd.replace("#", sys.argv[2])
    data_size = int(sys.argv[2])
else:
    print("Please specify frequency and data size")
os.system(perf_cmd)

def callback(data):
    pass

# send data
sTime = time.time()
c = BluetoothClient("xfyucat", callback)
str = "abcdefghij" * 100 # 1024 Bytes = 1kB
for i in range(0, data_size):
    c.send(str)
    print i

# Wait until MAX_TIME and end the perf measurement
curTime = time.time()
while (curTime - sTime < MAX_TIME):
    time.sleep(2)
    curTime = time.time()
os.system(KILL_CMD)
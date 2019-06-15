# Bluetooth - time power test
# Preparation: set freq, turn off all network and bluetooth
import os
import sys
import time

startTime = time.time()
if (len(sys.argv) > 1):
    version = sys.argv[1]
#    calib = sys.argv[2] # pwr or perf

#if (calib == "pwr"):
timefile = "./exp_bluetooth/time_" + version + ".txt"
#elif (calib == "perf"):
#    timefile = "./error_analysis/perf_time_" + version + ".txt"
#    filename = "./error_analysis/perf_" + version + ".txt"
#    EXEC_CMD = "bash ./get_cpu_usage.sh 0 > %s &" %filename
#    os.system(EXEC_CMD)

f = open(timefile, "w")

#########################################################
# Import
#########################################################
# This import part is time and power consuming
# f.write("import," + str(time.time() - startTime) + "\r\n") # import time
# from bluetool import Bluetooth # not workable on raspberry
import bluetooth as bt
from bluetooth.ble import DiscoveryService

#########################################################
# Idle
#########################################################
time.sleep(1.0)
stTime = time.time()
time.sleep(5)
FinTime = time.time()
f.write("idle,%f,%f\r\n" %(stTime - startTime, FinTime - startTime)) # idle time

#########################################################
# Turn on Bluetooth
#########################################################
UP_CMD = "sudo rfkill unblock bluetooth; sudo hciconfig hci0 up;"
time.sleep(1.0)
stTime = time.time()
os.system(UP_CMD)
FinTime = time.time()
f.write("turn_on,%f,%f\r\n" %(stTime - startTime, FinTime - startTime)) # turn on time

#########################################################
# Idle
#########################################################
stTime = time.time()
time.sleep(5)
FinTime = time.time()
f.write("turn_on_idle,%f,%f\r\n" %(stTime - startTime, FinTime - startTime)) # idle time

#########################################################
# Scan
#########################################################
def scan_ble(duration=8):
    svc = DiscoveryService()
    devs = svc.discover(duration) 
    print "Find %d devices: " %len(devs)
    if devs:
        for name, addr in devs.items():
	    print name, addr
    return devs

def scan_non_ble(duration=8):
    devs = bt.discover_devices(duration=duration, flush_cache=True, \
	lookup_names=True)

time.sleep(1.0)
print "scanning..."
stTime = time.time()
devs = scan_non_ble(10)
FinTime = time.time()

if devs:
    print "Find %d devices: " %len(devs)
    for name, addr in devs:
	print name, addr

f.write("scan,%f,%f\r\n" %(stTime - startTime, FinTime - startTime))

#########################################################
# Idle
#########################################################
stTime = time.time()
time.sleep(5)
FinTime = time.time()
f.write("scan_idle,%f,%f\r\n" %(stTime - startTime, FinTime - startTime)) # idle time

#########################################################
# Connect
#########################################################
addr = "9C:B6:D0:F5:34:5A"
port = 1

time.sleep(1.0)
try:
    stTime = time.time()
    sock = bt.BluetoothSocket( bt.RFCOMM )
    sock.connect((addr, port))
    FinTime = time.time()
except Exception as e:
    print(e)
    sys.exit()
f.write("connect,%f,%f\r\n" %(stTime - startTime, FinTime - startTime))

#########################################################
# Idle
#########################################################
stTime = time.time()
time.sleep(5)
FinTime = time.time()
f.write("connect_idle,%f,%f\r\n" %(stTime - startTime, FinTime - startTime)) # idle time

#########################################################
# Send
#########################################################
SIZE = [200,500,1000,2000,5000,10000,20000,50000,100000,200000,500000,1000000] # Byte
CNT = 5

for size in SIZE:
    MSG = "A" * size
    print "Testing %d Bytes" %size
    
    for i in range(0, CNT):
	stTime = time.time()
	cur_call = time.time()
        sock.send(MSG)
    	FinTime = time.time()
    	f.write("%d,%f,%f\r\n" %(size, stTime - startTime, FinTime - startTime))
        
sock.close()
f.close()
#if (calib == "pwr"):
#os.system("ssh pi@192.168.1.39 \"bash -c 'killall -9 bash'\"")
#elif (calib == "perf"):
#    KILL_CMD = "killall -9 bash"
#    os.system(KILL_CMD)


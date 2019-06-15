# Bluetooth - time power test
# Preparation: set freq, turn off all network and bluetooth
import os
import sys
import time

startTime = time.time()
if (len(sys.argv) > 1):
    version = sys.argv[1]

timefile = "./exp_bluetooth/time_" + version + ".txt"

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
# SIZE = [200,500,1000,2000,5000,10000,20000,50000,100000,200000,500000,1000000] # Byte
SIZEPS = [200,500,1000,2000,5000,10000,20000,50000,100000,200000]
CNT = 5
T = 1

for size in SIZEPS:
    MSG = "A" * size
    print "Testing %d Bps" %size
    
    stTime = time.time()
    for i in range(0, CNT):
	cur_call = time.time()
        sock.send(MSG)
	if (time.time() - cur_call < T):
	    time.sleep(cur_call + T - time.time())
	else:
            print "overload"
    FinTime = time.time()
    f.write("%d,%f,%f\r\n" %(size, stTime - startTime, FinTime - startTime))
        
sock.close()
f.close()


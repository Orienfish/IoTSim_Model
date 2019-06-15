# Wi-Fi power test
# Preparation: set freq, set bw, turn off all network
import os
import sys
import time

startTime = time.time()
if (len(sys.argv) > 1):
    version = sys.argv[1]
    
timefile = "./exp_wifi/time_" + version + ".txt"

f = open(timefile, "w")

#########################################################
# Import
#########################################################
# This import part is time and power consuming
import socket

#########################################################
# Idle
#########################################################
time.sleep(1.0)
stTime = time.time()
time.sleep(5)
FinTime = time.time()
f.write("idle,%f,%f\r\n" %(stTime - startTime, FinTime - startTime)) # idle time

#########################################################
# Turn on Wi-Fi
#########################################################
time.sleep(1.0)
UP_CMD = "sudo ifconfig wlan0 up; sudo ifconfig ifb0 up;"
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
# Connect 
#########################################################
TCP_IP = "192.168.1.60"
TCP_PORT = 5006

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = False
time.sleep(1.0)
while (connect == False):
    try:
	stTime = time.time()
	s.connect((TCP_IP, TCP_PORT))
	FinTime = time.time()
        connect = True
    except:
        print "No network!"
        time.sleep(5)
f.write("connect,%f,%f\r\n" %(stTime - startTime, FinTime - startTime))

#########################################################
# Idle
#########################################################
stTime = time.time()
time.sleep(5)
FinTime = time.time()
f.write("connect_idle,%f,%f\r\n" %(stTime - startTime, FinTime - startTime)) # idle time

#########################################################
# Sending different size of packets
#########################################################
SIZE = [200,500,1e3,2e3,5e3,1e4,2e4,5e4,1e5,2e5,5e5,1e6] # Byte
BW = 1000
CNT = 5

time.sleep(1.0)
SET_BW= "sudo bash /home/pi/Desktop/Target_Pi1/set_bw.sh %d" %BW
stTime = time.time()
os.system(SET_BW)
FinTime = time.time()
f.write("set_bw,%f,%f\r\n" %(stTime - startTime, FinTime - startTime)) # turn on time

for size in SIZE:
    MSG = "A" * int(size)
    print "Testing %d packets" %size
    for i in range(0, CNT):
        time.sleep(4.0) # idle
        stTime = time.time()
        s.send(MSG)
        FinTime = time.time()
        f.write("%d,%f,%f\r\n" %(size, stTime - startTime, FinTime - startTime))
        print i

#########################################################
# Finish
#########################################################
s.close()
f.close()




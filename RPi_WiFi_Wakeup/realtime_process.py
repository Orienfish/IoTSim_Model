# Simple script to read power trace and time stamps to plot a 
# realtime power curve during Wi-Fi wakeup
# The file path of power and time text files are specified in
# the main function
# Usage: python realtime_process.py 600_1000_nosample
# 600MHz is the frequency, 1000bps is the bandwidth
# bound, no sample means no performance sampling on the
# running Pi
from __future__ import division
import os
import sys
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt

#####################################################################

####################################################################
# Read the power traces
def load_pwr(pwrfile):
	train_data = []
	with open(pwrfile, "r") as f:
		f.readline() # date line
		f.readline() # label line
		line = f.readline() # first data
		while line:
			elem = line.strip().split(",")
			new_vec = np.zeros(2)
                        new_vec[0] = float(elem[1]) # time
                        new_vec[1] = float(elem[5]) # power
                        
			train_data.append(new_vec)

			line = f.readline()
	return train_data

# Read the time text file
# The first two lines record the time stamps of turning on Wi-Fi
# and connecting to AP
# The rest lines record the beginning and ending of sending 
# 1kB, 100kB, 1000kB, 10000kB packet
def load_time(timefile):
    time_pre = []
    time_start = []
    time_end = []
    with open(timefile, "r") as f:
        line = f.readline()
        time_pre.append(float(line))
        line = f.readline()
        time_pre.append(float(line))
	for line in f.readlines():
            elem0 = line.strip().split(',')[0]
    	    elem1 = line.strip().split(',')[1]
	    print elem0, elem1
	    time_start.append(float(elem0))
	    time_end.append(float(elem1))
    return time_pre, time_start, time_end

###################################################################

###################################################################
def main():
    if len(sys.argv) == 1:
        print "Please specify a version!"
        sys.exit()
    else:
        version = sys.argv[1]

    pwr_filename = "./pwr_realtime/pwr_%s.txt" %version
    time_filename = "./pwr_realtime/time_%s.txt" %version

    # read data
    meas_pwr = load_pwr(pwr_filename)
    time_pre, time_start, time_end = load_time(time_filename)
    ps = np.array(meas_pwr)

    plt.figure(figsize=(8,6), dpi=100)
    line1, = plt.plot(ps[:, 0], ps[:, 1], 'b-', label="Power Measurement")
    for t in time_pre:
        plt.axvline(x=t, color='brown', linestyle='--')
    plt.axvline(x=time_start[0], color='g', linestyle='--', label="Start Sending")
    plt.axvline(x=time_end[0], color='purple', linestyle='--', label="Finish Sending")
    for t in time_start:
        plt.axvline(x=t, color='g', linestyle='--')
    for t in time_end:
        plt.axvline(x=t, color='purple', linestyle='--')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Power Consumption (W)")
    plt.xlim(0.0, 40.0)
    plt.ylim(3.0, 4.2)
    plt.title("Wi-Fi Wakeup Power Consumption")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()


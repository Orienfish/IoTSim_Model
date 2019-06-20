# Simple script to read power trace and time stamps to plot a 
# realtime power curve during Bluetooth wakeup
# The file path of power and time text files are specified in
# the main function
# Usage: python realtime_process.py 600
# 600MHz is the frequency, no bandwidth setting for bluetooth
# All the traces in realtime bluetooth measurements were 
# obtained while no performance sampling is running
from __future__ import division
import os
import sys
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import cPickle as pickle
from sklearn.linear_model import LinearRegression

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
# The first two lines record the time stamps of import libraries
# and turning on Bluetooth
# The rest lines record the beginning and ending of scanning, 
# sending 1kB, 100kB, 1000kB, 10000kB packet
def load_time(timefile):
    time_pre = []
    time_start = []
    time_end = []
    with open(timefile, "r") as f:
        # time import
        line = f.readline()
        time_pre.append(float(line))
        # time up
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
        print "Please specify a model!"
	sys.exit()
    else:
        version = sys.argv[1] 

    pwr_filename = "./pwr_bt_realtime/pwr_%s.txt" %version
    time_filename = "./pwr_bt_realtime/time_%s.txt" %version

    # read data
    meas_pwr = load_pwr(pwr_filename)
    time_pre, time_start, time_end = load_time(time_filename)
    ps = np.array(meas_pwr)

    # plot
    plt.figure(figsize=(8,6), dpi=100)
    line1, = plt.plot(ps[:, 0], ps[:, 1], 'b-', label="Power Measurement")
    for t in time_pre:
        plt.axvline(x=t, color='brown', linestyle='--')
    plt.axvline(x=time_start[0], color='g', linestyle='--', label="Start")
    plt.axvline(x=time_end[0], color='purple', linestyle='--', label="Finish")
    for t in time_start:
        plt.axvline(x=t, color='g', linestyle='--')
    for t in time_end:
        plt.axvline(x=t, color='purple', linestyle='--')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Power Consumption (W)")
    plt.xlim(0.0, 60.0)
    plt.ylim(3.0, 4.0)
    plt.title("Bluetooth Wakeup Power Consumption")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()


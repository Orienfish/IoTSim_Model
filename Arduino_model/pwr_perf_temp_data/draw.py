# Draw the collected power and temperature trace
# Usage: python draw.py 10_1 # 10_1 is version
from __future__ import division
import os
import sys
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt

#####################################################################

####################################################################
def load_pwr(pwrfile):
    pwr_data = []
    with open(pwrfile, "r") as f:
	f.readline() # date line
	f.readline() # label line
	line = f.readline() # first data
	while line:
	    elem = line.strip().split(",")
	    new_vec = np.zeros(2)
            new_vec[0] = float(elem[1]) # time
            new_vec[1] = float(elem[5]) # power
                        
	    pwr_data.append(new_vec)

	    line = f.readline()
    return pwr_data

def load_temp(tempfile):
    temp_data = []
    with open(tempfile, "r") as f:
	line = f.readline()
	while line:
	    elem = line.strip().split(",")
	    new_vec = np.zeros(2)
            new_vec[0] = float(elem[1]) / 1000 # time in millis
            new_vec[1] = float(elem[0]) # temp
                        
	    temp_data.append(new_vec)

	    line = f.readline()
    return temp_data

###################################################################

###################################################################
def plot(pwr_array, temp_array):
    fig, ax1 = plt.subplots()
    color = "tab:red"
    ax1.plot(pwr_array[:, 0], pwr_array[:, 1], color=color, marker='.')
    # ax1.set_xlabel("Packet Size (B)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Power Consumption (W)", color=color)
    ax1.set_title("Arduino Power and Temperature")
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = "tab:blue"
    ax2.plot(temp_array[:, 0], temp_array[:, 1], color=color, marker='v')
    ax2.set_ylabel("Temperature", color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.show()
    
###################################################################

###################################################################
def main():
    if len(sys.argv) == 1:
        print "Please specify a version!"
	sys.exit()
    else:
        version = sys.argv[1] 

    pwr_filename = "./pwr_%s.txt" %version
    temp_filename = "./temp_%s.txt" %version
    
    # read data
    meas_pwr = load_pwr(pwr_filename)
    meas_temp = load_temp(temp_filename)
    meas_pwr_array = np.array(meas_pwr)
    meas_temp_array = np.array(meas_temp)
    print meas_pwr, meas_temp
   
    plot(meas_pwr_array, meas_temp_array)		
    

if __name__ == '__main__':
    main()

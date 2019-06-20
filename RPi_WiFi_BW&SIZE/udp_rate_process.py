# Calculate and plot the average Wi-Fi power using UDP and 1200MHz
# Either under various bandwidth and packet rate (pkt_1200)
# Or under various bandwidth and data rate (size_1200)
# 
# Data is in the folder ./udp_data, generated images are in ./img
# Usage: python udp_rate_process.py pkt_1200 # pkt_1200 is version
from __future__ import division
import os
import sys
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt

version = None
###################################################################

###################################################################
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

def load_time(timefile):
    phase_list = [] # records other phase we test
    bw_list, rate_list = [], [] # records the size we test
    time_data = dict()
    with open(timefile, "r") as f:
	for line in f.readlines():
	    elem = line.strip().split(',')
	    # print elem
	    try:
		bw = int(elem[0])
		if bw not in bw_list:
			bw_list.append(bw)
		rate = int(elem[1]) # pktrate or Byte/s
		if rate not in rate_list:
			rate_list.append(rate)
		stTime = float(elem[2])
		FinTime = float(elem[3])
		label = str(bw) + "," + str(rate)
	    except:
		label = elem[0]
		phase_list.append(elem[0])
		stTime = float(elem[1])
		FinTime = float(elem[2])

	    # add data to dict
	    # If label is one of the prepare process,
	    # the data input will be [label, start time, end time]
	    # Else if it is one of the bandwidth and rate test,
	    # the data input will be
	    # [bandwidth, rate, start time, end time]
            time_data[label] = [[stTime, FinTime]]
    return phase_list, bw_list, rate_list, time_data

###################################################################

###################################################################
def cal_avg_pwr(meas_pwr_array, tlist):
    total_energy = 0
    total_time = 0
    for st, ft in tlist:
	# find all the pwr measurements in (st, ft)
	pwr_in_interval = np.array(
	    [vec for vec in meas_pwr_array if vec[0] > st and vec[0] < ft]
	    )
	# if there exist, calculate the total energy
	if pwr_in_interval.size != 0:
	    # first interval
	    dt = pwr_in_interval[0, 0] - st
	    de = dt * pwr_in_interval[0, 1]
	    total_time += dt
	    total_energy += de
	    # print "%f, %f, %f, %f, %f, %f" %(st, ft, \
	    #	st, pwr_in_interval[0, 0], dt, de)
	    
	    # middle intervals
	    for i in range(0, pwr_in_interval.shape[0] - 1):
		dt = pwr_in_interval[i+1, 0] - pwr_in_interval[i, 0]
		de = dt * pwr_in_interval[i, 1]
		total_time += dt
		total_energy += de
		# print "%f, %f, %f, %f, %f, %f" %(st, ft, \
		#    pwr_in_interval[i+1, 0], pwr_in_interval[i, 0], \
		#    dt, de)
	    
	    # last interval
	    dt = ft - pwr_in_interval[-1, 0]
	    de = dt * pwr_in_interval[-1, 1]
	    total_time += dt
	    total_energy += de
	    # print "%f, %f, %f, %f, %f, %f" %(st, ft, \
	    #    pwr_in_interval[-1, 0], ft, dt, de)
	# the interval is too short and no pwr measurements in (st, ft)
	else:
	    lt = np.array(
		[1 if vec[0] < st else 0 for vec in meas_pwr_array]
		)
	    prev_t_idx = np.sum(lt)
	    prev_vec = meas_pwr_array[prev_t_idx - 1, :]
	    next_vec = meas_pwr_array[prev_t_idx, :] # the next vec
            # print "prev_vec: ", prev_vec
            # print "next_vec: ", next_vec 
	    # calculate avg pwr
	    dt = ft - st
	    de = dt * np.mean(np.array(prev_vec[1], next_vec[1]))
	    total_time += dt
            total_energy += de
            # print "%f, %f, %f, %f" %(st, ft, dt, de)
    return total_energy / total_time, total_energy, total_time
			
###################################################################

###################################################################
def plot_rt_pwr(ps, time_data):
    plt.figure(figsize=(8,6), dpi=100)
    line1, = plt.plot(ps[:, 0], ps[:, 1], 'b-', label="Power Measurement")
    # first line label
    for key in time_data:
	for st, ft in time_data[key]:
	    plt.axvline(x=st, color='g', linestyle='--')
	    plt.axvline(x=ft, color='purple', linestyle='--')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Power Consumption (W)")
    plt.xlim(0, 200.0)
    # plt.ylim(3.0, 3.5) # for 600MHz
    plt.ylim(3.2, 4.0) # for 1200MHz
    # plt.title("Wi-Fi Power Consumption")
    plt.legend()
    plt.show()

def plot_pwr_at_bw(bw, rate_list, pwr_list, t_list):
    global version
    fig, ax1 = plt.subplots()
    color = "tab:red"
    ax1.plot(rate_list, pwr_list, color=color, marker='.')
    # ax1.set_xlabel("Packet Size (B)")
    ax1.set_xlabel("Data Rate (B/s)")
    ax1.set_ylabel("Wi-Fi Power Consumption (W)", color=color)
    ax1.set_title("Wi-Fi Power Consumption at %d kbps" %bw)
    #ax1.set_xscale('log')
    ax1.set_ylim(0.05, 0.4)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = "tab:blue"
    ax2.plot(rate_list, t_list, color=color, marker='v')
    ax2.set_ylabel("Transmission Time (s)", color=color)
    #ax2.set_xscale('log')
    ax2.set_ylim(0, 50)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    figname = "./img/%s_bw_%d.png" %(version, bw)
    plt.savefig(figname, dpi=200)

def plot_pwr_at_rate(rate, bw_list, pwr_list, t_list):
    global version
    fig, ax1 = plt.subplots()
    color = "tab:red"
    ax1.plot(bw_list, pwr_list, color=color, marker='.')
    # ax1.set_xlabel("Packet Size (B)")
    ax1.set_xlabel("bandwidth (kbps)")
    ax1.set_ylabel("Wi-Fi Power Consumption (W)", color=color)
    ax1.set_title("Wi-Fi Power Consumption at %d B/s" %rate)
    ax1.set_xscale('log')
    ax1.set_ylim(0.05, 0.4)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = "tab:blue"
    ax2.plot(bw_list, t_list, color=color, marker='v')
    ax2.set_ylabel("Transmission Time (s)", color=color)
    ax2.set_xscale('log')
    ax2.set_ylim(0, 500)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    figname = "./img/%s_rate_%d.png" %(version, rate)
    plt.savefig(figname, dpi=200)

###################################################################

###################################################################
def main():
    global version
    if len(sys.argv) == 1:
        print "Please specify a version!"
	sys.exit()
    else:
        version = sys.argv[1] 

    pwr_filename = "./udp_data/pwr_%s.txt" %(version)
    time_filename = "./udp_data/time_%s.txt" %(version)
    result_filename = "./udp_data/result_%s.txt" %(version)
    
    # read data
    meas_pwr = load_pwr(pwr_filename)
    phase_list, bw_list, rate_list, time_data = \
    	load_time(time_filename)
    meas_pwr_array = np.array(meas_pwr)
    for key in time_data:
	time_data[key] = np.array(time_data[key])

    # Calculate the average power for each phase
    avg_pwr = dict()
    total_energy = dict()
    total_time = dict()
    for key in time_data:
	print "calculate avg pwr for ", key
	avg_pwr[key], total_energy[key], total_time[key] = \
	    cal_avg_pwr(meas_pwr_array, time_data[key])
	print "avg power: ", avg_pwr[key]
	print "total energy: ", total_energy[key]
    	print "total time: ", total_time[key]

    # log the result and get avg pwr
    res_f = open(result_filename, "w")
    idle_pwr = avg_pwr["idle"]
    res_f.write("phase, avg pwr, total energy, total time\r\n")
    for phase in phase_list:
	res_f.write("%s,%f,%f,%f\r\n" %(phase, avg_pwr[phase], \
	    total_energy[phase], total_time[phase]))

    print bw_list, rate_list
    bw_list.sort()
    rate_list.sort()
    pwr_array, time_array = [], [] # 2-D array
    for i in range(0, len(bw_list)):
    	rate_pwr_list, rate_time_list = [], []
    	for j in range(0, len(rate_list)):
    	    label = str(bw_list[i]) + "," + str(rate_list[j]) 
	    res_f.write("%d,%d,%f,%f,%f\r\n" %(bw_list[i], \
                rate_list[j], avg_pwr[label], \
                total_energy[label], total_time[label]))
	    rate_pwr_list.append(avg_pwr[label] - idle_pwr)
	    rate_time_list.append(total_time[label])
        pwr_array.append(rate_pwr_list)
        time_array.append(rate_time_list)
        # substract idle power and get avg pwr
    res_f.close()
    pwr_array = np.array(pwr_array)
    time_array = np.array(time_array)
    
    # plot
    plot_rt_pwr(meas_pwr_array, time_data)
    for i in range(0, len(bw_list)):
    	print pwr_array[i, :]
        plot_pwr_at_bw(bw_list[i], rate_list, pwr_array[i, :], \
     	    time_array[i, :])

    for i in range(0, len(rate_list)):
    	print pwr_array[:, i]
        plot_pwr_at_rate(rate_list[i], bw_list, pwr_array[:, i], \
    	    time_array[:, i])
    

if __name__ == '__main__':
    main()

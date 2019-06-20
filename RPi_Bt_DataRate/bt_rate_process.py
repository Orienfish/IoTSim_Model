# Calculate and plot average bluetooth power
# when sending data at various rate per second
# Usage: python bt_rate_process.py rate_1200
# rate_1200 is the version
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

def load_time(timefile):
    phase_list = [] # records other phase we test
    test_list = [] # records the size we test
    time_data = dict()
    with open(timefile, "r") as f:
	for line in f.readlines():
	    elem = line.strip().split(',')
	    # print elem
	    label = str(elem[0])
	    stTime = float(elem[1])
	    FinTime = float(elem[2])
			
	    # add data to dict
	    if label in time_data:
		time_data[label].append([stTime, FinTime])
	    else:
		time_data[label] = [[stTime, FinTime]]
	        # if label records the size of packet, add it to list
	        # Put it here so this process is only done
		# when the label first appears
		try:
		    test = int(label)
		    test_list.append(test)
		except:
		    phase_list.append(label)
    return phase_list, test_list, time_data

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
    plt.xlim(0, 120.0)
    # plt.ylim(3.0, 3.5) # for 600MHz
    plt.ylim(3.2, 4.0) # for 1200MHz
    plt.title("Bluetooth Power Consumption")
    plt.legend()
    plt.show()

    
def plot_avg_pwr(test_list, pwr_list, t_list):
    fig, ax1 = plt.subplots()
    color = "tab:red"
    ax1.plot(test_list, pwr_list, color=color, marker='.')
    # ax1.set_xlabel("Packet Size (B)")
    ax1.set_xlabel("Packet Rate (B/s)")
    ax1.set_ylabel("Bluetooth Power Consumption (W)", color=color)
    ax1.set_title("Bluetooth Power Consumption and Sending Time")
    ax1.set_xscale('log')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = "tab:blue"
    ax2.plot(test_list, t_list, color=color, marker='v')
    ax2.set_ylabel("Transmission Time (s)", color=color)
    ax2.set_xscale('log')
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

    pwr_filename = "./bt_rate_data/pwr_%s.txt" %version
    time_filename = "./bt_rate_data/time_%s.txt" %version
    result_filename = "./bt_rate_data/result_%s.txt" %version
    
    # read data
    meas_pwr = load_pwr(pwr_filename)
    phase_list, test_list, time_data = load_time(time_filename)
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

    # log the result and get avg bt pwr
    res_f = open(result_filename, "w")
    pwr_list, t_list = [], []
    idle_pwr = avg_pwr["idle"]
    res_f.write("phase, avg pwr, total energy, total time\r\n")
    for phase in phase_list:
	res_f.write("%s,%f,%f,%f\r\n" %(phase, avg_pwr[phase], \
	    total_energy[phase], total_time[phase]))
    for test in test_list:
	res_f.write("%d,%f,%f,%f\r\n" %(test, avg_pwr[str(test)], \
    	    total_energy[str(test)], total_time[str(test)]))
        # substract idle power and get bt avg pwr
	pwr_list.append(avg_pwr[str(test)] - idle_pwr)
	t_list.append(total_time[str(test)])
    res_f.close()
	
    
    # plot
    plot_rt_pwr(meas_pwr_array, time_data)
    plot_avg_pwr(test_list, pwr_list, t_list)
		
    

if __name__ == '__main__':
    main()

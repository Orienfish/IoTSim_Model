# Train and visualize prediction average power
# 
# Data is in the folder ./udp_data, generated images are in ./img
# Usage: python train_net.py size_1200 size_1200
# The first size_1200 is the version of data to train
# The second size_1200 is the version of predicted model to import
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
from mpl_toolkits.mplot3d import Axes3D

version = None

#####################################################################
def save_with_pickle(data, filename):
    """ save data to a file for future processing"""
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_with_pickle(filename):
    """ load data from a file"""
    if not os.path.exists(filename):
        return None

    with open(filename, 'rb') as f:
        return pickle.load(f)

    return None

# Save np array to csv
def save_csv(filename, keys, data_matrix):
    with open(filename, "w") as writer:
        # write header
        writer.write(','.join(keys))
        writer.write('\n')

        # write data in each row
        for vec in data_matrix:
            writer.write(','.join(["{0:.2f}".format(v) for v in vec]))
            writer.write('\n')
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
def getError(pred, msr):
    err = np.absolute(pred - msr) / msr
    maxErr = np.amax(err)
    avgErr = np.mean(err)
    return avgErr, maxErr			
###################################################################

###################################################################
def main():
    global version
    if len(sys.argv) != 2:
        print "Number of parameters is not right!"
	sys.exit()
    else:
        version = sys.argv[1]

    pwr_filename = "./udp_data/pwr_%s.txt" %(version)
    time_filename = "./udp_data/time_%s.txt" %(version)

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

    # get the idle power
    idle_pwr = avg_pwr["idle"]

    print bw_list, rate_list
    bw_list.sort()
    rate_list.sort()
    data_len = len(bw_list) * len(rate_list)
    train_label = ["bandwidth", "rate", "product", "power"]
    n_evt = len(train_label) - 1
    data_matrix = np.zeros((data_len, len(train_label))) # 2-D array
    print data_matrix.shape

    k = 0
    for i in range(0, len(bw_list)):
    	for j in range(0, len(rate_list)):
            data_matrix[k, 0] = bw_list[i]
            data_matrix[k, 1] = rate_list[j]
            data_matrix[k, 2] = bw_list[i] * rate_list[j]
            label = str(bw_list[i]) + "," + str(rate_list[j]) 
            data_matrix[k, n_evt] = avg_pwr[label] - idle_pwr
            k += 1

    save_csv("measurement_"+version+".csv", train_label, data_matrix)
    clf = LinearRegression()
    reg = clf.fit(data_matrix[:, :n_evt], data_matrix[:, n_evt])
    pred = clf.predict(data_matrix[:, :n_evt])
    score = clf.score(data_matrix[:, :n_evt], data_matrix[:, n_evt])
    avgErr, maxErr = getError(pred, data_matrix[:, n_evt])
    print("Score: %f" %score)
    print("Error: avg: %f max: %f" %(avgErr, maxErr))

    # Save model
    new_model = "./model/model." + version
    save_with_pickle(clf, new_model)
    print "model save to", new_model

    # Save coefficients
    #with open("./model/model_info.txt", "a+") as f:
    #    f.write("\r\nCoefficients of %s\r\n" %new_model)
    #    for i in range(0, n_evt):
    #        f.write("%s: " %train_label[i])
    #        f.write("%s " %reg.coef_[i])
    #    f.write("intercept: ")
    #    f.write("%s" %reg.intercept_)
    #    f.write("\r\nScore: %f\r\n" %score)
    #    f.write("Error: avg: %f max: %f\r\n" %(avgErr, maxErr))
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    # Use scatter
    #xline = data_matrix[:, 0]
    #yline = data_matrix[:, 1]
    #zline = data_matrix[:, n_evt]
    #ax.scatter3D(xline, yline, zline, color='blue', \
    #    label='Power Consumption')
    #ax.scatter3D(xline, yline, pred, color='red', \
    #    label='Predicted Power')

    # Use wireframe
    bw = np.array(bw_list)
    rate = np.array(rate_list)
    X, Y = np.meshgrid(rate, bw)
    Z1 = np.resize(data_matrix[:, n_evt], (len(bw_list), len(rate_list)))
    Z2 = np.resize(pred, (len(bw_list), len(rate_list)))
    ax.plot_wireframe(X, Y, Z1, rstride=2, cstride=2, color='blue', \
        label='Power Consumption')
    ax.plot_wireframe(X, Y, Z2, rstride=2, cstride=2, color='red', \
        label='Power Prediction')

    # Set title and labels
    ax.set_title('Wi-Fi Power Consumption and Predicted Power')
    ax.set_xlabel('Bandwidth (kbps)')
    #ax.set_ylabel('Packet Rate (#/s)')
    ax.set_ylabel('Data Rate (B/s)')
    ax.legend()
    plt.show()
    

if __name__ == '__main__':
    main()

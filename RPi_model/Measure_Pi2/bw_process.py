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
# Usage: python bw_process ./model/model.v1

bw = [50, 100, 200, 400, 800, 1000, 2000, 4000, 8000, 10000]
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

#####################################################################

####################################################################
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
			
def load_perf(perffile):
	train_data = []
	with open(perffile, "r") as f:
		line = f.readline()
		load_perf.label_list = line.strip().split(",")
		# print "label_list: ", load_perf.label_list
		
		line = f.readline() # first data
		while line:
			elem = line.strip().split(",")
			# new vec: [time, freq, util]
			new_vec = np.zeros(len(load_perf.label_list))
			for i in range(0, len(load_perf.label_list)):
				new_vec[i] = float(elem[i])
			
			if load_perf.model:
				pred_pwr = load_perf.model.predict([new_vec[1:]])[0]
			else:
				pred_pwr = 0.0

			train_data.append([new_vec[0], pred_pwr])
			
			line = f.readline()
	return train_data
			
load_perf.label_list = None
load_perf.model = None

###################################################################

###################################################################
# Align samples for the target timestamps
def align_samples(target_ts, ts, vs):
    assert len(ts) == len(vs)
    ret_list = []

    # List of interval 
    vs_in_interval = []
    target_idx = 0
    target_t = target_ts[0]
    def commit_interval(ret_list, vs_in_interval, target_idx):
        if vs_in_interval:
            ret_list.append(np.array(vs_in_interval).mean())
        else:
            ret_list.append(np.nan)

        # update target_idx and target_t to next stamp in target_ts
        target_idx += 1
        if target_idx < len(target_ts):
            return [], target_ts[target_idx], target_idx

        return [], None, target_idx

    prev_t = None
    prev_v = None
    for cur_t, cur_v in zip(ts, vs):
        while target_t is not None and target_t < cur_t:
            if prev_t and prev_t < target_t:
                # fill the samples in the interval
                vs_in_interval.append(prev_v + (cur_v - prev_v) * \
                        (target_t - prev_t) / (cur_t - prev_t))
            vs_in_interval, target_t, target_idx = \
                    commit_interval(ret_list, vs_in_interval, target_idx)

        # Prepare the next target
        vs_in_interval.append(cur_v)
        prev_t = cur_t
        prev_v = cur_v

    if target_t is not None: # last available timestamp
        vs_in_interval, target_t, target_idx = \
                commit_interval(ret_list, vs_in_interval, target_idx)

    # fill nan for unavailable target rates
    while target_idx < len(target_ts):
        ret_list.append(np.nan)
        target_idx += 1

    assert(len(ret_list) == len(target_ts))
    return np.array(ret_list)
###################################################################

###################################################################
def main():
    if len(sys.argv) == 1:
        print "Please specify a model!"
	sys.exit()
    else:
        filename = sys.argv[1] 

    # Load model
    load_perf.model = load_with_pickle(filename)

    net_pwr = []

    for i in range(0, len(bw)):
	    pwr_filename = "./pwr_measure/pwr_" + str(bw[i]) + ".txt"
	    perf_filename = "./bw_measure/perf_" + str(bw[i]) + ".txt"

	    # read data
	    meas_pwr = load_pwr(pwr_filename)
	    pred_pwr = load_perf(perf_filename)
	
	    ps = np.array(meas_pwr)
	    vs = np.array(pred_pwr)
	    print ps.shape, vs.shape
	    
	    n = 3 # [meas pwr, pred pwr, net pwr]
	    data_matrix = np.zeros((ps.shape[0], n))
	    # fill the measured power into the last column of data matrix
	    data_matrix[:, 0] = ps[:, 1]
	    # fill the aligned pred power
	    vs_aligned = align_samples(ps[:, 0], vs[:, 0], vs[:, 1])
	    data_matrix[:, 1] = vs_aligned
	
	    # Remove nans
	    data_matrix = np.array(
	            [vec for vec in data_matrix if not any(np.isnan(vec))]
	            )
	
	    # Calculate net power
	    data_matrix[:, 2] = data_matrix[:, 0] - data_matrix[:, 1]
    	    net_pwr.append(np.mean(data_matrix[:, 2]))
    
    
    plt.plot(bw, net_pwr, 'b*')
    plt.xlabel("Bandwidth (kbps)")
    plt.ylabel("Network Power Consumption (W)")
    plt.show()

if __name__ == '__main__':
    main()


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

from lib.perf_reader import PerfReader

#PWR_FILE_600 = "./pwr_measure/pwr_600_16050905302019.txt"
#PWR_FILE_1200 = "./pwr_measure/pwr_1200_16080405302019.txt"
#PERF_FILE_600 = "./cpu_measure/cpu_600_16040405302019.txt"
#PERF_FILE_1200 = "./cpu_measure/cpu_1200_16070005302019.txt"
#VERSION = "v1"

#PWR_FILE_600 = "./pwr_measure/pwr_600.2_16123305302019.txt"
#PWR_FILE_1200 = "./pwr_measure/pwr_1200.2_16102605302019.txt"
#PERF_FILE_600 = "./cpu_measure/cpu_600.2_16112905302019.txt"
#PERF_FILE_1200 = "./cpu_measure/cpu_1200.2_16092105302019.txt"
#VERSION = "v2"

#PWR_FILE_600 = "./pwr_measure/600.txt"
#PWR_FILE_1200 = "./pwr_measure/1200.txt"
#PERF_FILE_600 = "./cpu_measure/600.txt"
#PERF_FILE_1200 = "./cpu_measure/1200.txt"
#VERSION = "v3"

#PWR_FILE_600 = "./pwr_measure/cpu_600.txt"
#PWR_FILE_1200 = "./pwr_measure/cpu_1200.txt"
#PERF_FILE_600 = "./cpu_measure/cpu_600.txt"
#PERF_FILE_1200 = "./cpu_measure/cpu_1200.txt"
#VERSION = "v4"

PWR_FILE_600 = "./pwr_measure/cpu_perf1_600.txt"
PWR_FILE_1200 = "./pwr_measure/cpu_perf1_1200.txt"
PERF_FILE_600 = "./cpu_measure/perf1_600.txt"
PERF_FILE_1200 = "./cpu_measure/perf1_1200.txt"
VERSION = "perf_v1"

#PWR_FILE_600 = "./pwr_measure/cpu_perf2_600.txt"
#PWR_FILE_1200 = "./pwr_measure/cpu_perf2_1200.txt"
#PERF_FILE_600 = "./cpu_measure/perf2_600.txt"
#PERF_FILE_1200 = "./cpu_measure/perf2_1200.txt"
#VERSION = "perf_v2"
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
			
def load_perf(time, pmu_dict):
	if load_perf.label_list is None: # first sample
		load_perf.label_list = ["time"]
		load_perf.label_list += sorted(list(pmu_dict.keys()))
		
	if len(pmu_dict) != len(load_perf.label_list) - 1:
		print("PMU dict len does not match!")
		return
	
	new_vec = np.zeros(1 + len(pmu_dict))
	new_vec[0] = time # seconds
	for evt in pmu_dict:
		new_vec[load_perf.label_list.index(evt)] = pmu_dict[evt]
	load_perf.train_data.append(new_vec)
	
	if load_perf.model is not None: # predict
		pred_pwr = load_perf.model.predict([new_vec[1:]])[0]
	else:
		pred_pwr = 0.0
	load_perf.pred_pwr_list.append([new_vec[0], pred_pwr])
	return
			
load_perf.label_list = None
load_perf.model = None
load_perf.train_data = []
load_perf.pred_pwr_list = []

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

EVT_RATIO = 0.5
COMBINE_PP = True
PLOT_TYPES = ["MP", "PP", "freq", "util"]
MAX_TIME = 200.0

def plot(pwr, pred_pwr, perf):
    num_plots = len(PLOT_TYPES)
    if COMBINE_PP:
        num_plots -= 1
    fig, ax = plt.subplots(num_plots, figsize=(12, 8))

    ax_dict = dict()
    plot_idx = 0
    for type_name in PLOT_TYPES:
        ax_dict[type_name] = ax[plot_idx]
        if COMBINE_PP and type_name == "MP" and "PP" in PLOT_TYPES:
            pass
        else:
            plot_idx += 1

    meas_pwr_array = np.array(pwr)
    pred_pwr_array = np.array(pred_pwr)
    perf_array = np.array(perf)

    line, = ax_dict["MP"].plot(meas_pwr_array[:, 0], meas_pwr_array[:, 1], color="b")
    line2, = ax_dict["PP"].plot(perf_array[:, 0], pred_pwr_array, color="r")

    line_freq, = ax_dict["freq"].plot(perf_array[:, 0], perf_array[:, 1], color="g")
    line_util, = ax_dict["util"].plot(perf_array[:, 0], perf_array[:, 2], color="purple")

    ax_dict["MP"].set_xlim(5.0, MAX_TIME)
    ax_dict["MP"].set_ylim(3.0, 6.0)
    ax_dict["MP"].set_title("Power (Measurement)")
    ax_dict["MP"].set_ylabel("Power (W)")
    line.set_label("Power Measurement")
    ax_dict["MP"].legend()

    if "PP" in ax_dict:
        ax_dict["PP"].set_xlim(5.0, MAX_TIME)
        ax_dict["PP"].set_ylim(3.0, 6.0)
        ax_dict["PP"].set_title("Power (Measurement and Prediction)")
        ax_dict["PP"].set_ylabel("Power (W)")
        line2.set_label("Power Prediction")
        ax_dict["PP"].legend()

    ax_dict["freq"].set_xlim(5.0, MAX_TIME)
    ax_dict["freq"].set_ylim(0.0, 1500000.00)
    ax_dict["freq"].set_title("PMU - Frequency")
    ax_dict["freq"].set_ylabel("Instructions")

    ax_dict["util"].set_xlim(5.0, MAX_TIME)
    ax_dict["util"].set_ylim(0.0, 110.00)
    ax_dict["util"].set_title("PMU - CPU Utilization")
    ax_dict["util"].set_ylabel("CPU Utilization")

    plt.xlabel("Time (sec)")
    plt.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)
    plt.legend()
    plt.show()

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
    if len(sys.argv) == 1:
        filename = "model.tmp"
    else:
        filename = sys.argv[1] 

    # Load model if exists
    load_perf.model = load_with_pickle(filename)
    
    # init reader
    reader = PerfReader()

    # read data - 600MHz
    pwr_data_1 = load_pwr(PWR_FILE_600)
    load_perf.train_data = []
    load_perf.pred_pwr_list = []
    reader.perf_reader(PERF_FILE_600, load_perf)

    ps = np.array(pwr_data_1)
    vs = np.array(load_perf.train_data)
    print ps.shape, vs.shape
    
    n_evt = vs.shape[1] - 1 # get the # of events
    data_matrix_1 = np.zeros((ps.shape[0], n_evt + 1))
    # fill the power into the last column of data matrix
    data_matrix_1[:, n_evt] = ps[:, 1]
    # fill the first n_evt columns
    for idx in range(1, vs.shape[1]):
        vs_aligned = align_samples(ps[:, 0], vs[:, 0], vs[:, idx])
        data_matrix_1[:, idx - 1] = vs_aligned

    # Remove nans
    data_matrix_1 = np.array(
            [vec for vec in data_matrix_1 if not any(np.isnan(vec))]
            )

    # read data - 1200MHz
    pwr_data_2 = load_pwr(PWR_FILE_1200)
    load_perf.train_data = []
    load_perf.pred_pwr_list = []
    reader.perf_reader(PERF_FILE_1200, load_perf)

    ps = np.array(pwr_data_2)
    vs = np.array(load_perf.train_data)
    print ps.shape, vs.shape
    print ps[:, 0], vs[:, 0]
    
    n_evt = vs.shape[1] - 1 # get the # of events
    data_matrix_2 = np.zeros((ps.shape[0], n_evt + 1))
    # fill the power into the last column of data matrix
    data_matrix_2[:, n_evt] = ps[:, 1]
    # fill the first n_evt columns
    for idx in range(1, vs.shape[1]):
        vs_aligned = align_samples(ps[:, 0], vs[:, 0], vs[:, idx])
        data_matrix_2[:, idx - 1] = vs_aligned

    # Remove nans
    print data_matrix_2[10, :]
    data_matrix_2 = np.array(
            [vec for vec in data_matrix_2 if not any(np.isnan(vec))]
            )

    # Integrate matrix_1 and matrix_2
    print data_matrix_1.shape, data_matrix_2.shape
    data_matrix = np.vstack((data_matrix_1, data_matrix_2))

    load_perf.label_list.remove("time")
    save_csv("measurement_"+VERSION+".csv", load_perf.label_list + ["power"], data_matrix)
    clf = LinearRegression()
    reg = clf.fit(data_matrix[:, :n_evt], data_matrix[:, n_evt])
    pred = clf.predict(data_matrix[:, :n_evt])
    score = clf.score(data_matrix[:, :n_evt], data_matrix[:, n_evt])
    avgErr, maxErr = getError(pred, data_matrix[:, n_evt])
    print("Score: %f" %score)
    print("Error: avg: %f max: %f" %(avgErr, maxErr))

    # Save model
    new_model = "./model/model." + VERSION
    save_with_pickle(clf, new_model)
    print "model save to", new_model

    # Save coefficients
    with open("./model/model_info.txt", "a+") as f:
	f.write("\r\nCoefficients of %s\r\n" %new_model)
	for i in range(0, n_evt):
	    f.write("%s: " %load_perf.label_list[i])
	    f.write("%s " %reg.coef_[i])
	f.write("intercept: ")
	f.write("%s" %reg.intercept_)
	f.write("\r\nScore: %f\r\n" %score)
	f.write("Error: avg: %f max: %f\r\n" %(avgErr, maxErr))
    
    plot(pwr_data_1, pred_pwr_1, perf_data_1)
    plot(pwr_data_2, pred_pwr_2, perf_data_2)

if __name__ == '__main__':
    main()


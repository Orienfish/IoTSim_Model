import os
import sys
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sklearn
import cPickle as pickle
from sklearn.linear_model import LinearRegression

from lib.cpu_reader import PerfOnlineReader
from lib.multimeter import MultiMeter

VERSION="simple"

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
def pmu_callback(pmu_dict):
    if pmu_callback.label_list is None: # first sample
        pmu_callback.label_list = ["time"]
        pmu_callback.label_list += sorted(list(pmu_dict.keys()))

    for key in pmu_dict:
    	print key, pmu_dict[key]

    if len(pmu_dict) != len(pmu_callback.label_list) - 1:
        print("PMU measurement error")
        return
    if pwr_callback.start_time is None:
        return
    
    new_vec = np.zeros((1 + len(pmu_dict))) # [time, freq, util]
    # record the received time
    new_vec[0] = float(time.time() * 1000 - pwr_callback.start_time) / 1000
    for evt in pmu_dict:
        new_vec[pmu_callback.label_list.index(evt)] = pmu_dict[evt]
    pmu_callback.train_data.append(new_vec) # time and all the events, no pred

    if pmu_callback.model is not None:
        pred_pwr = pmu_callback.model.predict([new_vec[1:]])[0]
    else:
        pred_pwr = 0.0
    pmu_callback.pred_pwr_list.append([new_vec[0], pred_pwr])
    print(pred_pwr, pwr_callback.last_pwr)

pmu_callback.label_list = None
pmu_callback.train_data = []
pmu_callback.pred_pwr_list = []

def pwr_callback(pwr):
    if pwr_callback.start_time is None:
        pwr_callback.start_time = time.time() * 1000

    pwr_callback.last_pwr = pwr
    pwr_callback.train_data.append(np.array(
        [float(time.time() * 1000 - pwr_callback.start_time) / 1000, pwr]))

pwr_callback.train_data = []
pwr_callback.last_pwr = 0.0
pwr_callback.start_time = None
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
MAX_TIME = 120.0

def animate_plot():
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


    ts = np.arange(0, MAX_TIME, 0.1)
    line, = ax_dict["MP"].plot(ts, [0.0] * len(ts), color="b")
    line2, = ax_dict["PP"].plot(ts, [0.0] * len(ts), color="r")

    line_freq, = ax_dict["freq"].plot(ts, [0.0] * len(ts), color="g")
    line_util, = ax_dict["util"].plot(ts, [0.0] * len(ts), color="purple")

    def set_pmu_line(line, name, pmu_array):
        lidx = pmu_callback.label_list.index(name)
        Y = pmu_array[:,lidx]
        line.set_xdata(pmu_array[:,0])
        line.set_ydata(Y)

    def animate(i):
        meas_pwr_array = np.array(list(pwr_callback.train_data))
        pred_pwr_array = np.array(list(pmu_callback.pred_pwr_list))
        pmu_array = np.array(list(pmu_callback.train_data))
        # print(meas_pwr_array.shape)
        # print(pred_pwr_array.shape)

        if len(meas_pwr_array) == 0 or len(pred_pwr_array) == 0:
            return line, line2, line_freq, line_util

        last_pred_time = pred_pwr_array[:,0][-1]
        meas_pwr_array = meas_pwr_array[[meas_pwr_array[:,0] < last_pred_time]]

        if len(meas_pwr_array) == 0 or len(pred_pwr_array) == 0:
            return line, line2, line_freq, line_util

        line.set_xdata(meas_pwr_array[:,0])
        line.set_ydata(meas_pwr_array[:,1])

        line2.set_xdata(pred_pwr_array[:,0])
        line2.set_ydata(pred_pwr_array[:,1])

        if pmu_callback.label_list is not None: 
            set_pmu_line(line_freq, 'freq', pmu_array)
            set_pmu_line(line_util, 'util', pmu_array)

        return line, line2, line_freq, line_util

    def init():
        return line, line2, line_freq, line_util

    ani = animation.FuncAnimation(
            fig, animate, np.arange(1, 1000), init_func=init,
            interval=500, blit=True) # 1000 frames

    ax_dict["MP"].set_xlim(5.0, MAX_TIME)
    ax_dict["MP"].set_ylim(3.0, 6.0)
    ax_dict["MP"].set_title("Power (Measurement)")
    ax_dict["MP"].set_ylabel("Power (W)")

    if "PP" in ax_dict:
        ax_dict["PP"].set_xlim(5.0, MAX_TIME)
        ax_dict["PP"].set_ylim(3.0, 6.0)
        ax_dict["PP"].set_title("Power (Prediction)")
        ax_dict["PP"].set_ylabel("Power (W)")

    ax_dict["freq"].set_xlim(5.0, MAX_TIME)
    ax_dict["freq"].set_ylim(0.0, 1500000.00)
    ax_dict["freq"].set_title("PMU - Frequency")
    ax_dict["freq"].set_ylabel("Instructions")

    ax_dict["util"].set_xlim(5.0, MAX_TIME)
    ax_dict["util"].set_ylim(0.0, 100.00)
    ax_dict["util"].set_title("PMU - CPU Utilization")
    ax_dict["util"].set_ylabel("CPU Utilization")

    plt.xlabel("Time (sec)")
    plt.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)

    plt.show()

def main():
    if len(sys.argv) == 1:
        filename = "model.tmp"
    else:
        filename = sys.argv[1] 

    # Load model if exists
    pmu_callback.model = load_with_pickle(filename)

    # Run program and 
    mm = MultiMeter("pwr_tmp.txt")
    mm.run(pwr_callback)

    print("Start Perf + Program")
    reader = PerfOnlineReader()
    reader.run(pmu_callback)

    animate_plot()

    #time.sleep(10)
    reader.wait()

    reader.finish()
    mm.stop()

    # Create dataset to train the model again in case needed
    print("Measurement Done")
    print(pmu_callback.label_list)

    ps = np.array(pwr_callback.train_data)
    vs = np.array(pmu_callback.train_data)

    n_evt = vs.shape[1] - 1 # get the # of events
    data_matrix = np.zeros((ps.shape[0], n_evt + 1))
    # fill the power into the last column of data matrix
    data_matrix[:, n_evt] = ps[:, 1]
    # fill the first n_evt columns
    for idx in range(1, vs.shape[1]):
        vs_aligned = align_samples(ps[:, 0], vs[:, 0], vs[:, idx])
        data_matrix[:, idx - 1] = vs_aligned

    # Remove nans
    data_matrix = np.array(
            [vec for vec in data_matrix if not any(np.isnan(vec))]
            )

    pmu_callback.label_list.remove("time")
    save_csv("measurement_"+VERSION+".csv", pmu_callback.label_list + ["power"], data_matrix)
    clf = LinearRegression()
    reg = clf.fit(data_matrix[:, :n_evt], data_matrix[:, n_evt])
    score = clf.score(data_matrix[:, :n_evt], data_matrix[:, n_evt])
    print("Score: %f" %score)

    # Save model
    new_model = "./model/model." + VERSION + "." + \
    	datetime.datetime.now().strftime("%H%M%S%m%d%Y")
    save_with_pickle(clf, new_model)
    print "model save to", new_model

    # Save coefficients
    with open("./model/model_info.txt", "a+") as f:
	f.write("Coefficients of %s\r\n" %new_model)
	for i in range(0, n_evt): # ["cache-misses", "instructions"]
	    f.write("%s: " %pmu_callback.label_list[i])
	    f.write("%s " %reg.coef_[i])
	f.write("intercept: ")
	f.write("%s" %reg.intercept_)
	f.write("\r\nScore: %f\r\n" %score)

if __name__ == '__main__':
    main()


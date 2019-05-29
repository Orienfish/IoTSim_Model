from __future__ import division
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
from lib.net_trigger import NetTrigger

VERSION="simple_net"
BW = [50]
#BW = [50, 100, 200, 400, 600, 800, 1000, \
#	2000, 4000, 6000, 8000, 10000, \
#	20000, 40000, 60000, 80000, 10000] # kbps
TEST_TIME = 10 # test time (secs) for each bw

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

    #for key in pmu_dict:
    #	print key, pmu_dict[key]

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
    
    if pmu_callback.model is not None:
        pred_pwr = pmu_callback.model.predict([new_vec[1:]])[0]
    else:
        print "Base model is not availble!"
	sys.exit()

    # train data is the difference between power prediction and power measurement
    pmu_callback.train_data.append(pwr_callback.last_pwr - pred_pwr) 
    # print(pred_pwr, pwr_callback.last_pwr)

pmu_callback.label_list = None
pmu_callback.train_data = []

def pwr_callback(pwr):
    if pwr_callback.start_time is None:
        pwr_callback.start_time = time.time() * 1000

    pwr_callback.last_pwr = pwr

pwr_callback.last_pwr = 0.0
pwr_callback.start_time = None
###################################################################

###################################################################
# def plotBW():
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
        print "Please specify a base model!"
	sys.exit()
    else:
        filename = sys.argv[1] 

    # Load model if exists
    pmu_callback.model = load_with_pickle(filename)

    # dict for test results - power for network portion
    net_pwr = []

    # run different bw test
    for i in range(0, len(BW)):
	# Run program and 
    	mm = MultiMeter("pwr_tmp.txt")
    	mm.run(pwr_callback)

    	print "Start BW test %d" %BW[i]
    	reader = PerfOnlineReader()
    	reader.run(pmu_callback)

    	net = NetTrigger()
	net.runTest(BW[i])
	time.sleep(TEST_TIME)
	net.stop()
        reader.wait()
        reader.finish()
        mm.stop()

	net_pwr.append(np.mean(np.array(pmu_callback.train_data)))
	pmu_callback.train_data = []
	print "Test of bw %d: avg network pwr is %f" %(BW[i], net_pwr[i])

    # Create dataset to train the model again in case needed
    print("Measurement Done")

    bw_array = np.array(BW)
    power_array = np.array(net_pwr)
    data_matrix = np.zeros((bw_array.shape[0], 2))
    data_matrix[:, 0] = bw_array[:]
    data_matrix[:, 1] = power_array[:]

    save_csv("measurement_"+VERSION+".csv", ["bandwidth", "network power"], data_matrix)
    clf = LinearRegression()
    reg = clf.fit(data_matrix[:, 0], data_matrix[:, 1])
    pred = clf.predict(data_matrix[:, 0])
    score = clf.score(data_matrix[:, 0], data_matrix[:, 1])
    avgErr, maxErr = getError(pred, data_matrix[:, 1])
    print("Score: %f" %score)
    print("Error: avg: %f max: %f" %(avgErr, maxErr))

    # Save model
    new_model = "./model/model." + VERSION + "." + \
    	datetime.datetime.now().strftime("%H%M%S%m%d%Y")
    save_with_pickle(clf, new_model)
    print "model save to", new_model

    # Save coefficients
    with open("./model/model_net.txt", "a+") as f:
	f.write("\r\nBased on of %s (please refer to model_info.txt)\r\n" %filename)
	f.write("\r\nCoefficients of %s\r\n" %new_model)
	f.write("bandwidth: %s" %reg.coef_[i])
	f.write("intercept: %s" %reg.intercept_)
	f.write("\r\nScore: %f\r\n" %score)
	f.write("Error: avg: %f max: %f\r\n" %(avgErr, maxErr))

if __name__ == '__main__':
    main()


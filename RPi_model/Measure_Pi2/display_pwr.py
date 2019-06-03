from __future__ import division
import os
import sys
import time
#import numpy as np
import signal
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#import sklearn
#import cPickle as pickle
#from sklearn.linear_model import LinearRegression

# from lib.cpu_reader import PerfOnlineReader
from lib.multimeter import MultiMeter

looping = True
def sig_handler(signum, _):
    print "End of procedure"
    looping = False

#####################################################################
#def save_with_pickle(data, filename):
#    """ save data to a file for future processing"""
#    with open(filename, 'wb') as f:
#        pickle.dump(data, f)

#def load_with_pickle(filename):
#    """ load data from a file"""
#    if not os.path.exists(filename):
#        return None

#    with open(filename, 'rb') as f:
#        return pickle.load(f)

#    return None

# Save np array to csv
#def save_csv(filename, keys, data_matrix):
#    with open(filename, "w") as writer:
#        # write header
#        writer.write(','.join(keys))
#        writer.write('\n')

        # write data in each row
#        for vec in data_matrix:
#            writer.write(','.join(["{0:.2f}".format(v) for v in vec]))
#            writer.write('\n')
#####################################################################

####################################################################
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
"""
EVT_RATIO = 0.5
MAX_TIME = 50.0

def animate_plot():
    ts = np.arange(0, MAX_TIME, 0.1)
    fig = plt.figure()
    line, = plt.plot(ts, [0.0] * len(ts), color="b")

    def animate(i):
        meas_pwr_array = np.array(list(pwr_callback.train_data))
        # print(meas_pwr_array.shape)

        if len(meas_pwr_array) == 0:
            return line,

        line.set_xdata(meas_pwr_array[:,0])
        line.set_ydata(meas_pwr_array[:,1])

        return line,

    def init():
        return line,

    ani = animation.FuncAnimation(
            fig, animate, np.arange(1, 1000), init_func=init,
            interval=500, blit=True) # 1000 frames

    plt.xlim(5.0, MAX_TIME)
    plt.ylim(3.0, 6.0)
    plt.title("Power (Measurement)")
    plt.ylabel("Power (W)")
    plt.xlabel("Time (sec)")
    plt.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)

    plt.show()
"""
#def getError(pred, msr):
#    err = np.absolute(pred - msr) / msr
#    maxErr = np.amax(err)
#    avgErr = np.mean(err)
#    return avgErr, maxErr
###################################################################

###################################################################
def main():
    global looping
    signal.signal(signal.SIGINT, sig_handler)
    if len(sys.argv) > 1:
        version = sys.argv[1]
    else:
        print "Please specify a version!"
	sys.exit() 

    # Load model if exists
    # pmu_callback.model = load_with_pickle(filename)

    # Run program and
    pwr_filename = "./pwr/pwr_%s.txt" %version
    mm = MultiMeter(pwr_filename)
    mm.run(pwr_callback)

    # animate_plot()
    while looping:
	pass
    
    mm.stop()

    # Create dataset to train the model again in case needed
    print("Measurement Done")

if __name__ == '__main__':
    main()


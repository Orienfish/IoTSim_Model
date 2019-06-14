import os
import signal
import subprocess
import threading
import time

class PerfReader(object):
    def __init__(self):
        pass

    def perf_reader(self, file, callback):
        self.prev_time = None 
        self.pmu_dict = dict()
	self.callback = callback
        f = open(file, "r")
	line = f.readline()
        while line:
            line = line.strip()
            elems = line.split(",")

            time = float(elems[0])
            if "not counted" in line:
                self.digest(time, -1, -1)
                f.readline()
		continue

            val = int(elems[1])
            evt = str(elems[3])
            self.digest(time, val, evt)
	    # print(time, val, evt)
	    
	    line = f.readline()

    def digest(self, time, val, evt):
        if self.prev_time != time:
            if self.prev_time is not None:
                if not any([self.pmu_dict[key] < 0 for key in self.pmu_dict]):
                    self.callback(self.prev_time, self.pmu_dict)
		    # print self.prev_time
            self.pmu_dict = dict()

        self.prev_time = time
        self.pmu_dict[evt] = val



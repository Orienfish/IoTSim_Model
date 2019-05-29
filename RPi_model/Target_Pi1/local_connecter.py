#!/usr/bin/env python2.7
import paho.mqtt.publish as publish
import numpy as np
import time

if __name__ == '__main__':

    while True:
        with open("/home/pi/Desktop/IoTSim_Model/RPi_model/Target_Pi1/subject1.txt", "r") as f:
            for line in f:
            	publish.single("bwtest", line, hostname="192.168.1.58", port=1883)
		time.sleep(1)




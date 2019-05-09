##########################################################################
# Process the raw data, calculate avg power and total energy consumption
# Usage: python process.py filename or 
# 		 python process (will go through every file in the folder)
# Author: Orienfish
# Date: 05/07/2019
##########################################################################
# -*- coding: utf-8 -*-
# !/usr/bin/python
import sys
import os

ambient_power = 0.0496575499099

# read the time and power list from file
def read_txt(filename):
	with open(filename) as f:
		lines = f.readlines()
		lines = lines[2:] # omit first two lines
			
		# reset the list of time and power
		time = []
		power = []
		# extract time and power list
		for i in range(0, len(lines)):
			parse = lines[i].split(',')
			time.append(float(parse[1]))
			power.append(float(parse[5]))

	return time, power

# compute the total energy and avg power for this file
def compute_energy(time, power):
	prev_t = 0
	energy = 0
	for i in range(0, len(time)):
		delta_t = time[i] - prev_t
		energy += power[i] * delta_t
		prev_t = time[i] # update previous time stamp

	avgpower = energy / time[-1]
	print energy, avgpower
	return energy, avgpower 

# main
def main():
	filelist = []
	if len(sys.argv) == 2: # include file name
		filelist.append(sys.argv[1])
	else: # include every file ending with .txt in the folder
		cwd = os.getcwd()
		filelist = [f for f in os.listdir(cwd) if f.endswith(".txt")]
	# compute total energy and average power consumption for each file
	for filename in filelist:
		time, power = read_txt(filename)
		energy, avgpower = compute_energy(time, power)
		print "For filename %s: energy %f (J), avg power %f (W)" \
		% (filename, energy, avgpower)
		print "subtract ambient %f (W)" % (avgpower - ambient_power)


if __name__ == '__main__':
	main()
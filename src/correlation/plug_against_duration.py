#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	author: sanja7s
	---------------
	plot the distribution
"""
import os
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from collections import defaultdict #, OrderedDict
from matplotlib import colors
from mpl_toolkits.axes_grid import inset_locator 
import pandas as pd
matplotlib.style.use('ggplot')

IN_DIR = "../../data/jobs"
os.chdir(IN_DIR)

def read_in_data_per_job(f_in = 'jobs_plug_per_core.csv'):

	plug = []
	dur = []

	with open(f_in, 'r') as f1:
		for line in f1:
			try:
				n, job_id, n, avg_cores, n, job_len, n, p, n, \
				cpu1, n, cpu2, n, dram1, n, dram2, n, us, n, \
				sy, n, idn, n, wa, n, free, n, avg_job_cnt, n = line.strip().split('"')
			except ValueError:
				print p
			"""
			try:
				main_id, step_id = job_id.split('.')
			except ValueError as e:
				main_id = job_id
			"""
			plug.append(float(p))
			dur.append(float(job_len))

	print len(plug), len(dur)
	return plug, dur

	
def plot_data():

	x, y = read_in_data_per_job()

	fig = plt.figure()
	ax = fig.add_subplot(111)

	x = np.array(x)
	y =  np.array(y)

	pt_plug = pd.DataFrame({'plug':x})
	print(pt_plug.describe())
	pt_dur = pd.DataFrame({'duration':y})
	print(pt_dur.describe())
	
	ax.scatter(y,x,color='red',s=14.5,edgecolor='none')

	#ax.set_xscale('log')
	#ax.set_yscale('log')

	plt.xlabel('job duration')
	plt.ylabel('job plug')
	plt.grid(True)
	plt.legend(frameon=False, fontsize=14)
	plt.savefig('job_plug_against_dur.png')


def correlate_data(data):

	v1 = []
	v2 = []
	for k in data:
		v1.append(data[k][0])
		v2.append(data[k][1])

	v1 = np.array(v1)
	v2 = np.array(v2)

	print 'Cross-correlation ', np.correlate(v1, v2)
	print 'Pearson  ', np.corrcoef(v1, v2)


plot_data()
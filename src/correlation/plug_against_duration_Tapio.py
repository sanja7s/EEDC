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

def read_in_job_state(f_in = 'state_duration/state_duration_job_steps.csv'):

	job_state = defaultdict(str)

	with open(f_in, 'r') as f1:
		for line in f1:
			n, job_id, n, es, n, state, n, = line.strip().split('"')
			if 'CANCELLED' in state:
				state = 'CANCELLED'
			job_state[job_id] = state

	print set(job_state.values())
	return job_state

# from Tapio
def read_in_data_per_job(f_in = 'jobs_plug_per_core.csv'):

	job_st = read_in_job_state()

	plug = []
	dur = []

	plug_per_type = defaultdict(list)
	dur_per_type = defaultdict(list)

	with open(f_in, 'r') as f1:
		for line in f1:
			try:
				n, job_id, n, avg_cores, n, job_len, n, p, n, \
				cpu1, n, cpu2, n, dram1, n, dram2, n, us, n, \
				sy, n, idn, n, wa, n, free, n, avg_job_cnt, n = line.strip().split('"')
			except ValueError:
				print p
			
			plug.append(float(p))
			dur.append(float(job_len))

			plug_per_type[job_st[job_id]].append(float(p))
			dur_per_type[job_st[job_id]].append(float(job_len))

	#print len(plug), len(dur)
	#return plug, dur
	return plug_per_type, dur_per_type

# this node is now a bit outsider here, since i tested whteher any of the jobs running
# alone on a node is the whole within our timefrae, but they are not
def single_node_jobs_in_the_timeframe(f_in = 'all_job_end_start_time_job_ids.csv'):

	ss = ['9923129', '9917940', '9920409', '9899558', '9899559', \
	'9918157', '9917887', '9923478', '9886105', '9923898']

	#J.StartTS>=1467048960 and J.EndTS<=1467201193

	with open(f_in, 'r') as f1:
		for line in f1:
			n, job_id, n, start_TS, n, end_TS, n = line.strip().split('"')
			if job_id in ss: #and start_TS>=1467048960 and end_TS<=1467201193:
				print job_id

	
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

def plot_data_per_type():

	fig = plt.figure()
	ax = fig.add_subplot(111)

	p, d = read_in_data_per_job()

	c = {'COMPLETED':'magenta','CANCELLED':'green',\
		'TIMEOUT':'blue', 'FAILED':'red'}
	for state in d:
		print state
		x = np.array(p[state])
		y =  np.array(d[state])

		pt_plug = pd.DataFrame({'plug':x})
		print(pt_plug.describe())
		pt_dur = pd.DataFrame({'duration':y})
		print(pt_dur.describe())
	
		ax.scatter(np.log(y),np.log(x),color=c[state],s=14.5,edgecolor='none',label=state)

	#ax.set_xscale('log')
	#ax.set_yscale('log')
	#ax.set_xlim(0,1000000)
	#ax.set_ylim(0,1000000)

	plt.xlabel('log(job duration)')
	plt.ylabel('log(job plug)')
	plt.grid(True)
	handles, labels = ax.get_legend_handles_labels()
	l = ax.legend(handles, labels, loc=2)
	plt.savefig('per_state_job_plug_against_dur_7s_logpluglogdur.png')

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


#plot_data()

#single_node_jobs_in_the_timeframe()

plot_data_per_type()
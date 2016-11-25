#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	author: sanja7s
	---------------
	plot the distribution
"""
import os
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from collections import defaultdict
from matplotlib import colors
from pylab import MaxNLocator
import pylab as pl
from mpl_toolkits.axes_grid import inset_locator 
matplotlib.style.use('ggplot')

IN_DIR = "../../data/timelines"
os.chdir(IN_DIR)

font = {'family' : 'sans-serif',
		'variant' : 'normal',
		'weight' : 'light',
		'size'   : 14}

grid = {'color' : 'gray', 
		'alpha'  : 0.5,
		'linestyle' : '-.'}

lines = {'color' : 'gray'}

#xticks = {'color' : 'gray'}

matplotlib.rc('font', **font)
matplotlib.rc('grid', **grid)
matplotlib.rc('lines', **lines)
#matplotlib.rc('ticks', **ticks)

def read_in_plug_data(node):

	f_in = 'node_' + node +'_plug.csv'

	distr = defaultdict(int)
	with open(f_in, 'r') as f:
		for line in f:
			# n are irrelevant
			n, n, n, t, n, plug, n, n, n = line.strip().split('"')
			t = dt.datetime.fromtimestamp(int(t))
			plug = float(plug)
			distr[t] = plug
	return distr

def read_in_num_jobs_data(node):

	f_in = 'node_' + node +'_plug.csv'
	distr = defaultdict(int)
	with open(f_in, 'r') as f:
		for line in f:
			n, n, n, t, n, n, n, jobs_list, n6 = line.strip().split('"')
			t = dt.datetime.fromtimestamp(int(t))
			jobs = jobs_list.split(',')
			if jobs_list == "":
				distr[t] = 0
			else:
				distr[t] = len(jobs)
	return distr

def read_in_CPU_data(node):

	f_in = 'node_' + node +'_CPUMEM.csv'

	distr = defaultdict(int)
	with open(f_in, 'r') as f:
		for line in f:
			n, n, n, t, n, n, n, CPU1, n, CPU2, n, n, n, n, n = line.strip().split('"')
			t = dt.datetime.fromtimestamp(int(t))
			CPU1 = float(CPU1)
			CPU2 = float(CPU2)
			distr[t] = (CPU1, CPU2)
	return distr

def read_in_MEM_data(node):

	f_in = 'node_' + node +'_CPUMEM.csv'

	distr = defaultdict(int)
	with open(f_in, 'r') as f:
		for line in f:
			n, n, n, t, n, n, n, n, n, n, n, MEM1, n, MEM2, n = line.strip().split('"')
			t = dt.datetime.fromtimestamp(int(t))
			MEM1 = float(MEM1)
			MEM2 = float(MEM2)
			distr[t] = (MEM1, MEM2)
	return distr

def read_in_rb_data(node):

	f_in = 'node_' + node +'_rb.csv'

	distr = defaultdict(int)
	with open(f_in, 'r') as f:
		for line in f:
			n, n, n, t, n, n, n, r, n, b, n = line.strip().split('"')
			t = dt.datetime.fromtimestamp(int(t))
			r = int(r)
			b = int(b)
			distr[t] = (r, b)
	return distr	

def plot_plug_timeline(node):
	print 'Plotting plug values'
	d = read_in_plug_data(node)

	dates = d.keys()
	X = pd.to_datetime(dates)
	values = [v if v > 0 else 0 for v in d.values()]

	start_time = min(dates)
	end_time = max(dates)

	print start_time, end_time
	print min(values), max(values)
	
	fig, ax = plt.subplots()
	ax.scatter(X, values, marker='s', s=1)

	#ax.plot(X, values)

	fig.autofmt_xdate()

	ax.set_xlabel('time')
	ax.set_ylabel('plug value')

	plt.xlim(pd.to_datetime(start_time), pd.to_datetime(end_time))

	#plt.show()

	plt.savefig('plug_timeline_node_' + node + '.png')

	return fig, ax, plt

def plot_plug_timeline_v2(node):
	print 'Plotting plug values'
	d = read_in_plug_data(node)
	dates = d.keys()
	X = pd.to_datetime(dates)
	values = [v if v > 0 else 0 for v in d.values()]
	ts = pd.Series(values, index = X)
	start_time = min(dates)
	end_time = max(dates)
	print start_time, end_time
	print min(values), max(values)
	
	fig, ax = plt.subplots()
	ts.plot(color = 'darkblue')
	for tl in ax.get_yticklabels():
		tl.set_color('darkblue')
	fig.autofmt_xdate()
	ax.set_xlabel('time')
	ax.set_ylabel('plug value', color='darkblue')
	plt.xlim(pd.to_datetime(start_time), pd.to_datetime(end_time))

	ymin = 240
	ymax = 280
	if min(values) < 160:
		ymin = min(values) - 10
	if max(values) > 250:
		ymax = max(values) + 10
	plt.ylim(ymin, ymax)

	#plt.savefig(cwd + '/multiple_v2/plug_only/plug_timeline_node_' + node + '_v2.png')
	return fig, ax, plt

def plot_plug_and_num_jobs_timeline(node):
	print 'Plotting num of jobs values'
	d = read_in_num_jobs_data(node)

	dates = d.keys()
	X = pd.to_datetime(dates)
	values =  d.values()

	start_time = min(dates)
	end_time = max(dates)

	print start_time, end_time
	print min(values), max(values)

	fig, ax1, plt = plot_plug_timeline_v2(node)

	ax2 = ax1.twinx()
	ax2.scatter(X, values,
			   marker='s', color='red', s=7)

	ax2.set_ylabel('# of jobs', color='red')

	ya = ax2.get_yaxis()
	ya.set_major_locator(MaxNLocator(integer=True))

	plt.xlim(pd.to_datetime(start_time), pd.to_datetime(end_time))
	for tl in ax2.get_yticklabels():
		tl.set_color('r')

	cwd = os.getcwd()
	print cwd

	plt.savefig(cwd + '/lowest_norm_stdev/SandyBridge/num_jobs_and_plug_timeline_node_' + node + '_v2.png')

def plot_plug_and_CPUs_timeline(node):
	print 'Plotting CPUs values'
	d = read_in_CPU_data(node)
	dates = d.keys()
	X = pd.to_datetime(dates)
	values1 = []
	values2 = []
	for el in d.values():
		if el[0] > 0:
			v1 = el[0]
		else:
			v1 = 0
		values1.append(v1)
		if el[1] > 0:
			v2 = el[1]
		else:
			v2 = 0
		values2.append(v2)
	start_time = min(dates)
	end_time = max(dates)
	print start_time, end_time
	print 'Min and max CPU1 ', min(values1), max(values1)
	print 'Min and max CPU2 ', min(values2), max(values2)

	fig, ax1, plt = plot_plug_timeline_v2(node)
	ax2 = ax1.twinx()
	ts1 = pd.Series(values1, index = X)
	ax2.scatter(X, values1, marker='s', color='red', s=4, label =  'CPU1')
	#ts1.plot(color='red', label =  'CPU1')
	ts2 = pd.Series(values2, index = X)
	ax2.scatter(X, values2, marker='s', color='magenta', s=4, label =  'CPU2')
	#ts2.plot(color='magenta', label =  'CPU2')
	ax2.set_ylabel('CPU values', color='red')
	ya = ax2.get_yaxis()
	ya.set_major_locator(MaxNLocator(integer=True))
	plt.xlim(pd.to_datetime(start_time), pd.to_datetime(end_time))
	for tl in ax2.get_yticklabels():
		tl.set_color('r')
	handles, labels = ax2.get_legend_handles_labels()
	l = ax2.legend(handles, labels, loc=3)
	for text in l.get_texts():
		text.set_color('gray')
	plt.savefig('lowest_norm_stdev/SandyBridge/CPUs_plug_timeline_node_' + node + '.png')

def plot_plug_and_MEM_timeline(node):
	print 'Plotting DRAM values'
	d = read_in_MEM_data(node)

	dates = d.keys()
	X = pd.to_datetime(dates)
	values1 = [v[0] if v[0] > -1 else -1 for v in d.values()]
	values2 = [v[1] if v[1] > -1 else -1 for v in d.values()]

	start_time = min(dates)
	end_time = max(dates)

	print start_time, end_time
	print 'Min and max MEM1 ', min(values1), max(values1)
	print 'Min and max MEM2 ', min(values2), max(values2)

	fig, ax1, plt = plot_plug_timeline(node)

	ax2 = ax1.twinx()
	ax2.scatter(X, values1,
			   marker='s', color='darkgreen', s=4, label =  'DRAM1')
	ax2.scatter(X, values2,
			   marker='s', color='olive', s=4, label =  'DRAM2')

	ax2.set_ylabel('DRAM values', color='olive')

	plt.xlim(pd.to_datetime(start_time), pd.to_datetime(end_time))
	for tl in ax2.get_yticklabels():
		tl.set_color('olive')

	handles, labels = ax2.get_legend_handles_labels()
	l = ax2.legend(handles, labels, loc=1)
	for text in l.get_texts():
		text.set_color('gray')

	plt.savefig('MEM_plug_timeline_node_' + node + '.png')

def plot_plug_and_rb_timeline(node):
	print 'Plotting r b values'
	d = read_in_rb_data(node)

	dates = d.keys()
	X = pd.to_datetime(dates)
	values1 = [v[0] if v[0] > 0 else 0 for v in d.values()]
	values2 = [v[1] if v[1] > 0 else 0 for v in d.values()]

	start_time = min(dates)
	end_time = max(dates)

	print start_time, end_time
	print 'Min and max MEM1 ', min(values1), max(values1)
	print 'Min and max MEM2 ', min(values2), max(values2)

	fig, ax1, plt = plot_plug_timeline(node)

	ax2 = ax1.twinx()
	ax2.scatter(X, values1,
			   marker='s', color='tomato', s=3, label =  'r')
	ax2.scatter(X, values2,
			   marker='s', color='sage', s=3, label =  'b')

	ax2.set_ylabel('r and b values', color='sage')

	ya = ax2.get_yaxis()
	ya.set_major_locator(MaxNLocator(integer=True))

	plt.xlim(pd.to_datetime(start_time), pd.to_datetime(end_time))
	for tl in ax2.get_yticklabels():
		tl.set_color('sage')

	handles, labels = ax2.get_legend_handles_labels()
	l = ax2.legend(handles, labels, loc=1)
	for text in l.get_texts():
		text.set_color('gray')

	plt.savefig('rb_plug_timeline_node_' + node + '.png')

#plot_plug_and_num_jobs_timeline('c48')
#plot_plug_and_num_jobs_timeline('c578')

#plot_plug_and_num_jobs_timeline('c578')
#plot_plug_and_CPUs_timeline('c577')

"""
plot_plug_and_MEM_timeline('c48')
plot_plug_and_MEM_timeline('c577')

plot_plug_and_MEM_timeline('c31')
plot_plug_and_MEM_timeline('c63')

plot_plug_and_MEM_timeline('c750')
plot_plug_and_MEM_timeline('c34')
"""

"""
plot_plug_and_rb_timeline('c48')
plot_plug_and_rb_timeline('c577')

plot_plug_and_rb_timeline('c31')
plot_plug_and_rb_timeline('c63')

plot_plug_and_rb_timeline('c750')
plot_plug_and_rb_timeline('c34')
"""


"""
# for the nodes running only one job
plot_plug_timeline('c424')
plot_plug_and_num_jobs_timeline('c424')
"""



# this is for the only node that did not run any jobs
#plot_plug_and_num_jobs_timeline('c42')
#plot_plug_timeline_v2('c42')


"""
# for random nodes
for node in [ 'c31', 'c34', 'c42', 'c48', 'c63', 'c329', 'c424', \
		'c577', 'c578', 'c604', 'c672', 'c735', 'c750']:		
	#plot_plug_timeline_v2(node)
	plot_plug_and_num_jobs_timeline(node)
"""



# for the nodes running only one unique (same) job all the time
#plot_plug_timeline('c7')
#plot_plug_and_num_jobs_timeline('c7')

"""
for node in ['c9', 'c10', 'c11', 'c12', 'c13', 'c16', 'c18', 'c19', 'c20']:		
	#plot_plug_timeline_v2(node)
	#plot_plug_and_num_jobs_timeline(node)
	plot_plug_and_CPUs_timeline(node)
"""

#plot_plug_and_CPUs_timeline('c4')

"""
# these nodes have the highest normalized stdev of plug
for node in ['c849', 'c666', 'c747', 'c908', 'c658', 'c620', 'c85', 'c364']:		
	#plot_plug_timeline_v2(node)
	plot_plug_and_num_jobs_timeline(node)
	plot_plug_and_CPUs_timeline(node)
"""

"""
# these are some of the nodes that have the smallest normalized stdev of plug
# SandyBridge
for node in ['c423']:		
	#plot_plug_timeline_v2(node)
	plot_plug_and_num_jobs_timeline(node)
	plot_plug_and_CPUs_timeline(node)
"""








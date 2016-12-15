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







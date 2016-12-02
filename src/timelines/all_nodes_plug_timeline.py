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

IN_DIR = "../../data/timelines/all_TIMELINES"
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

def read_in_all_node_variables():
	f_in = 'nodedata.csv'
	distr_plug = defaultdict(float)
	distr_num_jobs = defaultdict(int)
	distr_CPU = defaultdict(tuple)
	distr_MEM = defaultdict(tuple)
	distr_rb = defaultdict(tuple)
	node_distr = defaultdict(list)
	i = 0
	TESTi = 10000
	with open(f_in, 'r') as f:
		for line in f:
			n, t, n, node, n, r, n, b, n, swpd, n, free, n,\
			buff, n, cache, n, si, n, so, n, bi, n, bo, n,\
			in1, n, cs, n, us, n, sy, n, id7s, n, wa, n,\
			st, n, cpu1, n, dram1, n, cpu2, n, dram2, n, p, n,\
			jobs_list, n, tp, n = line.split('"')

			if node not in node_distr:
				node_distr[node] = defaultdict(list)
				distr_plug[node] = defaultdict(float)
				distr_num_jobs[node] = defaultdict(int)
				distr_CPU[node] = defaultdict(tuple)
				distr_MEM[node] = defaultdict(tuple)
				distr_rb[node] = defaultdict(tuple)
			t = dt.datetime.fromtimestamp(int(t))
			jobs = jobs_list.split(',')
			"""
			i += 1
			if i == TESTi:
				return node_distr
			"""
			
			distr_plug[node][t] = float(p)
			if jobs_list == "":
				distr_num_jobs[node][t] = 0
			else:
				distr_num_jobs[node][t] = len(jobs)
			distr_CPU[node][t] = (float(cpu1), float(cpu2))
			distr_MEM[node][t] = (float(dram1), float(dram2))
			distr_rb[node][t] = (int(r), int(b))
			node_distr[node] = [distr_plug[node], distr_num_jobs[node], distr_CPU[node], \
								 distr_MEM[node], distr_rb[node]]
	return node_distr


def plot_plug_timeline(node, distr_plug):
	print 'Plotting plug values'
	d = distr_plug
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

	plt.savefig('plug/plug_timeline_node_' + node + '.png')
	return fig, ax, plt


def plot_plug_and_CPUs_timeline(node, d, distr_plug):
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

	fig, ax1, plt = plot_plug_timeline(node, distr_plug)
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
	plt.savefig('CPU_plug/CPUs_plug_timeline_node_' + node + '.png')

def plot_plug_and_MEM_timeline(node, d, distr_plug):

	dates = d.keys()
	X = pd.to_datetime(dates)
	values1 = [v[0] if v[0] > -1 else -1 for v in d.values()]
	values2 = [v[1] if v[1] > -1 else -1 for v in d.values()]

	start_time = min(dates)
	end_time = max(dates)

	print start_time, end_time
	print 'Min and max MEM1 ', min(values1), max(values1)
	print 'Min and max MEM2 ', min(values2), max(values2)

	fig, ax1, plt = plot_plug_timeline(node, distr_plug)

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

	plt.savefig('MEM/MEM_plug_timeline_node_' + node + '.png')

def plot_plug_and_rb_timeline(node, d, distr_plug):

	dates = d.keys()
	X = pd.to_datetime(dates)
	values1 = [v[0] if v[0] > 0 else 0 for v in d.values()]
	values2 = [v[1] if v[1] > 0 else 0 for v in d.values()]

	start_time = min(dates)
	end_time = max(dates)

	print start_time, end_time
	print 'Min and max MEM1 ', min(values1), max(values1)
	print 'Min and max MEM2 ', min(values2), max(values2)

	fig, ax1, plt = plot_plug_timeline(node, distr_plug)

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

	plt.savefig('rb/rb_plug_timeline_node_' + node + '.png')

def plot_plug_and_num_jobs_timeline(node, distr_num_jobs, distr_plug):
	
	d = distr_num_jobs

	dates = d.keys()
	X = pd.to_datetime(dates)
	values =  d.values()

	start_time = min(dates)
	end_time = max(dates)

	print start_time, end_time
	print min(values), max(values)

	fig, ax1, plt = plot_plug_timeline(node, distr_plug)

	ax2 = ax1.twinx()
	ax2.scatter(X, values,
			   marker='s', color='red', s=7)

	ax2.set_ylabel('# of jobs', color='red')

	ya = ax2.get_yaxis()
	ya.set_major_locator(MaxNLocator(integer=True))

	plt.xlim(pd.to_datetime(start_time), pd.to_datetime(end_time))
	for tl in ax2.get_yticklabels():
		tl.set_color('r')

	plt.savefig('n_jobs_plug/num_jobs_and_plug_timeline_node_' + node + '.png')


def plot_all():
	node_variables = read_in_all_node_variables()
	for node in node_variables:
		distr_plug = node_variables[node][0]
		distr_num_jobs = node_variables[node][1]
		distr_CPU = node_variables[node][2]
		distr_MEM = node_variables[node][3]
		distr_rb =  node_variables[node][4]

		plot_plug_timeline(node, distr_plug)
		plot_plug_and_num_jobs_timeline(node, distr_num_jobs, distr_plug)
		plot_plug_and_rb_timeline(node, distr_rb, distr_plug)
		plot_plug_and_CPUs_timeline(node, distr_CPU, distr_plug)
		plot_plug_and_MEM_timeline(node, distr_MEM, distr_plug)


plot_all()








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

IN_DIR = "../../data/nodes"
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


def create_distribution(x):

	d = defaultdict(int)
	for el in x:
		d[int(el)] += 1
	return d


def read_in_data_per_node(the_node_type):

	f_in = 'node_plug_n_jobs_variation' + the_node_type + '.csv'

	avg_plug = defaultdict(int)


	with open(f_in, 'r') as f:
		for line in f:
			node, m1, mm1, avg1, med1, stdev1, var1, \
			m2, mm2, avg2, med2, stdev2, var2 = line.split()

			avg_plug[node] = float(avg1)
			if float(avg1) == 0:
				print node

	return avg_plug

read_in_data_per_node('SandyBridge')

def plot_data(plt,lab='Haswell nodes', xlab='avg plug value', ylab = '# nodes', s=17, \
	fname = 'distr_of_node_plug.png', col='coral', the_node_type='Haswell'):

	d = create_distribution(read_in_data_per_node(the_node_type).values())

	ax = fig.add_subplot(111)

	x = np.array(d.keys())
	y =  np.array(d.values())

	pt_plug = pd.DataFrame({'avg node plug':x})
	print(pt_plug.describe())
	
	ax.scatter(x,y,color=col,s=s,edgecolor='none', label=lab)


	plt.xlabel(xlab)
	plt.ylabel(ylab)
	plt.grid(True)
	#plt.legend(frameon=False, fontsize=14, pos=2)
	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles, labels, loc=2)
	plt.grid(True)
	plt.savefig(fname)
	print 'Saved in figure ', fname

"""
fig = plt.figure()
plot_data(plt = plt, lab='Haswell nodes', xlab='avg plug value', ylab = '# nodes', s=17, \
	fname = 'distr_of_node_plug.png', col='coral', the_node_type='Haswell')
plot_data(plt = plt, lab='SandyBridge nodes', xlab='avg plug value', ylab = '# nodes', s=17, \
	fname = 'distr_of_node_plug.png', col='darkblue', the_node_type='SandyBridge')
"""




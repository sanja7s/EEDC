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
		d[int(100*el)] += 1
	return d


def read_in_data_per_node(the_node_type, the_variable):

	f_in = 'node_plug_n_jobs_variation' + the_node_type + '.csv'

	avg_var = defaultdict(float)


	with open(f_in, 'r') as f:
		for line in f:
			node, m1, mm1, avg1, med1, stdev1, var1, \
			m2, mm2, avg2, med2, stdev2, var2 = line.split()

			if the_variable == 'avg plug':
				avg_var[node] = float(avg1)
				if float(avg1) == 0:
					print node
			elif the_variable == 'avg # jobs':
				avg_var[node] = float(avg2)
				if float(avg2) == 0:
					print node
			elif the_variable == 'plug std':
				avg_var[node] = float(stdev1)
				if float(stdev1) == 0:
					print node
			elif the_variable == 'plug variance':
				avg_var[node] = float(var1)
				if float(var1) == 0:
					print node
			elif the_variable == '# jobs std':
				avg_var[node] = float(stdev2)
				if float(stdev2) == 0:
					print node
			elif the_variable == 'norm std':
				if float(avg1)== 0:
					continue
				avg_var[node] = float(stdev1)/float(avg1)
				if float(avg_var[node]) < 0.005:
					print node


	return avg_var

read_in_data_per_node('SandyBridge', 'plug')

def plot_data(plt, the_node_type='Haswell', the_variable='plug',s=17,col='coral'):

	lab=the_node_type+' nodes'
	xlab=the_variable+' value'
	ylab = '# nodes'
	fname = the_node_type +'_distr_of_node_' +the_variable+ '.png'

	if the_node_type == 'both':
		d1 = create_distribution(read_in_data_per_node('Haswell',the_variable).values())
		d2 = create_distribution(read_in_data_per_node('SandyBridge',the_variable).values())
	else:
		d = create_distribution(read_in_data_per_node(the_node_type,the_variable).values())

	ax = fig.add_subplot(111)
	if the_node_type == 'both':
		x1 = np.array(d1.keys())
		y1 =  np.array(d1.values())
		pt1 = pd.DataFrame({'node ' + the_variable:x1})
		print(pt1.describe())
		#ax.scatter(x1,y1,color='coral',s=s,edgecolor='none', label='Haswell')
		ax.plot(x1,y1,color='coral',label='Haswell')
		x2 = np.array(d2.keys())
		y2 =  np.array(d2.values())
		pt2 = pd.DataFrame({'node ' + the_variable:x2})
		print(pt2.describe())
		#ax.scatter(x2,y2,color='darkblue',s=s,edgecolor='none', label='SandyBridge')
		ax.plot(x2,y2,color='darkblue', label='SandyBridge')
	else:
		x = np.array(d.keys())
		y =  np.array(d.values())
		pt_plug = pd.DataFrame({'node ' + the_variable:x})
		print(pt_plug.describe())
		#ax.scatter(x,y,color=col,s=s,edgecolor='none', label=lab)
		ax.plot(x,y,color=col,label=lab)
		
	plt.xlabel(xlab)
	plt.ylabel(ylab)
	#ax.set_xscale('log')
	#ax.set_yscale('log')
	plt.grid(True)

	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles, labels, loc=1)
	plt.grid(True)
	plt.savefig(fname)
	print 'Saved in figure ', fname

"""
# plug
fig = plt.figure()
plot_data(plt, the_node_type='Haswell', the_variable='avg plug',s=17,col='coral')
fig = plt.figure()
plot_data(plt, the_node_type='SandyBridge', the_variable='avg plug',s=17,col='darkblue')
fig = plt.figure()
plot_data(plt, the_node_type='both', the_variable='avg plug',s=17)
"""

"""
# plug std
fig = plt.figure()
plot_data(plt, the_node_type='Haswell', the_variable='plug std',s=17,col='red')
fig = plt.figure()
plot_data(plt, the_node_type='SandyBridge', the_variable='plug std',s=17,col='darkgoldenrod')
fig = plt.figure()
plot_data(plt, the_node_type='both', the_variable='plug std',s=17)
"""

"""
# plug variance
fig = plt.figure()
plot_data(plt, the_node_type='Haswell', the_variable='plug variance',s=17,col='red')
fig = plt.figure()
plot_data(plt, the_node_type='SandyBridge', the_variable='plug variance',s=17,col='darkgoldenrod')
fig = plt.figure()
plot_data(plt, the_node_type='both', the_variable='plug variance',s=17)
"""

"""
# # jobs
fig = plt.figure()
plot_data(plt, the_node_type='Haswell', the_variable='avg # jobs',s=17,col='red')
fig = plt.figure()
plot_data(plt, the_node_type='SandyBridge', the_variable='avg # jobs',s=17,col='darkgoldenrod')
fig = plt.figure()
plot_data(plt, the_node_type='both', the_variable='avg # jobs',s=17)
"""

"""
# # jobs std
fig = plt.figure()
plot_data(plt, the_node_type='Haswell', the_variable='# jobs std',s=17,col='red')
fig = plt.figure()
plot_data(plt, the_node_type='SandyBridge', the_variable='# jobs std',s=17,col='darkgoldenrod')
fig = plt.figure()
plot_data(plt, the_node_type='both', the_variable='# jobs std',s=17)
"""

"""
# norm std
fig = plt.figure()
plot_data(plt, the_node_type='Haswell', the_variable='norm std',s=17,col='red')
fig = plt.figure()
plot_data(plt, the_node_type='SandyBridge', the_variable='norm std',s=17,col='darkgoldenrod')
fig = plt.figure()
plot_data(plt, the_node_type='both', the_variable='norm std',s=17)
"""



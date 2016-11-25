#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	author: sanja7s
	---------------
	plot the distribution
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from collections import defaultdict, OrderedDict
from matplotlib import colors
from mpl_toolkits.axes_grid import inset_locator 
#matplotlib.style.use('ggplot')

IN_DIR = "../data/plug"
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

def read_in_data(f_in = 'plug_per_job.csv'):

	distr_per_step = []
	distr_per_job = defaultdict(int)
	with open(f_in, 'r') as f:
		for line in f:
			try:
				n1, job_id, n2, plug, n3 = line.strip().split('"')

				distr_per_step.append(int(plug))
			except ValueError:
				print line
			try:
				main_id, step_id = job_id.split('.')
			except ValueError as e:
				main_id = job_id
			distr_per_job[main_id] += int(plug)

	print min(distr_per_step), max(distr_per_step)

	print min(distr_per_job.values()), max(distr_per_job.values())

	return distr_per_step
	#return distr_per_job.values()

#read_in_data()

def hist_plot_data():

	distr = read_in_data()
	plt.hist(distr)
	plt.show()

def create_distribution(x):

	d = defaultdict(int)
	for el in x:
		d[int(el)] += 1
	return d


def test_plot_data():

	distr = read_in_data()
	dd = {'plug': distr}
	data = pd.DataFrame(data=dd)

	print(data.describe())
	#data.boxplot()
	data.hist()

	plt.show()

#test_plot_data()


def plot_data(lab='', xlab='plug value in K', ylab = '# jobs', \
	fname = 'distr_of_distr_plug_per_job_step_log.eps', col='coral', \
	s=22, Move=0.00003, input_file='plug_per_job.csv'):

	d = create_distribution(read_in_data(input_file))

	d = create_distribution(d.values())

	fig = plt.figure()
	ax = fig.add_subplot(111)

	x = np.array(d.keys())
	y =  np.array(d.values())
	print 'xaxis lenght is ', np.amax(x)
	print 'yaxis lenght is ' , np.amax(y), \
	 ' and total elements are ', np.sum(y)
	mu = np.mean(x)
	sigma = np.std(x)
	median = np.median(x)
	
	ax.scatter(x+1,y,color=col,s=s,edgecolor='none')

	ax.set_xscale('log')
	ax.set_yscale('log')

	plt.xlabel(xlab)
	plt.ylabel(ylab)
	plt.grid(True)
	plt.legend(frameon=False, fontsize=14)

	def adjust_spines(ax, spines):
		for loc, spine in ax.spines.items():
			if loc in spines:
				#spine.set_position(('outward', 10))  # outward by 10 points
				spine.set_smart_bounds(False)
			else:
				spine.set_color('none')  # don't draw spine

		# turn off ticks where there is no spine
		if 'left' in spines:
			ax.yaxis.set_ticks_position('left')
		else:
			# no yaxis ticks
			ax.yaxis.set_ticks([])

		if 'bottom' in spines:
			ax.xaxis.set_ticks_position('bottom')
		else:
			# no xaxis ticks
			ax.xaxis.set_ticks([])

	adjust_spines(ax, ['left', 'bottom'])

 	textstr = '$\mu=%.2f$\n$\mathrm{m}=%.2f$\n$\sigma=%.2f$'\
 	%(mu, median, sigma)
 	# place a text box in upper left in axes coords
 	# these are matplotlib.patch.Patch properties
	ax.text(0.43+Move, 0.95, textstr, transform=ax.transAxes,\
		fontsize=14, verticalalignment='top', color=col) #bbox=props)

	plt.grid(True)
	plt.savefig(fname)
	print 'Saved in figure ', fname


plot_data()
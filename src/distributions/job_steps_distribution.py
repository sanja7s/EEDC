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
from mpl_toolkits.axes_grid import inset_locator 
#matplotlib.style.use('ggplot')

IN_DIR = "../data/jobs"
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

def read_in_data(f_in = 'all_job_ids.csv'):

	i = 0

	distr = defaultdict(int)
	with open(f_in, 'r') as f:
		for line in f:
			job_id = line.strip()[1:-1]
			try:
				main_id, step_id = job_id.split('.')
			except ValueError as e:
				main_id = job_id
			distr[main_id] += 1

	return distr.values()


def hist_plot_data():

	distr = read_in_data()
	plt.hist(distr)
	plt.show()

def create_distribution(x):

	d = defaultdict(int)
	for el in x:
		d[el] += 1
	return d

def simple_plot_data():

	d = create_distribution(read_in_data())
	#print d[0]
	d_zero = [i for i in d.keys() if d[i] == 0]
	print d_zero

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
	
	ax.scatter(x,y)

	ax.set_xscale('log')
	ax.set_yscale('log')


	plt.legend(frameon=False, fontsize=16)

	plt.show()


def test_plot_data():

	distr = read_in_data()
	dd = {'steps': distr}
	data = pd.DataFrame(data=dd)

	print(data.describe())
	#data.boxplot()
	data.hist()

	plt.show()


def plot_data(lab='', xlab='job steps', ylab = '# of jobs', \
	fname = 'all/distr_of_distr_all_job_steps.eps', col='green', \
	s=12, Move=0.00003, input_file='all_job_ids.csv'):

	d = create_distribution(read_in_data(input_file))

	d =  create_distribution(d.values())

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
	
	ax.scatter(x+1,y,color=col,s=10.5,edgecolor='none')

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
	ax.text(0.2+Move, 0.95, textstr, transform=ax.transAxes,\
		fontsize=14, verticalalignment='top', color=col) #bbox=props)


	plt.grid(True)

	plt.savefig(fname)
	print 'Saved in figure ', fname


plot_data(input_file='all_job_ids.csv')
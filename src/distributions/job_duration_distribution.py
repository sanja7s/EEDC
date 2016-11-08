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

IN_DIR = "../../data/jobs"
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

# times per step
def read_in_data(f_in = 'all_job_end_start_time.csv'):

	distr = []
	with open(f_in, 'r') as f:
		for line in f:
			et, st = line.strip().split(',')
			et = dt.datetime.fromtimestamp(int(et[1:-1]))
			st = dt.datetime.fromtimestamp(int(st[1:-1]))
			distr.append((et-st).total_seconds())
	return distr

# sum all job's steps times
def read_in_data_whole_jobs(f_in = 'all_job_end_start_time_job_ids.csv'):

	distr = defaultdict(int)
	with open(f_in, 'r') as f:
		for line in f:
			n1, job_id, n2, et, n3, st, n4 = line.strip().split('"')
			et = dt.datetime.fromtimestamp(int(et))
			st = dt.datetime.fromtimestamp(int(st))
			try:
				main_id, step_id = job_id.split('.')
			except ValueError as e:
				main_id = job_id
			assert (et-st).total_seconds() >= 0
			distr[main_id] += (et-st).total_seconds()

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

	ax.set_xlim(0, 100, auto=False)
	ax.set_ylim(0, 1300, auto=False)


	plt.legend(frameon=False, fontsize=16)

	plt.show()

def test_plot_data():

	distr = read_in_data_whole_jobs()
	#distr = read_in_data()
	dd = {'dur': distr}
	data = pd.DataFrame(data=dd)

	print(data.describe())
	#data.boxplot()
	#data.hist()

	plt.show()


	#ts = pd.DataFrame(distr)
	#ts = ts.hist()
	#ts.plot()
	#plt.show()

#test_plot_data()

def plot_data(lab='', xlab='job duration (days)', ylab = '# of job tasks (in K)', \
	fname = 'all/all_job_duration_days.eps', col='green', \
	s=12, Move=0.00003, input_file='job_end_start_time.csv'):

	d = create_distribution(read_in_data(input_file))
	#d_zero = [i for i in d.keys() if d[i] == 0]
	#print d_zero

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
	
	ax.scatter(x,y/1000,color=col,s=s,edgecolor='none',label=lab)

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

	def inset(x, y, col):
		inset_axes = inset_locator.inset_axes(ax,
							   width = '44%', 
							   height = '44%',
							   loc=1)

		adjust_spines(inset_axes, ['left', 'bottom'])

		pos1 = inset_axes.get_position() # get the original position 
		pos2 = [pos1.x0, pos1.y0 - 0.3, pos1.width/2.0, pos1.height/2.0] 
		inset_axes.set_position(pos2)

		inset_axes.scatter(x+1,y,color=col,s=10.5,edgecolor='none')
		#inset_axes.set_xlim(10, 100, auto=True)
		#inset_axes.set_ylim(1, 1300, auto=True)
		inset_axes.set_ylabel('')
		inset_axes.set_xlabel('')
		inset_axes.set_xscale('log')
		inset_axes.set_yscale('log')

	inset(x,y,col)

	plt.grid(True)

	plt.savefig(fname)
	print 'Saved in figure ', fname

def plot_data_whole_jobs(lab='', xlab='job duration (sec)', ylab = '# of jobs', \
	fname = 'all/all_job_duration_sec.eps', col='mediumvioletred', \
	s=14, Move=0.00003, input_file='all_job_end_start_time_job_ids.csv'):

	d = create_distribution(read_in_data_whole_jobs(input_file))
	#d_zero = [i for i in d.keys() if d[i] == 0]
	#print d_zero

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
	
	ax.scatter(x+1,y,color=col,s=s,edgecolor='none',label=lab)

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
	ax.text(0.46+Move, 0.95, textstr, transform=ax.transAxes,\
		fontsize=14, verticalalignment='top', color=col) #bbox=props)

	plt.grid(True)

	plt.savefig(fname)
	print 'Saved in figure ', fname


plot_data_whole_jobs()
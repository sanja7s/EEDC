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

IN_DIR = "../../data/users/job_dur_per_user"
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
def read_in_data(f_in = 'job_dur_per_user.csv'):

	user_jobs = defaultdict(list)

	distr = defaultdict(int)
	with open(f_in, 'r') as f:
		for line in f:
			n1, job_id, n2, et, n3, user, n4 = line.strip().split('"')
			et = int(et)
			try:
				main_id, step_id = job_id.split('.')
			except ValueError as e:
				main_id = job_id
				user_jobs[user].append(main_id)

			distr[main_id] += et

	print 'Users', len(user_jobs)

	user_tot_job_dur = defaultdict(int)
	for user in user_jobs:
		for job_id in user_jobs[user]:
			user_tot_job_dur[user] += distr[job_id]

	print user_tot_job_dur

	user_avg_job_dur = defaultdict(int)
	for user in user_jobs:
		cnt = 0.0
		for job_id in user_jobs[user]:
			user_avg_job_dur[user] += distr[job_id]
			cnt += 1
		user_avg_job_dur[user] /= float(cnt)

	print user_avg_job_dur

	#return user_tot_job_dur.values()
	return user_avg_job_dur.values()
	


def hist_plot_data():

	distr = read_in_data()
	plt.hist(distr)
	plt.show()

def create_distribution(x):

	d = defaultdict(int)
	for el in x:
		d[int(el/360)] += 1
	return d

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

def plot_data(lab='', xlab='avg job duration (hr)', ylab = '# of users', \
	fname = 'avg_job_dur_per_user_hr.png', col='red', \
	s=12, Move=0.00003):

	d = create_distribution(read_in_data())

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

	plt.xlabel(xlab)
	plt.ylabel(ylab)
	plt.grid(True)
	plt.legend(frameon=False, fontsize=14)

	ax.set_xscale('log')

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

	inset(x,y+1,col)

	plt.grid(True)

	plt.savefig(fname)
	print 'Saved in figure ', fname




plot_data()
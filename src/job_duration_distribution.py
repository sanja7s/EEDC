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
matplotlib.style.use('ggplot')

IN_DIR = "../data/jobs"
os.chdir(IN_DIR)

def read_in_data():

	distr = []
	f_in = 'job_end_start_time.csv'
	with open(f_in, 'r') as f:
		for line in f:
			et, st = line.strip().split(',')
			et = dt.datetime.fromtimestamp(int(et[1:-1]))
			st = dt.datetime.fromtimestamp(int(st[1:-1]))
			distr.append((et-st).total_seconds())
	return distr

def hist_plot_data():

	distr = read_in_data()
	plt.hist(distr)
	plt.show()

def create_distribution(x):

	d = defaultdict(int)
	for el in x:
		d[el/60] += 1
	return d

def plot_data():

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

	ax.scatter(x,y)

	ax.set_xscale('log')
	#ax.set_yscale('log')

	plt.legend(frameon=False, fontsize=16)

	plt.show()


	#ts = pd.DataFrame(distr)
	#ts = ts.hist()
	#ts.plot()
	#plt.show()

def test_plot_data():

	distr = read_in_data()
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

plot_data()
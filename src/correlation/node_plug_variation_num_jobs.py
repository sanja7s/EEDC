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

def read_in_node_types():
	f_in = 'node_types.csv'
	node_types = defaultdict(int)
	with open(f_in, 'r') as f:
		for line in f:
			# n are irrelevant
			n, node, n, t, n = line.strip().split('"')
			node_types[node] = t
	return node_types


def read_in_data(the_node_type):
	f_in = 'node_plug_jobslist.csv'
	distr_plug = defaultdict(list)
	distr_n_jobs = defaultdict(list)
	node_types = read_in_node_types()
	i = 0
	with open(f_in, 'r') as f:
		for line in f:
			# n are irrelevant
			n, node, n, plug, n, jobs_list, n = line.strip().split('"')
			if node_types[node] <> the_node_type:
				continue
			plug = float(plug)
			distr_plug[node].append(plug)
			if jobs_list == "":
				distr_n_jobs[node].append(0)
			else:
				jobs = jobs_list.split(',')
				distr_n_jobs[node].append(len(jobs))
			i += 1
			"""
			if i == 100000:
				print distr_n_jobs	
				return distr_plug, distr_n_jobs		
			"""	
	return distr_plug, distr_n_jobs

#read_in_data()

def save_data_per_node(the_node_type):

	def stats(d1):
		dd1 = np.array(d1)
		m1 = np.min(dd1)
		mm1 = np.max(dd1)
		avg1 = np.mean(dd1)
		med1 = np.median(dd1)
		stdev1 = np.std(dd1)
		var1 = np.var(dd1)
		return m1, mm1, avg1, med1, stdev1, var1

	d1, d2 = read_in_data(the_node_type)
	f_out = 'node_plug_n_jobs_variation' + the_node_type + '.csv'
	with open(f_out, 'w') as f:
		for node in d1:
			m1, mm1, avg1, med1, stdev1, var1 = stats(d1[node])
			m2, mm2, avg2, med2, stdev2, var2 = stats(d2[node])
			f.write(str(node) + '\t' \
				+ str(m1) + '\t' + str(mm1) + '\t' + str(avg1) + '\t' + str(med1) \
				+ '\t' + str(stdev1) + '\t' + str(var1) + '\t' \
				+ str(m2) + '\t' + str(mm2) + '\t' + str(avg2) + '\t' + str(med2) \
				+ '\t' + str(stdev2) + '\t' + str(var2) + '\n' )

#save_data_per_node(the_node_type='SandyBridge')

def find_correlations(the_node_type):
	f_in = 'node_plug_n_jobs_variation' + the_node_type + '.csv'
	M = []
	with open(f_in, 'r') as f:
		for line in f:
			node, min1, max1, avg1, med1, std1, var1, min2, max2, avg2, med2, std2, var2 = line.split('\t')
			M.append([float(min1), float(max1), float(avg1), float(med1), float(std1), float(var1)\
			 , float(min2), float(max2), float(avg2), float(med2), float(std2), float(var2)])
	M = np.array(M)
	print M.shape
	#print M
	M = np.transpose(M)
	print M.shape
	cor_M = np.corrcoef(M)
	f_out = 'cor_M_full' + the_node_type +'.tab'
	with open(f_out, 'w') as fo:
		for row in cor_M:
			for el in row:
				fo.write('%.3f \t' % (el))
			fo.write('\n')


find_correlations(the_node_type='SandyBridge')













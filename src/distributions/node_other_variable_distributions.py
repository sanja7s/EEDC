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
from collections import defaultdict, OrderedDict
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
matplotlib.rc('font', **font)
matplotlib.rc('grid', **grid)
matplotlib.rc('lines', **lines)
#matplotlib.rc('ticks', **ticks)

def create_distribution(x):

	d = defaultdict(int)
	for el in x:
		d[int(el)] += 1
	return d

def create_distribution_mem_GB(x):
	d = defaultdict(int)
	for el in x:
		# blocks * 1024 for bytes 

		# bytes / 1073741824 for GB
		d[int(el*1024/1073741824)] += 1
	return d

def create_distribution_mem_MB(x):
	d = defaultdict(int)
	for el in x:
		# blocks * 1024 for bytes 

		# bytes / 1073741824 for MB
		d[int(el*1024/1048576)] += 1

	return d

# here we read in all the variables assigned to the node,
# including the vmstat output
def read_in_data_per_node(the_node_type):
	f_in = 'nodedata.csv'
	avg_var = defaultdict(int)
	i = 0
	TESTi = 10000
	with open(f_in, 'r') as f:
		for line in f:
			n, ts, n, node, n, r, n, b, n, swpd, n, free, n,\
			buff, n, cache, n, si, n, so, n, bi, n, bo, n,\
			in1, n, cs, n, us, n, sy, n, id7s, n, wa, n,\
			st, n, cpu1, n, dram1, n, cpu2, n, dram2, n, p, n,\
			jobs, n, t, n = line.split('"')

			if t <> the_node_type:
				continue

			if node not in avg_var:
				avg_var[node] = defaultdict(list)

			# the data are output from mysql
			# and we read them in the same order
			# we have 7 * 3 + 1 variables
			avg_var[node]['r'].append(float(r))
			avg_var[node]['b'].append(float(b))
			avg_var[node]['swpd'].append(float(swpd))
			avg_var[node]['free'].append(float(free))
			avg_var[node]['buff'].append(float(buff))
			avg_var[node]['cache'].append(float(cache))
			avg_var[node]['si'].append(float(si))

			avg_var[node]['so'].append(float(so))
			avg_var[node]['bi'].append(float(bi))
			avg_var[node]['bo'].append(float(bo))
			avg_var[node]['in1'].append(float(in1))
			avg_var[node]['cs'].append(float(cs))
			avg_var[node]['us'].append(float(us))
			avg_var[node]['sy'].append(float(sy))

			avg_var[node]['id7s'].append(float(id7s))
			avg_var[node]['wa'].append(float(wa))
			avg_var[node]['st'].append(float(st))
			avg_var[node]['cpu1'].append(float(cpu1))
			avg_var[node]['dram1'].append(float(dram1))
			avg_var[node]['cpu2'].append(float(cpu2))
			avg_var[node]['dram2'].append(float(dram2))

			avg_var[node]['p'].append(float(p))

			for k1 in avg_var[node].keys():
				for k2 in avg_var[node].keys():
					assert len(avg_var[node][k1]) == len(avg_var[node][k1])
			"""
			i += 1
			if i == TESTi:
				return avg_var
			"""
	return avg_var

# from the given timeline data, we find averages: 
# mean, median and (norm) stdev
def calculate_avg_data(d):
	# this functions does the averages from one timeline
	def stats(l):
		l = np.array(l)
		# check against divison by zero
		if np.mean(l) > 0:
			return np.mean(l), np.median(l), np.std(l), np.std(l)/np.mean(l)
		return np.mean(l), np.median(l), np.std(l), 0
	# we save the output in the dict a
	# holding for each node a list of 4 averages
	a = OrderedDict()
	for node in d:
		a[node] = OrderedDict()
		for k in d[node]:
			avg, med, stdev, norm_stdev = stats(d[node][k])
			a[node][k] = [avg, med, stdev, norm_stdev]
	return a

def save_avg_data(the_node_type, the_avg_type, a):
	# each average type in one file with 22 variables
	# as this is how we can compare the nodes best then
	f_out = 'FIN_' + the_node_type + '_nodes_' + the_avg_type + '_values_FIN.csv'

	test_node = a.keys()[0]
	with open(f_out, 'w') as f:
		# the data headline (column names), happy to found a way to 
		# format print a list
		f.write("'{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', \
				'{7}', '{8}', '{9}', '{10}', '{11}', '{12}', \
				'{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}',\
				'{20}', '{21}', '{22}' \n".format('node', *(a[test_node].keys())))

		for node in a:
			if the_avg_type == 'mean':
				i = 0
			elif the_avg_type == 'median':
				i = 1
			elif the_avg_type == 'stdev':
				i = 2
			elif the_avg_type == 'norm_stdev':
				i = 3
			[m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, \
			m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22]\
			= [a[node][x][i] for x in a[node].keys()]

			f.write("'{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', \
				'{7}', '{8}', '{9}', '{10}', '{11}', '{12}',\
				'{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}',\
				'{20}', '{21}', '{22}' \n".format(node, m1, m2, m3, m4, \
				m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16,\
				 m17, m18, m19, m20, m21, m22))

def save_all():
	for the_node_type in ['Haswell', 'SandyBridge']:
		d =  read_in_data_per_node(the_node_type)
		a = calculate_avg_data(d)
		for the_avg_type in ['mean', 'median', 'stdev', 'norm_stdev']:
			save_avg_data(the_node_type, the_avg_type, a)

#save_all()

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

def read_in_data_2(the_node_type, the_avg_type):
	
	f_out = 'FIN_' + the_node_type + '_nodes_'+the_avg_type+'_values_FIN.csv'

	a = defaultdict(list)

	with open(f_out, 'r') as f:
		headline = f.readline()
		h = headline.split('\'')
		h1 = [x for x in h if x.strip() != ',' and x.strip() != '']
		h1 = h1[1:]
		#print h1
		for line in f:
			n, node, n, m1, n, m2, n, m3, n, m4, n, m5, n,\
			 m6, n, m7, n, m8, n, m9, n, m10, n, m11, \
			n, m12, n, m13, n, m14, n, m15, n, m16, n, m17,\
			 n, m18, n, m19, n, m20, n, m21, n, m22, n\
			= line.split('\'')

			avg_values = [m1, m2, m3, m4, m5, m6, m7, m8, m9,\
				 m10, m11, m12, m13, m14, m15, m16,\
				 m17, m18, m19, m20, m21, m22]
	
			for k in h1:
				a[k].append(float(avg_values[h1.index(k)]))

	return a

def plot_data_2(a, b=None, the_node_type='Haswell', the_avg_type='mean', \
		the_variable='p',s=17,col='coral'):

	fig = plt.figure()
	ax = fig.add_subplot(111)

	lab=the_node_type + ' nodes'
	if the_variable in ['id7s', 'us', 'sy', 'wa']:
		xlab=the_variable + ' value (in % of CPU time)'
	else:
		xlab=the_variable + ' value'
	ylab = '# nodes'
	fname = 'other_variables_7s/' + the_node_type + '/' \
			+ the_node_type +'_distr_of_node_' + \
			the_avg_type + '_' + the_variable + '.png'

	if the_node_type == 'both':
		if the_variable in ['free', 'cache']:
			d1 = create_distribution_mem_GB(a)
			d2 = create_distribution_mem_GB(b)
			xlab=the_variable + ' value' + ' (in GB)'
		elif the_variable in ['swpd', 'buff']:
			d1 = create_distribution_mem_MB(a)
			d2 = create_distribution_mem_MB(b)
			xlab=the_variable + ' value' + ' (in MB)'
		else:
			d1 = create_distribution(a)
			d2 = create_distribution(b)
	else:
		if the_variable in ['free', 'cache']:
			d = create_distribution_mem_GB(a)
			xlab=the_variable + ' value' + ' (in GB)'
		elif the_variable in ['swpd', 'buff']:
			d = create_distribution_mem_MB(a)
			xlab=the_variable + ' value' + ' (in MB)'
		else:
			d = create_distribution(a)

	
	if the_node_type == 'both':
		x1 = np.array(d1.keys())
		y1 =  np.array(d1.values())
		pt1 = pd.DataFrame({'node ' + the_variable:x1})
		print(pt1.describe())
		ax.scatter(x1,y1,color='coral',s=s,edgecolor='none', label='Haswell')
		#ax.plot(x1,y1,color='coral',label='Haswell')
		x2 = np.array(d2.keys())
		y2 =  np.array(d2.values())
		pt2 = pd.DataFrame({'node ' + the_variable:x2})
		print(pt2.describe())
		ax.scatter(x2,y2,color='darkblue',s=s,edgecolor='none', label='SandyBridge')
		#ax.plot(x2,y2,color='darkblue', label='SandyBridge')
	else:
		x = np.array(d.keys())
		y =  np.array(d.values())
		pt_plug = pd.DataFrame({'node ' + the_variable:x})
		print(pt_plug.describe())
		ax.scatter(x,y,color=col,s=s,edgecolor='none', label=lab)
		#ax.plot(x,y,color=col,label=lab)
		
	plt.xlabel(xlab)
	plt.ylabel(ylab)
	if the_variable in ['swpd', 'buff', 'bi', 'bo']:
		ax.set_xscale('symlog')
		ax.set_yscale('symlog')
		plt.xlim(xmin=-1)
		plt.ylim(ymin=-1)
	plt.grid(True)

	handles, labels = ax.get_legend_handles_labels()
	ax.legend(handles, labels, loc=1)
	plt.grid(True)
	plt.savefig(fname)
	print 'Saved in figure ', fname


def plot_all():
	
	for the_node_type in ['SandyBridge']:
		for the_avg_type in ['mean', 'median', 'stdev', 'norm_stdev']:
			a = read_in_data_2(the_node_type, the_avg_type)
			for k in a.keys():
				plot_data_2(a[k], None, the_node_type, the_avg_type, \
					the_variable=k,s=17,col='coral')
	# both			
	for the_avg_type in ['mean', 'median', 'stdev', 'norm_stdev']:
		a = read_in_data_2('Haswell', the_avg_type)
		b = read_in_data_2('SandyBridge', the_avg_type)
		for k in a.keys():
			plot_data_2(a[k], b[k], 'both', the_avg_type, \
				the_variable=k,s=17,col='coral')
	
def plot_one(the_variable):
	
	for the_node_type in ['SandyBridge', 'Haswell']:
		for the_avg_type in ['mean', 'median', 'stdev', 'norm_stdev']:
			a = read_in_data_2(the_node_type, the_avg_type)
			plot_data_2(a[the_variable], None, the_node_type, the_avg_type, \
					the_variable=the_variable,s=17,col='coral')
	# both			
	
	for the_avg_type in ['mean', 'median', 'stdev', 'norm_stdev']:
		a = read_in_data_2('Haswell', the_avg_type)
		b = read_in_data_2('SandyBridge', the_avg_type)
		plot_data_2(a[the_variable], b[the_variable], 'both', the_avg_type, \
				the_variable=the_variable,s=17,col='coral')
	

#plot_all()
plot_one('r')
plot_one('b')
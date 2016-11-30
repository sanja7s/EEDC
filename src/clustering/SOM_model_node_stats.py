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

IN_DIR = "../../data/nodes/SOM_clustering"
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

def read_in_SOM_output():
	f_in = 'node_assigned_classes'
	node_classes = defaultdict(int)
	with open(f_in, 'r') as f:
		# headline
		f.readline()
		for line in f:
			node_id, node_class = line.split('\t')
			node_classes[node_id] = int(node_class)
	return node_classes

def read_in_node_id_mapping():
	f_in = 'node_ids'
	node_ids =  defaultdict(int)
	with open(f_in, 'r') as f:		
		# headline
		f.readline()
		for line in f:
			node_id, node = line.split('\t')
			node_ids[node_id] = node.strip()[1:-1]
	return node_ids

def read_in_node_types():
	f_in = '../node_types.csv'
	node_types =  defaultdict(str)
	with open(f_in, 'r') as f:		
		for line in f:
			node, node_type = line.split(',')
			node_types[node[1:-1]] = node_type.strip()[1:-1]
	return node_types

def find_nodes_per_class():
	node_classes = read_in_SOM_output()
	node_ids = read_in_node_id_mapping()
	the_node_classes =  defaultdict(list)
	for node_id in node_ids:
		the_node_classes[node_classes[node_id]].append(node_ids[node_id])

	for the_class in the_node_classes:
		print the_class, len(the_node_classes[the_class])
	return the_node_classes

def find_node_types_per_class():
	node_classes = find_nodes_per_class()
	node_types = read_in_node_types()

	node_types_per_class = defaultdict(list)

	for the_class in node_classes:
		for the_node in node_classes[the_class]:
			node_types_per_class[the_class].append(node_types[the_node])

	from collections import Counter

	for the_class in node_types_per_class:
		print the_class, Counter(node_types_per_class[the_class])

	return node_types_per_class

find_node_types_per_class()

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


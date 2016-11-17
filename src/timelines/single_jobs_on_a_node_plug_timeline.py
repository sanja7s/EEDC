#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	author: sanja7s
	---------------
	plot the distribution
"""
import os
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from collections import defaultdict
from matplotlib import colors
from mpl_toolkits.axes_grid import inset_locator 
import networkx as nx


IN_DIR = "../../data/nodes/"
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


def read_in_single_jobs_on_a_node_data():

	f_in = 'all_nodes_plug.csv'

	distr = defaultdict(int)

	with open(f_in, 'r') as f:
		for line in f:
			n, node, n, t, n, plug, n, jobs_list, n = line.strip().split('"')
			t = dt.datetime.fromtimestamp(int(t))
			jobs = jobs_list.split(',')
			if distr[node] == 0:
				if len(jobs) > 1:
					distr[node] = 1

	sol = [x for x in distr.keys() if distr[x] == 0]
	print len(sol)
	print sol
	return distr


read_in_single_jobs_on_a_node_data()

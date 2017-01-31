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

def node_type(node):
	"""
	Node numbering scheme is as follows:
	[c1-c309] [c321-c478] old compute nodes (Sandy Bridge)
	[c579-c628],[c639-c985] new compute nodes (Haswell) -- 50 + 346

	Special nodes:
	c309-c320 old big memory nodes (Sandy Bridge)
	c629-c638 new big memory nodes (Haswell) -- 10
	c577,c578 old huge memory nodes (HP Proliant DL560)
	c986-c989 new huge memory nodes (Dell R930)

	TOTAL Haswell 406
	"""
	if node.strip() in ['c'+str(x) for x in range(1, 310)]:
		return 'SandyBridge'
	if node.strip() in ['c'+str(x) for x in range(321, 479)]:
		return 'SandyBridge'
	if node.strip() in ['c'+str(x) for x in range(579, 629)]:
		return 'Haswell'
	if node.strip() in ['c'+str(x) for x in range(639, 986)]:
		return 'Haswell'

	if node.strip() in ['c'+str(x) for x in range(309, 321)]:
		return 'SandyBridgeBig'
	if node.strip() in ['c'+str(x) for x in range(629, 639)]:
		return 'HaswellBig'	

	if node.strip() in ['c'+str(x) for x in range(577, 579)]:
		return 'OldHuge'
	if node.strip() in ['c'+str(x) for x in range(986, 990)]:
		return 'NewHuge'

def read_in_plug_data_corrected_type():

	f_in = 'node_types_plug.csv'
	i = 0
	distr = defaultdict(list)
	with open(f_in, 'r') as f:
		for line in f:
			# n are irrelevant
			n, node, n, n, n, plug, n, t, n = line.strip().split('"')
			plug = float(plug)
			t = node_type(node)
			distr[t].append(plug)

	return distr

def read_in_plug_data():

	f_in = 'node_types_plug.csv'
	i = 0
	distr = defaultdict(list)
	with open(f_in, 'r') as f:
		for line in f:
			# n are irrelevant
			n, n, n, n, n, plug, n, t, n = line.strip().split('"')
			plug = float(plug)
			distr[t].append(plug)

	return distr

def box_plot_plug_per_type():

	fig, axes = plt.subplots(nrows=1, ncols=2)

	d = read_in_plug_data()
	d = dict(d)
	#d1 = [d[k] for k in d.keys() if k == 'SandyBridgeBig'][0]
	#print d1
	#pt1 = pd.DataFrame({'SandyBridgeBig': d1})
	#print(pt1.describe())
	d2 = [d[k] for k in d.keys() if k == 'SandyBridge'][0]
	pt2 = pd.DataFrame({'SandyBridge': d2})
	print(pt2.describe())
	d3 = [d[k] for k in d.keys() if k == 'Haswell'][0]
	pt3 = pd.DataFrame({'Haswell': d3})
	print(pt3.describe())
	#d4 = [d[k] for k in d.keys() if k == 'HaswellBig'][0]
	#pt4 = pd.DataFrame({'HaswellBig': d4})
	#print(pt4.describe())
	#d5 = [d[k] for k in d.keys() if k == 'NA'][0]
	#pt5 = pd.DataFrame({'NA': d5})
	#print(pt5.describe())
	#d6 = [d[k] for k in d.keys() if k == 'OldHuge'][0]
	#pt6 = pd.DataFrame({'OldHuge': d6})
	#print(pt6.describe())

	#ax = pt1.plot(kind='box', ax=axes[0])
	#ax.set_ylim(0,685)
	ax = pt2.plot(kind='box', ax=axes[0])
	ax.set_ylim(0,400)
	ax = pt3.plot(kind='box', ax=axes[1])
	ax.set_ylim(0,400)
	#ax = pt4.plot(kind='box', ax=axes[3])
	#ax.set_ylim(0,685)
	#ax = pt5.plot(kind='box', ax=axes[4])
	#ax.set_ylim(0,685)
	#ax = pt6.plot(kind='box', ax=axes[5])
	#ax.set_ylim(0,685)
	plt.savefig('consumption_per_Haswell_SandyBridge_node_type.png')
	plt.show()


box_plot_plug_per_type()
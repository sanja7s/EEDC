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

def parse_node_list(nl):
	node_type = nl[0]
	node_ids = nl[2:-1].split(',')
	nnl = []
	for el in node_ids:
		if '-' in el:
			start_of_range, end_of_range = el.split('-')
			for i in range(int(start_of_range), int(end_of_range)+1):
				nnl.append(node_type + str(i))
		else:
			nnl.append(node_type + el)
	return nnl

def edge_list_from_node_list(el, l):
	nn = len(l)
	for i in range(nn):
		for j in range(i, nn):
			s = tuple(sorted((l[i], l[j])))
			el[s] += 1

# times per step
def read_in_data_and_save_edge_list(f_in = 'job_node_list_network.csv', \
	f_out='co-occurrence_edge_list.csv'):

	edge_list = defaultdict(int)
	with open(f_in, 'r') as f:
		for line in f:
			n1, job_id, n2, num_nodes, n3, node_list, n4 = line.strip().split('"')

			parsed_node_list = parse_node_list(node_list)
			edge_list_from_node_list(edge_list, parsed_node_list)

	i = 0
	with open(f_out, 'w') as fo:
		print len(edge_list)
		for el in edge_list:
			#print el[0], el[1], edge_list[el]
			fo.write(str(el[0]) + ',' +  str(el[1]) + ',' + str(edge_list[el]) + '\n')
			i += 1

	print '%d lines saved in the file %s ' % (i, f_out)

#read_in_data_and_save_edge_list()

def analyze_graph_from_edge_list(f_in='co-occurrence_edge_list.csv', \
		f_out_cc = 'node_conn_comps.tsv'):
	G = nx.read_edgelist(f_in, delimiter=',', create_using=nx.Graph(), data=(('weight',int),))
	print nx.info(G)

	conn_comp = sorted(nx.connected_components(G), key = len, reverse=True)
	print 'Num of connected components ', len(conn_comp)

	fcc = open(f_out_cc, 'w')
	conn_comp_node_list = defaultdict(list)
	i = 0
	for comp in conn_comp:
		print len(comp)
		for node in comp:
			fcc.write(node + '\t')
		i += 1
		fcc.write('\n')
	print 'Processed components ', i

	
analyze_graph_from_edge_list()
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	author: sanja7s
	---------------
	find nodes running no jobs during our time if any: NOT ANY
"""
import os
import pandas as pd
from collections import defaultdict


IN_DIR = "../../data/nodes/"
os.chdir(IN_DIR)


def read_in_no_jobs_on_a_node_data():

	f_in = 'all_nodes_plug.csv'

	distr = defaultdict(int)

	with open(f_in, 'r') as f:
		for line in f:
			n, node, n, t, n, plug, n, jobs_list, n = line.strip().split('"')
			if distr[node] == 0:
				if jobs_list != "":
					distr[node] = 1

	sol = [x for x in distr.keys() if distr[x] == 0]
	print len(sol)
	print sol
	return distr


read_in_no_jobs_on_a_node_data()

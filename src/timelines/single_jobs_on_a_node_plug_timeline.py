#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	author: sanja7s
	---------------
	find nodes running only one job during our time if any
"""
import os
import pandas as pd
from collections import defaultdict


IN_DIR = "../../data/nodes/"
os.chdir(IN_DIR)


def read_in_single_jobs_on_a_node_data():

	f_in = 'all_nodes_plug.csv'

	distr = defaultdict(int)
	old_job = ''
	with open(f_in, 'r') as f:
		for line in f:
			n, node, n, t, n, plug, n, jobs_list, n = line.strip().split('"')
			jobs = jobs_list.split(',')
			if distr[node] == 0:
				if len(jobs) > 1 or jobs_list == "" or jobs[0] == 'NA':
					distr[node] = 1
				else:
					if old_job == '':
						old_job = jobs[0]
					else:
						try:
							assert old_job == jobs[0]
						except AssertionError:
							print old_job, jobs[0]
							distr[node] = 1

	sol = [x for x in distr.keys() if distr[x] == 0]
	print len(sol)
	print sol
	return distr


read_in_single_jobs_on_a_node_data()

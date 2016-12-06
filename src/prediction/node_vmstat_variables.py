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
from collections import defaultdict, OrderedDict

IN_DIR = "../../data/nodes/prediction/weka"
os.chdir(IN_DIR)

def node_type(node):
	"""
	Node numbering scheme is as follows:
	[c1-c309] [c321-c478] old compute nodes (Sandy Bridge)
	[c579-c628],[c639-c985] new compute nodes (Haswell)

	Special nodes:
	c309-c320 old big memory nodes (Sandy Bridge)
	c629-c638 new big memory nodes (Haswell)
	c577,c578 old huge memory nodes (HP Proliant DL560)
	c986-c989 new huge memory nodes (Dell R930)
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

#print len(read_in_node_types())

def read_in_data_per_node_and_save_arff(node='c28'):
	
	f_in = 'node_' + node + '_vmstat_timestamp.csv'
	f_out = 'node_' + node + '_vmstat_timestamps.arff'

	arff_header = \
	"@RELATION " + node + "_traintest" + '\n' + '\n' + \
	"@ATTRIBUTE Timestamp DATE \"yyyy-MM-dd HH:mm:ss\" " + '\n' + \
	"@ATTRIBUTE r REAL" + '\n' + \
	"@ATTRIBUTE b REAL" + '\n' + \
	"@ATTRIBUTE swpd REAL" + '\n' + \
	"@ATTRIBUTE free REAL" + '\n' + \
	"@ATTRIBUTE cache REAL" + '\n' + \
	"@ATTRIBUTE si REAL" + '\n' + \
	"@ATTRIBUTE so REAL" + '\n' + \
	"@ATTRIBUTE bi REAL" + '\n' + \
	"@ATTRIBUTE bo REAL" + '\n' + \
	"@ATTRIBUTE in1 REAL" + '\n' + \
	"@ATTRIBUTE cs REAL" + '\n' + \
	"@ATTRIBUTE us REAL" + '\n' + \
	"@ATTRIBUTE sy REAL" + '\n' + \
	"@ATTRIBUTE id REAL" + '\n' + \
	"@ATTRIBUTE wa REAL" + '\n' + \
	"@ATTRIBUTE plug REAL" + '\n' + '\n' + \
	"@DATA" + '\n' 

	with open(f_in, 'r') as f:
		with open(f_out, 'w') as fo:
			fo.write(arff_header)
			for line in f:
				ts, r, b, swpd, free, cache, si, so, bi, bo, in1, cs, us, sy, id7, wa, plug \
				 = line.split(',')

				t = dt.datetime.fromtimestamp(int(ts))

				fo.write("\"{0}\",{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16}"\
					.format(t, r, b, swpd, free, cache, si, so, bi, bo, in1, cs, us, sy, id7, wa, plug))

		
read_in_data_per_node_and_save_arff()
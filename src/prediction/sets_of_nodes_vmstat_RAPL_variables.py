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
from numpy import random

IN_DIR = "../../data/prediction/Haswell10/"
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

def test_RAPL_negatives(nodeset = "Haswell10"):

	f_in = 'node_' + nodeset + '_vmstat_RAPL_timestamp.csv'
	f_out = 'cleaned_node_' + nodeset + '_vmstat_RAPL_timestamp.csv'

	i = 0
	j = 0

	with open(f_in, 'r') as f:
		with open(f_out, 'w') as fo:
			for line in f:
				ts, r, b, swpd, free, cache, si, so, bi, bo, in1, cs, us, sy, id7, wa, c1, c2, d1, d2, jobs, plug \
				 = line.split(';')
				i += 1
				if float(c1) >= 0 and float(c2) >= 0 and float(d1) >= 0 and float(d2) >= 0 :
					fo.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20}"\
					.format(ts, r, b, swpd, free, cache, si, so, bi, bo, in1, cs, us, sy, id7, wa, c1, c2, d1, d2, plug))
				else:
					j += 1
	print 'Negative instances ', j, ' out of total ', i

def sample_data_per_node_and_save_train_test(nodeset = "Haswell10"):

	def the_header(T):
		arff_header = \
		"@RELATION " + nodeset + T + '\n' + '\n' + \
		"@ATTRIBUTE r NUMERIC" + '\n' + \
		"@ATTRIBUTE b NUMERIC" + '\n' + \
		"@ATTRIBUTE swpd NUMERIC" + '\n' + \
		"@ATTRIBUTE free NUMERIC" + '\n' + \
		"@ATTRIBUTE cache NUMERIC" + '\n' + \
		"@ATTRIBUTE si NUMERIC" + '\n' + \
		"@ATTRIBUTE so NUMERIC" + '\n' + \
		"@ATTRIBUTE bi NUMERIC" + '\n' + \
		"@ATTRIBUTE bo NUMERIC" + '\n' + \
		"@ATTRIBUTE in1 NUMERIC" + '\n' + \
		"@ATTRIBUTE cs NUMERIC" + '\n' + \
		"@ATTRIBUTE us NUMERIC" + '\n' + \
		"@ATTRIBUTE sy NUMERIC" + '\n' + \
		"@ATTRIBUTE id NUMERIC" + '\n' + \
		"@ATTRIBUTE wa NUMERIC" + '\n' + \
		"@ATTRIBUTE cpu1 REAL" + '\n' + \
		"@ATTRIBUTE cpu2 REAL" + '\n' + \
		"@ATTRIBUTE dram1 REAL" + '\n' + \
		"@ATTRIBUTE dram2 REAL" + '\n' + \
		"@ATTRIBUTE plug NUMERIC" + '\n' + '\n' + \
		"@DATA" + '\n' 
		return arff_header
	
	f_in = 'cleaned_node_' + nodeset + '_vmstat_RAPL_timestamp.csv'
	f_out_1 = 'sample_nodes_' + nodeset + '_vmstat_RAPL_traintest.arff'
	#f_out_2 = 'node_' + nodeset + '_vmstat_RAPL_test.arff'

	f = open(f_in, 'r')
	TOT = len(f.read().splitlines())
	f.close()
	sample_size = TOT / 10
	sample_index = np.random.randint(0, TOT, sample_size)

	with open(f_in, 'r') as f:
		print 'Total lines in the file ', TOT
		i = 0
		j = 0
		with open(f_out_1, 'w') as fo1:
			fo1.write(the_header('_train_RAPL'))
			for line in f:
				if i in sample_index:
					j += 1
					ts, r, b, swpd, free, cache, si, so, bi, bo, in1, cs, us, sy, id7, wa, c1, c2, d1, d2, plug \
					 = line.split(',')
					fo1.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19}"\
						.format(r, b, swpd, free, cache, si, so, bi, bo, in1, cs, us, sy, id7, wa, c1, c2, d1, d2, plug))
				i += 1
				if i % 10000 == 0:
					print i
		

	print 'Written total lines ', j, 'out of ', i

def read_in_data_per_node_and_save_SHUFFLE_train_test(nodeset = "Haswell10"):

	def the_header(T):
		arff_header = \
		"@RELATION " + node + T + '\n' + '\n' + \
		"@ATTRIBUTE r NUMERIC" + '\n' + \
		"@ATTRIBUTE b NUMERIC" + '\n' + \
		"@ATTRIBUTE swpd NUMERIC" + '\n' + \
		"@ATTRIBUTE free NUMERIC" + '\n' + \
		"@ATTRIBUTE cache NUMERIC" + '\n' + \
		"@ATTRIBUTE si NUMERIC" + '\n' + \
		"@ATTRIBUTE so NUMERIC" + '\n' + \
		"@ATTRIBUTE bi NUMERIC" + '\n' + \
		"@ATTRIBUTE bo NUMERIC" + '\n' + \
		"@ATTRIBUTE in1 NUMERIC" + '\n' + \
		"@ATTRIBUTE cs NUMERIC" + '\n' + \
		"@ATTRIBUTE us NUMERIC" + '\n' + \
		"@ATTRIBUTE sy NUMERIC" + '\n' + \
		"@ATTRIBUTE id NUMERIC" + '\n' + \
		"@ATTRIBUTE wa NUMERIC" + '\n' + \
		"@ATTRIBUTE plug NUMERIC" + '\n' + '\n' + \
		"@DATA" + '\n' 
		return arff_header
	
	f_in = 'cleaned_node_' + node + '_vmstat_timestamp.csv'
	f_out_1 = 'node_' + node + '_vmstat_SHUFFLE_train.arff'
	f_out_2 = 'node_' + node + '_vmstat_SHUFFLE_test.arff'

	f = open(f_in, 'r')
	F = f.read().splitlines()
	TOT = len(F)
	random.shuffle(F)
	print 'Total lines in the file ', TOT
	n1 = int(9 * TOT / 10)
	print 'Training set size ', n1


	with open(f_out_1, 'w') as fo1:
		fo1.write(the_header('_SHUFFLE_train_RAPL'))
		for i in range(n1):
			line = F[i]
			ts, r, b, swpd, free, cache, si, so, bi, bo, in1, cs, us, sy, id7, wa, c1, c2, d1, d2, plug \
				 = line.split(',')
			i += 1
			fo1.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19}"\
					.format(r, b, swpd, free, cache, si, so, bi, bo, in1, cs, us, sy, id7, wa, c1, c2, d1, d2, plug))

	print 'Test set size ', TOT-n1
	with open(f_out_2, 'w') as fo2:
		fo2.write(the_header('_SHUFFLE_test_RAPL'))
		for i in range(n1,TOT):
			line = F[i]
			ts, r, b, swpd, free, cache, si, so, bi, bo, in1, cs, us, sy, id7, wa, c1, c2, d1, d2, plug \
				 = line.split(',')
			i += 1
			fo2.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19}"\
					.format(r, b, swpd, free, cache, si, so, bi, bo, in1, cs, us, sy, id7, wa, c1, c2, d1, d2, plug))

	print 'Written total lines ', i

#read_in_data_per_node_and_save_SHUFFLE_train_test()	

#read_in_data_per_node_and_save_train_test()

#test_RAPL_negatives()
sample_data_per_node_and_save_train_test()

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

IN_DIR = "../../data/jobs/SOM_clustering/3x3"
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
	f_in = 'jobsteps_assigned_classes'
	job_classes = defaultdict(int)
	with open(f_in, 'r') as f:
		# headline
		f.readline()
		for line in f:
			job_id, job_class = line.split('\t')
			job_classes[job_id] = int(job_class)
	return job_classes

def read_in_job_id_mapping():
	f_in = 'JobStepIDS'
	job_ids =  defaultdict(int)
	i = 0
	with open(f_in, 'r') as f:		
		# headline
		f.readline()
		for line in f:
			job_id, job = line.split('\t')
			job_ids[job_id] = job.strip()[1:-1]
			# this is just a test
			try:
				main_id, step_id = job.split('.')
			except ValueError as e:
				#print job
				i += 1
	#print i
	return job_ids


def read_in_job_partition():
	f_in = '../../job_partitions.csv'
	job_partitions =  defaultdict(str)
	testme = defaultdict(int)
	with open(f_in, 'r') as f:		
		for line in f:
			n, job, n, job_partition, n = line.split('"')
			try:
				job, step_id = job.split('.')
				testme[job] += 1
			except ValueError as e:
				job_partitions[job] = job_partition
				testme[job] += 0

	s =  [x for x in testme if testme[x] == 0]
	print len(s)
	return job_partitions

def read_in_job_users():
	f_in = '../../job_users.csv'
	job_users=  defaultdict(str)
	with open(f_in, 'r') as f:		
		for line in f:
			n, job, n, user, n = line.split('"')
			try:
				job, step_id = job.split('.')

			except ValueError as e:
				job_users[job] = user

	return job_users

def find_jobs_per_class():
	job_classes = read_in_SOM_output()
	job_ids = read_in_job_id_mapping()
	the_job_classes =  defaultdict(list)
	for job_id in job_ids:
		the_job_classes[job_classes[job_id]].append(job_ids[job_id])

	for the_class in the_job_classes:
		print the_class, len(the_job_classes[the_class])
	return the_job_classes

#find_jobs_per_class()

def find_partitions_per_class():
	job_classes = find_jobs_per_class()
	job_types = read_in_job_partition()

	job_types_per_class = defaultdict(list)

	for the_class in job_classes:
		for the_job in job_classes[the_class]:
			the_job = the_job.split('.')[0]
			job_types_per_class[the_class].append(job_types[the_job])

	from collections import Counter

	for the_class in job_types_per_class:
		print the_class, Counter(job_types_per_class[the_class])

	return job_types_per_class

#find_partitions_per_class()

def find_users_per_class():
	job_classes = find_jobs_per_class()
	job_types = read_in_job_users()

	job_types_per_class = defaultdict(list)

	for the_class in job_classes:
		for the_job in job_classes[the_class]:
			the_job = the_job.split('.')[0]
			job_types_per_class[the_class].append(job_types[the_job])

	from collections import Counter

	for the_class in job_types_per_class:
		print the_class, Counter(job_types_per_class[the_class])

	return job_types_per_class

find_users_per_class()




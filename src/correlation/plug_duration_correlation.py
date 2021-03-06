#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	author: sanja7s
	---------------
	plot the distribution
"""
import os
import datetime as dt
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib
from collections import defaultdict #, OrderedDict
#from matplotlib import colors
#from mpl_toolkits.axes_grid import inset_locator 
#matplotlib.style.use('ggplot')

IN_DIR = "../../data"
os.chdir(IN_DIR)

def read_in_data_per_job(f_in_1 = 'plug/plug_per_job.csv', \
	f_in_2 = 'jobs/all_job_end_start_time_job_ids.csv'):

	plug_per_job = defaultdict(int)

	with open(f_in_1, 'r') as f1:
		for line in f1:
			try:
				n1, job_id, n2, plug, n3 = line.strip().split('"')
			except ValueError:
				print plug
			try:
				main_id, step_id = job_id.split('.')
			except ValueError as e:
				main_id = job_id
			plug_per_job[main_id] += int(plug)

	print len(plug_per_job)

	dur_per_job = defaultdict(int)

	with open(f_in_2, 'r') as f2:
		for line in f2:
			n1, job_id, n2, et, n3, st, n4 = line.strip().split('"')
			et = dt.datetime.fromtimestamp(int(et))
			st = dt.datetime.fromtimestamp(int(st))
			try:
				main_id, step_id = job_id.split('.')
			except ValueError as e:
				main_id = job_id
			assert (et-st).total_seconds() >= 0
			dur_per_job[main_id] += (et-st).total_seconds()

	print len(dur_per_job)

	per_job = defaultdict(tuple)

	cnt = 0

	for job in plug_per_job:
		if job in dur_per_job:
			per_job[job] = (plug_per_job[job], dur_per_job[job])
		else:
			cnt += 1

	print 'No dur data for %d jobs' % cnt

	return per_job

def read_in_data_per_step(f_in_1 = 'plug/plug_per_job.csv', \
	f_in_2 = 'jobs/all_job_end_start_time_job_ids.csv'):

	plug_per_step= defaultdict(int)

	with open(f_in_1, 'r') as f1:
		for line in f1:
			try:
				n1, job_id, n2, plug, n3 = line.strip().split('"')
			except ValueError:
				print plug
			plug_per_step[job_id] = int(plug)

	print len(plug_per_step)

	dur_per_step = defaultdict(int)

	with open(f_in_2, 'r') as f2:
		for line in f2:
			n1, job_id, n2, et, n3, st, n4 = line.strip().split('"')
			et = dt.datetime.fromtimestamp(int(et))
			st = dt.datetime.fromtimestamp(int(st))
			assert (et-st).total_seconds() >= 0
			dur_per_step[job_id] += (et-st).total_seconds()

	print len(dur_per_step)

	per_step = defaultdict(tuple)

	cnt = 0

	for step in plug_per_step:
		if step in dur_per_step:
			per_step[step] = (plug_per_step[step], dur_per_step[step])
		else:
			cnt += 1

	print 'No dur data for %d steps' % cnt

	return per_step


def read_in_data_per_step_per_state(f_in_1 = 'plug/plug_per_job.csv', \
	f_in_2 = 'jobs/state_duration/state_duration_job_steps.csv'):

	plug_per_step= defaultdict(int)

	with open(f_in_1, 'r') as f1:
		for line in f1:
			try:
				n1, job_id, n2, plug, n3 = line.strip().split('"')
			except ValueError:
				print plug
			plug_per_step[job_id] = int(plug)

	distr_completed = defaultdict(int)
	distr_cancelled = defaultdict(int)
	distr_timeout = defaultdict(int)
	distr_failed = defaultdict(int)
	i = 0

	with open(f_in_2, 'r') as f:
		for line in f:
			i += 1
			n0, JobID, n1, elapsed, n2, state, n3 = line.split('"')
			elapsed = int(elapsed)
			JobID = JobID
			state = state
			if 'CANCELLED' in state:
				state = 'CANCELLED'
			if state == 'CANCELLED':
				distr_cancelled[JobID] = elapsed
			elif state == 'COMPLETED':
				distr_completed[JobID] = elapsed
			elif state == 'FAILED':
				distr_failed[JobID] = elapsed
			else:
				distr_timeout[JobID] = elapsed

	# distr_cancelled, distr_timeout, distr_failed, distr_completed

	per_step = defaultdict(tuple)

	cnt = 0

	for step in plug_per_step:
		if step in distr_cancelled:
			per_step[step] = (plug_per_step[step], distr_cancelled[step])
		else:
			cnt += 1

	print 'No dur data for %d steps' % cnt

	return per_step

def correlate_data(data):

	v1 = []
	v2 = []
	for k in data:
		v1.append(data[k][0])
		v2.append(data[k][1])

	v1 = np.array(v1)
	v2 = np.array(v2)

	print 'Cross-correlation ', np.correlate(v1, v2)
	print 'Pearson  ', np.corrcoef(v1, v2)

"""
print 'Per Step'
data = read_in_data_per_job()
correlate_data(data)
print 'Per job'
data2 = read_in_data_per_step()
correlate_data(data2)
"""
print 'Per step CANCELLED'
data1_state = read_in_data_per_step_per_state()
correlate_data(data1_state)
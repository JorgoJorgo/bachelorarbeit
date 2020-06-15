import sys
import networkx as nx
import numpy as np
import itertools
import random
import time
from objective_function_experiments import *

# run experiments for infocom 2019 paper
# seed is used for pseudorandom number generation in this run
# switch determines which experiments are run
def infocom_experiments(switch):
	write_graphs()
	print('generated graphs')
	for (method, name) in [(RandomTrees, 'Random'), (GreedyArborescenceDecomposition, 'Greedy')]:
		if switch in ['subset', 'all']:
			experiment_objective_subset(
			    measure_stretch, method, "stretch_for_subset_"+name)
			experiment_objective_subset(
			    measure_load, method, "load_for_subset_"+name)
		if switch in ['independent', 'all']:
			print(name, 'independent experiments')
			experiment_objective(num_independent_paths_in_arbs,
			                     method, "independent_paths_"+name)
		if switch in ['SRLG', 'all']:
			print(name, 'SRLG experiments')
			experiment_SRLG(method, name)


if __name__ == "__main__":
	start = time.time()
	seed = 1
	n = 100
	rep = 100
	k = 8
	f_num = 40
	samplesize=20
	switch = 'all'
	if len(sys.argv)>1:
		switch = sys.argv[1]
	if len(sys.argv)>2:
		seed = sys.argv[2]
	if len(sys.argv) > 3:
		rep = int(sys.argv[3])
	if len(sys.argv) > 4:
		n = int(sys.argv[4])
		if n < 20:
			k = 5
	samplesize = min(int(n/2), samplesize)
	f_num = min(n, f_num)
	set_parameters([n, rep, k, samplesize, f_num, seed, "infocom2019-"])
	infocom_experiments(switch)
	end = time.time()
	print(end-start)
	print(time.asctime( time.localtime(start)))
	print(time.asctime( time.localtime(end)))

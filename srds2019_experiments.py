import sys
import networkx as nx
import numpy as np
import itertools
import random
import time
from objective_function_experiments import *

def run_experiments():
    global name, n, rep, k, samplesize, f_num, seed
    write_graphs()
    print('generated graphs')
    for (method, name) in [(Trees, 'Greedy'), (RR_swap, 'RR-swap')]:
        if switch in ['zoo', 'all']:
            original_params = [n, rep, k, samplesize, f_num, seed, "srds2019-"]
            zoo_count = 0
            for i in range(261):
                samplesize = 10
                f_num= 5
                n = 20
                set_parameters([n, rep, k, samplesize, f_num, seed, "zoo-srds2019-"])
                g = read_zoo(i, 4)
                if g == None:
                    continue
                k = nx.edge_connectivity(g)
                n = len(g.nodes())
                m = len(g.edges())
                print('nodes, edges, connectivity', n, m, k)
                samplesize = min(int(n/2), samplesize)
                f_num = min(int(m/4), f_num)
                set_parameters([n, rep, k, samplesize, f_num, seed, "zoo-srds2019-"])
                experiment_objective_subset(measure_stretch, method, str(
                    f_num)+"_stretch_for_subset_"+name, seed=i, gml=True)
                experiment_objective_subset(measure_load, method, str(
                    f_num)+"_load_for_subset_"+name, seed=i, gml=True)
                # experiment_objective_subset(measure_dividedbyhops, method, "divided_by_hops_for_important_sources_"+name, seed=seed)
                zoo_count += 1
            print('Ran '+str(zoo_count)+' zoo experiment successfully')
            [n, rep, k, samplesize, f_num, seed, name] = original_params
            set_parameters(original_params)
        if switch in ['subset', 'all']:
            experiment_objective_subset(measure_stretch, method, str(
                f_num)+"_stretch_for_subset_"+name, seed=seed)
            experiment_objective_subset(measure_load, method, str(
                f_num)+"_load_for_subset_"+name, seed=seed)
        if switch in ['independent', 'all']:
            experiment_objective(num_independent_paths_in_arbs, method, str(
                f_num)+"_independent_paths_"+name, seed=seed)
        if switch in ['SRLG', 'all']:
            experiment_SRLG(method, str(f_num)+"_"+name, seed=seed)
            experiment_SRLG_node_failures(
                method, str(f_num)+"_"+name, seed=seed)

if __name__ == "__main__":
    start = time.time()
    seed = 1
    n = 100
    rep = 100
    k = 8
    f_num = 40
    samplesize=20
    switch = 'all'
    if len(sys.argv) > 1:
        switch = sys.argv[1]
    if len(sys.argv) > 2:
        seed = int(sys.argv[2])
    if len(sys.argv) > 3:
        rep = int(sys.argv[3])
    if len(sys.argv) > 4:
        n = int(sys.argv[4])
        if n < 20:
            k = 5
    if len(sys.argv) >5:
        k= int(sys.argv[5])
    samplesize = min(int(n/2), samplesize)
    f_num = min(n, f_num)
    random.seed(seed)
    set_parameters([n, rep, k, samplesize, f_num, seed, "srds2019-"])
    run_experiments()
    end = time.time()
    print(end-start, 'seconds')
    print('start time', time.asctime(time.localtime(start)))
    print('end time', time.asctime(time.localtime(end)))

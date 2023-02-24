import statistics
import sys
import networkx as nx
import numpy as np
import itertools
import random
import time
from routing import *

# global variables
seed = 1
n = 10
rep = 1
k = 8
f_num = 40
samplesize = 20
name = "experiment-objective-function"


# set global parameters in this file and in routing_stats
def set_parameters(params):
    #print("params:" , params)
    set_objective_parameters(params)

# set global parameters in this file and in routing_stats
def set_objective_parameters(params):
    global seed, n, rep, k, samplesize, name, f_num
    [n, rep, k, samplesize, f_num, seed, name] = params
    #print("f_num set_obj_params", f_num)
    set_routing_params(params)

# print global parameters in this file and in routing_stats
def print_objective_parameters():
    print(n, rep, k, samplesize, f_num, seed, name)

# objective functions
def measure_dividedbyhops(g, DEBUG=False):
    return measure_obj(g, 'hops', DEBUG=DEBUG)


def measure_load(g, DEBUG=False):
    return measure_obj(g, 'load', DEBUG=DEBUG)


def measure_stretch(g, DEBUG=False):
    return measure_obj(g, 'stretch', DEBUG=DEBUG)


def measure_product(g, DEBUG=False):
    return measure_obj(g, 'product', DEBUG=DEBUG)


# evaluate routes with simulations for sample size
def measure_obj(g, obj, DEBUG=False):
    # calculate x = maximum number of hops/load/stretch with f failures for a set of samplesize source-root pairs
    T = get_arborescence_list(g)
    stat = statistics(RouteDetCirc, "DetCirc")
    success = 0
    for i in range(f_num + 1):
        stat.reset(g.nodes())
        SimulateGraph(g, True, [stat], i, samplesize, tree=T)
        success += stat.succ
    if stat.succ > 0:
        if obj == 'hops':
            return -10000 * success + np.max(stat.hops)
        if obj == 'load':
            return -10000 * success + stat.load
        if obj == 'stretch':
            return -10000 * success + np.max(stat.stretch)
        if obj == 'product':
            return -10000 * success + np.max(stat.stretch) * stat.load
    else:
        return float("inf")


# count the number of independent paths to the root in arborescences T1 and T2
def num_independent_paths(T1, T2, root):
    SP1 = nx.shortest_path(T1, target=root)
    SP2 = nx.shortest_path(T2, target=root)
    count = 0
    for v in T1.nodes():
        if v in SP1 and v in SP2 and set(SP1[v][1:-1]).isdisjoint(set(SP2[v][1:-1])):
            count += 1
    return count


# count the number of independent paths to the root in decomposition associated with g
def num_independent_paths_in_arbs(g):
    root = g.graph['root']
    T = get_arborescence_list(g)
    n = len(g.nodes())
    count = 0
    for T1, T2 in itertools.combinations(T, 2):
        if root in T1.nodes() and root in T2.nodes():
            count += num_independent_paths(T1, T2, root)
        else:
            return 0
    return count

#hier wird in die results  result reingeschrieben
# run experiment for the objective function with the decomposition method,
# string for the method and parameters over a subset only
def experiment_objective_subset(obj_func, method, objstr=None, seed=11, gml=False, torus=False):
    if objstr == None:
        objstr = str(obj_func)
    random.seed(seed)
    filename = "results/" + name + "_objective_" + \
               str(n) + "_" + str(k) + "_" + str(seed) + "_" + objstr + ".txt"
    filename_time = "results/" + name + "_objective_" + \
                    str(n) + "_" + str(k) + "_" + str(seed) + "_" + objstr + "_time.txt"
    if gml:
        filename = "results/" + name + "-gml_failure_objective_" + \
                   str(n) + "_" + str(k) + "_" + str(seed) + "_" + objstr + ".txt"
    if torus:
        filename = "results/" + name + "-torus_failure_objective_" + \
                   str(n) + "_" + str(k) + "_" + str(seed) + "_" + objstr + ".txt"
    outstretch = open(filename, 'a')
    outstretch.write(
        "#n= %d, connectivity= %d, repetitions= %d\n" % (n, k, rep))
    outstretch.write(
        "#graph, before/after, intensity, 'objective', success rate, switches, load, load, max stretch, mean stretch, max hops, mean hops\n")
    outtime = open(filename_time, 'a')
    outtime.write(
        "#n= %d, connectivity= %d, repetitions= %d\n" % (n, k, rep))
    outtime.write("#n, time to compute arborescence, time for swapping in seconds\n")
    stat = Statistic(RouteDetCirc, "DetCirc")
    failure_range = range(f_num, 0, -1)
    data = {i: {'before': {'succ': [], 'hops': []}, 'after': {
        'succ': [], 'hops': []}} for i in failure_range}
    for j in range(rep):
        random.seed(j)
        if gml:
            g = read_zoo(seed, k)
        else:
            g = read_graph(j)
        t_arb = time.time()
        method(g)
        t_arb = time.time() - t_arb
        if num_complete_nodes(g) == n:
            before = obj_func(g)
            T1 = get_arborescence_list(g)
            t_swap = time.time()
            count = greedy_swap_obj(g, obj_func)
            t_swap = time.time() - t_swap
            outtime.write("%i, %.6f, %.6f\n" % (n, t_arb, t_swap))
            after = obj_func(g)
            if before < after:
                print("objective",objstr, "repetition",j, "before", before, "after", after, "t_swap",t_swap, "number of swaps", count, 'has not been optimized')
                sys.exit(-1)
            T2 = get_arborescence_list(g)
            stat.reset(g.nodes())
            fails = g.graph['fails']
            ss = min(samplesize,len(set(connected_component_nodes_with_d_after_failures(g,fails[:f_num],g.graph['root'])))- 1)
            SimulateGraph(g, True, [stat], f_num, ss, tree=T1)
            for f1 in failure_range:
                stat.reset(g.nodes())
                random.seed(j)
                SimulateGraph(g, True, [stat], f1, ss, tree=T1)
                brs = int(stat.succ) / samplesize
                brh = (stat.totalSwitches)
                data[f1]['before']['succ'].append(brs)
                data[f1]['before']['hops'].append(brh)
                outstretch.write("regular, before, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n" % (
                    f1, -1 * before, brs, brh, stat.load, stat.load, np.max(stat.stretch), np.mean(stat.stretch),
                    np.max(stat.hops), np.mean(stat.hops)))

                if np.mean(stat.stretch) < 0 and stat.succ > 0:
                    print('before', j, f1, brs, np.max(stat.stretch), np.mean(
                        stat.stretch), np.max(stat.hops), np.mean(stat.hops))
                    print('stretch', stat.stretch)
                    print('hops', stat.hops)
                    sys.exit()
                if (np.max(stat.stretch) > n - 1):
                    print('large stretch, line 273', np.max(stat.stretch))
                    print(stat.stretch)
                    print(stat.succ, 'successes')
                    sys.exit()
                stat.reset(g.nodes())
                random.seed(g.graph['seed'])
                SimulateGraph(g, True, [stat], f1, ss, tree=T2)
                ars = int(stat.succ) / samplesize
                arh = (stat.totalSwitches)
                data[f1]['after']['succ'].append(ars)
                data[f1]['after']['hops'].append(arh)
                outstretch.write("regular, after, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n" % (
                    f1, -1 * after, ars, arh, stat.load, stat.load, np.max(stat.stretch), np.mean(stat.stretch),
                    np.max(stat.hops), np.mean(stat.hops)))
                if np.mean(stat.stretch) < 0 and stat.succ > 0:
                    print('after', j, f1, brs, np.max(stat.stretch), np.mean(
                        stat.stretch), np.max(stat.hops), np.mean(stat.hops))
                    print('stretch', stat.stretch)
                    print('hops', stat.hops)
                    sys.exit()
            sys.stdout.flush()
            outstretch.flush()
            if rep == 1:
                break
    outstretch.close()


# run experiment for the objective function with the decomposition method,
# string for the method and parameters
def experiment_objective(obj_func, method, objstr=None, seed=1):
    if objstr == None:
        objstr = str(obj_func)
    random.seed(seed)
    filename = "results/srds-objective_" + \
               str(n) + "_" + str(k) + "_" + str(seed) + "_" + objstr + ".txt"
    outstretch = open(filename, 'a')
    outstretch.write(
        "#n= %d, connectivity= %d, repetitions= %d\n" % (n, k, rep))
    if "independent" in objstr:
        outstretch.write(
            "graph type, before, objective, after, objective\n")
    else:
        outstretch.write(
            "#graph, before/after, intensity, 'objective', success rate, switches, max load, mean load, max stretch, mean stretch, max hops, mean hops\n")
    stat = Statistic(RouteDetCirc, "DetCirc")
    failure_range = [int(n / 10 * i) for i in range(1, 5 * k)]
    data = {i: {'before': {'succ': [], 'hops': []}, 'after': {
        'succ': [], 'hops': []}} for i in failure_range}
    for j in range(rep):
        g = read_graph(j)
        method(g)
        if num_complete_nodes(g) == n:
            before = obj_func(g)
            T1 = get_arborescence_list(g)
            if "independent" in objstr:
                greedy_swap_obj(g, obj_func, max=True)
            else:
                greedy_swap_obj(g, obj_func)
            after = obj_func(g)
            T2 = get_arborescence_list(g)
            print(j, before, after, obj_func)
            if "independent" in objstr:
                outstretch.write("regular, before, %d, after, %d\n" % (before, after))
                continue
            ss = min(samplesize,len(set(connected_component_nodes_with_d_after_failures(g,fails[:max(failure_range)],g.graph['root'])))- 1)
            for f in failure_range:
                stat.reset(g.nodes())
                # , fails=fails) #replace True by False to use fails
                SimulateGraph(g, True, [stat], f, ss, tree=T1)
                brs = int(stat.succ) / n
                brh = (stat.totalSwitches)
                data[f]['before']['succ'].append(brs)
                data[f]['before']['hops'].append(brh)
                #                                  alg, f, succ, switches, load      stretch,    hops
                outstretch.write("regular, before, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n" % (
                    f, before, brs, brh, stat.load, stat.load, np.max(stat.stretch), np.mean(stat.stretch),
                    np.max(stat.hops), np.mean(stat.hops)))

                stat.reset(g.nodes())
                SimulateGraph(g, True, [stat], f, ss, tree=T2)  # , fails=fails)
                ars = int(stat.succ) / n
                arh = (stat.totalSwitches)
                data[f]['after']['succ'].append(ars)
                data[f]['after']['hops'].append(arh)

                #                                  alg,f, succ, switches, load      stretch,    hops
                outstretch.write("regular, after, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n" % (
                    f, after, ars, arh, stat.load, stat.load, np.max(stat.stretch), np.mean(stat.stretch),
                    np.max(stat.hops), np.mean(stat.hops)))
                if (np.max(stat.stretch) > n - 1):
                    print('large stretch, line 376', np.max(stat.stretch))
                    print(stat.stretch)
                    print(stat.succ, 'successes')
                    sys.exit()
            print(objstr, j, before, after)
            sys.stdout.flush()
            outstretch.flush()

    if "independent" not in objstr:
        for f in failure_range:
            brs = np.mean(data[f]['before']['succ'])
            bsh = np.mean(data[f]['before']['hops'])
            ars = np.mean(data[f]['after']['succ'])
            arh = np.mean(data[f]['after']['hops'])
            print('%d failures, avg before success hops, after success hops %.2f, %.2f, %.2f, %.2f' % (
                f, brs, bsh, ars, arh))
            brs = np.min(data[f]['before']['succ'])
            bsh = np.min(data[f]['before']['hops'])
            ars = np.min(data[f]['after']['succ'])
            arh = np.min(data[f]['after']['hops'])
            print('%d failures, min before success hops, after success hops %.2f, %.2f, %.2f, %.2f' % (
                f, brs, bsh, ars, arh))
            sys.stdout.flush()
            
    outstretch.close()


# return the number of links in the shared risk link group belong to the last two arborescences
def count_SRLG(g, k, SRLG):
    count = 0
    for (u, v) in SRLG:
        if g[u][v]['arb'] in [k - 1, k - 2]:
            count += 1
    return count


# run SLRG experiments for infocom 2019 paper
# seed is used for pseudorandom number generation in this run
# switch determines which experiments are run
def experiment_SRLG(method, name, seed=11):
    random.seed(seed)
    filename = "results/srds-SRLG_" + str(n) + "_" + str(k) + "_" + str(seed) + "_" + name
    outstretch = open(filename + ".txt", 'a')
    outstretch.write(
        "#n= %d, connectivity= %d, repetitions= %d\n" % (n, k, rep))
    outstretch.write(
        "#graph, before/after, random, intensity, SRLG in last arbs, # successes, switches, max load, mean load, max stretch, mean stretch, max hops, mean hops\n")
    stat = Statistic(RouteDetCirc, "DetCirc")
    failure_range = [int(n / 10 * i) for i in range(1, 5 * k)]
    data = {f: {'before': {'random': {'succ': [], 'hops': []}, 'SRLG': {'succ': [], 'hops': []}}, 'after': {
        'random': {'succ': [], 'hops': []}, 'SRLG': {'succ': [], 'hops': []}}} for f in failure_range}
    for f in failure_range:
        for j in range(rep):
            g = read_graph(j)
            edg = list(g.edges())
            SRLG = random.sample(edg, f)
            method(g)
            if num_complete_nodes(g) == n:
                before = count_SRLG(g, k, SRLG)
                T1 = get_arborescence_list(g)

                for (u, v) in SRLG:
                    index = g[u][v]['arb']
                    if index in range(k - 2) and v != g.graph['root']:
                        for vv in g[u]:
                            if vv != g.graph['root'] and (u, vv) not in SRLG and (vv, u) not in SRLG \
                                    and g[u][vv]['arb'] in [k - 1, k - 2]:
                                swap(g, u, v, u, vv)

                after = count_SRLG(g, k, SRLG)
                T2 = get_arborescence_list(g)

                fails = random.sample(edg, f)
                g.graph['fails'] = fails
                stat.reset(g.nodes())
                samplessize = len(set(connected_component_nodes_with_d_after_failures(g,fails[:f],g.graph['root'])))- 1
                SimulateGraph(g, False, [stat], f, samplessize, tree=T1)
                brs = int(stat.succ) / n
                brh = (stat.totalSwitches)
                outstretch.write("regular, before, True, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n" % (
                f, before, brs, brh, np.max(
                    stat.load), np.mean(stat.load), np.max(stat.stretch), np.mean(stat.stretch), np.max(stat.hops),
                np.mean(stat.hops)))

                stat.reset(g.nodes())
                g.graph['fails'] = SRLG
                samplessize = len(set(connected_component_nodes_with_d_after_failures(g,fails[:f],g.graph['root'])))- 1
                SimulateGraph(g, False, [stat], f, samplessize, tree=T1)
                bss = int(stat.succ) / n
                bsh = (stat.totalSwitches)
                outstretch.write(
                    "regular, before, False, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n" % (
                    f, before, bss, bsh, np.max(
                        stat.load), np.mean(stat.load), np.max(stat.stretch), np.mean(stat.stretch), np.max(stat.hops),
                    np.mean(stat.hops)))

                stat.reset(g.nodes())
                g.graph['fails'] = fails
                samplessize = len(set(connected_component_nodes_with_d_after_failures(g,fails[:f],g.graph['root'])))- 1
                SimulateGraph(g, False, [stat], f, samplessize, tree=T2)
                ars = int(stat.succ)
                arh = (stat.totalSwitches)
                outstretch.write("regular, after, True, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n" % (
                f, after, ars, arh, np.max(
                    stat.load), np.mean(stat.load), np.max(stat.stretch), np.mean(stat.stretch), np.max(stat.hops),
                np.mean(stat.hops)))

                stat.reset(g.nodes())
                g.graph['fails'] = SRLG
                samplessize = len(set(connected_component_nodes_with_d_after_failures(g,fails[:f],g.graph['root'])))- 1
                SimulateGraph(g, False, [stat], f, samplessize, tree=T2)

                ass = int(stat.succ) / n
                ash = (stat.totalSwitches)
                outstretch.write("regular, after, False, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n" % (
                f, after, ass, ash, np.max(
                    stat.load), np.mean(stat.load), np.max(stat.stretch), np.mean(stat.stretch), np.max(stat.hops),
                np.mean(stat.hops)))
                if (np.max(stat.stretch) > n - 1):
                    print('large stretch, line 462', np.max(stat.stretch))
                    print(stat.stretch)
                    print(stat.succ, 'successes')
                    sys.exit()
                sys.stdout.flush()
                outstretch.flush()

                data[f]['before']['random']['succ'].append(brs)
                data[f]['before']['random']['hops'].append(brh)
                data[f]['before']['SRLG']['succ'].append(bss)
                data[f]['before']['SRLG']['hops'].append(bsh)
                data[f]['after']['random']['succ'].append(ars)
                data[f]['after']['random']['hops'].append(arh)
                data[f]['after']['SRLG']['succ'].append(ass)
                data[f]['after']['SRLG']['hops'].append(ash)
        brs = np.mean(data[f]['before']['random']['succ'])
        brh = np.mean(data[f]['before']['random']['hops'])
        bss = np.mean(data[f]['before']['SRLG']['succ'])
        bsh = np.mean(data[f]['before']['SRLG']['hops'])
        ars = np.mean(data[f]['after']['random']['succ'])
        ash = np.mean(data[f]['after']['random']['hops'])
        ass = np.mean(data[f]['after']['SRLG']['succ'])
        ash = np.mean(data[f]['after']['SRLG']['hops'])
        print('%d avg before %.2f, %.2f, %.2f, %.2f' % (f, brs, bss, brh, bsh))
        print('%d avg after %.2f, %.2f, %.2f, %.2f' % (f, ars, ass, arh, ash))
        sys.stdout.flush()
    outstretch.close()


# run SLRG experiments for infocom 2019 paper with node failures
# seed is used for pseudorandom number generation in this run
# switch determines which experiments are run
def experiment_SRLG_node_failures(method, name, seed=11):
    random.seed(seed)
    filename = "results/srds-SRLG_" + str(n) + "_" + str(k) + "_" + str(seed) + "_" + name
    outstretch = open(filename + ".txt", 'a')
    outstretch.write(
        "#n= %d, connectivity= %d, repetitions= %d\n" % (n, k, rep))
    outstretch.write(
        "#graph, before/after, random, intensity, SRLG in last arbs, # successes, switches, max load, mean load, max stretch, mean stretch, max hops, mean hops\n")
    stat = Statistic(RouteDetCirc, "DetCirc")
    failure_range = range(1, f_num + 1)
    data = {f: {'before': {'random': {'succ': [], 'hops': []}, 'SRLG': {'succ': [], 'hops': []}}, 'after': {
        'random': {'succ': [], 'hops': []}, 'SRLG': {'succ': [], 'hops': []}}} for f in failure_range}
    for f in failure_range:
        for j in range(rep):
            g = read_graph(j)
            edg = list(g.edges())
            SRLG = g.graph['fails'][:f_num]
            method(g)
            if num_complete_nodes(g) == n:
                before = count_SRLG(g, k, SRLG)
                T1 = get_arborescence_list(g)

                for (u, v) in SRLG:
                    index = g[u][v]['arb']
                    if index in range(k - 2) and v != g.graph['root']:
                        for vv in g[u]:
                            if vv != g.graph['root'] and (u, vv) not in SRLG and (vv, u) not in SRLG and g[u][vv][
                                'arb'] in [k - 1, k - 2]:
                                swap(g, u, v, u, vv)

                after = count_SRLG(g, k, SRLG)
                T2 = get_arborescence_list(g)

                stat.reset(g.nodes())

                samplessize = len(set(connected_component_nodes_with_d_after_failures(g,SRLG,g.graph['root'])))- 1
                SimulateGraph(g, False, [stat], f, samplessize, tree=T1)
                brs = int(stat.succ) / n
                brh = (stat.totalSwitches)

                stat.reset(g.nodes())
                SimulateGraph(g, False, [stat], f, samplessize, tree=T2)
                ars = int(stat.succ) / n
                arh = (stat.totalSwitches)

                outstretch.write("regular, before, True, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n" % (
                f, before, brs, brh, np.max(
                    stat.load), np.mean(stat.load), np.max(stat.stretch), np.mean(stat.stretch), np.max(stat.hops),
                np.mean(stat.hops)))
                if ars >= brs:
                    outstretch.write(
                        "regular, after, True, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n" % (
                        f, after, ars, arh, np.max(
                            stat.load), np.mean(stat.load), np.max(stat.stretch), np.mean(stat.stretch),
                        np.max(stat.hops), np.mean(stat.hops)))
                else:
                    outstretch.write(
                        "regular, after, True, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n" % (
                        f, before, brs, brh, np.max(
                            stat.load), np.mean(stat.load), np.max(stat.stretch), np.mean(stat.stretch),
                        np.max(stat.hops), np.mean(stat.hops)))
                    print("success rate suffered")
                sys.stdout.flush()
                outstretch.flush()
                print(method, name, seed, f)

    outstretch.close()
# erstellt die graphen
# generate rep random k-regular graphs with connectivity k using seed and
# write them to file
def write_graphs():
    d = []
    ecc = []
    sp = []
    for i in range(rep):
        g = nx.random_regular_graph(k, n).to_directed()
        while nx.edge_connectivity(g) < k:
            g = nx.random_regular_graph(k, n).to_directed()
        prepare_graph(g,k,0)
        GreedyArborescenceDecomposition(g)
        d.append(depth(g))
        ecc.append(nx.eccentricity(g, 0))
        sp.append(nx.average_shortest_path_length(g))
        s = ''
        for e in g.graph['fails']:
            s = s + str(e[0]) + ' ' + str(e[1]) + '\n'
        f = open('results/' + name + str(seed) + '_graph_' +
                 str(n) + '_' + str(i) + '.txt', 'w')
        f.write(s[:-1])
        f.close()

def create_custom_graph():
    #jetziger graph ist der beispielgraph für die motivation von mod breite in multipletrees
    g = nx.Graph()
    max_node = 7
    for i in range(1,max_node):#geht von 1 bis max_node -1
        g.add_node(i)
    #endfor 

    g.add_edge(1,2)
    g.add_edge(1,3)
    g.add_edge(1,4)
    g.add_edge(1,5)
    

    g.add_edge(2,6)
    g.add_edge(3,6)
    g.add_edge(4,6)
    g.add_edge(5,6)
    g.add_edge(1,6)
    # g.add_edge(2,5)

    # g.add_edge(3,6)
    # g.add_edge(3,7)
    # g.add_edge(3,8)

    # g.add_edge(4,9)

    # g.add_edge(5,14)
    # g.add_edge(5,15)

    # g.add_edge(6,14)
    # g.add_edge(6,10)

    # g.add_edge(7,11)

    # g.add_edge(8,12)

    # g.add_edge(9,13)

    # g.add_edge(10,15)

    # g.add_edge(11,17)

    # g.add_edge(12,19)

    # g.add_edge(13,20)

    # g.add_edge(14,18)

    # g.add_edge(15,16)

    # g.add_edge(16,21)

    # g.add_edge(17,21)

    # g.add_edge(18,21)

    # g.add_edge(19,21)

    # g.add_edge(20,21)

    #random1 = random.randint(1,max_node-1)
    #random2 = random.randint(1,max_node-1)
    #random3 = random.randint(1,max_node-1)
    #random4 = random.randint(1,max_node-1)
    fails = list()
    #fails.append((random1,random2))
    #fails.append((random3,random4))
    # fails.append((8,12))
    # fails.append((5,15))
    fails.append((1,6))
    return g,fails

# read generated k-regular graphs from file system
def read_graph(i):
    g = nx.read_edgelist('results/' + name + str(seed) + '_graph_' +
                         str(n) + '_' + str(i) + '.txt', nodetype=int).to_directed()
    for (u, v) in g.edges():
        g[u][v]['arb'] = -1
    g.graph['seed'] = 0
    g.graph['k'] = k
    g.graph['root'] = 0
    fails = []
    f = open('results/' + name + str(seed) +
             '_graph_' + str(n) + '_' + str(i) + '.txt', 'r')
    for line in f:
        s = line.replace('\n', '').split(' ')
        fails.append((int(s[0]), int(s[1])))
    f.close()
    g.graph['fails'] = fails
    return g

# generate random ring of clique graphs with n nodes and connectivity k1-1
# in cliques and k2 between neighboring cliques
def create_ring_of_cliques(l,k1, k2, seed):
    #print('l', l, 'k1', k1, 'k2', k2)
    if k2 >= k1*k1:
        print('k2 must be at most k1*k1 for create_ring_of_cliques')
        sys.exit()
    n = l*(k1)
    m = l*(k1*(k1-1)/2+k2)
    random.seed(seed)
    g = nx.Graph()
    g.add_nodes_from(range(n))
    for i in range(l):
        ## wire inside each clique
        for u in range(i*k1, (i+1)*k1):
            for v in range(u,(i+1)*k1):
                g.add_edge(u,v)
        ## wire between cliques
        if i>0:
            for j in range(k2):
                u = random.choice(range(i*k1, (i+1)*k1))
                v = random.choice(range((i-1)*k1, (i)*k1))
                while (u,v) in g.edges():
                    u = random.choice(range(i*k1, (i+1)*k1))
                    v = random.choice(range((i-1)*k1, (i)*k1))
                g.add_edge(u,v)
        else:
            for j in range(k2):
                u = random.choice(range(0, k1))
                v = random.choice(range((l-1)*k1, (l)*k1))
                while (u,v) in g.edges():
                    u = random.choice(range(0,k1))
                    v = random.choice(range((l-1)*k1, (l)*k1))
                g.add_edge(u,v)
    # n selfloops to be removed
    g.remove_edges_from(nx.selfloop_edges(g))
    if (len(g.edges())!= m):
        print("Bug in ring of clique generation")
        sys.exit()
    g = g.to_directed()
    prepare_graph(g,2*k2,seed)
    return g

# set attributes for algorithms
def prepare_graph(g,k,seed):
    g.graph['seed'] = seed
    g.graph['k'] = k
    g.graph['root'] = 0
    g2 = g.to_undirected()
    g2.remove_edges_from(nx.selfloop_edges(g2))
    fails = list(g2.edges())
    random.seed(seed)

    good = False
    count = 0
    while not good:
        count += 1
        random.shuffle(fails)
        G = g.to_undirected()
        n = len(g.nodes())
        G.remove_edges_from(fails[:n])
        Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
        if 0 in Gcc[0]:
            good = True
        elif count > 10:
            g.graph['root'] = list(Gcc[0])[0]
            good = True
        #else:
        #    print('reshuffle in prepare graph', count)
    g.graph['fails'] = fails

# return j th zoo graph if it can be trimmed into a graph of connectivity at least 4 and at
# least 10 nodes
def read_zoo(j, min_connectivity):
    zoo_list = list(glob.glob("./benchmark_graphs/*.graphml"))
    if len(zoo_list) == 0:
        print("Add Internet Topology Zoo graphs (*.graphml files) to directory benchmark_graphs")
        print("(download them from http://www.topology-zoo.org/dataset.html")
        sys.exit()
    if len(zoo_list) <= j:
        return None
    #print(" J : " , j ) 
    #print(" Zoo_List  : " , zoo_list )
    #print("Zoo_List[j] : " , zoo_list[j]) 
    g1 = nx.Graph(nx.read_graphml(zoo_list[j]))
    g2 = nx.convert_node_labels_to_integers(g1)
    g2.remove_edges_from(nx.selfloop_edges(g2))
    g2 = g2.to_directed()
    # print(nx.edge_connectivity(g2),',', len(g2.nodes))
    n_before = len(g2.nodes)

    
    #print("Nodes befor Trimming : " , len(g2.nodes))
    degree = min(3, min_connectivity)
    degree = min(1, min_connectivity)
    #print("Start Trimming")
    while nx.edge_connectivity(g2) < min_connectivity:
        #print("G2 Degree before Trim : " , nx.edge_connectivity(g2) , " Nodes : " , len(g2.nodes))
        g2 = trim2(g2, degree)
        if len(g2.nodes) == 0:
            # print(zoo_list[j],"too sparse",len(g1.nodes), len(g1.edges))
            return None
        #print("G2 Degree after Trim : " , nx.edge_connectivity(g2) , " Nodes : " , len(g2.nodes))
        degree += 1
    #if len(g2.nodes) <= 10:
    #    return None
    #print(" ")
    g = g2.to_directed()
    print(j, zoo_list[j],'n_before=', n_before, 'n_after=', len(g.nodes), 'm_after=', len(g.edges), 'connectivity=', nx.edge_connectivity(g2), 'degree=', degree)

    #print(" ")
    #print(" ")
    for (u, v) in g.edges():
        g[u][v]['arb'] = -1
    prepare_graph(g, nx.edge_connectivity(g), seed)
    g.graph['undirected failures'] = False
    g.graph['pos'] = nx.spring_layout(g)
    return g


# read AS graphs and trims them to be of connectivity at least conn
def generate_trimmed_AS(conn):
    import fnss
    files = glob.glob('./benchmark_graphs/*.cch')
    if len(files) == 0:
        print("Add Rocketfuel Graphs (*.cch) to directory benchmark_graphs")
        sys.exit()
    for x in files:
        if 'r0' in x or 'r1' in x or 'pop' in x or 'README' in x:
            continue
        g = nx.Graph()
        print(x)
        g.add_edges_from(fnss.parse_rocketfuel_isp_map(x).edges())
        # print("Trimming to connectivity %i" %conn)
        gt = trim_merge(g, conn)
        # relabelling
        gtL = nx.convert_node_labels_to_integers(gt)
        if (gtL.number_of_nodes() == 0):
            print("AS-Graph %s contains no node after trimming" % x)
            continue
        if (gtL.number_of_nodes() >= 1000):
            print("AS-Graph %s contains too many nodes" % x, gtL.number_of_nodes())
            continue
        if (nx.edge_connectivity(gtL) < conn):
            print("AS-Graph %s is not connected enough for connectivity %i" % (x, conn))
            continue
        else:
            print("AS-Graph %s with %i nodes is good" % (x, gtL.number_of_nodes()))
            nx.write_edgelist(gtL, x[:-4].replace("graphs/", "graphs/AS") + "-" + str(conn) + ".csv")

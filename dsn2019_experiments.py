import sys
import networkx as nx
import numpy as np
import random
import time
from arborescences import *
import objective_function_experiments as ofe
import glob

# run experiments with AS graphs (pre-generated)
# outX denote file handles to write results to
# seed is used for pseudorandom number generation in this run
# rep denotes the number of repetitions in the secondary for loop
def run_AS(outstretch=None, outtime=None, seed=0, rep=5):
    global swappy
    astr = ['RR-swap']  # , 'Greedy', 'Random']
    algos = {'RR-swap': RR_swap, 'Greedy': Trees, 'Random': RandomTrees}
    swappy = [0]
    files = glob.glob('./benchmark_graphs/AS*.csv')
    for x in files:
        print(x)
        sys.stdout.flush()
        k = int(x[-5:-4])
        g = nx.read_edgelist(x).to_directed()
        n = len(g.nodes())
        print(x, "number of nodes", n)
        sys.stdout.flush()
        g.graph['k'] = k
        nodes = list(g.nodes())
        random.shuffle(nodes)
        data = {v: {'complete': 0, 'stretch': [0 for i in range(min(rep, n))], 'depth': [0 for i in range(
            min(rep, n))], 'time': [0.0 for i in range(min(rep, n))]} for (v, k) in algos.items()}
        for count in range(min(rep, n)):
            g.graph['root'] = nodes[count]
            for a in astr:
                reset_arb_attribute(g)
                random.seed(seed)
                t1 = time.time()
                algos[a](g)
                t2 = time.time()
                s = -1
                d = -1
                t = t2-t1
                if num_complete_nodes(g) == n:
                    s = stretch(g)
                    d = depth(g)
                    data[a]['complete'] += 1
                    print("success", x, count)
                else:
                    print("fail", "results/dsn-fail_" +
                          x[-10:-4]+"_"+str(nodes[count])+".png", x, count)
                    drawArborescences(g, "results/dsn-fail_" +
                                      x[-10:-4]+"_"+str(nodes[count])+".png")
                data[a]['stretch'][count] = s
                data[a]['depth'][count] = d
                data[a]['time'][count] = t
                if outstretch != None:
                    outstretch.write("%s, %d, %d, %s, %d, %d\n" %
                                     (x, n, k, a, count, s))
                    outstretch.flush()
                if outtime != None:
                    outtime.write("%s, %d, %d, %s, %d, %f\n" %
                                  (x, n, k, a, count, t))
                    outtime.flush()
                sys.stdout.flush()
        count = min(rep, n)
        print(count, 'repetitions, k', g.graph['k'], 'n', n, x)
        print("algo, complete runs, stretch mean, median, max, avg time")
        for a in astr:
            comp = data[a]['complete']
            s = data[a]['stretch'][:count]
            d = data[a]['depth'][:count]
            t = data[a]['time'][:count]
            if comp > 0:
                s = [si for si in data[a]['stretch'][:count] if si > -1]
                d = [di for di in data[a]['depth'][:count] if di > -1]
                print(a + " %.2f ,%.2f (%d), %.2f (%d), %.2f (%.2f) s" % (comp/count,
                                                                          np.mean(s), np.max(s), np.mean(d), np.max(d), np.mean(t), np.max(t)))
            else:
                print(a + " %.2f, %.2f (%.2f) s" %
                      (comp/count, np.mean(t), np.max(t)))
        print()
        sys.stdout.flush()
        if rep == 1:
            return


# run experiments with regular graphs (pre-generated)
# k is the number of arborescences constructure
# n the number of nodes in the regular graphs
# outX denote file handles to write results to
# seed is used for pseudorandom number generation in this run
# rep denotes the number of repetitions in the secondary for loop
def run_regular(k=4, n=50, rep=100, outstretch=None, outtime=None, seed=0):
    global edge_labels, swappy
    edge_labels = {i: {} for i in range(k)}
    edge_labels[-1] = {}
    astr = ['RR', 'RR-con', 'RR-swap', 'RR-swap-con', 'Greedy', 'random']
    astr = ['RR', 'RR-swap', 'Greedy', 'random']
    algos = {'Later': BalanceLater, 'RR': RR, 'RR-con': RR_con, 'RR-swap': RR_swap, 'RR-swap-con': RR_con_swap, 'Greedy': Trees,
             'Greedy-swap-stretch': OptimizeGreedyStretch, 'Greedy-swap-depth': OptimizeGreedyDepth, 'bestSw': BestSwap, 'random': RandomTrees}
    data = {v: {'complete': 0, 'stretch': [0 for i in range(rep)], 'depth': [0 for i in range(
        rep)], 'time': [0.0 for i in range(rep)]} for (v, k) in algos.items()}
    swappy = [0]
    for i in range(rep):
        print("run regular, repetition, #complete, swappy",
              i, data[astr[0]]['complete'], np.max(swappy))
        sys.stdout.flush()
        random.seed(i)
        g = init_k_graph(k, n)
        root = list(g.nodes())[0]
        g.graph['root'] = root
        g.graph['k'] = k
        for a in astr:
            reset_arb_attribute(g)
            random.seed(i+seed)
            t1 = time.time()
            algos[a](g)
            t2 = time.time()
            s = -1
            d = -1
            t = t2-t1
            if num_complete_nodes(g) == n:
                s = stretch(g)
                d = depth(g)
                data[a]['complete'] += 1
            else:
                drawArborescences(g, "results/dsn-fail_"+str(i)+".png")
                print("failed")
            data[a]['stretch'][i] = s
            data[a]['depth'][i] = d
            data[a]['time'][i] = t
            comp = data[a]['complete']
            if outstretch != None:
                outstretch.write("regular, %d, %d, %s, %d, %d\n" %
                                 (n, k, a, i, s))
                outstretch.flush()
            if outtime != None:
                outtime.write("regular, %d, %d, %s, %d, %f\n" %
                              (n, k, a, i, t))
                outtime.flush()
            sys.stdout.flush()
    print()
    print(rep, 'repetitions, k', g.graph['k'], 'n', n, 'random regular graphs')
    print("algo, complete runs, stretch mean, median, max, avg time")
    for a in astr:
        comp = data[a]['complete']
        if comp > 0:
            s = [si for si in data[a]['stretch'][:rep] if si > -1]
            d = [di for di in data[a]['depth'][:rep] if di > -1]
            print(a + " %d ,%.2f (%d), %.2f (%d), %.2f (%.2f) s" % (comp,
                                                                    np.mean(s), np.max(s), np.mean(d), np.max(d), np.mean(t), np.max(t)))
            print(a + " %d ,%.2f (%d), %.2f (%d), %.2f (%.2f) s" % (comp,
                                                                    np.mean(s), np.max(s), np.mean(d), np.max(d), np.mean(t), np.max(t)))


# run experiments for dsn 2019 paper
# seed is used for pseudorandom number generation in this run
# switch determines which experiments are run
def dsn_experiments(switch="all", seed=0, short=None):
    if switch in ["AS", "all"]:
        for i in range(4,8):
            ofe.generate_trimmed_AS(i)
        if short:
            rep = short
        else:
            rep = 1000
        filename = "results/dsn2019-as_seed_"+str(seed)
        outstretch = open(filename+"_stretch.txt", 'a')
        outstretch.write(
            "#graph, size, connectivity, algorithm, index, stretch\n")
        outstretch.write(
            "#"+str(time.asctime(time.localtime(time.time())))+"\n")
        outtime = open(filename+"_time.txt", 'a')
        outtime.write("#graph, size, connectivity, algorithm, index, time\n")
        outtime.write("#"+str(time.asctime(time.localtime(time.time())))+"\n")
        run_AS(outstretch=outstretch, outtime=outtime, rep=rep, seed=seed)
        outstretch.close()
        outtime.close()
    if short:
        rep = short
    else:
        rep = 200
    if switch in ["connectivity", "all"]:
        n = 100
        for k in [5, 10, 15, 20, 25, 30]:  # ,200]:
            filename = "results/dsn2019-regular_nodes_grow_connectivity"+str(k)
            outstretch = open(filename+"_stretch.txt", 'a')
            outstretch.write(
                "#graph, size, connectivity, algorithm, index, stretch\n")
            outstretch.write(
                "#"+str(time.asctime(time.localtime(time.time())))+"\n")
            outtime = open(filename+"_time.txt", 'a')
            outtime.write(
                "#graph, size, connectivity, algorithm, index, time\n")
            outtime.write(
                "#"+str(time.asctime(time.localtime(time.time())))+"\n")
            run_regular(k=k, n=n, rep=rep, outstretch=outstretch,
                        outtime=outtime, seed=seed)
            outstretch.close()
            outtime.close()
            if short:
                break
    if switch in ["size", "all"]:
        k = 5
        for n in [10, 20, 50, 100, 200, 500, 1000]:  # ,200]:
            filename = "results/dsn2019-regular_nodes_grow_size"+str(n)
            outstretch = open(filename+"_stretch.txt", 'a')
            outstretch.write(
                "#graph, size, connectivity, algorithm, index, stretch\n")
            outstretch.write(
                "#"+str(time.asctime(time.localtime(time.time())))+"\n")
            outtime = open(filename+"_time.txt", 'a')
            outtime.write(
                "#graph, size, connectivity, algorithm, index, time\n")
            outtime.write(
                "#"+str(time.asctime(time.localtime(time.time())))+"\n")
            run_regular(k=k, n=n, rep=rep, outstretch=outstretch,
                        outtime=outtime, seed=seed)
            outstretch.close()
            outtime.close()
            if short:
                break


if __name__ == "__main__":
    global rep
    start = time.time()
    print(time.asctime(time.localtime(start)))
    switch = 'all'
    seed = 0
    short = None
    if len(sys.argv) > 1:
        switch = sys.argv[1]
    if len(sys.argv) > 2:
        seed = int(sys.argv[2])
    if len(sys.argv) > 3:
        short = int(sys.argv[3])
    if len(sys.argv) > 4:
        n = int(sys.argv[4])
    dsn_experiments(switch=switch, seed=seed, short=short)
    end = time.time()
    print("time elapsed", end-start)
    print("start time", time.asctime(time.localtime(start)))
    print("end time", time.asctime(time.localtime(end)))
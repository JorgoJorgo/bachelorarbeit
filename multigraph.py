import sys
import networkx as nx
import numpy as np
import itertools
import random
import time
from arborescences import *
from objective_function_experiments import *

DEBUG = False

# Bonsai with k0, k1
def MultiBonsai(g, k0, k1):
    reset_arb_attribute(g)
    multi_round_robin(g, k0, k1, cut=True, swap=True, reset=True, strict=True)
    return get_arborescence_list(g)

# Bonsai with preset k
def MultiBonsaiConnectivity(g):
    reset_arb_attribute(g)
    k0 = g.graph['k']
    k1 = nx.edge_connectivity(g)
    multi_round_robin(g, k0, k1, cut=True, swap=True, reset=True, strict=True)
    return get_arborescence_list(g)

# Bonsai with degree of destination as k
def MultiBonsaiDestinationDegree(g):
    reset_arb_attribute(g)
    # k is set to degree of root
    g.graph['k'] = len(g.in_edges(g.graph['root']))
    k0 = g.graph['k']
    k1 = nx.edge_connectivity(g)
    return multi_round_robin(g, k0, k1, cut=True, swap=True, reset=True, strict=False)

# compute the k^th arborescence of g greedily, prefer unused edges
def FindTreePreferUnused(g):
    n = len(g.nodes())
    T = nx.DiGraph()
    T.add_node(g.graph['root'])
    R = {g.graph['root']}
    c = nx.edge_connectivity(g)
    # heap of all border edges in form [(edge metric, (e[0], e[1])),...]
    h = []
    preds = sorted(g.predecessors(
        g.graph['root']), key=lambda k: random.random())
    #DEBUG = True
    dist = {g.graph['root']:0}
    for x in preds:
        heappush(h, (n*g[x][g.graph['root']]['used'], (x, g.graph['root'])))
    count = 0

    while len(h) > 0:
        if DEBUG: print(count, "heap", h)
        count +=1
        (d, e) = heappop(h)
        g.remove_edge(*e)
        # graph without this edge must still be c-1 connected
        if DEBUG: print("e", e, d)
        if DEBUG: print("e[0]", e[0])
        if DEBUG: print("dist of e[0]", dist[e[1]]+1)
        if DEBUG: print("e[0] not in R", e[0] not in R)
        if DEBUG: print("TestCut(g, e[0], g.graph['root']", TestCut(g, e[0], g.graph['root']))
        if DEBUG: print("c-1", c-1)
        if e[0] not in R and (TestCut(g, e[0], g.graph['root']) >= c-1):
            dist[e[0]] = dist[e[1]]+1
            if DEBUG: print("dist of e[0]", dist[e[0]])
            R.add(e[0])
            preds = sorted(g.predecessors(e[0]), key=lambda k: random.random())
            for x in preds:
                if x not in R:
                    heappush(h, (g[x][e[0]]['used']*n+dist[e[0]]+1, (x, e[0])))
            T.add_edge(*e)
        else:
            g.add_edge(*e)
    if len(R) < len(g.nodes()):
        print("Couldn't find next edge, number of nodes in arb", len(R))
        sys.exit() #TODO remove
        sys.stdout.flush()
    return T

# Greedy Decomposition creating k0 many spanning arborescences and fragments up to k1
def GreedyMultiArborescenceDecompositionPreferUnused(g, k0, k1):
    reset_arb_attribute(g)
    g.graph['k'] = k0
    GreedyArborescenceDecomposition(g)
    gg = g.to_directed()
    multi_arb_list = {i:[] for i in range(k1)}
    for (u,v) in gg.edges():
        if g[u][v]['arb'] > -1:
            gg[u][v]['used'] = 1
            multi_arb_list[g[u][v]['arb']].append((u,v, 0))
        else:
            gg[u][v]['used'] = 0
    for k in range(k0,k1):
        temp = gg.to_directed()
        for (u,v) in gg.edges():
            temp[u][v]['used'] = gg[u][v]['used']
        T = FindTreePreferUnused(temp)
        if not (T is None):
            for (u, v) in T.edges():
                if g[u][v]['arb'] == -1:
                    g[u][v]['arb'] = k
                multi_arb_list[k].append((u,v,gg[u][v]['used']))
                gg[u][v]['used'] += 1
    g.graph['used'] = True
    max_used = 0
    sum_additional = 0
    for (u,v) in gg.edges():
        g[u][v]['used'] = gg[u][v]['used']
        max_used = max(max_used, gg[u][v]['used'])
        sum_additional += max(0, gg[u][v]['used'] - 1)
    g.graph['max_used'] = max_used
    g.graph['sum_additional'] = sum_additional
    g.graph['multi_arb_list'] = multi_arb_list
    return get_arborescence_list(g)

# round robin implementation of constructing arborescences with re-use of edges if necessary
def multi_round_robin(g, k0, k1, cut=False, swap=False, reset=True, strict=True, ):
    if reset:
        reset_arb_attribute(g)
    n = Network(g, k1, g.graph['root']) #k1 was g.graph['k']
    K = n.K
    h = []
    dist = []
    prepareDS(n, h, dist, reset)
    index = 0
    swaps = 0
    count = 0
    num = len(g.nodes())
    count = 0
    while n.num_complete_nodes() < num and count < K*num*num:
        count += 1
        if len(h[index]) == 0:
            if swap and trySwap(n, h, index):
                index = (index + 1) % K
                swaps += 1
                continue
            else:
                #if swap:
                #    print("1 couldn't swap for index ", index, strict)
                if strict:
                    g = n.g
                    return -1
                else:
                    #print('not strict', n.num_complete_nodes(), max([len(h[i]) for i in range(K)]), count)
                    if max([len(h[i]) for i in range(K)]) == 0:
                        g = n.g
                        return get_arborescence_list(g)
                    else:
                        index = (index + 1) % K
                        continue
        (d, e) = heappop(h[index])
        while e != None and n.g[e[0]][e[1]]['arb'] > -1:  # in used_edges:
            if len(h[index]) == 0:
                if swap and trySwap(n, h, index):
                    index = (index + 1) % K
                    swaps += 1
                    e = None
                    continue
                else:
                    #if swap:
                    #    print("2 couldn't swap for index ", index)
                    if strict:
                        g = n.g
                        return -1
                    else:
                        #print('not strict', n.num_complete_nodes(), max([len(h[i]) for i in range(K)]), count)
                        if max([len(h[i]) for i in range(K)]) == 0:
                            g = n.g
                            return get_arborescence_list(g)
                        else:
                            index = (index + 1) % K
                            e = None
                            break
            else:
                (d, e) = heappop(h[index])
        ni = n.nodes_index(index)
        condition = (e != None and e[0] not in ni and e[1] in ni)
        if cut:
            condition = condition and (
                    K - index == 1 or TestCut(n.rest_graph(index), e[0], n.root) >= K-index-1)
        if condition:
            n.add_to_index(e[0], e[1], index)
            #print("normal add for index", index, e)
            # print(get_arborescence_dict(g)[index].nodes())
            # print(get_arborescence_dict(g)[index].edges())
            add_neighbors_heap_index(n, h, index, [e[0]])
            index = (index + 1) % K
    g = n.g

    g.graph['used'] = True
    max_used = 0
    sum_additional = 0
    for (u,v) in gg.edges():
        g[u][v]['used'] = gg[u][v]['used']
        max_used = max(max_used, gg[u][v]['used'])
        sum_additional += max(0, gg[u][v]['used'] - 1)
    g.graph['max_used'] = max_used
    g.graph['sum_additional'] = sum_additional
    return get_arborescence_list(g)

def draw_arborescence_index(g, index, pngname="results/weighted_graph.png"):
    plt.clf()
    multi = g.graph['multi_arb_list']
    arb_edges = [(u,v) for (u,v,used) in multi[index]]
    elabels = {(u,v):used for (u,v,used) in multi[index]}
    if 'pos' not in g.graph:
        g.graph['pos'] = nx.spring_layout(g)
    pos = g.graph['pos']
    nx.draw_networkx_labels(g, pos)
    nodes = list(g.nodes)
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'pink', 'olive',
              'brown', 'orange', 'darkgreen', 'navy', 'purple']
    node_colors = {v: 'gray' for v in nodes}
    color_list = [node_colors[v] for v in nodes]
    nx.draw_networkx_nodes(g, pos, nodelist=nodes, alpha=0.6,
                           node_color=color_list, node_size=2)
    nx.draw_networkx_edges(g, pos, edgelist=g.edges(),
                           width=1, alpha=0.1, edge_color='k')
    nx.draw_networkx_edges(g, pos, edgelist=arb_edges,
                               width=1, arrows=True, arrowsize=30, alpha=0.5, edge_color=colors[index%len(colors)])
    nx.draw_networkx_edge_labels(g, pos, elabels)
    plt.axis('off')
    plt.savefig(pngname)  # save as png
    plt.close()

def draw_graph(g, pngname="results/weighted_graph.png"):
    plt.clf()
    if 'pos' not in g.graph:
        g.graph['pos'] = nx.spring_layout(g)
    pos = g.graph['pos']
    nx.draw_networkx_labels(g, pos)
    nodes = list(g.nodes)
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'pink', 'olive',
              'brown', 'orange', 'darkgreen', 'navy', 'purple']
    node_colors = {v: 'gray' for v in nodes}
    color_list = [node_colors[v] for v in nodes]
    nx.draw_networkx_nodes(g, pos, nodelist=nodes, alpha=0.6,
                           node_color=color_list, node_size=2)
    nx.draw_networkx_edges(g, pos, edgelist=g.edges(),
                           width=1, alpha=0.5, edge_color='k')
    plt.axis('off')
    plt.savefig(pngname)  # save as png
    plt.close()

def draw(g, pngname="results/weighted_graph.png"):
    plt.clf()
    k = g.graph['k']
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'pink', 'olive',
              'brown', 'orange', 'darkgreen', 'navy', 'purple']
    if 'pos' not in g.graph:
        g.graph['pos'] = nx.spring_layout(g)
    pos = g.graph['pos']
    nx.draw_networkx_labels(g, pos)
    nodes = list(g.nodes)
    node_colors = {v: 'gray' for v in nodes}
    for node in nodes:
        if is_complete_node(g, node):
            node_colors[node] = 'black'
    color_list = [node_colors[v] for v in nodes]
    nx.draw_networkx_nodes(g, pos, nodelist=nodes, alpha=0.6,
                           node_color=color_list, node_size=2)
    for j in range(k):
        edge_j = [(u, v) for (u, v, d) in g.edges(data=True) if d['arb'] == j]
        nx.draw_networkx_labels(g, pos)
        nx.draw_networkx_edges(g, pos, edgelist=edge_j,
                               width=1, alpha=0.5, edge_color=colors[j%len(colors)])

    #if g.graph['used']:
    #    edge_labels = {(u,v):g[u][v]['used'] for (u,v) in g.edges()}
    #    nx.draw_networkx_edge_labels(g,pos, edge_labels)

    plt.axis('off')
    plt.savefig(pngname)  # save as png
    plt.close()
    for j in range(k):
        edge_j = [(u, v) for (u, v, d) in g.edges(data=True) if d['arb'] == j]
        nx.draw_networkx_labels(g, pos)
        nx.draw_networkx_edges(g, pos, edgelist=edge_j, width=1,
                               alpha=0.5, edge_color=colors[j%len(colors)])  # , arrowsize=20)
        plt.savefig(pngname+str(j)+'.png')  # save as png
        plt.close()


def experiments(n=10, seed=1, rep=10, switch='all'):
    out = open('results/multigraph-'+ switch + ".txt", 'w')
    out.write("n %i, seed %i, rep %i" % (n, seed, rep))
    for i in range(rep):
        random.seed(100*seed+i)
        good = True
        if switch in ["er", "all"]:
            #g = nx.random_regular_graph(k, n).to_directed()
            g = nx.erdos_renyi_graph(n, 1.5/np.log(n), 100*seed+i).to_directed()
            while nx.edge_connectivity(g) < 1:
                g = nx.erdos_renyi_graph(n,2*np.log(n)/n, 100*seed+i).to_directed()
        if switch in ["grid"]:
            d = 4
            g = nx.grid_2d_graph(d, d).to_directed()
            pos = {d*u+v:[u,v] for (u,v) in g.nodes()}
            g = nx.convert_node_labels_to_integers(g)
            g.graph['pos'] = pos
        if switch in ["zoo"]:
            g = read_zoo(i, 1)
            if g == None:
                good = False
            else:
                nn = len(g.nodes())
                mm = len(g.edges())
                avg_d = int(2*mm/nn)
                if g == None or nn >= 1.5*n or nn < 0.75*n or avg_d != 4:
                    good = False
        if not good:
            continue
        #nx.write_edgelist(g, "augmentation/"+switch+"-n-"+str(n)+"-i-"+str(i)+".edgelist")
        prepare_graph(g,nx.edge_connectivity(g),seed)
        g.graph['root'] = 0
        degrees = [g.degree(v) for v in g.nodes()]
        k1 = int(np.max(degrees)/2)
        k0 = g.graph['k']
        print("i", i,"k0", k0, "k1", k1)
        g_greedy = g.to_directed()
        #draw_graph(g_greedy, "results/graph"+switch+"_"+str(i)+".png")
        start = time.time()
        GreedyMultiArborescenceDecompositionPreferUnused(g_greedy, k0, k1)
        end = time.time()
        #for j in range(k1):
        #    draw_arborescence_index(g_greedy, j, "results/greedy_"+switch+"_"+str(i)+"_"+str(j)+"".png")
        n = len(g.nodes())
        out.write("\ni %i, n %i, k0 %i, k1 %i" % (i, n, k0, k1))
        out.write("\n   Greedy max number of times an edge is used " + str(g_greedy.graph['max_used']))
        out.write("\n   Greedy number of additional edges " + str(g_greedy.graph['sum_additional']))
        out.write("\n   Runtime in seconds " + str(end-start))
        multi_list = g_greedy.graph['multi_arb_list']
        for j in range(k1):
            out.write("\n      arb %i: " % j)
            out.write(str(multi_list[j]))
        out.flush()
        print("   Greedy max number of times an edge is used", g_greedy.graph['max_used'])
        print("   Greedy number of additional edges", g_greedy.graph['sum_additional'])
        print("   Runtime in seconds " + str(end-start))
    out.close()

if __name__ == "__main__":
    #default values
    seed = 0 #random seed
    n = 10 # number of nodes
    rep = 100 #number of experiments
    switch = 'all' #which experiments to run with these parameters
    if len(sys.argv) > 1:
        seed = int(sys.argv[1])
    if len(sys.argv) > 2:
        n = int(sys.argv[2])
    if len(sys.argv) > 3:
        rep = int(sys.argv[3])
    if len(sys.argv) > 4:
        switch = sys.argv[4]
    start = time.time()
    experiments(n, seed, rep, switch)
    end = time.time()
    print("time elapsed", end - start)
    print("start time", time.asctime(time.localtime(start)))
    print("end time", time.asctime(time.localtime(end)))
import os
import sys
import networkx as nx
from networkx import minimum_edge_cut as cut
from networkx.algorithms.flow import shortest_augmenting_path
from networkx.algorithms.connectivity import build_auxiliary_edge_connectivity
from networkx.algorithms.flow import build_residual_network
import numpy as np
import matplotlib.pyplot as plt
import itertools
from itertools import combinations
import random
import heapq
from heapq import heappush, heappop
import time

swappy = []

# set up associated data structures for k arborescences
# an edge that does not belong to any arborescences has its
# 'arb' attribute set to -1


def init_k_graph(k, n):
    g = nx.random_regular_graph(k, n).to_directed()
    while nx.edge_connectivity(g) < k:
        g = nx.random_regular_graph(k, n).to_directed()
    for (u, v) in g.edges():
        g[u][v]['arb'] = -1
    g.graph['k'] = k
    g.graph['root'] = 0 #set root node to be 0
    return g

# reset the arb attribute for all edges to -1, i.e., no arborescence assigned yet


def reset_arb_attribute(g):
    for (u, v) in g.edges():
        g[u][v]['arb'] = -1

# given a graph g and edge (u1, v1) and edge (u2,v2) swap the arborescences
# they belong to (will crash if the edges dont belong to the graph)


def swap(g, u1, v1, u2, v2):
    i1 = g[u1][v1]['arb']
    i2 = g[u2][v2]['arb']
    g[u1][v1]['arb'] = i2
    g[u2][v2]['arb'] = i1

# given a graph g and a minimum degree min, nodes with degree two are contracted into a link
# recursively and then all nodes with a degree < min are removed
# from g recursively until the graph is empty or all remaining nodes have at
# least degree min

def trim_merge(g, min):
    while True:
        while True:
            rem = []
            for v in g.nodes():
                if g.degree(v) == 2:
                    neighbors = list(g.neighbors(v))
                    for i in range(len(neighbors)-1):
                        g.add_edge(neighbors[0], neighbors[i+1])
                    rem.append(v)
            if len(rem) == 0:
                break
            g.remove_nodes_from(rem)
        rem = []
        for v in g.nodes():
            if g.degree(v) < min:
                rem.append(v)
        if len(rem) == 0:
            break
        g.remove_nodes_from(rem)
    return g

# given a graph g and a minimum degree min_degree, nodes with a lower degree are removed
# from g and their ex-neighbors are connected recursively until the graph is
# empty or all remaining nodes have at least degree min_degree


def trim2(g, min_degree):
    while True:
        rem = []
        for v in g.nodes():
            if g.degree(v) < min_degree:
                rem.append(v)
                for u in g[v]:
                    for u1 in g[v]:
                        g.add_edge(u, u1)
                break
        g.remove_nodes_from(rem)
        if len(rem) == 0:
            break
    return g

# given graph g return the ith arborescence as a digraph


def get_arborescence(g, i):
    a = nx.DiGraph()
    a.graph['root'] = g.graph['root']
    for (u, v) in g.edges():
        index = g[u][v]['arb']
        if index != i:
            continue
        a.add_edge(u, v)
    return a

# given a graph return the arborescences in a dictionary with indices as keys


def get_arborescence_dict(g):
    arbs = {}
    for (u, v) in g.edges():
        index = g[u][v]['arb']
        if index not in arbs:
            arbs[index] = nx.DiGraph()
            arbs[index].graph['root'] = g.graph['root']
            arbs[index].graph['index'] = index
        arbs[index].add_edge(u, v)
    return arbs

# given a graph return a list of its arborescences


def get_arborescence_list(g):
    arbs = get_arborescence_dict(g)
    sorted_indices = sorted([i for i in arbs.keys() if i >= 0])
    return [arbs[i] for i in sorted_indices]

# given a graph g, check if the associated graphs derived from the arb attribute
# are indeed acyclic


def is_arborescence_decomposition(g):
    arbs = get_arborescence_list(g)
    for a in arbs:
        if not nx.is_directed_acyclic_graph(a):
            return False
    return True

# return the number of paths in two trees that don't share an edge when
# traversing them towards the root


def num_independent_paths(T1, T2, root):
    SP1 = nx.shortest_path(T1, target=root)
    SP2 = nx.shortest_path(T2, target=root)
    count = 0
    for v in T1.nodes():
        if v in SP1 and v in SP2 and set(SP1[v][1:-1]).isdisjoint(set(SP2[v][1:-1])):
            count += 1
    return count

# return the number of indepependent paths in all pairs of
# arborescences associated with this graph g


def num_independent_paths_in_arbs(g):
    root = g.graph['root']
    T = get_arborescence_dict(g)
    n = len(g.nodes())
    count = 0
    for T1, T2 in itertools.combinations(T.values(), 2):
        if root in T1.nodes() and root in T2.nodes():
            count += num_independent_paths(T1, T2, root)
        else:
            return 0
    return count

# check the swappable condition (see DSN paper for background)
# given two edges outgoing from u to v1 and v2, vi should not be on the shortest
# path to the root on (u,vj)'s arborescence starting from u


def swappable(u, v1, v2, T1, T2):
    return not in_sp_to_r(T1, v2, u) and not in_sp_to_r(T2, v1, u)

# return true if v is on the shortest path to the root node starting from u on g


def in_sp_to_r(g, v, u):
    if g.graph['index'] == -1:
        return False
    return (v in nx.shortest_path(g, u, g.graph['root']))

# swap greedily while a pair of nodes with a better objective function evaluation
# after the swap can be found
# default is to minimize the objective function, passing along max=True will
# maximize it
def greedy_swap_obj(g, obj, max=False):
    arbs = get_arborescence_dict(g)
    o = obj(g)
    new_o = 0
    test = [(u, v) for (u, v) in g.edges() if u != g.graph['root']]
    random.shuffle(test)
    swapped = True
    count = 0
    while swapped:
        swapped = False
        for (u, v1) in test:
            for v2 in [nbr for nbr in g[u] if nbr != v1]:
                if swappable(u, v1, v2, arbs[g[u][v1]['arb']], arbs[g[u][v2]['arb']]):
                    swap(g, u, v1, u, v2)
                    new_o = obj(g)
                    if max:
                        if new_o> o:
                            o = new_o
                            swapped = True
                            count += 1
                        else:
                            swap(g, u, v1, u, v2)
                    else:
                        if new_o < o:
                            o = new_o
                            swapped = True
                            count += 1
                        else:
                            swap(g, u, v1, u, v2)
    return count

# return the stretch of the arborescence with index i on g (how much longer the
# path to the root is in the arborescence than in the original graph)
def stretch_index(g, index):
    arbs = get_arborescence_list(g)
    dist = nx.shortest_path_length(g, target=g.graph['root'])
    distA = {}
    if g.graph['root'] in arbs[index].nodes():
        distA = nx.shortest_path_length(arbs[index], target=g.graph['root'])
    else:
        return float("inf")
    stretch_vector = []
    for v in g.nodes():
        if v != g.graph['root']:
            stretch = -1
            if v in arbs[index].nodes() and v in distA:
                stretch = max(stretch, distA[v]-dist[v])
            else:
                return float("inf")
            stretch_vector.append(stretch)
    return max(stretch_vector)

# return the stretch of the arborence with the largest stretch


def stretch(g):
    stretch_vector = []
    for index in range(g.graph['k']):
        stretch_vector.append(stretch_index(g, index))
    return max(stretch_vector)

# return the longest path to the root in all arborescences


def depth(g):
    arbs = get_arborescence_list(g)
    distA = [{} for index in range(len(arbs))]
    for index in range(len(arbs)):
        if g.graph['root'] in arbs[index].nodes():
            distA[index] = nx.shortest_path_length(
                arbs[index], target=g.graph['root'])
        else:
            return float("inf")
    depth_vector = []
    for v in g.nodes():
        if v != g.graph['root']:
            depth = -1
            for index in range(len(arbs)):
                if v in arbs[index].nodes() and v in distA[index]:
                    depth = max(depth, distA[index][v])
                else:
                    return float("inf")
                depth_vector.append(depth)
    return max(depth_vector)

# return a list containing the arborescences of g in order of their depth


def total_arb_order_depth(g):
    arbs = get_arborescence_list(g)
    h = []
    for index in range(len(arbs)):
        heappush(h, (index, nx.eccentricity(g, v=g.graph['root'])))
    arb_order = []
    while len(h) > 0:
        (dist, index) = heappop(h)
        arb_order.append(arbs[index])
    return arb_order

# return a list containing the arborences of g in order of their stretch


def total_arb_order_stretch(g):
    arbs = get_arborescence_list(g)
    h = []
    for index in range(len(arbs)):
        heappush(h, (index, nx.eccentricity(g, v=g.graph['root'])))
    arb_order = []
    while len(h) > 0:
        (dist, index) = heappop(h)
        arb_order.append(arbs[index])
    return arb_order

# return a dictionary that lists the arborescence indices in shortest path order
# for each node


def arb_order(g):
    arbs = get_arborescence_list(g)
    distA = [{} for index in range(len(arbs))]
    for index in range(len(arbs)):
        if g.graph['root'] in arbs[index].nodes():
            distA[index] = nx.shortest_path_length(
                arbs[index], target=g.graph['root'])
        else:
            return float("inf")
    arb_order_dict = {}
    for v in g.nodes():
        if v != g.graph['root']:
            h = []
            dist_dict = {index: distA[index][v] for index in range(len(arbs))}
            for k, v in dist_dict:
                heappush(h, (v, k))
            arb_order_dict[v] = []
            while len(h) > 0:
                (dist, index) = heappop(h)
                arb_order_dict[v].append(index)
    return arb_order_dict

# return the nodes belonging to arborence i


def nodes_index(g, i):
    return set([u for (u, v, d) in g.edges(data=True) if d['arb'] == i or u == g.graph['root']])

# return the outgoing edges for node v with arborescence i


def outgoing_edges_index(g, v, i):
    return [u for u in g[v] if g[v][u]['arb'] == i]

# return the number of nodes that have one outgoing edge in each arborescence


def num_complete_nodes(g):
    complete = 0
    for v in g.nodes():
        c = True
        for i in range(g.graph['k']):
            if v != g.graph['root'] and len(outgoing_edges_index(g, v, i)) != 1:
                c = False
        if c:
            complete += 1
    return complete

# return true iff there is exactly one outgoing edge from node for each
# arborescence


def is_complete_node(g, node):
    for i in range(g.graph['k']):
        if len(outgoing_edges_index(g, node, i)) != 1:
            return False
    else:
        return True

# return length of shortest path between u and v on the indexth arborescence of g


def shortest_path_length(g, index, u, v):
    arbs = get_arborescence_dict(g)
    return nx.shortest_path_length(arbs[index], u, v)



# return nodes in giant connected component after failures


def giant_connected_component_nodes_after_failures(g, failures):
    G =g.to_undirected()
    G.remove_edges_from(failures)
    Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    return list(Gcc[0])

# return nodes in connected component with node d (after failures have been removed)

def connected_component_nodes_with_d_after_failures(g, failures, d):
    G =g.to_undirected()
    G.remove_edges_from(failures)
    Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    for i in range(len(Gcc)):
        if d in Gcc[i]:
            return list(Gcc[i])

# save png of arborescence embeddings


def drawArborescences(g, pngname="results/weighted_graph.png"):
    plt.clf()
    k = g.graph['k']
    edge_labels = {i: {} for i in range(k)}
    edge_labels[-1] = {}
    for e in g.edges():
        arb = g[e[0]][e[1]]['arb']
        edge_labels[arb][(e[0], e[1])] = ""
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
                               width=1, alpha=0.5, edge_color=colors[j])
    plt.axis('off')
    plt.savefig(pngname)  # save as png
    plt.close()
    for j in range(k):
        edge_j = [(u, v) for (u, v, d) in g.edges(data=True) if d['arb'] == j]
        nx.draw_networkx_labels(g, pos)
        nx.draw_networkx_edges(g, pos, edgelist=edge_j, width=1,
                               alpha=0.5, edge_color=colors[j])  # , arrowsize=20)
        plt.savefig(pngname+str(j)+'.png')  # save as png
        plt.close()

# return best edges to swap for stretch in g

def drawGraphWithLabels(g, pngname):
    plt.clf()
    if 'pos' not in g.graph:
        g.graph['pos'] = nx.spring_layout(g)
    pos = g.graph['pos']
    nx.draw_networkx_labels(g, pos)
    nx.draw_networkx_edges(g, pos, edgelist=list(g.edges()), style='solid',
                           width=2)
    nx.draw_networkx_nodes(g, pos, nodelist=list(g.nodes()), node_color='blue', alpha=1)
    nx.draw_networkx_nodes(g, pos, nodelist=[g.graph['root']], node_color='yellow', alpha=1)
    plt.axis('off')
    plt.savefig(pngname)  # save as png
    plt.close()

def find_best_swap(g):
    s = stretch(g)
    test = [(u, v) for (u, v) in g.edges() if u != g.graph['root']]
    e1 = None
    e2 = None
    for (u1, v1) in test:
        for (u2, v2) in test:
            if (v1 != v2) or (u1 != u2):
                swap(g, u1, v1, u2, v2)
                new_s = stretch(g)
                if new_s < s:
                    s = new_s
                    e1 = (u1, v1)
                    e2 = (u2, v2)
                swap(g, u1, v1, u2, v2)
    return e1, e2

# recursively swap best edges found (with respect to stretch) in g
def best_swap(g):
    (e1, e2) = find_best_swap(g)
    while e1 != None:
        swap(g, e1[0], e1[1], e2[0], e2[1])
        (e1, e2) = find_best_swap(g)

# return the edge connectivity of g between s and t
def TestCut(g, s, t):
    return nx.edge_connectivity(g, s, t)

# return a random arborescence rooted at the root
def FindRandomTree(g, k):
    T = nx.DiGraph()
    T.add_node(g.graph['root'])
    R = {g.graph['root']}
    dist = dict()
    dist[g.graph['root']] = 0
    # heap of all border edges in form [(edge metric, (e[0], e[1])),...]
    hi = []
    preds = sorted(g.predecessors(
        g.graph['root']), key=lambda k: random.random())
    for x in preds:
        hi.append((0, (x, g.graph['root'])))
        if k > 1:
            continue
    while len(hi) > 0:  # len(h) > 0:
        (d, e) = random.choice(hi)
        hi.remove((d, e))
        g.remove_edge(*e)
        if e[0] not in R and (k == 1 or TestCut(g, e[0], g.graph['root']) >= k-1):
            dist[e[0]] = d+1
            R.add(e[0])
            preds = sorted(g.predecessors(e[0]), key=lambda k: random.random())
            for x in preds:
                if x not in R:
                    hi.append((d+1, (x, e[0])))
            T.add_edge(*e)
        else:
            g.add_edge(*e)
    if len(R) < len(g.nodes()):
        print("Couldn't find next edge for tree with root %s" % str(r))
        sys.stdout.flush()
    return T

# associate random trees as arborescences with g
def RandomTrees(g):
    gg = g.to_directed()
    K = g.graph['k']
    k = K
    while k > 0:
        T = FindRandomTree(gg, k)
        if T is None:
            return None
        for (u, v) in T.edges():
            g[u][v]['arb'] = K-k
        gg.remove_edges_from(T.edges())
        k = k-1

# compute the k^th arborescence of g greedily
def FindTree(g, k):
    T = nx.DiGraph()
    T.add_node(g.graph['root'])
    R = {g.graph['root']}
    dist = dict()
    dist[g.graph['root']] = 0
    # heap of all border edges in form [(edge metric, (e[0], e[1])),...]
    h = []
    preds = sorted(g.predecessors(
        g.graph['root']), key=lambda k: random.random())
    for x in preds:
        heappush(h, (0, (x, g.graph['root'])))
        if k > 1:
            continue
    while len(h) > 0:
        (d, e) = heappop(h)
        g.remove_edge(*e)
        if e[0] not in R and (k == 1 or TestCut(g, e[0], g.graph['root']) >= k-1):
            dist[e[0]] = d+1
            R.add(e[0])
            preds = sorted(g.predecessors(e[0]), key=lambda k: random.random())
            for x in preds:
                if x not in R:
                    heappush(h, (d+1, (x, e[0])))
            T.add_edge(*e)
        else:
            g.add_edge(*e)
    if len(R) < len(g.nodes()):
        #print(
        #    "Couldn't find next edge for tree with g.graph['root'], ", k, len(R))
        sys.stdout.flush()
    return T

# compute the k^th arborescence of g greedily without checking for remaining connectivity
def FindTreeNoTestCut(g, k):
    T = nx.DiGraph()
    T.add_node(g.graph['root'])
    R = {g.graph['root']}
    dist = dict()
    dist[g.graph['root']] = 0
    # heap of all border edges in form [(edge metric, (e[0], e[1])),...]
    h = []
    preds = sorted(g.predecessors(
        g.graph['root']), key=lambda k: random.random())
    for x in preds:
        heappush(h, (0, (x, g.graph['root'])))
        if k > 1:
            continue
    while len(h) > 0:
        (d, e) = heappop(h)
        g.remove_edge(*e)
        if e[0] not in R:
            dist[e[0]] = d+1
            R.add(e[0])
            preds = sorted(g.predecessors(e[0]), key=lambda k: random.random())
            for x in preds:
                if x not in R:
                    heappush(h, (d+1, (x, e[0])))
            T.add_edge(*e)
        else:
            g.add_edge(*e)
    if len(R) < len(g.nodes()):
        print(
            "Couldn't find next edge for tree with g.graph['root']")
        sys.stdout.flush()
    return T

# associate a greedy arborescence decomposition with g
def GreedyArborescenceDecomposition(g):
    reset_arb_attribute(g)
    gg = g.to_directed()
    K = g.graph['k']
    k = K
    while k > 0:
        T = FindTree(gg, k)
        if T is None:
            return None
        for (u, v) in T.edges():
            g[u][v]['arb'] = K-k
        gg.remove_edges_from(T.edges())
        k = k-1
    return get_arborescence_list(g)

# run one iteration for a greedy arborescence and then round robin
def BalanceLater(g):
    reset_arb_attribute(g)
    gg = g.to_directed()
    K = g.graph['k']
    T = FindTree(gg, K)
    if T is None:
        return None
    for (u, v) in T.edges():
        g[u][v]['arb'] = K-1
    gg.graph['k'] = K-1
    gg.graph['root'] = g.graph['root']
    gg.remove_edges_from(T.edges())
    reset_arb_attribute(gg)
    round_robin(gg, swap=True)
    for (u, v) in gg.edges():
        g[u][v]['arb'] = gg[u][v]['arb']
    return get_arborescence_list(g)


# associate a greedy arborescence decomposition with g and then swap edges
# greedily to optimize stretch
def OptimizeGreedyStretch(g):
    GreedyArborescenceDecomposition(g)
    greedy_swap(g, stretchi=True)
    return get_arborescence_list(g)

# associate a greedy arborescence decomposition with g and then swap edges
# greedily to optimize Depth
def OptimizeGreedyDepth(g):
    GreedyArborescenceDecomposition(g)
    greedy_swap(g, stretchi=False)
    return get_arborescence_list(g)

# associate a greedy arborescence decomposition with g and then swap edges
# trying to find the best swap to optimize stretch
def BestSwap(g):
    GreedyArborescenceDecomposition(g)
    best_swap(g)
    return get_arborescence_list(g)

# Helper class (some algorithms work with Network, others without),
# methods as above
class Network:
    # initialize variables
    def __init__(self, g, K, root):
        self.g = g
        self.K = K
        self.root = root
        self.arbs = {}
        self.build_arbs()
        self.dist = nx.shortest_path_length(self.g, target=root)

    # create arbs data structure from edge attributes
    def build_arbs(self):
        self.arbs = {index: nx.DiGraph() for index in range(self.K)}
        for (u, v) in self.g.edges():
            index = self.g[u][v]['arb']
            if index > -1:
                self.arbs[index].add_edge(u, v)

    # create arborescence for index given edge attributes
    def build_arb(self, index):
        self.arbs[index] = nx.DiGraph()
        for (u, v) in self.g.edges():
            if self.g[u][v]['arb'] == index:
                self.arbs[index].add_edge(u, v)

    # return graph of edges not assigned to any arborescence
    def rest_graph(self, index):
        rest = nx.DiGraph()
        for (u, v) in self.g.edges():
            i = self.g[u][v]['arb']
            if i > index or i == -1:
                rest.add_edge(u, v)
        return rest

    # add edge (u,v) to arborescence of given index
    def add_to_index(self, u, v, index):
        old_index = self.g[u][v]['arb']
        self.g[u][v]['arb'] = index
        if index > -1:
            self.arbs[index].add_edge(u, v)
        if old_index > -1:
            self.build_arb(old_index)

    # remove edge (u,v) from the arborescence it belonged to
    def remove_from_arbs(self, u, v):
        old_index = self.g[u][v]['arb']
        self.g[u][v]['arb'] = -1
        if old_index > -1:
            self.build_arb(old_index)

    # swap arborescence assignment for edges (u1,v1) and (u2,v2)
    def swap(self, u1, v1, u2, v2):
        i1 = self.g[u1][v1]['arb']
        i2 = self.g[u2][v2]['arb']
        self.g[u1][v1]['arb'] = i2
        self.g[u2][v2]['arb'] = i1
        self.build_arb(i1)
        self.build_arb(i2)

    # return true iff graph with arborescence index i is a DAG
    def acyclic_index(self, i):
        return nx.is_directed_acyclic_graph(self.arbs[i])

    # return true if graoh of given index is really an arborescence
    def is_arb(self, index):
        arb = self.arbs[index]
        root = self.root
        if root in arb.nodes():
            distA = nx.shortest_path_length(arb, target=root)
        else:
            return False
        for v in arb.nodes():
            if v == root:
                continue
            if arb.out_degree(v) != 1 or v not in distA:
                return False
            # if self.K - index > 1:
            #   rest = self.rest_graph(index)
               # if not v in rest.nodes() or TestCut(self.rest_graph(index), v, root) < self.K-index-1:
                #    return False
        return True

    # return nodes that are part of arborescence for given index
    def nodes_index(self, index):
        if index > -1:
            arb = self.arbs[index]
            l = list(arb.nodes())
            for u in l:
                if u != self.root and arb.out_degree(u) < 1:
                    arb.remove_node(u)
            return arb.nodes()
        else:
            return self.g.nodes()

    # return number of nodes in all arborescences
    def num_complete_nodes(self):
        return len(self.complete_nodes())

    # return nodes which belong to all arborescences
    def complete_nodes(self):
        c = set(self.g.nodes())
        for arb in self.arbs.values():
            c = c.intersection(set(arb.nodes()))
        return c

    # return number of nodes in all arborescences
    def shortest_path_length(self, index, u, v):
        return nx.shortest_path_length(self.arbs[index], u, v)

    # return true iff node v is in shortest path from node u to root in
    # arborescence of given index
    def in_shortest_path_to_root(self, v, index, u):
        return (v in nx.shortest_path(self.arbs[index], u, self.root))

    # return predecessors of node v in g (as a directed graph)
    def predecessors(self, v):
        return self.g.predecessors(v)

# set up network data structures before using them
def prepareDS(n, h, dist, reset=True):
    if reset:
        reset_arb_attribute(n.g)
    for i in range(n.K):
        dist.append({n.root: 0})
        preds = sorted(n.g.predecessors(n.root), key=lambda k: random.random())
        heapT = []
        for x in preds:
            heappush(heapT, (0, (x, n.root)))
        h.append(heapT)
        n.arbs[i].add_node(n.root)

# try to swap an edge on arborescence index for network with heap h
def trySwap(n, h, index):
    ni = list(n.nodes_index(index))
    for v1 in ni:
        for u in n.g.predecessors(v1):
            index1 = n.g[u][v1]['arb']
            if u == n.root or index1 == -1 or u in ni:
                continue
            for v in n.g.successors(u):
                if n.g[u][v]['arb'] != -1 or v not in n.nodes_index(index1):
                    continue
                if not n.in_shortest_path_to_root(v1, index1, v):
                    n.add_to_index(u, v, index)
                    n.swap(u, v, u, v1)
                    if n.is_arb(index) and n.is_arb(index1):
                        update_heap(n, h, index)
                        update_heap(n, h, index1)
                        add_neighbors_heap(n, h, [u, v, v1])
                        return True
                    #print("undo swap")
                    n.swap(u, v, u, v1)
                    n.remove_from_arbs(u, v)
    return False

# add a new items to the heap
def update_heap(n, h, index):
    new = []
    for (d, e) in list(h[index]):
        if e[1] in n.arbs[index].nodes():
            d = n.shortest_path_length(index, e[1], n.root)+1
            heappush(new, (d, e))
    h[index] = new

# add neighbors to heap
def add_neighbors_heap(n, h, nodes):
    n.build_arbs()
    for index in range(n.K):
        add_neighbors_heap_index(n, h, index, nodes)


# add neighbors to heap for a given index and nodes
def add_neighbors_heap_index(n, h, index, nodes):
    ni = n.nodes_index(index)
    dist = nx.shortest_path_length(n.g, target=n.root)
    for v in nodes:
        if v not in ni:
            continue
        preds = sorted(n.g.predecessors(v), key=lambda k: random.random())
        d = n.shortest_path_length(index, v, n.root)+1
        stretch = d*1.0/dist[v]
        stretch = d
        for x in preds:
            if x not in ni and n.g[x][v]['arb'] == -1:
                heappush(h[index], (stretch, (x, v)))

# Round robin version without testing for cuts and swaps
def RR(g):
    return (round_robin(g, cut=False, swap=False))

# Round robin version with testing for cuts and no swaps


def RR_con(g):
    return (round_robin(g, cut=True, swap=False))

# Round robin version without testing for cuts and with swaps


def RR_swap(g):
    return (round_robin(g, cut=False, swap=True))

# Round robin version with testing for cuts and swaps


def RR_con_swap(g):
    return (round_robin(g, cut=True, swap=True))

# basic round robin implementation of constructing arborescences
def round_robin(g, cut=False, swap=False, reset=True):
    global swappy
    if reset:
        reset_arb_attribute(g)
    n = Network(g, g.graph['k'], g.graph['root'])
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
                if swap:
                    print("1 couldn't swap for index ", index)
                #drawArborescences(g, "balanced")
                # sys.stdout.flush()
                # plt.show()
                return -1
        (d, e) = heappop(h[index])
        while e != None and n.g[e[0]][e[1]]['arb'] > -1:  # in used_edges:
            if len(h[index]) == 0:
                if swap and trySwap(n, h, index):
                    index = (index + 1) % K
                    swaps += 1
                    e = None
                    continue
                else:
                    if swap:
                        print("2 couldn't swap for index ", index)
                    g = n.g
                    #print("2uuu", count, index)
                    #drawArborescences(g, "balanced")
                    # sys.stdout.flush()
                    # plt.show()
                    return -1
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
    swappy.append(swaps)
    g = n.g
    return get_arborescence_list(g)

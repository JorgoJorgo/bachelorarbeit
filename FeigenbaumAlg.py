import networkx as nx
import pickle
import copy
import random
import matplotlib.pyplot as plt
DEBUG = False

# Implementation of the algorithm described in https://cpsc.yale.edu/sites/default/files/files/tr1454.pdf
# To use it in benchmark_template.py, import Feigenbaum and extend algos with  'Feigenbaum': [FeigenbaumAlg.DAG, FeigenbaumAlg.FeigenbaumAlg]
# The first entry of the list is the precomputation algorithm, the second the actual routing algorithm
# Implemented by Paula-Elena Gheorghe

# function which returns a directed acyclic graph by applying the BFS
# algorithm on a given graph, rooted in the destination vertex
# given undirected graph g
# destination d (the root of the DAG)

def DAG(g,d=None):
    if (d is None):
        root = None
        gen = ((x,y) for x,y in g.nodes(data=True) if root == None)
        for (x,y) in gen:
            if y != {}: # if the node has an attribute
                if 'root' in y: # if the node has been marked as a root, it will be chosen as the destination node
                    root = x
        if root:
            d = root # we choose the node which was marked as the root node as the destination node
        else:
            d = list(g.nodes)[0] # we choose an arbitrary node as the destination node if no node was marked as the root node
    l = list(nx.edge_bfs(g, d))
    dag = nx.DiGraph()
    dag.add_edges_from(l)
    dag_reversed = dag.reverse() # the direction of all the edges will be reversed
    return dag_reversed

# the following function shall be called only once, in order to avoid overwriting edge attributes
# directed acyclic graph dag

def Initialization(dag):
    
    # we first pick a random edge from the graph to see if it already has an attribute 
    # (i.e. if it has already been initialized)
    i = 0
    n = list(dag.nodes)[i] # node from the DAG
    while (not list(dag.out_edges(n))):
        i += 1
        n = list(dag.nodes)[i]

    e = list(dag.out_edges(n))[0] # the first outgoing edge from node n

    # the DAG should be initialized only once; if the edges already have attributes, then 
    # the function has already been called
    if dag.get_edge_data(e[0], e[1]) != {}:
        return True

    value = []
    nx.set_edge_attributes(dag,value,"fp") # 'fp' attribute = forwarding pattern 
    value.append("null") # give a "null (set)" attribute to all the edges
    return False 

# directed acyclic graph dag

def dagForwardingRules(dag):

    for node in dag.nodes():
        if len(dag.out_edges(node)) > 0: # if the node can rely upon at least one outgoing edge
            for e in dag.out_edges(node): # if the edge is reliable
                outgoing_list = list(dag.out_edges(e[1]))  # we obtain the outgoing edges of the second node (which shares edge 'e' with the previous node)
                if (outgoing_list):
                    edge = outgoing_list[0] # we arbitrary choose the first edge which appears in the list of the second node's outgoing edges
                    dag[e[0]][e[1]]["fp"] = str(edge) # the package from the incoming edge will be redirected to the previously chosen outgoing edge
                    # when node e[1] receives a package from node e[0] through the edge that they share,
                    # it will be directed to an outgoing edge from node e[1]


# source s
# destination d
# link failure set fails 
# directed acyclic graph dag

def FeigenbaumAlg(s, d, fails, dag):
    
    if DEBUG:
        print('\n---DEBUG---\n')

    no_edges = len(list(dag.edges))
    no_nodes = len(list(dag.nodes)) + 1

    if no_edges == 0:
        if DEBUG:
            print("The DAG has no edges.")
        return (True, no_nodes, 0, [])


    # 1) Initialize: give a "null (set)" attribute to all the edges 

    already_initialized = Initialization(dag)

    # 2) Construct DAG (already done -> see "dag" parameter)

    # 3) Install DAG-based forwarding rules

    dagForwardingRules(dag)

    # 4) Install additional forwarding rules

    dag_copy = copy.deepcopy(dag) # dag_copy will contain all the alternative routing rules that will be set in the following steps
    node_list = (node for node in dag.nodes if node != d)

    if not already_initialized:
        for node in node_list:


            # the node is problematic, i.e. there do not yet exist at least two 
            # edge-disjoint forwarding paths to the destination in the forwarding-pattern
            # we must install additional forwarding rules

            # the nodes in question are:
            # node i (the current "node")
            # node j (adjacent to i)
            # node x (adjacent to j, with a path to the destination which doesn't contain the node i)

            found_j = False # a minimal node j has not yet been found
            it = 0
            pred = [] # list of the node's (pre-)predecessors

            for pred_node in dag.predecessors(node):
                pred.append(pred_node)

            if pred: # if the node has at least one predecessor, we will compute an alternative forwaring pattern

                j = pred[it]

                stop = False

                while (not found_j and not stop):

                    for pred_j in dag.predecessors(j):
                        if pred_j not in pred:
                            pred.append(pred_j)

                    found_x = False

                    cond1 = (x for x in dag.successors(j) if not found_x)

                    for x in cond1:
                        disjoint_paths = []
                        try:
                            disjoint_paths = list(nx.edge_disjoint_paths(dag, x, d))
                        except:
                            pass
                        if disjoint_paths:
                            cond2 = (path for path in disjoint_paths if not found_x)
                            for path in cond2:
                                if node not in path: # so that there will not be any cycles in the re-routing scheme
                                    found_x = True
                                    found_j = True
                    if found_x:
                        # compute simple route R between j and node
                        R = nx.algorithms.shortest_paths.generic.shortest_path(dag,j,node)
                        c = len(R) - 1
                        # compute inverse path from i to j
                        while not c == 0:
                            dag_copy.add_edge(R[c],R[c-1], fp = "null", alt = "alt") # 'alt' attribute = alternative routing path
                            c -= 1
                        c = len(R) - 1
                        while c>1 and dag_copy.edges[R[c] , R[c-1]]["fp"] == "null":
                            edge = (R[c-1],R[c-2])
                            dag_copy[R[c]][R[c-1]]["fp"] = str(edge) # set new edge attributes
                            c -= 1
                        if c == 1:
                            edge = (j,x)
                            dag_copy[R[c]][R[c-1]]["fp"] = str(edge)

                        if DEBUG:
                            print("The Feigenbaum Algorithm algorithm was applied successfully for node %s." % node)

                    if not found_j:
                        it += 1
                        if it >= len(pred): # we could not find a suitable predecessor node to which the node in question could send the package as an alternative routing path
                            if DEBUG:
                                print("An alternative fowarding pattern could not be computed for node %s." % node)
                            stop = True
                        else:
                            j = pred[it]
                    else:
                        if DEBUG:
                            print("-> The reliable node j is %s." % j)
            else:
                if DEBUG:
                    print("An alternative fowarding pattern could not be computed for node %s." % node)

        nx.write_gpickle(dag_copy, "routing_rules.gpickle") # we serialize the dag_copy graph, which contains the normal and the alternative routing rules


    dag_copy = nx.read_gpickle("routing_rules.gpickle") # we deserialize the dag_copy graph, which contains the normal and the alternative routing rules
    result = routing_feigenbaumalg(dag_copy, s, d, fails) # we check if the start node can still route the package to the desination node after some edges fail              

    if DEBUG:
        print('\n---DEBUG---\n')
    
    # (True/False, hops, 0, [])
    return (result[0],result[1],0,[])


# DAG which contains all the routing rules dag_copy 
# start node s
# destination node d
# link failure set fails 

def routing_feigenbaumalg(dag_copy, s, d, fails):

    """
    if DEBUG:
        nx.draw_networkx(dag_copy)
        plt.show()
    """
    
    for e in fails: # removing the failed edges from the DAG (both the normal and the alternative routing rules, if the case requires it)
        if (e[0],e[1]) in list(dag_copy.edges):
            dag_copy.remove_edge(e[0],e[1])
        if (e[1],e[0]) in list(dag_copy.edges):
            dag_copy.remove_edge(e[1],e[0])
            
    """
    if DEBUG:   
        nx.draw_networkx(dag_copy)
        plt.show()
    """

    no_nodes = len(list(dag_copy.nodes))

    try: 
        R = nx.algorithms.shortest_paths.generic.shortest_path(dag_copy,s,d)
        hops = len(R) - 1
    except:
        if DEBUG:
            print('There is no path from source node %s to destination anymore.' % s)
        hops = no_nodes + 1
        # Failure
        return (True, hops)
    
    # Success
    return (False, hops)

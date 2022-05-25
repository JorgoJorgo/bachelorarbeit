import sys
import networkx as nx
import numpy as np
import itertools
import random
import time
from arborescences import *
from objective_function_experiments import *

def MaximizeAdhocExtraLinks(g):
    AdHocExtraLinks(g)
    return GreedyMaximalDAG(g)
def MaximizeAugmentation(g):
    AugmentationDecomposition(g)
    return GreedyMaximalDAG(g)
def MaximizeAugmentationPreferReal(g):
    AugmentationDecompositionPreferReal(g)
    return GreedyMaximalDAG(g)
def MaximizeFindClusters(g):
    FindClusters(g)
    return GreedyMaximalDAG(g)



# keep forwarding precomputation
def KeepForwardingPrecomputation(g):
    verbose = 0 #set to 0 for normal, to 1 for verbose output
    d = g.graph['root']
    n = len(g.nodes())
    dist = nx.shortest_path_length(g, d)
    edge_weight = {}
    node_weight = {v: 0 for v in g.nodes()}
    dist_nodes = {i: set() for i in range(n)}
    down_links = {v: set() for v in g.nodes()}
    A_links = {v: set() for v in g.nodes()}
    up_links = {v: set() for v in g.nodes()}
    for (u,v) in g.edges():
        if u==v:
            continue
        if dist[u] > dist[v]:
            edge_weight[(u,v)] = n*n
            down_links[u].add(v)
        elif dist[u] == dist[v]:
            edge_weight[(u,v)] = n
            A_links[u].add(v)
        elif dist[u] < dist[v]:
            edge_weight[(u,v)] = 1
            up_links[u].add(v)
        node_weight[u] += edge_weight[(u,v)]
        dist_nodes[dist[u]].add(u)
        dist_nodes[dist[v]].add(v)
    label = {} #eulerian label
    label_size = {} #eulerian size
    for k,v in dist_nodes.items():
        if len(v) < 2:
            continue
        subgraph = g.subgraph(v)   #check if its euler, see paper again
        for component in nx.strongly_connected_components(subgraph):
            count = 0
            for (u,v) in nx.eulerian_circuit(g.subgraph(component)):
                label[(u,v)]=count
                if verbose == 1:  print('Das Label von ' + str((u,v)) + ' ist ' +  str(label[(u,v)]))
                count += 1
                #label_size[(u,v)] = len(component)
                label_size[(u,v)] = g.subgraph(component).number_of_edges()
                if verbose == 1:  print('Die Label Size von ' + str((u,v)) + ' ist ' + str(label_size[(u,v)]))
                #label_size[(u,v)] = len(g.subgraph(component)) #component or subgraph component?

# output to file to check for bugs
# =============================================================================
#     with open('keep-forward-precomp-debug.txt', mode='w') as file_object:
#         for i in g.nodes():
#             #for j in range(len(down_links[i])):
#             if len(down_links[i])>0:
#                 for j in down_links[i]:
#                     # downl = down_links[i]
#                     # dl = downl[j]
#                     print('A downlink of node ' + str(i) + ' is to node ' + str(j) + '\r\n', file=file_object)
#                     if len(A_links[i])>0:
#                         for j in A_links[i]:
#                             print(' An A-link of node ' + str(i) + ' is to node ' + str(j) + ' with label of ' + str(label[(i,j)]) + ' and label size of ' + str(label_size[(i,j)])  +'\r\n',file=file_object)
# =============================================================================

    return [label_size, label, edge_weight, node_weight, down_links, A_links, up_links]

# keep forwarding routing
def KeepForwardingRouting(s,d,fails,precomp, g):

    verbose = 0 #set to 0 for normal, to 1 for verbose output (latter limits hops to 20)
    [label_size, label, edge_weight, node_weight, down_links, A_links, up_links] = precomp
    hops = 0
    switches = 0 #doesn't make sense in this context, keep it so it fits with other data strucutrures
    failure_encountered = False
    detour_edges = [] #add edges taken to this list when the first failure has been encountered...
    n = len(g.nodes())
    incoming_link = (s,s)
    incoming_node = s
    if verbose == 1: print(' ################################################################ start new experiment with source ' + str(s) + ' and destination ' + str(d))
    while (s != d):


        if verbose == 1: print('Start new try to find a next link ++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        #remove incoming node from all link lists
        curr_dl = list(down_links[s])
        if incoming_node in curr_dl:
            curr_dl.remove(incoming_node)
        curr_al = list(A_links[s])
        if incoming_node in curr_al:
            curr_al.remove(incoming_node)
        curr_ul = list(up_links[s])
        if incoming_node in curr_ul:
            curr_ul.remove(incoming_node)

        #sort up/down according to weights (higher->earlier) and a-list according to labels (lower->earlier)  #maybe refactor to only sort if there is a failure to speed  up...
        curr_dl = sorted(curr_dl, key = lambda x: int(node_weight[x]), reverse=True)
        for t in curr_dl:
            if verbose == 1: print('The weight of down-node ' + str(t) + ' is ' + str(node_weight[t])) #todo verbose...up...
        curr_al = sorted(curr_al, key = lambda x: int(label[(s,x)]), reverse=False)  #KeyError: (670, 670) ...???? Maybe related to preprocessing..?
        for t in curr_al:
            if verbose == 1: print('The label of a-node ' + str(t) + ' is ' + str(label[(s,t)])) #todo verbose...up...
        curr_ul = sorted(curr_ul, key = lambda x: int(node_weight[x]), reverse=True)
        for t in curr_ul:
            if verbose == 1: print('The weight of up-node ' + str(t) + ' is ' + str(node_weight[t])) #todo: verbose...up...

        #init for a links
        a_overflow = 0 #counter, to try all a-links only once
        a_count = -1 #init counter for label of link (for safety)
        if incoming_link in list(A_links[incoming_node]): #if incoming was a-link, get correct counter
            a_count = label[incoming_link] # get label from incoming link
        elif len(curr_al)>0:
            a_count = label[(s,curr_al[0])]
        if len(curr_dl)>0:  # if down list is not empty, set nxt as first element of down list
            curr_list = curr_dl
            nxt = curr_list[0]
            curr_index = 0  # 0 for down, 1 for A, 2 for up
            if verbose == 1: print('I try the down link from ' + str(s) + ' to ' + str(nxt))
        elif len(curr_al)>0:  # if a list is not empty, set nxt as next a link: if incoming is a-link, then next, else, as first element of down list
            curr_list = curr_al
            if incoming_link in list(A_links[incoming_node]): #if incoming was a link
                a_count = (a_count+1) % label_size[incoming_link] #increase counter by 1
                nxt = next(i for i in list(A_links[s]) if label[(s,i)] == a_count)
            else:  #if incoming was not a-link
                nxt = curr_list[0]
                a_count = label[(s,curr_list[0])]
            curr_index = 1  # 0 for down, 1 for A, 2 for up
        elif len(curr_ul)>0:  # if a list is not empty, set nxt as first element of down list
            curr_list = curr_ul
            nxt = curr_list[0]
            curr_index = 2  # 0 for down, 1 for A, 2 for up
            if verbose == 1: print('I try the up link from ' + str(s) + ' to ' + str(nxt))
        else: #note: this should not happen, as we did not yet check if the next link is failed, but added for good measure...
           nxt = incoming_node
           curr_index = 3
           if verbose == 1: print('Oh no: Only the incoming edge is left to take from ' + str(s) + ' to ' + str(nxt) + ', even though the last hop was from ' + str(incoming_node)) #Todo : give a hard error because this should never happen, print out.. even sys.exit?




        if verbose == 1: print('Currently s is ' + str(s) + ' and nxt is ' + str(nxt) + ' and d is ' + str(d) + ' and the incoming node is ' + str(incoming_node))

        while (s, nxt) in fails or (nxt, s) in fails:
            if verbose == 1: print(' ### failure on the link ' + str((s,nxt)))
            if curr_index == 0: # down_links usage
                if curr_list.index(nxt) < len(curr_list)-1: # are there elements left?
                    if incoming_node != curr_list[curr_list.index(nxt)+1]:
                        nxt = curr_list[curr_list.index(nxt)+1] #next item from down_links
                        if verbose == 1: print('#################### found another down link################# from ' + str(s) + ' to ' + str(nxt))

                elif a_count>-1:
                    if verbose == 1: print('No elements left in down_link: I switch to a_links')
                    curr_index = 1
                    curr_list = curr_al
                    if a_count == label[(s,curr_al[0])]:
                        nxt = next(i for i in list(A_links[s]) if label[(s,i)] == a_count) #todo optimize, call curr_al
                        if verbose == 1: print('in down-loop, the first to try a-link is from ' + str(s) + ' to ' + str(nxt) + ' with an a_count of ' + str(a_count))
                    else:
                        a_count = (a_count+1) % label_size[incoming_link] #increase counter by 1
                        nxt = next(i for i in list(A_links[s]) if label[(s,i)] == a_count) #todo optimize, call curr_al
                        if verbose == 1: print('the a-link is from ' + str(s) + ' to ' + str(nxt) + ' with an a_count of ' + str(a_count))

                else:
                    if verbose == 1: print('No elements left in a_link or a_link empty: I switch to up_links')
                    curr_index = 2
                    curr_list = curr_ul #list(up_links[s])
                    if len(curr_list)>0:
                        nxt = curr_list[0]
                        if verbose == 1: print('the up-link is from ' + str(s) + ' to ' + str(nxt))
                    else:
                        nxt = incoming_node
                        curr_index = 3
                        if verbose == 1: print('Oh no: Only the incoming edge is left to take from ' + str(s) + ' to ' + str(nxt) + ', even though the last hop was from ' + str(incoming_node))

            elif curr_index == 1:
                if a_overflow < label_size[(s,curr_list[0])]:
                    a_overflow = a_overflow+1
                    if curr_list.index(nxt) < len(curr_list)-1:
                        if verbose == 1: print('the current index is ' + str(curr_list.index(nxt)) + ' and the length of the current list is ' + str(len(curr_list)) + ' and the label is ' + str(label[(s,nxt)]))
                        if verbose == 1: print('the next element is ' + str(curr_list[curr_list.index(nxt)+1]) + ' with an index of ' + str(curr_list.index(nxt)+1))
                        nxt = next(i for i in list(curr_list) if label[(s,i)] > a_count)
                        a_count = label[(s,nxt)]
                        if verbose == 1: print('trigger 1: the a-link is from ' + str(s) + ' to ' + str(nxt) + ' with an a_count of ' + str(a_count))
                    else:
                        nxt = curr_list[0]
                        a_count = label[(s,nxt)]
                    if verbose == 1: print('the a-link is from ' + str(s) + ' to ' + str(nxt))

                else:
                    if verbose == 1: print('No elements left in a_link: I switch to up_links')
                    curr_index = 2
                    curr_list = curr_ul #list(up_links[s])
                    if len(curr_list)>0:
                        nxt = curr_list[0]
                        if verbose == 1: print('the up-link is from ' + str(s) + ' to ' + str(nxt))
                    else:
                        nxt = incoming_node
                        curr_index = 3
                        if verbose == 1: print('Oh no: Only the incoming edge is left to take from ' + str(s) + ' to ' + str(nxt) + ', even though the last hop was from ' + str(incoming_node))

            elif curr_index == 2: # up_links usage
                if curr_list.index(nxt) < len(curr_list)-1: # are there elements left?
                    if incoming_node != curr_list[curr_list.index(nxt)+1]:
                        nxt = curr_list[curr_list.index(nxt)+1] #next item from down_links
                        if verbose == 1: print('#################### found another up link#################')
                    else:
                        if verbose == 1: print('oh no (up) only incoming is alive')
                        curr_index = 3
                        nxt = incoming_node
                else:
                    nxt = incoming_node
                    curr_index = 3
                    if verbose == 1: print('Oh no: Only the incoming edge is left to take from ' + str(s) + ' to ' + str(nxt) + ', even though the last hop was from ' + str(incoming_node))
            else:
                print('Error: Nxt is ' + str(nxt) + ' current node is ' + str(s))
                sys.exit()

        if failure_encountered:
            detour_edges.append((s,nxt))
        hops += 1
        n_end = n*n+20
        if verbose == 1: n_end=20
        if hops > n_end: #n*n*n:  #to kill early, later set back to n*n*n
            #probably a loop, return
            if verbose == 1: print('********************************************'''''''''''''''''''' I am stuck in a loop with many hops, good bye')
            return (True, -1, switches, detour_edges)
        incoming_link = (s,nxt)
        incoming_node = s
        if verbose == 1: print('Great success: Next hop is alive: I will go from ' + str(s) + ' to ' + str(nxt))
        s = nxt
    if verbose == 1: print('~~~~~~~~~~~~~~~~~~~~ Destination reached!~~~~~~~~~~~~~~~~~~~~~~~~~')
    return (False, hops, switches, detour_edges)



# add edges to DAGs until no further edges can be added
def GreedyMaximalDAG(g):
    not_assigned = set((u,v) for (u, v) in g.edges() if g[u][v]['arb'] == -1)
    assigned = [1]
    count = 0
    while len(assigned) > 0:
        assigned = []
        for (u,v) in not_assigned:
            dec_dict = get_arborescence_dict(g)
            for (index,arb) in dec_dict.items():
                if v in arb.nodes():
                    temp = arb.to_directed()
                    temp.add_edge(u,v)
                    if nx.is_directed_acyclic_graph(temp):
                        g[u][v]['arb'] == index
                        assigned.append((u,v))
                        break
        not_assigned.difference_update(assigned)
    return get_arborescence_list(g)


# Bonsai with preset k
def Bonsai(g):
    reset_arb_attribute(g)
    round_robin_strict(g, cut=True, swap=True, reset=True, strict=True)
    return get_arborescence_list(g)

# Bonsai with degree of destination as k
def BonsaiDestinationDegree(g):
    reset_arb_attribute(g)
    # k is set to degree of root
    g.graph['k'] = len(g.in_edges(g.graph['root']))
    return round_robin_strict(g, cut=True, swap=True, reset=True, strict=False)

# add edges to DAGs until no further edges can be added
def DegreeMaxDAG(g):
    reset_arb_attribute(g)
    gg = g.to_directed()
    # K is set to degree of root
    K = len(g.in_edges(g.graph['root']))
    k = K
    while k > 0:
        T = FindTreeNoContinue(gg, k)
        if T is None or len(T.edges()) == 0:
            K = K-1
            k = k-1
            continue
        for (u, v) in T.edges():
            g[u][v]['arb'] = K-k
        gg.remove_edges_from(T.edges())
        k = k-1
    return GreedyMaximalDAG(g)

# compute the k^th arborescence of g greedily
def FindTreeNoContinue(g, k):
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
        # the original FindTree method continues here if k > 1
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

# use networkx edge augmentation
def AugmentationDecompositionPreferReal(g):
    AugmentationDecomposition(g, prefer=True)

# use networkx edge augmentation
# if prefer = True then the decomposition favours real edges
def AugmentationDecomposition(g, prefer=False):
    g1 = g.to_undirected()
    g1.remove_edges_from(nx.selfloop_edges(g1))
    if 'k' not in g1.graph.keys():
        g1.graph['k'] = nx.edge_connectivity(g1)
    k0 = g1.graph['k']
    # set k1 to max degree
    degrees = [g1.degree(v) for v in g1.nodes()]
    k1 = np.max(degrees)
    g1.graph['k1'] = k1
    g2 = g1.to_undirected()
    g2.remove_edges_from(nx.selfloop_edges(g2))
    augmentation = list(nx.k_edge_augmentation(g2, k1))
    g2.add_edges_from(augmentation)
    g2 = g2.to_directed()
    for (u,v) in g2.edges():
        g2[u][v]['virtual'] = (u,v) in augmentation or (v,u) in augmentation
        if not prefer:
            g2[u][v]['virtual'] = False
    g2.graph['k'] = k1
    GreedyArborescenceDecompositionPreferReal(g2)
    reset_arb_attribute(g)
    for (u,v) in g2.edges:
        if (u,v) in g.edges():
            g[u][v]['arb'] = g2[u][v]['arb']
    return get_arborescence_list(g)

# compute the k^th arborescence of g greedily
def FindTreePreferReal(g, k):
    n = len(g.nodes())
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
        if g[x][g.graph['root']]['virtual']:
            heappush(h, (n+0, (x, g.graph['root'])))
        else:
            heappush(h, (0, (x, g.graph['root'])))

    while len(h) > 0:
        (d, e) = heappop(h)
        g.remove_edge(*e)
        if e[0] not in R and (k == 1 or TestCut(g, e[0], g.graph['root']) >= k-1):
            dist[e[0]] = d+1
            R.add(e[0])
            preds = sorted(g.predecessors(e[0]), key=lambda k: random.random())
            for x in preds:
                if x not in R:
                    if g[x][e[0]]['virtual']:
                        heappush(h, (n+d+1, (x, e[0])))
                    else:
                        heappush(h, (d+1, (x, e[0])))
            T.add_edge(*e)
        else:
            g.add_edge(*e)
    if len(R) < len(g.nodes()):
        print("Couldn't find next edge for tree with g.graph['root'], ", k, len(R))
        sys.stdout.flush()
    return T

# associate a greedy arborescence decomposition with g
def GreedyArborescenceDecompositionPreferReal(g):
    reset_arb_attribute(g)
    gg = g.to_directed()
    for (u,v) in gg.edges():
        gg[u][v]['virtual'] = g[u][v]['virtual']
    sys.stdout.flush()
    K = g.graph['k']
    k = K
    while k > 0:
        for (u,v) in gg.edges():
            gg[u][v]['virtual'] = g[u][v]['virtual']
        T = FindTreePreferReal(gg, k)
        if T is None:
            return None
        for (u, v) in T.edges():
            g[u][v]['arb'] = K-k
        gg.remove_edges_from(T.edges())
        k = k-1
    return get_arborescence_list(g)

# Route according to deterministic circular routing, skip current arborescence if no neighbors.
# source s
# destination d
# link failure set fails
# arborescence decomposition T
def RouteDetCircSkip(s, d, fails, T, g):
    curT = 0
    detour_edges = []
    hops = 0
    switches = 0
    k = len(T)
    if k == 0:
        return (True, -2, switches, detour_edges)
    n = max([len(T[i].nodes()) for i in range(k)])
    dist = nx.shortest_path_length(g, target=d)
    #print('nodes', g.nodes())
    #print('dist', dist.keys())
    #print('s,d', s, d )
    #drawGraphWithLabels(g,"tst.png")
    while (s != d):
        while (s not in T[curT].nodes()) and switches < k*n:
            curT = (curT+1) % k
            switches += 1
        if switches >= k*n:
            break
        nxt = list(T[curT].neighbors(s))
        if len(nxt) == 0:
            #print("Warning: no neighbours available --> switching to the next tree")
            curT = (curT+1) % k
            switches += 1
            continue
        if (d,s) in g.edges() and not ((d,s) in fails or (s,d) in fails):
            nxt = [d]+nxt
        if len(nxt) == 0:
            curT = (curT+1) % k
            switches += 1
            break
        breaking = False
        #remove bad nodes from list  TODO (ensure this is not needed)
        len_nxt = len(nxt)
        nxt = [x for x in nxt if x in dist.keys()]
        if len(nxt) < len_nxt :
            print('shortened')
            nx.write_edgelist(g, "somethingwrong.csv")
            drawGraphWithLabels(g,"somethingwrong.png")
            if len(nxt) == 0:
                curT = (curT+1) % k
                switches += 1
                break
        #sort list of next hops by distance
        nxt = sorted(nxt, key = lambda ele: dist[ele])
        index = 0
        while (nxt[index], s) in fails or (s, nxt[index]) in fails:
            index = index + 1
            if index >= len(nxt):
                curT = (curT+1) % k
                switches += 1
                breaking = True
                break
        if not breaking:
            if switches > 0 and curT > 0:
                detour_edges.append((s, nxt[index]))
            s = nxt[index]
            hops += 1
        if hops > n*n or switches > k*n:
            return (True, -1, switches, detour_edges)
    return (False, hops, switches, detour_edges)

# Route according to deterministic circular routing as described by Chiesa et al.
# Extended to work for non-spanning arborescences
# source s
# destination d
# link failure set fails
# arborescence decomposition T
def RouteDetCircNotSpanning(s, d, fails, T):
    curT = 0
    detour_edges = []
    hops = 0
    switches = 0
    if T == []:
        return (True, -1, switches, detour_edges)
    n = len(T[0].nodes())
    k = len(T)
    while (s != d):
        if (s not in T[curT].nodes()):
            #print('node %i not in arborescences %i' % (s,curT))
            return (True, -1, switches, detour_edges)
        nxt = list(T[curT].neighbors(s))
        if len(nxt) != 1:
            print("Bug: too many or too few neighbours")
            sys.exit()
            return (True, -1, switches, detour_edges)
        nxt = nxt[0]
        if (nxt, s) in fails or (s, nxt) in fails:
            curT = (curT+1) % k
            switches += 1
        else:
            if switches > 0 and curT > 0:
                detour_edges.append((s, nxt))
            s = nxt
            hops += 1
        if hops > n or switches > k*n:
            return (True, -1, switches, detour_edges)
    return (False, hops, switches, detour_edges)


# Algo 1:
# give weights to arcs, form minimal weight virtual link usage arborescences
def VirtualLinks(g):
    reset_arb_attribute(g)
    R = g.to_directed()
    n = len(g.nodes())
    # k is connectivity
    k0 = g.graph['k']
    # k1 is set to degree of root (not described in algo...)
    k1 = len(g.in_edges(g.graph['root']))
    #run greedy arborescence decomposition for k
    Ts = GreedyArborescenceDecomposition(g)
    T1 = Ts[0]
    # set w(e) = 1 for all arcs used in T and set R = g\T
    for (u, v) in g.edges():
        if g[u][v]['arb'] >= 0:
            g[u][v]['w'] = 1
            R.remove_edge(u,v)
        else:
            g[u][v]['w'] == 0
    for i in range(k0,k1):
        components = list(nx.connected_component_subgraphs(R))
        for c in components:
            if g.graph['root'] in c.nodes():
                c1 = c
                T = nx.minimum_spanning_tree(c1)
                break
        components.remove(c1)
        while len(T.nodes()) < n:
            Bi = nx.minimum_spanning_tree(components[0])
            (a, b, p1) = min_distance_path(T, Bi, T1)
            Bi.add_edges(p1)
            T.add_edges(Bi.edges())
            for (u,v) in Bi.edges():
                g[u][v]['w'] += 1
                if g[u][v]['arb'] <= 0:
                    g[u][v]['arb']  = i
            R.remove_edges(Bi.edges())
            components=components[1:]
    return get_arborescence_list(g)

# helper function finding nodes a in T, b in Bi with shortest path p1
# on T1 from b to a, return (a,b,p1)
def min_distance_path(T, Bi, T1):
    min_dist = len(T1.nodes()) + 1
    result = (-1,-1, -1)
    for a in T.nodes():
        for b in Bi.nodes():
            # could be extended to consider weights?
            p1 = nx.shortest_path(T1,source=b, target=a)
            if len(p1) < min_dist:
                result = (a,b,p1)
    return result


# ------------------------------------------------------------------------------
# [Andrzej] The following functions are required by the FindClusters heuristic algorithm
# 1) Find all clusters in the original graph, mark the involved nodes including direct neighbors.
# 2) Find the strongly connected components within a subgraph comprising the marked nodes.
# 3) Make sure the connected components contain at least 3 nodes.
# 4) To improve local edge connectivity, remove all nodes of degree 1 from the connected components.
# 5) Find local trees in the connected components (greedy).
# 6) Assign the unused arcs of the original graph to the new local trees (existing assignments have priority).


# For each node, compute additional parameters
def compute_additional_node_parameters( G, mark_cluster_neighbors ):
    #print( "Computing additional node parameters" )

    # Distances from all source nodes to the root node

    distances = nx.shortest_path_length( G, target = G.graph[ 'root' ] )

    # Clustering coefficient of each node

    clustering_coefficients = nx.clustering( G )

    # Other parameters

    for u in G.nodes():
        G.nodes[ u ][ 'marked' ] = False

    for u in G.nodes():
        G.nodes[ u ][ 'clustering_coefficient' ] = clustering_coefficients[ u ]

        if not u in distances:
            distances[ u ] = len( G.edges() )

        G.nodes[ u ][ 'distance_to_root' ] = distances[ u ]

        # Mark nodes based on the following criteria

        if clustering_coefficients[ u ] > 0.0:
            G.nodes[ u ][ 'marked' ] = True

            if mark_cluster_neighbors:
                for v in G[ u ]:
                    G.nodes[ v ][ 'marked' ] = True

        #print("%s" % G.nodes[ u ])

    return G


# Return a subgraph of 'G' based on the marked nodes
def return_subgraph_with_marked_nodes( G ):
    marked_nodes = list()

    for u in G.nodes():
        if 'marked' in G.nodes[ u ].keys() and G.nodes[ u ][ 'marked' ] == True:
            marked_nodes.append( u )

    Gm = nx.DiGraph( G.subgraph( marked_nodes ) )

    # Remove nodes which have been included in the subgraph, but had not been marked

    nodes_to_remove = list()

    for u in Gm.nodes():
        #print("%s" % Gm.nodes[ u ])
        if not 'marked' in Gm.nodes[ u ].keys() or Gm.nodes[ u ][ 'marked' ] == False:
            nodes_to_remove.append( u )

    Gm.remove_nodes_from( nodes_to_remove )

    return Gm


# Return the list of nodes having degree 1
def return_nodes_of_degree_one( G ):
    deg_one_nodes = list()

    for u in G.nodes():
        if len( G[ u ] ) == 1:
            deg_one_nodes.append( u )

    return deg_one_nodes


# Return the list of nodes having the minimum degree
def return_nodes_of_min_degree( G ):
    min_deg_nodes = list()
    Gm = G.to_undirected()
    degree_histogram = nx.degree_histogram( Gm )
    d = 0

    for n in degree_histogram:
        if n > 0:
            break

        d += 1

    #print( "--> Selected %d nodes of degree %d" % ( n, d ) )

    for u in Gm.nodes():
        if nx.degree( Gm, u ) == d:
            min_deg_nodes.append( u )

    return ( d, min_deg_nodes )


# Return the node which is the closest to the destination
def return_gw_node_towards_the_global_root( G ):
    gw = -1
    distance = -1

    for u in G.nodes():
        if distance == -1 or G.nodes[ u ][ 'distance_to_root' ] < distance:
            gw = u
            distance = G.nodes[ u ][ 'distance_to_root' ]

    return gw


# The main function of this algorithm (variant in which clusters neighbors are marked as well)
def FindClusters( G ):
    #
    # Compute additional graph parameters and include them as metadata
    # associated with nodes of the graph
    #

    G = compute_additional_node_parameters( G, True )

    #
    # Find the primary set of spanning arborescences covering the entire graph 'G'
    #

    GreedyArborescenceDecomposition( G )

    #
    # Create a subgraph 'Gm' of 'G' based on the marked nodes
    #

    Gm = return_subgraph_with_marked_nodes( G )
    #print( "[FindClusters] --> Initial parameters of Gm: n = %d, e = %d, k = %d" % ( nx.number_of_nodes( Gm ), nx.number_of_edges( Gm ), nx.edge_connectivity( Gm ) ) )

    #
    # Identify and print all strongly connected components of 'Gm', such that contain at least 3 nodes
    #

    components = list()
    components_all = list( nx.strongly_connected_components( Gm ) )

    for c in components_all:
        if len( c ) > 2:
            components.append( list( c ) )

    #print( "[FindClusters] --> Connected components having at least 3 nodes: %d" % len( components ) )

    #
    # For each connected component, try to improve its 'k'
    # Then, find the corresponding 'k' spanning arborescences
    #

    extra_arborescences_count = 0

    for c in components:
        #print( "[FindClusters] Connected component: Gc = %s" % c )
        Gc = nx.DiGraph( Gm.subgraph( c ) )

        # Try to improve the local edge connectivity by removing nodes of degree 1

        while nx.number_of_nodes( Gc ) > 3:
            deg_one_nodes = return_nodes_of_degree_one( Gc )

            if len( deg_one_nodes ) == 0:
                break

            Gc.remove_nodes_from( deg_one_nodes )
            #print( "[FindClusters] --> Removed nodes of degree 1: %s" % deg_one_nodes )

        if nx.number_of_nodes( Gc ) < 3:
            continue

        Gc.graph[ 'k' ] = nx.edge_connectivity( Gc )

        if Gc.graph[ 'k' ] < 2:
            #print( "[FindClusters] --> Falling back to the main tree" )
            continue

        Gc.graph[ 'root' ] = return_gw_node_towards_the_global_root( Gc )

        #print( "[FindClusters] --> Edge connectivity of Gc: %d" % Gc.graph[ 'k' ] )
        #print( "[FindClusters] --> Number of nodes: %d in G, %d in Gc" % ( nx.number_of_nodes( G ), nx.number_of_nodes( Gc ) ) )
        #print( "[FindClusters] --> Number of arcs: %d in G, %d in Gc" % ( nx.number_of_edges( G ), nx.number_of_edges( Gc ) ) )
        #print( "[FindClusters] --> Number of arborescences: %d in G, %d in Gc" % ( G.graph[ 'k' ], Gc.graph[ 'k' ] ) )

        # Find the set of arborescences covering the entire subgraph 'Gc'

        GreedyArborescenceDecomposition( Gc )

        # Assign the corresponding arcs of the original graph to exactly one arborescence (sometimes just 'set of links')
        # Existing assignments have priority over the new ones

        extra_arborescences = dict()

        for ( u, v ) in Gc.edges():
            if Gc[ u ][ v ][ 'arb' ] == -1 or G[ u ][ v ][ 'arb' ] > -1:
                continue

            if not Gc[ u ][ v ][ 'arb' ] in extra_arborescences.keys():
                extra_arborescences[ Gc[ u ][ v ][ 'arb' ] ] = list()

            extra_arborescences[ Gc[ u ][ v ][ 'arb' ] ].append( ( u, v ) )

        i = 0	# Index of an extra tree

        for ( arb_id, arc_list ) in extra_arborescences.items():
            for ( u, v ) in arc_list:
                G[ u ][ v ][ 'arb' ] = G.graph[ 'k' ] + extra_arborescences_count + i
                #print( "[FindClusters] --> Added an arc into an extra tree: G[ u ][ v ][ 'arb' ] = %d, G.graph[ 'k' ] = %d, extra_arborescences_count = %d, i = %d" % ( G[ u ][ v ][ 'arb' ], G.graph[ 'k' ], extra_arborescences_count, i ) )

            i += 1

        # Note that not all of the extra arborescences may have been added to 'G',
        # as the already-assigned arcs will not be included in new arborescences

        extra_arborescences_count += len( extra_arborescences )

    arborescence_list = get_arborescence_list( G )
    #print( "[FindClusters] Result: constructed %d trees" % len( arborescence_list ) )

    return arborescence_list

# ------------------------------------------------------------------------------

def drawArborescences(g, pngname="results/weighted_graph.png"):
    plt.clf()
    k = g.graph['k']
    if 'k1' in g.graph.keys():
        k = g.graph['k1']
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

def drawAugmentedGraph(g, pngname="results/augmented_graph.png"):
    plt.clf()
    if 'pos' not in g.graph:
        g.graph['pos'] = nx.spring_layout(g)
    pos = g.graph['pos']
    nx.draw_networkx_labels(g, pos)
    nodes = list(g.nodes)
    edge_solid = [(u, v) for (u, v, d) in g.edges(data=True) if d['augmented'] == False]
    edge_dashed = [(u, v) for (u, v, d) in g.edges(data=True) if d['augmented'] == True]
    nx.draw_networkx_edges(g, pos, edgelist=edge_solid, style='solid',
                               width=2)
    nx.draw_networkx_edges(g, pos, edgelist=edge_dashed, style='dashed',
                           width=1)
    nx.draw_networkx_nodes(g, pos, nodelist=nodes, node_color='blue', alpha=1)
    nx.draw_networkx_nodes(g, pos, nodelist=[g.graph['root']], node_color='yellow', alpha=1)
    plt.axis('off')
    plt.savefig(pngname)  # save as png
    plt.close()

# basic round robin implementation of constructing arborescences
def round_robin_strict(g, cut=False, swap=False, reset=True, strict=True):
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
                #if swap:
                #    print("1 couldn't swap for index ", index, strict)
                if strict:
                    g = n.g
                    return -1
                else:
                    #print('not strict', n.num_complete_nodes(), max([len(h[i]) for i in range(K)]), count)
                    swappy.append(swaps)
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
                        swappy.append(swaps)
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
    swappy.append(swaps)
    g = n.g
    return get_arborescence_list(g)

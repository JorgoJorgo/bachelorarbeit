import sys
import networkx as nx
import numpy as np
import itertools
import random
import time
from arborescences import *
from extra_links import *
import glob

from trees import get_parent_node

#global variables in this file
seed = 1
n = 10
rep = 1
k = 8
f_num = 40
samplesize=20
name = "experiment-routing"

#set global variables
def set_params(params):
    set_routing_params(params)

def set_routing_params(params):
    global seed, n, rep, k, samplesize, name, f_num
    [n, rep, k, samplesize, f_num, seed, name] = params


#################################################################################################################################
#TODO
# hier fehlt noch mein routingalgorithmus
#################################################################################################################################

#wir fangen an alle edps nach aufsteigender länge durchzugehen
#am ende wenn wir alle edps durchhaben probieren wir den tree durchzugehen da dieser der längste ist und somit die meisten möglichkeiten drin hat zusätzlich zum längsten edp

#source s 
#destination d
#failures fails edge (u,v)
#paths [source][destination]{'trees':{graph}], 'edps':[[]] , 'distance':[distanzen von allen nodes zur destination]}
#die edps sind dabei in aufsteigender Reihenfolge sortiert
def RouteOneTree(s,d,fails,paths):
    currentNode = -1
    edpIndex = 0
    detour_edges = []
    hops = 0
    switches = 0
    tree = paths[s][d]['tree']
    edps_for_s_d = paths[s][d]['edps']
    #distance = paths[s][d]['distance']
    print('Routing started for ' , s , " to " , d )
    #print(fails)
    #anhand der edps (außer dem längsten, also dem letzten) mit dfs versuchen zu routen
    for edp in edps_for_s_d:
        if edp != edps_for_s_d[len(edps_for_s_d) -1]:
            currentNode = edp[edpIndex]
            while (currentNode != d):
                if (edp[edpIndex], edp[edpIndex +1]) in fails or (edp[edpIndex +1], edp[edpIndex]) in fails:
                    # wir schalten zum nächsten pfad
                    switches += 1
                    #die kanten die wir wieder zurückgehen sind die kanten die wir schon in dem edp gelaufen sind
                    detour_edges.append( (edp[edpIndex], edp[edpIndex +1]) )
                    #wir fangen beim neuen edp ganz am anfang an
                    edpIndex = 0
                    break
                else :#die kante gehen und zum nächsten knoten schalten
                    edpIndex += 1
                    hops += 1
                    currentNode = edp[edpIndex]
            #endwhile
            if currentNode == d : #wir haben die destination mit einem der edps erreicht
                print('Routing done via EDP')
                print('------------------------------------------------------')
                #input("Press key to continue...")
                return (False, hops, switches, detour_edges)

    #endfor
    # wenn wir es nicht geschafft haben anhand der edps allein zum ziel zu routen dann geht es am längsten edp weiter
    print('Routing via EDPs FAILED')
    edp = edps_for_s_d[len(edps_for_s_d) -1]
    #hier speichert  man die nodes die man schon durchlaufen hat, damit man nachher beim route_in_tree weiß welche kante man nicht gehen soll
    visitedNodes = []
    route_in_tree = False #wird auf true gesetzt wenn der edp einen fehler hat und wir nur über den tree routen wollen
    currentNode = edp[edpIndex]
    while (currentNode != d):
        if not route_in_tree:
            if (edp[edpIndex], edp[edpIndex +1]) in fails or (edp[edpIndex +1], edp[edpIndex]) in fails:
                # wir schalten zum nächsten pfad
                switches += 1
                #die kanten die wir wieder zurückgehen sind die kanten die wir schon in dem edp gelaufen sind
                detour_edges.append((edp[edpIndex], edp[edpIndex +1]))
                route_in_tree = True
                #print(fails)
                #print('Roting in tree started')
                #print("Source:", s , " ", "Destination:", d)
                PG = nx.nx_pydot.write_dot(tree , "./graphen/tree"+ str(s) + "_" +  str(d))
            else :#die kante gehen und zum nächsten knoten schalten
                edpIndex += 1
                hops += 1
                visitedNodes.append(currentNode)
                currentNode = edp[edpIndex]
        else:
            # wir könnnen den edp nicht entlang und gehen jetzt durch den Baum
            #und starten ab dem knoten im edp der eine kaputte kante hat
            #possibleNextNodes = list(nx.neighbors(tree, currentNode)) #alle nachbarn holen
            #input(" vor jetziger node ... ")
            print("Jetziger Node : " , currentNode)
            
            # alle kinder entfernen, bei denen wir schon waren
            #da wir immer die kinder zu visited nodes hinzufügen wird die liste immer kleiner und die nächste iteration merkt dass man alle kinder schon "probiert"
            #hat und man muss dann einen knoten hoch gehen
            possibleNextNodes = list(nx.neighbors(tree, currentNode))
            print("Mögliche Nachbarn vor der Kürzung : " , possibleNextNodes)
            tmp = []
            for el in possibleNextNodes:
                if el in visitedNodes:
                    continue
                else:
                    tmp.append(el)

            possibleNextNodes = tmp
            
            print("Mögliche Nachbarn nach der Kürzung : " , possibleNextNodes)
            print("VisitedNodes : " , visitedNodes)

            if len(possibleNextNodes) == 0: # Es können keine kinder als nächster knoten mehr genutzt werden
                if currentNode == s:
                    break

                visitedNodes.append(currentNode) # das heisst dass unser jetziger knoten auch schon "durchlaufen" ist und keinen weg zum ziel darstellt
                currentNode = get_parent_node(tree , currentNode) # wir müssen eine ebene im baum hoch um noch weitere potenzielle knoten zu finden
            else:
                print(possibleNextNodes)
                #sortieren der nodes anhand ihrer ränge
                #lambda sort https://stackoverflow.com/a/46851604
                possibleNextNodes.sort(key=lambda x: (getRank(tree, x))) #man braucht von den nachbarn den, mit dem kürzesten abstand zum ziel
                print(possibleNextNodes)
                #input("......................weiter....................")
                print("_____________________________________")
                
                #kante mit dem kleinsten rang wird genommen und geprüft ob sie funktioniert
                if (currentNode, possibleNextNodes[0]) in fails or (possibleNextNodes[0], currentNode) in fails:
                    visitedNodes.append(possibleNextNodes[0]) # wenn sie nicht funktioniert dann wird sie als "visited angesehen 
                    switches += 1
                    #die kanten die wir wieder zurückgehen sind die kanten die wir schon in dem edp gelaufen sind
                    detour_edges.append((currentNode, possibleNextNodes[0]))
                else: # choosen node enthält den node den wir langehen wollen (kleinster abstand zur destination)
                    hops += 1
                    visitedNodes.append(currentNode)
                    currentNode = possibleNextNodes[0]
            

            
    #endwhile
    if currentNode == d : #wir haben die destination mit einem der edps erreicht
        print('Routing done via Tree')
        print('------------------------------------------------------')
        #input("Press key to continue...")
        return (False, hops, switches, detour_edges)

    print('Routing failed')
    print('------------------------------------------------------')
    #input("Press key to continue...")
    return (True, hops, switches, detour_edges)

    


def getRank(tree, el):
    return tree.nodes[el]["rank"]

# Route according to deterministic circular routing as described by Chiesa et al.
# source s
# destination d
# link failure set fails
# arborescence decomposition T
def RouteDetCirc(s, d, fails, T):
    curT = 0
    detour_edges = []
    hops = 0
    switches = 0
    n = len(T[0].nodes())
    k = len(T)
    while (s != d):
        while (s not in T[curT].nodes()) and switches < k*n:
            curT = (curT+1) % k
            switches += 1
        if switches >= k*n:
            break
        nxt = list(T[curT].neighbors(s))
        if len(nxt) != 1:
            print("Bug: too many or to few neighbours")
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

#select next arborescence to bounce
def Bounce(s, d, T, cur):
    for i in range(len(T)):
        if (d, s) in T[i].edges():
            return i
    else:
        return (cur+1) % len(T)

# Route with bouncing for 3-connected graph by Chiesa et al.
# source s
# destination d
# link failure set fails
# arborescence decomposition T
def RouteDetBounce(s, d, fails, T):
    detour_edges = []
    curT = 0
    hops = 0
    switches = 0
    n = len(T[0].nodes())
    while (s != d):
        nxt = list(T[curT].neighbors(s))
        if len(nxt) != 1:
            print("Bug: too many or to few neighbours")
        nxt = nxt[0]
        if (nxt, s) in fails or (s, nxt) in fails:
            if curT == 0:
                curT = Bounce(s, nxt, T, curT)
            else:
                curT = 3 - curT
            switches += 1
        else:
            if switches > 0:
                detour_edges.append((s, nxt))
            s = nxt
            hops += 1
        if hops > 3*n or switches > k*n:
            print("cycle Bounce")
            return (True, hops, switches, detour_edges)
    return (False, hops, switches, detour_edges)

#construct BIDB 7 matrix
def PrepareBIBD(connectivity):
    global matrix
    matrix = []
    matrix.append([5,0,6,1,2,4,3])
    matrix.append([0,1,2,3,4,5,6])
    matrix.append([6,2,0,4,1,3,5])
    matrix.append([4,3,5,0,6,1,2])
    matrix.append([1,4,3,2,5,6,0])
    matrix.append([2,5,4,6,3,0,1])
    matrix.append([3,6,1,5,0,2,4])

# Route with BIBD matrix
# source s
# destination d
# link failure set fails
# arborescence decomposition T
def RouteBIBD(s, d, fails, T):
    if len(matrix) == 0:
        PrepareBIBD(k)
    detour_edges = []
    curT = matrix[int(s) % (k-1)][0]
    hops = 0
    switches = 0
    source = s
    n = len(T[0].nodes())
    while (s != d):
        nxt = list(T[curT].neighbors(s))
        if len(nxt) != 1:
            print("Bug: too many or to few neighbours")
        nxt = nxt[0]
        if (nxt, s) in fails or (s, nxt) in fails:
            switches += 1
            # print(switches)
            curT = matrix[int(source) % (k-1)][switches % k]
        else:
            if switches > 0:
                detour_edges.append((s, nxt))
            s = nxt
            hops += 1
        if hops > 3*n or switches > k*n:
            print("cycle BIBD")
            return (True, hops, switches, detour_edges)
    return (False, hops, switches, detour_edges)

#build data structure for square one algorithm
SQ1 = {}
def PrepareSQ1(G, d):
    global SQ1
    H = build_auxiliary_edge_connectivity(G)
    R = build_residual_network(H, 'capacity')
    SQ1 = {n: {} for n in G}
    for u in G.nodes():
        if (u != d):
            k = sorted(list(nx.edge_disjoint_paths(
                G, u, d, auxiliary=H, residual=R)), key=len)
            SQ1[u][d] = k

# Route with Square One algorithm
# source s
# destination d
# link failure set fails
# arborescence decomposition T
def RouteSQ1(s, d, fails, T):
    curRoute = SQ1[s][d][0]
    k = len(SQ1[s][d])
    detour_edges = []
    index = 1
    hops = 0
    switches = 0
    c = s  # current node
    n = len(T[0].nodes())
    while (c != d):
        nxt = curRoute[index]
        if (nxt, c) in fails or (c, nxt) in fails:
            for i in range(2, index+1):
                detour_edges.append((c, curRoute[index-i]))
                c = curRoute[index-i]
            switches += 1
            c = s
            hops += (index-1)
            curRoute = SQ1[s][d][switches % k]
            index = 1
        else:
            if switches > 0:
                detour_edges.append((c, nxt))
            c = nxt
            index += 1
            hops += 1
        if hops > 3*n or switches > k*n:
            print("cycle square one")
            return (True, hops, switches, detour_edges)
    return (False, hops, switches, detour_edges)


# Route with randomization as described by Chiesa et al.
# source s
# destination d
# link failure set fails
# arborescence decomposition T
P = 0.5358  # bounce probability
def RoutePR(s, d, fails, T):
    detour_edges = []
    curT = 0
    hops = 0
    switches = 0
    n = len(T[0].nodes())
    while (s != d):
        nxt = list(T[curT].neighbors(s))
        if len(nxt) != 1:
            print("Bug: too many or to few neighbours")
        nxt = nxt[0]
        if (nxt, s) in fails or (s, nxt) in fails:
            x = random.random()
            if x <= P:
                curT = Bounce(s, nxt, T, curT)
            else:
                newT = random.randint(0, len(T)-2)
                if newT >= curT:
                    newT = (newT+1) % len(T)
                curT = newT
            switches += 1
        else:
            if switches > 0:
                detour_edges.append((s, nxt))
            s = nxt
            hops += 1
        if hops > 3*n or switches > k*n:
            print("cycle PR")
            return (True, hops, switches, detour_edges)
    return (False, hops, switches, detour_edges)

# Route randomly without bouncing as described by Chiesa et al.
# source s
# destination d
# link failure set fails
# arborescence decomposition T
def RoutePRNB(s, d, fails, T):
    detour_edges = []
    curT = 0
    hops = 0
    switches = 0
    n = len(T[0].nodes())
    while (s != d):
        nxt = list(T[curT].neighbors(s))
        if len(nxt) != 1:
            print("Bug: too many or to few neighbours")
        nxt = nxt[0]
        if (nxt, s) in fails or (s, nxt) in fails:
            newT = random.randint(0, len(T)-2)
            if newT >= curT:
                newT = (newT+1) % len(T)
            curT = newT
            switches += 1
        else:
            if switches > 0:
                detour_edges.append((s, nxt))
            s = nxt
            hops += 1
        if hops > 3*n or switches > k*n:
            print("cycle PRNB")
            return (True, hops, switches, detour_edges)
    return (False, hops, switches, detour_edges)

# Route with bouncing variant by Chiesa et al.
# source s
# destination d
# link failure set fails
# arborescence decomposition T
def RouteDetBounce2(s, d, fails, T):
    detour_edges = []
    curT = 0
    hops = 0
    switches = 0
    n = len(T[0].nodes())
    while (s != d):
        nxt = list(T[curT].neighbors(s))
        nxt = nxt[0]
        if (nxt, s) in fails or (s, nxt) in fails:
            if curT == 0:
                curT = Bounce(s, nxt, T, curT)
            else:
                curT = 1+(curT) % (len(T)-1)
            switches += 1
        else:
            if switches > 0:
                detour_edges.append((s, nxt))
            s = nxt
            hops += 1
        if hops > 3*n or switches > k*n:
            #print("cycle DetBounce2")
            return (True, hops, switches, detour_edges)
    return (False, hops, switches, detour_edges)

#compute best arb for low stretch to use next
arb_order = {}
def next_stretch_arb(s, curT):
    indices = arb_order[s]
    index = (indices.index_of(curT) + 1) % k
    return index

# Choose next arborescence to minimize stretch when facing failures
# source s
# destination d
# link failure set fails
# arborescence decomposition T
def Route_Stretch(s, d, fails, T):
    curT = 0
    detour_edges = []
    hops = 0
    switches = 0
    n = len(T[0].nodes())
    while (s != d):
        # print "At ", s, curT
        nxt = list(T[curT].neighbors(s))
        # print "neighbours:", nxt
        if len(nxt) != 1:
            print("Bug: too many or to few neighbours")
        nxt = nxt[0]
        if (nxt, s) in fails or (s, nxt) in fails:
            curT = next_stretch_arb(s, curT)
            switches += 1
        else:
            if switches > 0 and curT > 0:
                detour_edges.append((s, nxt))
            s = nxt
            hops += 1
        if hops > 2*n or switches > k*n:
            print("cycle det circ")
            return (True, hops, switches, detour_edges)
    return (False, hops, switches, detour_edges)


# run routing algorithm on graph g
# RANDOM: don't use failset associated with g, but construct one at random
# stats: statistics object to fill
# f: number of failed links
# samplesize: number of nodes from which we route towards the root
# dest: nodes to exclude from using in sample
# tree: arborescence decomposition to use
def SimulateGraph(g, RANDOM, stats, f, samplesize, precomputation=None, dest=None, tree=None, targeted=False):
    edg = list(g.edges())
    fails = g.graph['fails']
    if fails != None:
        if len(fails) < f:
            fails = fails + edg[:f - len(fails) + 1]
        edg = fails
    if f > len(edg):
        print('more failures than edges')
        print('simulate', len(g.edges()), len(fails), f)
        return -1
    d = g.graph['root']
    g.graph['k'] = k
    if precomputation is None:
        precomputation = tree
        if precomputation is None:
            precomputation = GreedyArborescenceDecomposition(g)
            #if precomputation is None:
             #   return -1
    fails = edg[:f]
    if targeted:
        fails = []
    failures1 = {(u, v): g[u][v]['arb'] for (u, v) in fails}
    failures1.update({(v, u): g[u][v]['arb'] for (u, v) in fails})

    g = g.copy(as_view=False)
    g.remove_edges_from(failures1.keys())
    nodes = list(set(connected_component_nodes_with_d_after_failures(g,[],d))-set([dest, d]))
    dist = nx.shortest_path_length(g, target=d)
    #if len(nodes) < samplesize:
    #    print('Not enough nodes in connected component of destination (%i nodes, %i sample size), adapting it' % (len(nodes), samplesize))
    #    samplesize = len(nodes)
    nodes = list(set(g.nodes())-set([dest, d]))
    random.shuffle(nodes)
    count = 0
    for s in nodes[:samplesize]:
        count += 1
        for stat in stats:
            if targeted:
                fails = list(nx.minimum_edge_cut(g,s=s,t=d))[1:]
                random.shuffle(fails)
                failures1 = {(u, v): g[u][v]['arb'] for (u, v) in fails}
                g.remove_edges_from(failures1.keys())
                x = dist[s]
                dist[s] = nx.shortest_path_length(g,source=s,target=d)
                #print(len(fails),x,dist[s]) #DEBUG
            if (s == d) or (not s in dist):
                stat.fails += 1
                continue
            (fail, hops) = stat.update(s, d, fails, precomputation, dist[s])
            if fail:
                stat.hops = stat.hops[:-1]
                stat.stretch = stat.stretch[:-1]
            elif hops < 0:
                stat.hops = stat.hops[:-1]
                stat.stretch = stat.stretch[:-1]
                stat.succ = stat.succ - 1
            if targeted:
                for ((u, v), i) in failures1.items():
                    g.add_edge(u, v)
                    g[u][v]['arb'] = i
            if stat.succ + stat.fails != count:
                print('problem, success and failures do not add up', stat.succ, stat.fails, count)
                print('source', s)
                if stat.has_graph:
                    drawGraphWithLabels(stat.graph, "results/problem.png")
    if not targeted:
        for ((u, v), i) in failures1.items():
            g.add_edge(u, v)
            g[u][v]['arb'] = i
    for stat in stats:
        stat.finalize()
    sys.stdout.flush()
    return fails

# class to collect statistics on routing simulation
class Statistic:
    def __init__(self, routeFunction, name, g=None):
        self.funct = routeFunction
        self.name = name
        self.has_graph = g is not None
        if g is not None:
            self.graph = g

    def reset(self, nodes):
        self.totalHops = 0
        self.totalSwitches = 0
        self.fails = 0
        self.succ = 0
        self.stretch = [-2]
        self.hops = [-2]
        self.lastsuc = True
        self.load = {(u, v): 0 for u in nodes for v in nodes}
        self.lat = 0

    # add data for routing simulations from source s to destination
    # despite the failures in fails, using arborescences T and the shortest
    # path length is captured in shortest
    def update(self, s, d, fails, T, shortest):
        if not self.has_graph:
            (fail, hops, switches, detour_edges_used) = self.funct(s, d, fails, T)
        else:
            (fail, hops, switches, detour_edges_used) = self.funct(s, d, fails, T, self.graph)
        #if switches == 0:
        #    fail = False
        if fail:
            self.fails += 1
            self.lastsuc = False
            self.stretch.append(-1)
            self.hops.append(-1)
            for e in detour_edges_used:
                self.load[e] += 1
        else:
            self.totalHops += hops
            self.succ += 1
            self.totalSwitches += switches
            if shortest == 0:
                shortest = 1
            self.stretch.append(hops-shortest)
            self.hops.append(hops)
            for e in detour_edges_used:
                self.load[e] += 1
            self.lastsuc = True
        return (fail, hops)

    def max_stretch(self):
        return max(self.stretch)

    # compute statistics when no more data will be added
    def finalize(self):
        self.lat = -1
        self.load = max(self.load.values())
        if len(self.hops) > 1:
            self.hops = self.hops[1:]
            self.stretch = self.stretch[1:]
        else:
            self.hops = [0]
            self.stretch = [0]

        if len(self.hops) > 0:
            self.lat = np.mean(self.hops)
        return max(self.stretch)

    def max_load(self):
        return max(self.load.values())

    def load_distribution(self):
        return [x*1.0/self.size**2 for x in np.bincount(self.load.values())]

from platform import node
import sys
import time
from traceback import print_list
from typing import List, Any, Union

import networkx as nx
import numpy as np
import itertools

from arborescences import *
DEBUG = False

######################################################
#TODO : 
# - trees kürzen
# - trees ranken  
# - trees im tree array speichern
# - multipletrees routen
#
######################################################


def multiple_trees_pre(graph):
    paths = {}

    for source in graph.nodes:

        for destination in graph.nodes:
            
            if source != destination:
                
                edps = all_edps(source, destination, graph)
                edps.sort(key=len, reverse=True)

                trees = multiple_trees(source,destination,graph,edps)
                

                if source in paths:
                    paths[source][destination] = { 'trees': trees, 'edps': edps}
                else:
                    paths[source] = {}
                    paths[source][destination] = {'trees': trees, 'edps': edps}

                
    return paths

#gibt für ein source-destination paar alle trees zurück
def multiple_trees(source, destination, graph, all_edps):
    trees = [] #hier werden alle trees gespeichert
    for i in range(0,len(all_edps)-1): #um zu versuchen aus jedem edp einen Baum zu bauen
        tree = nx.DiGraph()
        tree.add_node(source)
        pathToExtend = all_edps[i]

        for j in range(1,len(pathToExtend)-2): #alle knoten durchgehen und deren nachbarn suchen, angefangen mit den knoten aus dem edp
            nodes = pathToExtend[:len(pathToExtend) -2]#in nodes stehen dann alle knoten drin die wir schon besucht haben
                                                       # -2 damit die destination nicht mit drin steht
            it = 0
            while it < len(nodes):
                neighbors = list(nx.neighbors(graph, nodes[j]))

                for k in range(0,len(neighbors)-1): #jedend der nachbarn einfügen der noch nicht zu einem tree gehört
                    #if edge to neighbors[k] not part of any tree already
                    for tree_to_check in trees: 
                        if tree_to_check.has_edge(nodes[j],neighbors[k]):
                            nodes.append(neighbors[k])
                            tree_to_check.add_edge(nodes[j], neighbors[k])
                        #endif
                    #endfor
                it = it + 1
            #endwhile
        #endfor
        changed = True 
        while changed == True: #solange versuchen zu kürzen bis nicht mehr gekürzt werden kann 
            old_tree = tree.copy()
            remove_redundant_paths(source, destination, tree, graph)
            changed = tree.order() != old_tree.order() # order returns the number of nodes in the graph.
        rank_tree(tree , source)
        connect_leaf_to_destination(tree, source,destination)
        trees.append(tree)
    #endfor
    return trees

#methode um für jedes source destination paar einen baum zu bauen
def one_tree_pre(graph):
    #die paths struktur besteht daraus : für jeden source (1. index) zu jeder destination (2. index) gibt es 1 Objekt dass den Baum drin hat (Attribut 'tree') und alle EDPs (Attribut 'edps')
    # und alle weglängen zur destination in 'distance'

    paths = {}

    #paths = [[0 for x in range(graph.order())] for y in range(graph.order())]
    print("Anzahl Knoten: " , graph.order())
    print("Knoten : " , list(graph.nodes))
    #source_index = 0
    #destination_index = 0
    for source in graph.nodes:

        for destination in graph.nodes:
            
            if source != destination: #and source == 28 and destination == 13:                
                edps = all_edps(source, destination, graph)
                edps.sort(key=len)
                longest_edp = edps[len(edps)-1]

                
                tree = one_tree(source,destination,graph,longest_edp)

                #print("Versuche auf index ", source , " und ", destination ," zuzugreifen ")
                if source in paths:
                    paths[source][destination] = { 'tree': tree, 'edps': edps}
                else:
                    paths[source] = {}
                    paths[source][destination] = {'tree': tree, 'edps': edps}

                
    return paths

#hilfsfunktion damit man die weglänge von jedem node zur distance hat , das braucht man um die reihenfolge festzulegen die man bei den verzweigungen nimmt 
def compute_distance_to_dest(tree, destination):
    return dict(nx.single_target_shortest_path_length(tree, destination))

#den baum bauen indem man jeden knoten von der source aus mitnimmt der mit einem knoten aus dem baum benachbart ist
#dabei guckt man sich die nachbarn im ursprungsgraphen  an und fügt die dann in einem anderen graphen (tree) ein
# am ende löscht man noch die pfade die nicht zum destination führen
# der baum ist ein gerichteter graph , damit man im tree die struktur zwischen parent/children erkennen kann anhand eingehender/ausgehender kanten
def one_tree(source, destination, graph, longest_edp):
    #print("EDP aus dem der Tree gebaut wird für ", source , " nach " , destination ," : " , longest_edp)
    tree = nx.DiGraph()
    tree.add_node(source)

    pathToExtend = longest_edp
    
    for i in range(0,len(pathToExtend)-1): # i max 7
        
        nodes = pathToExtend[:len(pathToExtend) -2]
        it = 0 # um die nachbarn der nachbarn zu bekommen
        while it < len(nodes):

            neighbors = list(nx.neighbors(graph, nodes[it]))

            for j in neighbors:
                if (not tree.has_node(j)) and (j!= destination): #not part of tree already and not the destiantion
                    nodes.append(j)
                    
                    tree.add_node(j) #add neighbors[j] to tree
                    tree.add_edge(nodes[it], j) # add edge to new node
                #end if
            
            #end for
            it = it+1
        #end while
    #end for
    
    PG = nx.nx_pydot.write_dot(tree , "./graphen/tree_all")
    changed = True 
    while changed == True: #solange versuchen zu kürzen bis nicht mehr gekürzt werden kann 
        old_tree = tree.copy()
        remove_redundant_paths(source, destination, tree, graph)
        changed = tree.order() != old_tree.order() # order returns the number of nodes in the graph.
    PG = nx.nx_pydot.write_dot(tree , "./graphen/tree_unranked"+ str(source) + str(destination))

    rank_tree(tree , source)
    connect_leaf_to_destination(tree, source, destination)

    #add 'rank' property to the added destinaton, -1 for highest priorty in routing
    tree.nodes[destination]["rank"] = -1


    #OG = nx.nx_pydot.write_dot(graph , "./graphen/graph")
    #PG = nx.nx_pydot.write_dot(tree , "./graphen/tree"+ str(source) + str(destination))
    #input("press enter")
    #print("fertiger tree")
    #print(tree)
    return tree

# den baum von den leafs aus ranken, dabei kriegen die leafs als ersten ihren rang 
# und parents nehmen den kleinsten rang ihrer kinder + 1 für die Kante zu ihrem kind
def rank_tree(tree , source):
    nx.set_node_attributes(tree, sys.maxsize, name="rank")

    # initiualize with all leafes
    done_nodes = [node for node in tree if len(list(nx.neighbors(tree, node))) == 0]


    for leaf in done_nodes: #initially we add rank 0 to all leafes
        tree.nodes[leaf]["rank"] = 0
        
    #es geht nicht darum dass jedes kind eines nodes einen rang hat , der erste rang ist dann auch der kleinste
    #weil dieser rang auch am schnellsten gebildet wurde
    while tree.order() != len(done_nodes):

        to_add = []
        for node in done_nodes:
            parent = get_parent_node(tree, node)
            if parent in done_nodes or parent in to_add:
                continue # parent already labled  by child with shorter distance
            else: #parent not labeled paths[source][destination] = { 'tree': tree, 'edps': edps}
                children= list(nx.neighbors(tree, parent)) #get ranks of children
                children_rank = []
                for child in children:
                    children_rank.append(tree.nodes[child]["rank"])
                tree.nodes[parent]["rank"] = min(children_rank) + 1
                to_add.append(parent)
        #endfor        
        done_nodes.extend(to_add)
    #endwihle

def get_parent_node(tree, node):
    pre = list(tree.predecessors(node))
    if len(pre) > 1:
        raise AssertionError("Node" + node + "has multiple  predecessors.")
    if len(pre) == 1:
        return pre[0]
    else:
        return node #Wurzel des Baumes
        
#löscht die blätter die keine direkte kante zum destination haben
#jeden knoten durchgehen  in tree der nur 1 Kante hat (also ein blatt ist) und prüfen ob dieser eine direkte kante hat zum destination in graph
def remove_redundant_paths(source, destination, tree, graph):
    nodes_to_remove = []
    for node in tree.nodes:
        #prüfen ob node den man hat ein blatt ist (genau 1 nachbarn hat)
        neighbors = list(nx.neighbors(tree, node))
        if len(neighbors) == 0 and node != source:
            #print("leaf:", node)
            #prüfen ob blatt aus dem tree im ursprungsgraphen eine direkte kante zum destination hat
            if not graph.has_edge(node,destination):
                # nur leaf mit verbindung zur destination werden
                nodes_to_remove.append(node)
                #print("adding " + str(node) + " to remove list")
    tree.remove_nodes_from(nodes_to_remove)

#beim start dieser funktion wurden alle redundanten pfade entfernt und die leaves haben im ursprungsgraph eine direkte verbindung zur destination
def connect_leaf_to_destination(tree, source, destination):
    #beinhaltet tupel aus nodes
    nodes_to_connect = []
    #nodes finden die blätter sind
    for node in tree.nodes:
        neighbors = list(nx.neighbors(tree, node))
        if len(neighbors) == 0 and node != source:
            nodes_to_connect.append((node, destination))
    #edges hinzufügen
    tree.add_edges_from(nodes_to_connect)

#hilfsfunktion die den Iterator einmal durchgeht und diesen als liste zurückgibt
def finish_iterator(neighbors_as_iterator):
    neighbors_as_list = []
    while True:
        try:
            # Iterate by calling next
            item = next(neighbors_as_iterator)
            neighbors_as_list.append(item)
            #print(item)
        except StopIteration:
            # exception will happen when iteration will over
            return neighbors_as_list
            break

def all_edps(source, destination, graph):
    return list(nx.edge_disjoint_paths(graph, source , destination))

#kriegt alle edps rein und bestimmt den längesten
#def find_longest_edp(edps):
#    #längsten edp
#    longest_edp = []
#    for nodes in edps:
#        #print(nodes)
#        if len(longest_edp)<len(nodes):
#            longest_edp = nodes
#
#    return longest_edp

    
#             "trees"        
#graph[a][b][[a,b], [a,f,z,b]]

#a -> b -> c
#|    |
#f -> z 
def convertNxGraphToTree(Graph, distances, source, destination):
    tree = Tree(source, distances[source], None)

    currentNode = tree
    visited = [source]
    for neighbour in nx.neighbors(Graph,currentNode.nxNode):
        if neighbour not in visited:
            currentNode.children.append(Tree(neighbour, distances[neighbour], currentNode))
            visited.append(neighbour)

    

#nxNode ist dafür da um zu sehen wo der knoten aus dem baum der knoten im echten graphen ist
#distance_to_dest gibt die distanz zur destination aus um die knoten in reihenfolge zu bringen
#children beinhaltet alle neighbours aus dem graphen ohne den parent
#parent ist der knoten aus dem man entstnaden ist
class Tree:
    nxNode = None
    distance_to_dest = -1
    children = []
    parent = None
    def __init__(self, nxNode, distance_to_dest, parent, children=[]):
        self.nxNode = nxNode
        self.distance_to_dest = distance_to_dest
        self.children = children
        self.parent = parent


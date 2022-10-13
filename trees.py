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
#TODO : redundante Paths entfernen
#        testen
#        die trees in one_tree_pre speichern
#
#       datenstruktur um die trees zu speichern
#       routing
#
#
#
######################################################


#methode um für jedes source destination paar einen baum zu bauen
def one_tree_pre(graph):
    paths = [graph.order()][graph.order()]
    for source in graph.nodes:
        for destination in graph.nodes:
            if source != destination:
                paths[source][destination] = one_tree(source,destination,graph)
    return paths


#den baum bauen indem man jeden knoten von der source aus mitnimmt der mit einem knoten aus dem baum benachbart ist
#dabei guckt man sich die nachbarn im ursprungsgraphen  an und fügt die dann in einem anderen graphen (tree) ein
# am ende löscht man noch die pfade die nicht zum destination führen
def one_tree(source, destination, graph):
    #print("Source :" + str(source))
    #print("Destination :" + str(destination))
    tree = nx.Graph()
    tree.add_node(source)

    pathToExtend = find_longest_edp(source, destination, graph)
    #print("nach dem EDP Algorithmus")
    #print("Source :" + str(source))
    #print("Destination :" + str(destination))
    #print("EDP :" + str(pathToExtend))
    for i in range(0,len(pathToExtend)-1): # i max 7
        nodes = pathToExtend
        it = 0
        while it < len(nodes):
            #print("node = : " + nodes[i])
            neighbors = list(nx.neighbors(graph, nodes[i]))
            #print("nachbarn von " + str(nodes[i]) + " : ")
            #print(neighbors)
            for j in range (0, len(neighbors)):
                if not tree.has_node(neighbors[j]): #not part of tree already
                    nodes.append(neighbors[j])
                    #print(nodes)
                    #print("Knoten " + str(neighbors[j]) + " wurde hinzugefügt")
                    tree.add_node(neighbors[j]) #add neighbors[j] to tree
                    tree.add_edge(nodes[i], neighbors[j]) # add edge to new node
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
        changed = tree.order() == old_tree.order() # order returns the number of nodes in the graph.
        time.sleep(1)
    connect_leaf_to_destination(tree, source, destination)

    print("Source: " + str(source))
    print("Destination: " + str(destination))
    OG = nx.nx_pydot.write_dot(graph , "./graphen/graph")
    PG = nx.nx_pydot.write_dot(tree , "./graphen/tree")
    input("press enter")
    #print("fertiger tree")
    #print(tree)
    return tree

        
#löscht die blätter die keine direkte kante zum destination haben
#jeden knoten durchgehen  in tree der nur 1 Kante hat (also ein blatt ist) und prüfen ob dieser eine direkte kante hat zum destination in graph
def remove_redundant_paths(source, destination, tree, graph):
    nodes_to_remove = []
    for node in tree.nodes:
        #prüfen ob node den man hat ein blatt ist (genau 1 nachbarn hat)
        neighbors = list(nx.neighbors(tree, node))
        if len(neighbors) == 1 and node != source:
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
        if len(neighbors) == 1 and node != source:
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

#bestimme longest EDP von (Source,Destination)
def find_longest_edp(source,destination,graph):
    #alle edps
    edps = list(nx.edge_disjoint_paths(graph, source , destination))
    #längsten edp
    longest_edp = []
    for nodes in edps:
        #print(nodes)
        if len(longest_edp)<len(nodes):
            longest_edp = nodes

    return longest_edp
    
#             "trees"        
#graph[a][b][[a,b], [a,f,z,b]]

#a -> b -> c
#|    |
#f -> z 

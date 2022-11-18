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


#die struktur von paths : 
#Für jede Kombination aus Source-Destination gibt es einen Eintrag
#paths[source][destination] = {
#                               'trees': hier Ist dann ein Array drin, welches aus weiteren Arrays besteht in denen die Trees drin stehen
#                               ,
#                               'edps': hier Ist dann ein Array drin, welches aus weiteren Arrays besteht in denen die EDPs drin stehen
#                              }
def multiple_trees_pre(graph):
    paths = {}
    PG = nx.nx_pydot.write_dot(graph, "./multiple_trees_graphen/graph")
    
    for source in graph.nodes:
        #print("Durchlauf source")
        for destination in graph.nodes:
            #print("Durchlauf destination")
            if source != destination:
                
                edps = all_edps(source, destination, graph) #Bildung der EDPs
                
                edps.sort(key=len, reverse=True) #Sortierung der EDPs
                
                print("Start building trees for ", source , " to ", destination)
                trees = multiple_trees(source,destination,graph,edps)
                
                trees = remove_single_node_trees(trees)#EDPs die nicht erweitert werden konnten, da andere Bäume die Kanten schon vorher verbaut haben,
                                                        #führen nicht zum Ziel und müssen gelöscht werden
                
                print_trees(source,destination,trees)
                #print("Printing trees finished for " , source , " - " , destination)
                print(" ")
                if source in paths:
                    paths[source][destination] = { 'trees': trees, 'edps': edps}
                else:
                    paths[source] = {}
                    paths[source][destination] = {'trees': trees, 'edps': edps}

                
    return paths

#gibt für ein source-destination paar alle trees zurück
def multiple_trees(source, destination, graph, all_edps):
    trees = [] #hier werden alle trees gespeichert
    #print(all_edps)
    for i in range(0,len(all_edps)-1): #jeden edp einmal durchgehen
                                      #um zu versuchen aus jedem edp einen Baum zu bauen
        tree = nx.DiGraph()
        tree.add_node(source)
        pathToExtend = all_edps[i]

        #print("---- Nächster Tree für " , pathToExtend , " ----")
        nodes = pathToExtend[:len(pathToExtend) -1]#in nodes stehen dann alle knoten drin die wir besuchen wollen um deren nachbarn auch reinzupacken
                                                   # am anfang ganzer edp drin und -2 damit die destination nicht mit drin steht
        
        for j in range(0,len(pathToExtend)-2): #alle knoten aus nodes[] durchgehen und deren nachbarn suchen, angefangen mit den knoten aus dem edp
            
                       
            it = 0
            while it < len(nodes):
                
                neighbors = list(nx.neighbors(graph, nodes[it])) #für jeden knoten aus nodes die nachbarn finden und gucken ob sie in den tree eingefügt werden dürfen

                for k in range(0,len(neighbors)-1): #jeden der nachbarn durchgehen

                    if(neighbors[k] != nodes[j] and neighbors[k] != destination): #kanten zu sich selbst dürfen nicht rein da dann baum zu kreis wird und kanten zur destination auch nicht
                        
                        #print(destination)
                        #print(neighbors[k])
                        #print("Nodes Array : ", nodes)
                        #print("Tree Nodes : " , list(tree.nodes))
                        #print("Tree Edges : " , list(tree.edges))
                        #print("All Trees : ", trees)

                        #prüfen ob kante von nodes[j] nach neighbors[k] schon in anderen trees verbaut ist
                        is_in_other_tree = False
                        if(len(trees)>0):#wenn es schon andere trees gibt muss man alle anderen durchsuchen
                            for tree_to_check in trees: 
                                if (tree_to_check.has_edge(nodes[j],neighbors[k])): #wenn ein tree die edge schon drin hat dann darf man die edge nicht mehr benutzen
                                    is_in_other_tree = True
                                    break
                                #endif
                            #endfor
                        
                            if not ( is_in_other_tree or (tree.has_node(neighbors[k])) ):
                                #print("Füge die Kante : ", nodes[j] , " - " , neighbors[k] , " ein bei len(trees) > 0")
                                nodes.append(neighbors[k]) 
                                tree.add_node(neighbors[k])
                                tree.add_edge(nodes[j],neighbors[k])
                            #endif
                        #endif
                        else: #das ist der fall wenn es noch keine anderen trees zum checken gibt, ob die kante schon verbaut ist
                            if not((neighbors[k] == destination) or (tree.has_node(neighbors[k]))): #dann darf die kante nicht zur destination sein
                                                                                                    #der knoten darf nicht im jetzigen tree drin sein
                                #print("Füge die Kante : " , nodes[j] , " - " , neighbors[k] , " ein bei len(trees) = 0")
                                
                                tree.add_node(neighbors[k])
                                tree.add_edge(nodes[j],neighbors[k])
                            #endif
                            #wenn der node der grad in den tree eingefügt wurde schon in nodes war dann soll er nicht nochmal eingefügt werden
                            if not (neighbors[k]in nodes): #damit knoten nicht doppelt in nodes eingefügt werden
                                nodes.append(neighbors[k]) 
                            #endif
                        #endelse
                    #endif
                #endfor
                it = it + 1                
            #endwhile
        #endfor

        changed = True 
        #print_trees_with_redundant(source,destination,trees)

        #print("Kürze jetzt den Tree")
        while changed == True: #solange versuchen zu kürzen bis nicht mehr gekürzt werden kann 
            old_tree = tree.copy()
            remove_redundant_paths(source, destination, tree, graph) 
            changed = tree.order() != old_tree.order() # order returns the number of nodes in the graph.
        #endwhile

        #man muss prüfen ob nur die source im baum ist , da man im nächsten schritt der destination einen Rang geben muss
        if( tree.order() > 1 ):
            rank_tree(tree , source)
            connect_leaf_to_destination(tree, source,destination)
            #print("Versuche jetzt auf dem Tree : " , list(tree.nodes), " den Rang für ", destination , " einzufügen")
            tree.nodes[destination]["rank"] = -1
            trees.append(tree) 
        #endif
    #endfor
    return trees

#hilfsfunktion, welche bäume aus der liste entfernt die nur aus der source bestehen
def remove_single_node_trees(trees):
    new_trees = []
    for tree in trees:
        if(tree.order() > 1):
            new_trees.append(tree)
    return new_trees

#hilfsfunktion mit der man die trees aus der multipletrees im ordner speichern kann 
def print_trees(source,destination,trees):
    index = 0
    for tree in trees:
        PG = nx.nx_pydot.write_dot(tree , "./multiple_trees_graphen/tree_"+ str(source) + "_" + str(destination)+ "_" + str(index))
        index = index + 1

def print_trees_with_redundant(source,destination,trees):
    index = 0
    for tree in trees:
        PG = nx.nx_pydot.write_dot(tree , "./multiple_trees_graphen/tree_ungekuerzt"+ str(source) + "_" + str(destination)+ "_" + str(index))
        index = index + 1


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


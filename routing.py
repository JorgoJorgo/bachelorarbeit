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



def RouteMultipleTrees(s,d,fails,paths):

    #alle EDPS entlang routen
    currentNode = s
    edpIndex = 0
    detour_edges = []
    hops = 0
    switches = 0
    trees = paths[s][d]['trees']
    #print("Paths edp : " ,sorted(paths[s][d]['edps'],key=len))
    edps_for_s_d = sorted(paths[s][d]['edps'],key=len) # Aufsteigend die EDPs sortieren damit man den größten als letztes hat
    longest_edp = edps_for_s_d[len(edps_for_s_d) -1]
    visitedEdges = []
    print(" ")
    print('Routing started for ' , s , " to " , d )

    #########################################   FOR DEBUG ONLY                #####################################################
    skip_edps = False
    skip_trees = False
    if(skip_edps):
        print("Skipping the EDPs")
    #endif
    if(skip_trees):
        print("Skipping Trees")
    #endif

    ###############################################################################################################################


    if( not skip_edps ):



        #als erstes versucht man nur über die Edps zu routen

        for edp in edps_for_s_d:

            #jedoch muss der letzte Edp besonders betrachtet und daher diese Schleife zum Abbruch bringt
            if edp != edps_for_s_d[len(edps_for_s_d) -1]:

                currentNode = edp[edpIndex]

                #jeder edp wird so weit durchlaufen bis man mit dem currentNode das Ziel erreicht oder 
                while (currentNode != d):
                    
                    #wenn man auf eine Kaputte Kante stößt
                    if (edp[edpIndex], edp[edpIndex +1]) in fails or (edp[edpIndex +1], edp[edpIndex]) in fails:
                        
                        # wir schalten zum nächsten pfad
                        switches += 1

                        #die kanten die wir wieder zurückgehen, um wieder zur source zu kommen,  sind die kanten die wir schon in dem edp gelaufen sind
                        detour_edges.append( (edp[edpIndex], edp[edpIndex +1]) )

                        #wir fangen beim neuen edp ganz am anfang an
                        edpIndex = 0
                        break

                    #wenn die nächste Kante im Edp (edpIndex nach edpIndex + 1)
                    else :#die kante gehen und zum nächsten knoten schalten
                        edpIndex += 1
                        hops += 1
                        currentNode = edp[edpIndex]
                #endwhile
                if currentNode == d : #wir haben die destination mit einem der edps erreicht
                    print('Routing done via EDP')
                    #print('------------------------------------------------------')
                    #input("Press key to continue...")
                    return (False, hops, switches, detour_edges)
        #endfor

        #keiner der edps hat uns zum ziel gebracht


        #den letzten EDP so weit gehen wie möglich
        
        edpIndex = 0

        #print("Longest EDP : ", longest_edp )
        #fails.append( (longest_edp[len(longest_edp)-1],longest_edp[len(longest_edp)-2]))
        #print("Fails : " , fails)
        while((longest_edp[edpIndex],longest_edp[edpIndex+1])not in fails and  (longest_edp[edpIndex +1 ],longest_edp[edpIndex]) not in fails ):
            #print("Checking if : (" , longest_edp[edpIndex] , ",", longest_edp[edpIndex+1] , ") in fails ")
            #print("Or check if : (" , longest_edp[edpIndex+1] , ",", longest_edp[edpIndex] , ") in fails ")
            #wenn man in die schleife reingekommen ist, dann bedeutet dies, dass man die kante gehen kann
            #daher wird zum nächsten node geschaltet, indem man currentnode neu setzt 

            edpIndex += 1
            hops += 1
            currentNode = longest_edp[edpIndex]
            #print("Current Node : " , currentNode)
            #falls wir mit dem letzten edp ans ziel gekommen sind
            if(currentNode == d):
                #print("Routing done via last EDP")
                #print('------------------------------------------------------')
                return (False, hops, switches, detour_edges)
            
            if (edpIndex > len(list(longest_edp))-1):
                #print("Out of Bounds im letzten EDP")
                break
        #endwhile
    #endif
    if(not skip_trees):
        print(" ")
        print("Routing via Tree started")

        #print("Erster Tree in dem geroutet wird : " , list(trees[0].nodes))
        print(" ")
        #print("CurrentNode bevor in den Tree rein : ", currentNode)
        #wir müssen prüfen ob der node auch wirklich im tree drin ist
        while(not trees[0].has_node(currentNode)): #wenn der jetzige node nicht drin ist dann gehen wir einen node zurück und im worst case sind wir in der wurzel
                edpIndex = edpIndex -1
                hops += 1
                visitedEdges.append((currentNode,longest_edp[edpIndex+1]))
                detour_edges.append((longest_edp[edpIndex], longest_edp[edpIndex -1]))
                currentNode = longest_edp[edpIndex]
                #print("CurrentNode nicht im Tree , nächster CurrentNode : ", currentNode)
                continue; # skip loop and try with previous node again
        #endwhile

        #jetzt ist in currentNode ein Node drin der im Tree ist

        for tree in trees:
            #in currentnode ist jetzt der node von dem wir das routen im tree starten wollen
            visitedEdges = []
            #print("Baum der probiert wird : ", list(tree.nodes))
            

            #nun muss im tree geroutet werden
            while (currentNode != d):
                

                #alle möglichen nächsten Kanten des jetzigen nodes herausfinden
                possibleNextEdges = list(tree.out_edges(currentNode) )
                #print("Mögliche Kanten vor der Kürzung : " , possibleNextEdges)
                tmp = []
                for el in possibleNextEdges:
                    if el in visitedEdges:
                        continue
                    #endif
                    else:
                        tmp.append(el)
                    #endelse
                #endfor

                possibleNextEdges = tmp
                
                #print("Mögliche Kanten nach der Kürzung : " , possibleNextEdges)
                #print("VisitedEdges : " , visitedEdges)

                if len(possibleNextEdges) == 0: # Es können keine kinder als nächster knoten mehr genutzt werden
                    
                    if currentNode == s: #das würde bedeuten dass es keine ausweichmöglichkeiten von der wurzel aus gibt, also muss der Tree gewechselt werden
                        #print("Baum muss gewechselt werden !")
                        break
                    #endif

                    parent = get_parent_node(tree , currentNode)
                    visitedEdges.append((currentNode,parent)) # das heisst dass unser jetziger knoten auch schon "durchlaufen" ist und keinen weg zum ziel darstellt
                    currentNode = parent # wir müssen eine ebene im baum hoch um noch weitere potenzielle knoten zu finden
                #endif
                else: #der jetzige Knoten hat Kinder von denen aus wir zum Ziel kommen
                   

                    #da man ganze kanten hat und diese keine ränge haben um sortiert werden zu können, müssen die knoten aus den kanten in eine separate liste
                    #gepackt werden um dann einzelne nodes zu haben die sortert werden können
                    possibleNextNodes = []
                    for edge in possibleNextEdges:
                        possibleNextNodes.append(edge[1])
                    #endfor

                    #sortieren der nodes anhand ihrer ränge
                    #print("Possible next Node before sort : ", possibleNextNodes)
                    #lambda sort https://stackoverflow.com/a/46851604
                    possibleNextNodes.sort(key=lambda x: (getRank(tree, x))) #man braucht von den nachbarn den, mit dem kürzesten abstand zum ziel
                    #print("Possible next Nodes after sort : ", possibleNextNodes)

                    #input("......................weiter....................")
                    print("_____________________________________")
                    


                    #hier muss man nur den ersten index prüfen aus den possible next nodes da, wenn dieser nicht klappt dann unter den "visitedEdges" fällt und im nächsten Durchlauf
                    #direkt rausgefiltert wird wenn man erneut die possible next edges überprüft


                    #kante mit dem kleinsten rang wird genommen und geprüft ob sie funktioniert
                    if (currentNode, possibleNextNodes[0]) in fails or (possibleNextNodes[0], currentNode) in fails:
                        visitedEdges.append( (currentNode,possibleNextNodes[0]) )
                        visitedEdges.append( (possibleNextNodes[0],currentNode) ) # wenn sie nicht funktioniert dann wird sie als "visited angesehen 
                        switches += 1
                        #die kanten die wir wieder zurückgehen sind die kanten die wir schon in dem edp gelaufen sind
                        detour_edges.append((currentNode, possibleNextNodes[0]))
                    #endif
                    else: # choosen node enthält den node den wir langehen wollen (kleinster abstand zur destination)
                        hops += 1
                        visitedEdges.append( (currentNode,possibleNextNodes[0]) )
                        visitedEdges.append( (possibleNextNodes[0],currentNode) ) # die kante wird als "besucht" eingefügt da man die Kante dann weitergeht
                        currentNode = possibleNextNodes[0]
                    #endelse

                #endelse 
                 
            #endwhile

            if (currentNode == d):#falls wir am ziel angekommen sind
                print("Routing done via the Tree : ", list(tree.nodes))
                #print(" ")
                return (False, hops, switches, detour_edges)
            #endif
            
            #print("Schalte auf den nächsten Tree ")
            #print(" ")

        #endfor
        print("Routing failed via Trees ")
        #print(" ")
        return (True, hops, switches, detour_edges)
    #endif

###########################################################################################################################################################
###########################################################################################################################################################



#neue routingmethode, welche die alte RouteOneTree verbessert in dem punkt, dass nur lokale informationen nötig sind zum routen
#denn bei fehlern wurde das paket nicht zurück an die source geführt bei den edps sondern dort "hinteleportiert" in dem man den currentnode
#auf den ersten index des edps gesetzt hat
def RouteOneTreeNew (s,d,fails,paths):
    if s != d :
        currentNode = -1
        edpIndex = 0
        detour_edges = []
        hops = 0
        switches = 0
        tree = paths[s][d]['tree']
        edps_for_s_d = paths[s][d]['edps']

        print('Routing started for ' , s , " to " , d )




        #als erstes anhand der EDPs (außer dem längsten, also dem letzten) versuchen zu routen
        for edp in edps_for_s_d:

            currentNode = s
            last_node = s 

            print("EDP in der EDP Schleife : " , edp)

            if edp != edps_for_s_d[len(edps_for_s_d) -1]:

                currentNode = edp[edpIndex]


                #jeder EDP wird so weit durchlaufen bis man mit dem currentNode zum Ziel kommt oder man auf eine kaputte Kante stößt
                while (currentNode != d):


                    #man prüft ob die nächste Kante im EDP kaputt ist so, indem man guckt ob eine Kante vom currentNode edp[edpIndex] zum nächsten Node im EDP edp[edpIndex+1] in Fails ist
                    #dies beruht auf lokalen Informationen, da EDPs nur eine eingehende Kante haben ( auf der das Paket ankommt ) und eine ausgehende Kante (auf der das Paket nicht ankommt)
                    if (edp[edpIndex], edp[edpIndex +1]) in fails or (edp[edpIndex +1], edp[edpIndex]) in fails:
                        

                        #wenn man auf eine fehlerhafte Kante stößt dann wechselt man den Pfad
                        switches += 1

                        #die kanten die wir wieder zurückgehen sind die kanten die wir schon in dem edp gelaufen sind
                        detour_edges.append( (edp[edpIndex], edp[edpIndex +1]) )

                        #wir fangen beim neuen edp ganz am anfang an
                        tmp_node = currentNode #und gehen eine Kante hoch, also den edp zurück
                        currentNode = last_node #das "rückwärts den edp gehen" kann so gemacht werden, da die pakete so nur über den port gehen müssen über den sie reingekommen sind
                        last_node = tmp_node
                        hops += 1
                        break

                    else :#wenn die kante die man gehen will inordnung ist, die kante gehen und zum nächsten knoten schalten
                        edpIndex += 1
                        hops += 1
                        last_node = currentNode 
                        currentNode = edp[edpIndex] #man kann hier currentnode direkt so setzen, da es im edp für jeden knoten jeweils 1 ausgehende
                                                    #und genau eine eingehende Kante gibt
                        #print("Es wird zum nächsten Node geschaltet : " , currentNode)
                    #endif

                #endwhile

                #nun gibt es 2 Möglichkeiten aus denen die while-Schleife abgebrochen wurde : Ziel erreicht / EDP hat kaputte Kante 


                if currentNode == d : #wir haben die destination mit einem der edps erreicht
                    print('Routing done via EDP')
                    print('------------------------------------------------------')
                    #input("Press key to continue...")
                    return (False, hops, switches, detour_edges)
                #endif

                print("Starte Rückführung zur Source " , s)

                

                #wenn man hier angelangt ist, dann bedeutet dies, dass die while(currentNode != d) beendet wurde weil man auf eine kaputte kante gestoßen ist 
                #und dass man nicht an der destination angekommen ist, daher muss man jetzt an die source zurück um den nächsten edp zu starten
                while currentNode != s: #hier findet die Rückführung statt
                    detour_edges.append( (last_node,currentNode) )

                    last_node = currentNode #man geht den edp so weit hoch bis man an der source ist
                    currentNode = edp[edpIndex-1] #man kann auch hier direkt den edp index verwenden da man genau 1 eingehende kante hat
                    edpIndex = edpIndex-1
                    #print("CurrentNode : ", currentNode)
                    hops += 1

                #endwhile
                print("Bin an der Source angekommen")
            #endif

        #endfor

        # wenn wir es nicht geschafft haben anhand der edps allein zum ziel zu routen dann geht es am längsten edp weiter
        print('Routing via EDPs FAILED')
        
        edp = edps_for_s_d[len(edps_for_s_d) -1]#speichern des letzten EDPs

        PG = nx.nx_pydot.write_dot(tree , "./graphen/tree_"+ str(s) + "_" +  str(d))
        currentNode = edp[edpIndex]#edpIndex = 0 da der letzte Schritt die Rückführung zur Source war 


        #gleich wie oben, versuchen EDP zu durchlaufen, nur ohne Rückführung
        while (currentNode != d):
            
            if (edp[edpIndex], edp[edpIndex +1]) in fails or (edp[edpIndex +1], edp[edpIndex]) in fails:
                print("Bin auf kaputte Kante gestoßen im letzten EDP , currentNode : ", currentNode)
                # wir schalten zum nächsten pfad
                switches += 1
                #die kanten die wir wieder zurückgehen sind die kanten die wir schon in dem edp gelaufen sind
                detour_edges.append((edp[edpIndex], edp[edpIndex +1]))
                PG = nx.nx_pydot.write_dot(tree , "./graphen/tree_"+ str(s) + "_" +  str(d))
                break;
            else :#die kante gehen und zum nächsten knoten schalten
                #print("Gehe einen Schritt im letzten edp currentNode : " ,currentNode)
                edpIndex += 1
                hops += 1
                currentNode = edp[edpIndex]
            #endif

        #endwhile


        #wenn man aus dieser schleife raus ist dann hat man entweder das ziel mit dem letzten edp erreicht
        #oder man ist so weit es geht im letzten edp vorangekommen

        if currentNode == d : #wir haben die destination mit dem LETZTEN edp erreicht
            print('Routing done via LAST EDP')
            print('------------------------------------------------------')
            #input("Press key to continue...")
            return (False, hops, switches, detour_edges)

        #oder man muss jetzt das routen im tree beginnen
        #es wird ab der letzten im edp durchlaufenen Kante gestartet

        print("Routing via Tree started")
        last_node = currentNode


        while(currentNode != d):#in dieser Schleife findet das Routing im Tree statt
                                #die idee hinter dieser schleife ist ein großes switch-case
                                #bei dem man je nach eingehenden und funktionierenden ausgehenden ports switcht
                                #nach jedem schritt den man im baum geht folgt die prüfung ob man schon am ziel angekommen ist


            #kommt das paket von einer eingehenden kante an dann wird der kleinste rang der kinder gewählt
            #denn man war noch nicht an diesem node
            if last_node == get_parent_node(tree,currentNode) or last_node == currentNode:


                print("---")
                print("Im Fall das man aus einem Parent Node kommt, currentNode : ", currentNode)
                #suche das kind mit dem kleinsten  rang



                children = []
                #es werden alle Kinder gespeichert zu denen der jetzige Knoten einen Verbindung hat und sortiert nach ihren Rängen
                out_edges_with_fails = tree.out_edges(currentNode)
                out_edges = []
                for edge in out_edges_with_fails:
                    if edge in fails or tuple(reversed(edge)) in fails:
                        print("Kante ist in Fails")
                    else: 
                        out_edges.append(edge)
                    #endif
                #endfor
                for nodes in out_edges:
                    children.append(nodes[1])
                #endfor
                children.sort(key=lambda x: (getRank(tree, x)))


                if len(children) >  0 : #wenn es kinder gibt, zu denen die Kanten nicht kaputt sind
                    #setze lastnode auf currentnode
                    #setze current node auf das kind mit dem kleinesten rang
                    #dadurch "geht man" die kante zum kind
                    last_node = currentNode
                    currentNode = children[0]
                    hops += 1
                   

                else: #wenn alle Kanten zu den Kindern kaputt sind dann ist man fertig wenn man an der source ist oder man muss eine kante hoch
                    #print("Es gibt keine möglichen Kinder !")
                    if currentNode == s: 
                        break; #das routing ist gescheitert
                    #endif


                    #man nimmt die eingehende kante des currentnode und "geht eine stufe hoch"
                    hops += 1
                    detour_edges.append( (currentNode, last_node) )
                    last_node = currentNode
                    currentNode = get_parent_node(tree,currentNode)
                    #print("Gehe eine Stufe hoch, currentNode : ", currentNode)

                #endif
            #endif



            children_of_currentNode = []

            for nodes in tree.out_edges(currentNode):
                    children_of_currentNode.append(nodes[1])
            #endfor

            #wenn das Paket nicht aus einer eingehenden Kante kommt, dann muss es aus einer ausgehenden kommen
            #dafür muss man den Rang des Kindes bestimmen von dem das Paket kommt
            #das Kind mit dem nächsthöheren Rang suchen
            if last_node in children_of_currentNode:
                print("---")
                print("Im Fall das man aus einem Kind Knoten kommt, currentNode : ", currentNode)

                
                

                #alle funktionierenden Kinder finden
                children = []
                out_edges_with_fails = tree.out_edges(currentNode)
                out_edges = []
                for edge in out_edges_with_fails:
                    if edge in fails or tuple(reversed(edge)) in fails:
                        print("Kante ist in Fails")
                    else: 
                        out_edges.append(edge)
                    #endif

                #endfor
                for nodes in out_edges:
                    children.append(nodes[1])
                #endfor
                children.sort(key=lambda x: (getRank(tree, x)))

                

                #wenn es Funktionierende Kinder gibt dann muss man das Kind suchen mit dem nächstgrößeren Rang
                if len(children) > 0: 
                    #prüfen ob es noch kinder gibt mit größerem rang , also ob es noch zu durchlaufene kinder gibt
                    #print("Suche jetzt im Array : ", last_node)
                    

                    #welchen index hat das kind nach seinem "rank" in der sortierten liste
                    index_of_last_node = children.index(last_node) if last_node in children else -1 
                
                    #alle  kinder ohne das wo das paket herkommt
                    children_without_last = [a for a in children if a != last_node] 

                    

                    #es gibt keine möglichen kinder mehr und man ist an der Source
                    #dann ist das Routing fehlgeschlagen
                    if len(children_without_last) == 0 and currentNode == s : 
                        #print("Es gibt keine möglichen Kinder mehr")
                        break;

                    #Sonderfall (noch unklar ob nötig)
                    #wenn man aus einem Kind kommt, zu dem die Kante fehlerhaft ist
                    #man nimmt trotzdem das nächste Kind
                    elif index_of_last_node == -1:
                        #print("Habe in den Kindern nicht den Knoten gefunden wo ich her komme aber gehe zum nächste Kind tiefer , currentNode :" , currentNode)
                        hops += 1
                        last_node = currentNode
                        currentNode = children[0]


                    #das kind wo das paket herkommt hatte den höchsten rang der kinder, also das letztmögliche
                    #daher muss man den Baum eine Stufe hoch
                    elif index_of_last_node == len(children)-1: 
                        #print("LastNode war das letzte mögliche Kind, lastNode :" , last_node)
                        #print("Gehe den Baum eine Stufe hoch")
                        if currentNode != s: #man muss eine stufe hoch gehen
                            hops += 1
                            detour_edges.append( (currentNode, last_node) )
                            last_node = currentNode
                            currentNode = get_parent_node(tree,currentNode)
                        else:#sonderfall wenn man an der Source ist dann ist das Routing gescheitert
                            break;

                    #es gibt noch mindestens 1 Kind mit höherem Rang
                    elif index_of_last_node < len(children)-1 : 
                        #print("Gehe den Baum eine Stufe tiefer : ", children[index_of_last_node+1])
                        #wenn ja dann nimm das Kind mit dem nächst größeren Rang aus der sortierten Children Liste
                        hops += 1
                        last_node = currentNode
                        currentNode = children[index_of_last_node+1]

                    #es gibt keine kinder mehr am currentnode
                    else: 
                        #print("Gehe den Baum eine Stufe hoch : ", get_parent_node(tree,currentNode))
                        #wenn nein dann setze currentnode auf den parent
                        hops += 1
                        detour_edges.append( (currentNode, last_node) )
                        last_node = currentNode
                        currentNode = get_parent_node(tree,currentNode)
                    #endif

                #wenn es keine funktionierenden Kinder gibt dann geht man eine Stufe hoch
                else: 
                    detour_edges.append( (currentNode, last_node) )
                    hops += 1
                    #print("Es gibt keine möglichen Kinder !")
                    last_node = currentNode
                    currentNode = get_parent_node(tree,currentNode)
                    #print("Gehe eine Stufe hoch, currentNode : ", currentNode)
                #endif
            
                
        #endwhile

        #hier kommt man an wenn die while schleife die den tree durchläuft "gebreakt" wurde und man mit dem tree nicht zum ziel gekommen ist
        #oder wenn die bedingung nicht mehr gilt (currentNode != d) und man das ziel erreicht hat

        if currentNode == d : #wir haben die destination mit dem tree erreicht
            print('Routing done via Tree')
            print('------------------------------------------------------')
            #input("Press key to continue...")
            return (False, hops, switches, detour_edges)

        print('Routing failed')
        print('------------------------------------------------------')
        #input("Press key to continue...")
        return (True, hops, switches, detour_edges)
    else: 
        return (True, 0, 0, [])


#wir fangen an alle edps nach aufsteigender länge durchzugehen
#am ende wenn wir alle edps durchhaben probieren wir den tree durchzugehen da dieser der längste ist und somit die meisten möglichkeiten drin hat zusätzlich zum längsten edp

#source s 
#destination d
#failures fails edge (u,v)
#paths [source][destination]{'trees':{graph}], 'edps':[[]] , 'distance':[distanzen von allen nodes zur destination]}
#die edps sind dabei in aufsteigender Reihenfolge sortiert
def RouteOneTree(s,d,fails,paths):
    
    if s != d :
        currentNode = -1
        edpIndex = 0
        detour_edges = []
        hops = 0
        switches = 0
        tree = paths[s][d]['tree']
        edps_for_s_d = paths[s][d]['edps']
        #print("Alle EDPs : " , edps_for_s_d)
        #print("Tree : ", list(tree.nodes))
        #distance = paths[s][d]['distance']
        print('Routing started for ' , s , " to " , d )
        #print(fails)
        #anhand der edps (außer dem längsten, also dem letzten) mit dfs versuchen zu routen
        for edp in edps_for_s_d:
            print("EDP in der EDP Schleife : " , edp)
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
        #print("Alle EDPs : " , edps_for_s_d)
        #print("len(edps_for_s_d) -1 : ", len(edps_for_s_d) -1)
        #print("EDP für den Baum : " , edp)
        #print("EDP Index : ", edpIndex)
        PG = nx.nx_pydot.write_dot(tree , "./graphen/tree_"+ str(s) + "_" +  str(d))
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
                    PG = nx.nx_pydot.write_dot(tree , "./graphen/tree_"+ str(s) + "_" +  str(d))
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
                #print("Jetziger Node : " , currentNode)
                
                # alle kinder entfernen, bei denen wir schon waren
                #da wir immer die kinder zu visited nodes hinzufügen wird die liste immer kleiner und die nächste iteration merkt dass man alle kinder schon "probiert"
                #hat und man muss dann einen knoten hoch gehen
                
                # wenn wir zum im tree routen schalten wollen aber current node nicht im tree ist dann müssen wir den edp zurück bis wir im tree sind
                # spätestens an der wurzel (edp[0]) sind wir im tree
                if not tree.has_node(currentNode):
                    edpIndex = edpIndex -1
                    hops += 1
                    visitedNodes.append(currentNode)
                    detour_edges.append((edp[edpIndex], edp[edpIndex -1]))
                    currentNode = edp[edpIndex]
                    continue; # skip loop and try with previous node again
                

                
                possibleNextNodes = list(nx.neighbors(tree, currentNode))
                #print("Mögliche Nachbarn vor der Kürzung : " , possibleNextNodes)
                tmp = []
                for el in possibleNextNodes:
                    if el in visitedNodes:
                        continue
                    else:
                        tmp.append(el)

                possibleNextNodes = tmp
                
                #print("Mögliche Nachbarn nach der Kürzung : " , possibleNextNodes)
                #print("VisitedNodes : " , visitedNodes)

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
    else: 
        return (True, 0, 0, [])


def getRank(tree, el):
    #print("el : ", el)
    #print("Versuche aus dem Tree : ", list(tree.nodes))
    #print("Den Rang zu finden von ", tree.nodes[el])
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
            if precomputation is None:
               return -1
    fails = edg[:f]
    if targeted:
        fails = []
    failures1 = {(u, v): g[u][v]['arb'] for (u, v) in fails}
    failures1.update({(v, u): g[u][v]['arb'] for (u, v) in fails})

    g = g.copy(as_view=False)
    g.remove_edges_from(failures1.keys())
    nodes = list(set(connected_component_nodes_with_d_after_failures(g,[],d))-set([dest, d]))
    dist = nx.shortest_path_length(g, target=d)
    if len(nodes) < samplesize:
        print('Not enough nodes in connected component of destination (%i nodes, %i sample size), adapting it' % (len(nodes), samplesize))
        PG = nx.nx_pydot.write_dot(g , "./failedGraphs/graph")
        samplesize = len(nodes)
    nodes = list(set(g.nodes())-set([dest, d]))
    random.shuffle(nodes)
    count = 0
    for s in nodes[:samplesize]:
        print("Loop over samplesize is runing")
        count += 1
        for stat in stats:
            print("Loop over stats is runing")
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

###################################################################################################################################
#routing MultipleTrees ohne ausschließlicher Nutzung lokaler Informationen
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



####################################################################################################################################
#Routing im onetree ohne ausschließlicher nutzung lokaler informationen


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


###################################################################################################################
#hier ist das alte multipletrees bei dem das "j" durch "it" in der while schleife getauscht werden musste

def multiple_trees(source, destination, graph, all_edps):
    trees = [] #hier werden alle trees gespeichert 
    #print(all_edps)

    #für jeden tree muss hier sein edp eingefügt werden in den graph 
    #print("All EDPs : " , all_edps)
    for i in range(0,len(all_edps)):

        current_edp = all_edps[i]
        #print("Current EDP : ", current_edp)
        tree = nx.DiGraph()
        tree.add_node(source)
        for j in range(1,len(current_edp)-1):
            tree.add_node(current_edp[j])
            tree.add_edge(current_edp[j-1], current_edp[j])

        trees.append(tree)

    assert len(trees) == len(all_edps), 'Not every edp got a tree!'

    for i in range(0,len(all_edps)): #jeden edp einmal durchgehen
                                      #um zu versuchen aus jedem edp einen Baum zu bauen
        #tree = nx.DiGraph()
        #tree.add_node(source)
        tree = trees[i] # Baum der zuvor mit dem edp gefüllt wurde
        pathToExtend = all_edps[i]

        #print("---- Nächster Tree für " , pathToExtend , " ----")
        nodes = pathToExtend[:len(pathToExtend) -1]#in nodes stehen dann alle knoten drin die wir besuchen wollen um deren nachbarn auch reinzupacken
                                                   # am anfang ganzer edp drin und -2 damit die destination nicht mit drin steht
        
        for j in range(0,len(pathToExtend)-1): #alle knoten aus nodes[] durchgehen und deren nachbarn suchen, angefangen mit den knoten aus dem edp
            
                       
            it = 0
            while it < len(nodes):
                
                neighbors = list(nx.neighbors(graph, nodes[it])) #für jeden knoten aus nodes die nachbarn finden und gucken ob sie in den tree eingefügt werden dürfen

                for k in range(0,len(neighbors)): #jeden der nachbarn durchgehen

                    #if(neighbors[k] != nodes[j] and neighbors[k] != destination): #kanten zu sich selbst dürfen nicht rein da dann baum zu kreis wird und kanten zur destination auch nicht
                    if(neighbors[k] != nodes[it] and neighbors[k] != destination): #kanten zu sich selbst dürfen nicht rein da dann baum zu kreis wird und kanten zur destination auch nicht    
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
                                #if (tree_to_check.has_edge(nodes[j],neighbors[k])): #wenn ein tree die edge schon drin hat dann darf man die edge nicht mehr benutzen
                                if (tree_to_check.has_edge(nodes[it],neighbors[k])): #wenn ein tree die edge schon drin hat dann darf man die edge nicht mehr benutzen
                                    is_in_other_tree = True
                                    break
                                #endif
                            #endfor
                        
                            if not ( is_in_other_tree or (tree.has_node(neighbors[k])) ):
                                #print("Füge die Kante : ", nodes[j] , " - " , neighbors[k] , " ein bei len(trees) > 0")
                                nodes.append(neighbors[k]) 
                                tree.add_node(neighbors[k])
                                #tree.add_edge(nodes[j],neighbors[k])
                                tree.add_edge(nodes[it],neighbors[k])
                            #endif
                        #endif
                        else: #das ist der fall wenn es noch keine anderen trees zum checken gibt, ob die kante schon verbaut ist
                            if not((neighbors[k] == destination) or (tree.has_node(neighbors[k]))): #dann darf die kante nicht zur destination sein
                                                                                                    #der knoten darf nicht im jetzigen tree drin sein
                                #print("Füge die Kante : " , nodes[j] , " - " , neighbors[k] , " ein bei len(trees) = 0")
                                
                                tree.add_node(neighbors[k])
                                #tree.add_edge(nodes[j],neighbors[k])
                                tree.add_edge(nodes[it],neighbors[k])
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
            rank_tree(tree , source,all_edps[i])
            connect_leaf_to_destination(tree, source,destination)
            #print("Versuche jetzt auf dem Tree : " , list(tree.nodes), " den Rang für ", destination , " einzufügen")
            tree.nodes[destination]["rank"] = -1
            #trees.apend(tree)
        #endif
    #endfor
    return trees


#####################################################
#hier ist die alte route multiple trees, welche entfernt wurde weil bei diesem routing die edps nicht gesondert betrachtet werden, abgesehen davon dass diese priorisiert werden
#dadurch dass sie den kleinsten rang haben in ihren kindern. Also wurde der ganze erste part, also das routing durch die edps entfernt

def RouteMultipleTrees(s,d,fails,paths):

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


     #alle EDPS entlang routen
    currentNode = s
    edpIndex = 0
    detour_edges = []
    hops = 0
    switches = 0
    trees = paths[s][d]['trees']
    edps_for_s_d = sorted(paths[s][d]['edps'],key=len) # Aufsteigend die EDPs sortieren damit man den größten als letztes hat
    print(" ")
    print('Routing started for ' , s , " to " , d )

    if(not skip_edps):

        if(s != d):

            #als erstes anhand der EDPs (außer dem längsten, also dem letzten) versuchen zu routen
            for edp in edps_for_s_d:

                currentNode = s
                last_node = s 

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
                #endif

            #endfor

            # wenn wir es nicht geschafft haben anhand der edps allein zum ziel zu routen dann geht es am längsten edp weiter
            print('Routing via EDPs FAILED')

        #endif
    #endif
    if(not skip_trees):

        print(" ")
        print("Routing via Tree started")

        for tree in trees:
            
            #hier wurde das Routing von OneTree eingesetzt
            while(currentNode != d):#in dieser Schleife findet das Routing im Tree statt
                                #die idee hinter dieser schleife ist ein großes switch-case
                                #bei dem man je nach eingehenden und funktionierenden ausgehenden ports switcht
                                #nach jedem schritt den man im baum geht folgt die prüfung ob man schon am ziel angekommen ist


                #kommt das paket von einer eingehenden kante (parent) an dann wird der kleinste rang der kinder gewählt
                #denn man war noch nicht an diesem node
                if last_node == get_parent_node(tree,currentNode) or last_node == currentNode:


                    #suche das kind mit dem kleinsten  rang



                    children = []
                    #es werden alle Kinder gespeichert zu denen der jetzige Knoten einen Verbindung hat und sortiert nach ihren Rängen
                    out_edges_with_fails = tree.out_edges(currentNode)
                    out_edges = []
                    for edge in out_edges_with_fails:
                        if edge in fails or tuple(reversed(edge)) in fails:
                            continue

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
                        if currentNode == s: 
                            break; #das routing für diesen Baum
                        #endif


                        #man nimmt die eingehende kante des currentnode und "geht eine stufe hoch"
                        hops += 1
                        detour_edges.append( (currentNode, last_node) )
                        last_node = currentNode
                        currentNode = get_parent_node(tree,currentNode)

                    #endif
                #endif



                children_of_currentNode = []

                for nodes in tree.out_edges(currentNode):
                        children_of_currentNode.append(nodes[1])
                #endfor

                #wenn das Paket nicht aus einer eingehenden Kante kommt, dann muss es aus einer ausgehenden (kind) kommen
                #dafür muss man den Rang des Kindes bestimmen von dem das Paket kommt
                #das Kind mit dem nächsthöheren Rang suchen
                if last_node in children_of_currentNode:

                    #alle funktionierenden Kinder finden
                    children = []
                    out_edges_with_fails = tree.out_edges(currentNode)
                    out_edges = []
                    for edge in out_edges_with_fails:
                        if edge in fails or tuple(reversed(edge)) in fails:
                            continue 
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
                        

                        #welchen index hat das kind nach seinem "rank" in der sortierten liste
                        index_of_last_node = children.index(last_node) if last_node in children else -1 
                    
                        #alle  kinder ohne das wo das paket herkommt
                        children_without_last = [a for a in children if a != last_node] 

                        #es gibt keine möglichen kinder mehr und man ist an der Source
                        #dann ist das Routing fehlgeschlagen für diesen Baum
                        if len(children_without_last) == 0 and currentNode == s : 
                            break;

                        #Sonderfall (noch unklar ob nötig)
                        #wenn man aus einem Kind kommt, zu dem die Kante fehlerhaft ist
                        #man nimmt trotzdem das nächste Kind
                        elif index_of_last_node == -1:
                            hops += 1
                            last_node = currentNode
                            currentNode = children[0]

                        #das kind wo das paket herkommt hatte den höchsten rang der kinder, also das letztmögliche
                        #daher muss man den Baum eine Stufe hoch
                        elif index_of_last_node == len(children)-1: 
                            
                            if currentNode != s: #man muss eine stufe hoch gehen
                                hops += 1
                                detour_edges.append( (currentNode, last_node) )
                                last_node = currentNode
                                currentNode = get_parent_node(tree,currentNode)
                            else:#sonderfall wenn man an der Source ist dann ist das Routing gescheitert
                                break;

                        #es gibt noch mindestens 1 Kind mit höherem Rang
                        elif index_of_last_node < len(children)-1 : 
                            #wenn ja dann nimm das Kind mit dem nächst größeren Rang aus der sortierten Children Liste
                            hops += 1
                            last_node = currentNode
                            currentNode = children[index_of_last_node+1]

                        #es gibt keine kinder mehr am currentnode
                        else: 
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
                        last_node = currentNode
                        currentNode = get_parent_node(tree,currentNode)
                    #endif
                
                    
            #endwhile

            if (currentNode == d):#falls wir am ziel angekommen sind
                print("Routing done via the Tree : ", list(tree.nodes))
                print(" ")
                return (False, hops, switches, detour_edges)
            #endif

            #das war in OneTree egal, da man nur 1 Tree hatte, aber hier kann die Source der Bäume nicht an den gleichen Knoten dran sein wie
            #andere Bäume, daher muss der eingehende Port des Pakets auf den currentNode gesetzt werden (hier die Source) damit man 
            #weiß dass man den nächsten Baum nimmt
            last_node = currentNode
        #endfor 
        print("Routing failed via Trees ")
        print(" ")
        return (True, hops, switches, detour_edges)    
    #endif

###########################################################################################################################################################
###########################################################################################################################################################

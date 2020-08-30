import networkx
import benchmark_template
from benchmark_template import one_experiment
from routing import *
import arborescences

"""
Authors: 
Ioan Marian Dan, 
Diana-Alexandra Deac
Daniel Alejandro Robles
Alhamzeh Ismail

License: GNU General Public License (GPL) version 3
https://opensource.org/licenses/GPL-3.0

SCENARIO: In order to route a packet over the graph from source towards the destination, the randomized routing algorithm takes the first (randomly chosen) arborescence and it redirects the packet on that arborescence. If the link fails, the randomized routing algorithm takes a second arborescence (again randomly chosen) and redirects the packet through it. The process repeats itself each time a link fails, using any of the existing arborescences in the set. 

IMPROVEMENT: We noticed that there are some cases (it happens perhaps more often in small graphs) when the destination node happens to be a neighbour to the source node, but the randomized routing algorithm does not take this into consideration. Instead, it continues to take arborescences in a random order, switching if a link fails, until it finds the destination. The problem is that there can be many hops to reach the destination, although the destination is next to the source. In order to save time (especially when the destination is next to the source) we improved the function that implements the randomized routing algorithm (def RoutePR(s,d,fails,T)), so that it checks first if the destination is one of the source’s neighbours. 

Before having the algorithm run as designed by Chiesa, we check the source’s neighbours to see if one of them is the same as destination. If the destination is the same as one of the neighbours of the source, we then check if the path between them (source to destination/neighbour)  is included in the fails set. 

IMPROVEMENT: If the path between source and destination/neighbour is not in the fails set, we send the packet directly on this link/path to the destination, and the process ends here (function returns). If the path between source and destination/neighbour is in the fails set, we exit the improved block and we start to redirect the packet as always on the first (randomly chosen) arborescence, and if there are link failures we choose the next arborescence and so on. The latter process is also executed if the destination node is not in the neighbours of the source node, thus circumventing the  block in the algorithm with our improvement.
"""


# Route with randomly chosen arborescence, if
# the starting node is connected to the destination,
# the corresponding link is tried first.
# source s
# destination d
# link failure set fails
# arborescence decomposition T
P = 0.5358  # bounce probability
def RouteTryLinkToDestinationFirstPR(s, d, fails, T):
    detour_edges = []
    curT = 0
    hops = 0
    switches = 0
    n = len(T[0].nodes())

    """our team from hier"""
    print("Enter the neighbors check block. Retrieving the destination in the neighborhood of source...")
    number_of_arbs = len(T)
    destination_is_neightbor = False
    failed = False
    index = 0
    while(index < number_of_arbs):
        #print(index)
        first_neighbor = list(T[index].neighbors(s))[0]
        if(first_neighbor == d):
            if(first_neighbor, s) in fails or (s, first_neighbor) in fails:
                failed = True
                print("Destination is neighbour to the source but the edge between them is FAILED")
            else:
                destination_is_neightbor = True
                s = first_neighbor
                if (destination_is_neightbor == True):
                    print("For this source, the destination was found in neighborhood!!!!")
                    return (False, 1, index, detour_edges)
        index += 1
        if index > 0:
            detour_edges.append((s, first_neighbor))
    if (failed == False):
        print("Exit the neighbors check block. The destination was not found in neighborhood!!!! ")
    else:
        print("Exit the neighbors check block. The destination was found in neighborhood but FAILED!!!! ")
    """our team till hier"""


    while (s != d):
        nxt = list(T[curT].neighbors(s))  # if neighbor  == d und kanten ist nicht in fails then go there
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


if __name__ == "__main__":
    #       TEST IMPROVEMENT 1 , NEIGHBOUR CHECK
    n = 6           # knoten
    rep = 1         # repetitions when testing
    k = 3           # konnectivity
    samplesize = 10 # num von quellen
    f_num = 2       # failures zu testen
    seed = 4444 #
    benchmark_template.set_parameters([n, rep, k, samplesize, f_num, seed, "benchmark-"])   # set global variables
    g = init_k_graph(k, n)      # generate the graph
    g.graph['fails'] = None     # at first the graph has no fails
    out = open("Test" + ".txt", 'w')    #a - append modus
    out.write("Hello there")
    one_experiment(g, seed, out, [GreedyArborescenceDecomposition, RoutePR])
    out.close()
    arbs = GreedyArborescenceDecomposition(g)   #generate the arborescences of the graph (# of arbs == k)
    #fails = [ (4, 5), (4,0)]           # fails to try the routing algo wit fail between sourde and destination/neighbour
    fails = [(1, 2), (3, 2) , (4, 5)]   # fails on the generated graph
    drawArborescences(g, "TestARB")     # name of the pictures with the graph and each generated arb
    source = 4      # source node
    destination = 0 # destination node
    print(RoutePR(source, destination, fails, arbs))    #call of the function implementing randomized routing algorithmus
    #       PROOF k-1 RESILIENCY
    print()
    print()
    print("k-1 resiliency check bellow: ")
    fails = [(4,5), (4,1), (2,3), (2,1), (4,3)]       #run until this fails are make k-1 fails on the graph, because we cannot generate the same graph repeatedly (mentioned under problems in the paper)
    drawArborescences(g, "TestARB_k-1_Resiliency")  ## name of the pictures with the graph and each generated arb
    source = 4      # source node
    destination = 0 # destination node
    print(RoutePR(source, destination, fails, arbs))    #call of the function implementing randomized routing algorithmus

    #       SOME CHECKS
    print()
    print()
    print("number of nodes in each ARB: ")
    l = len(arbs[0].nodes())
    print(l)
    print("number of arbs generated in graph (always = k): ")
    print(len(arbs))
    print("number of neighbours of source, in the given arborescence in the set of arborescences: ")
    nxt = list(arbs[0].neighbors(source))
    print(len(nxt))
    print("all tests completed")
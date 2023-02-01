import matplotlib.pyplot as plt
import csv
import numpy as np
import math
#liest text datei
#parse csv zu array
#plott

##################################################################################################################
#Hier müssen die algorithm1 , algorithm2 , TitleAlgo1 . TitleAlgo1 NACH JEDEM BEENDETEM PLOT geändert werden
algorithm1 = 'one_tree'
algorithm2 = 'one_tree_breite_mod'
TitleAlgo1 = " One Tree"
TitleAlgo2 = " One Tree Breite Mod"

#Filepath und FR müssen nach jedem FR geändert werden
filepath = "OneTree_vs_OneTree_Breite_Mod/benchmark-regular-FR10-1tVS1tM-40-5.txt"
FR = '_fr10'

###################################################################################################################
f = open(filepath, "r")
reader = csv.reader(f)
# Skip two header lines
next(reader)
next(reader)

data = []
for line in reader:
    [graph, size, connectivity, algorithm, index, stretch, load, hops, success, routing_computation_time, pre_computation_time] = line
    data.append({ "graph": graph, "size": int(size), "connectivity" : int(connectivity), "algorithm" : algorithm, "index": int(index), "stretch": int(stretch), "load": int(load), "hops": int(hops), "success": float(success), "routing_computation_time" : float(routing_computation_time), "pre_computation_time" : float(pre_computation_time)})



#print(data)
accumulated = {
    "multiple_tree": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},

    algorithm2 + "_fr2": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm2 +"_fr3": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm2 + "_fr4": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm2 + "_fr5": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm2 + "_fr6": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm2 + "_fr7": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm2 +"_fr8": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm2 + "_fr9": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm2 + "_fr10": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    
    algorithm1 + "_fr2": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm1 +"_fr3": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm1 + "_fr4": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm1 + "_fr5": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm1 + "_fr6": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm1 + "_fr7": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm1 +"_fr8": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm1 + "_fr9": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    algorithm1 + "_fr10": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    #... hier muss dann für jeden algorithmus den ich habe ein dict erstellt werden
}


# value for  multiple_tree


for result in data:

    
    #hier werden jetzt die daten nach algorithmen sortiert
    if result['algorithm'] == " Multiple Trees FR8":
        accumulated['multiple_tree']['count'] = 1 + accumulated['multiple_tree']['count']
        accumulated['multiple_tree']['stretch'] = result['stretch'] + accumulated['multiple_tree']['stretch']
        accumulated['multiple_tree']['load'] = result['load'] + accumulated['multiple_tree']['load']
        accumulated['multiple_tree']['hops'] = result['hops'] + accumulated['multiple_tree']['hops']
        accumulated['multiple_tree']['success'] = result['success'] + accumulated['multiple_tree']['success']
        accumulated['multiple_tree']['routing_computation_time'] = result['routing_computation_time'] + accumulated['multiple_tree']['routing_computation_time']
        accumulated['multiple_tree']['pre_computation_time'] = result['pre_computation_time'] + accumulated['multiple_tree']['pre_computation_time']
#############################################################################################################################################
    #hier müssen dann für jedes der dicts noch die daten auch aufsummiert werden
    if result['algorithm'] == TitleAlgo1 +" FR2":
        accumulated[algorithm1 + '_fr2']['count'] = 1 + accumulated[algorithm1 + '_fr2']['count']
        accumulated[algorithm1 + '_fr2']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr2']['stretch']
        accumulated[algorithm1 + '_fr2']['load'] = result['load'] + accumulated[algorithm1 + '_fr2']['load']
        accumulated[algorithm1 + '_fr2']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr2']['hops']
        accumulated[algorithm1 + '_fr2']['success'] = result['success'] + accumulated[algorithm1 + '_fr2']['success']
        accumulated[algorithm1 + '_fr2']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr2']['routing_computation_time']
        accumulated[algorithm1 + '_fr2']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr2']['pre_computation_time']

    if result['algorithm'] == TitleAlgo1 +" FR3":
        accumulated[algorithm1 + '_fr3']['count'] = 1 + accumulated[algorithm1 + '_fr3']['count']
        accumulated[algorithm1 + '_fr3']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr3']['stretch']
        accumulated[algorithm1 + '_fr3']['load'] = result['load'] + accumulated[algorithm1 + '_fr3']['load']
        accumulated[algorithm1 + '_fr3']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr3']['hops']
        accumulated[algorithm1 + '_fr3']['success'] = result['success'] + accumulated[algorithm1 + '_fr3']['success']
        accumulated[algorithm1 + '_fr3']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr3']['routing_computation_time']
        accumulated[algorithm1 + '_fr3']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr3']['pre_computation_time']

    
    if result['algorithm'] == TitleAlgo1 +" FR4":
        accumulated[algorithm1 + '_fr4']['count'] = 1 + accumulated[algorithm1 + '_fr4']['count']
        accumulated[algorithm1 + '_fr4']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr4']['stretch']
        accumulated[algorithm1 + '_fr4']['load'] = result['load'] + accumulated[algorithm1 + '_fr4']['load']
        accumulated[algorithm1 + '_fr4']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr4']['hops']
        accumulated[algorithm1 + '_fr4']['success'] = result['success'] + accumulated[algorithm1 + '_fr4']['success']
        accumulated[algorithm1 + '_fr4']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr4']['routing_computation_time']
        accumulated[algorithm1 + '_fr4']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr4']['pre_computation_time']
    
    if result['algorithm'] == TitleAlgo1 +" FR5":
        accumulated[algorithm1 + '_fr5']['count'] = 1 + accumulated[algorithm1 + '_fr5']['count']
        accumulated[algorithm1 + '_fr5']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr5']['stretch']
        accumulated[algorithm1 + '_fr5']['load'] = result['load'] + accumulated[algorithm1 + '_fr5']['load']
        accumulated[algorithm1 + '_fr5']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr5']['hops']
        accumulated[algorithm1 + '_fr5']['success'] = result['success'] + accumulated[algorithm1 + '_fr5']['success']
        accumulated[algorithm1 + '_fr5']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr5']['routing_computation_time']
        accumulated[algorithm1 + '_fr5']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr5']['pre_computation_time']

    if result['algorithm'] == TitleAlgo1 +" FR6":
        accumulated[algorithm1 + '_fr6']['count'] = 1 + accumulated[algorithm1 + '_fr6']['count']
        accumulated[algorithm1 + '_fr6']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr6']['stretch']
        accumulated[algorithm1 + '_fr6']['load'] = result['load'] + accumulated[algorithm1 + '_fr6']['load']
        accumulated[algorithm1 + '_fr6']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr6']['hops']
        accumulated[algorithm1 + '_fr6']['success'] = result['success'] + accumulated[algorithm1 + '_fr6']['success']
        accumulated[algorithm1 + '_fr6']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr6']['routing_computation_time']
        accumulated[algorithm1 + '_fr6']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr6']['pre_computation_time']

    if result['algorithm'] == TitleAlgo1 +" FR7":
        accumulated[algorithm1 + '_fr7']['count'] = 1 + accumulated[algorithm1 + '_fr7']['count']
        accumulated[algorithm1 + '_fr7']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr7']['stretch']
        accumulated[algorithm1 + '_fr7']['load'] = result['load'] + accumulated[algorithm1 + '_fr7']['load']
        accumulated[algorithm1 + '_fr7']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr7']['hops']
        accumulated[algorithm1 + '_fr7']['success'] = result['success'] + accumulated[algorithm1 + '_fr7']['success']
        accumulated[algorithm1 + '_fr7']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr7']['routing_computation_time']
        accumulated[algorithm1 + '_fr7']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr7']['pre_computation_time']

    if result['algorithm'] == TitleAlgo1 +" FR8":
        accumulated[algorithm1 + '_fr8']['count'] = 1 + accumulated[algorithm1 + '_fr8']['count']
        accumulated[algorithm1 + '_fr8']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr8']['stretch']
        accumulated[algorithm1 + '_fr8']['load'] = result['load'] + accumulated[algorithm1 + '_fr8']['load']
        accumulated[algorithm1 + '_fr8']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr8']['hops']
        accumulated[algorithm1 + '_fr8']['success'] = result['success'] + accumulated[algorithm1 + '_fr8']['success']
        accumulated[algorithm1 + '_fr8']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr8']['routing_computation_time']
        accumulated[algorithm1 + '_fr8']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr8']['pre_computation_time']

    if result['algorithm'] == TitleAlgo1 +" FR9":
        accumulated[algorithm1 + '_fr9']['count'] = 1 + accumulated[algorithm1 + '_fr9']['count']
        accumulated[algorithm1 + '_fr9']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr9']['stretch']
        accumulated[algorithm1 + '_fr9']['load'] = result['load'] + accumulated[algorithm1 + '_fr9']['load']
        accumulated[algorithm1 + '_fr9']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr9']['hops']
        accumulated[algorithm1 + '_fr9']['success'] = result['success'] + accumulated[algorithm1 + '_fr9']['success']
        accumulated[algorithm1 + '_fr9']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr9']['routing_computation_time']
        accumulated[algorithm1 + '_fr9']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr9']['pre_computation_time']

    if result['algorithm'] == TitleAlgo1 +" FR10":
        accumulated[algorithm1 + '_fr10']['count'] = 1 + accumulated[algorithm1 + '_fr10']['count']
        accumulated[algorithm1 + '_fr10']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr10']['stretch']
        accumulated[algorithm1 + '_fr10']['load'] = result['load'] + accumulated[algorithm1 + '_fr10']['load']
        accumulated[algorithm1 + '_fr10']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr10']['hops']
        accumulated[algorithm1 + '_fr10']['success'] = result['success'] + accumulated[algorithm1 + '_fr10']['success']
        accumulated[algorithm1 + '_fr10']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr10']['routing_computation_time']
        accumulated[algorithm1 + '_fr10']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr10']['pre_computation_time']

    

    
##############################################################################################################################################
     #hier müssen dann für jedes der dicts noch die daten auch aufsummiert werden
    if result['algorithm'] == TitleAlgo2 +" FR2":
        accumulated[algorithm2 + '_fr2']['count'] = 1 + accumulated[algorithm2 + '_fr2']['count']
        accumulated[algorithm2 + '_fr2']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr2']['stretch']
        accumulated[algorithm2 + '_fr2']['load'] = result['load'] + accumulated[algorithm2 + '_fr2']['load']
        accumulated[algorithm2 + '_fr2']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr2']['hops']
        accumulated[algorithm2 + '_fr2']['success'] = result['success'] + accumulated[algorithm2 + '_fr2']['success']
        accumulated[algorithm2 + '_fr2']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr2']['routing_computation_time']
        accumulated[algorithm2 + '_fr2']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr2']['pre_computation_time']

    if result['algorithm'] == TitleAlgo2 +" FR3":
        accumulated[algorithm2 + '_fr3']['count'] = 1 + accumulated[algorithm2 + '_fr3']['count']
        accumulated[algorithm2 + '_fr3']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr3']['stretch']
        accumulated[algorithm2 + '_fr3']['load'] = result['load'] + accumulated[algorithm2 + '_fr3']['load']
        accumulated[algorithm2 + '_fr3']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr3']['hops']
        accumulated[algorithm2 + '_fr3']['success'] = result['success'] + accumulated[algorithm2 + '_fr3']['success']
        accumulated[algorithm2 + '_fr3']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr3']['routing_computation_time']
        accumulated[algorithm2 + '_fr3']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr3']['pre_computation_time']

    
    if result['algorithm'] == TitleAlgo2 +" FR4":
        accumulated[algorithm2 + '_fr4']['count'] = 1 + accumulated[algorithm2 + '_fr4']['count']
        accumulated[algorithm2 + '_fr4']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr4']['stretch']
        accumulated[algorithm2 + '_fr4']['load'] = result['load'] + accumulated[algorithm2 + '_fr4']['load']
        accumulated[algorithm2 + '_fr4']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr4']['hops']
        accumulated[algorithm2 + '_fr4']['success'] = result['success'] + accumulated[algorithm2 + '_fr4']['success']
        accumulated[algorithm2 + '_fr4']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr4']['routing_computation_time']
        accumulated[algorithm2 + '_fr4']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr4']['pre_computation_time']
    
    if result['algorithm'] == TitleAlgo2 +" FR5":
        accumulated[algorithm2 + '_fr5']['count'] = 1 + accumulated[algorithm2 + '_fr5']['count']
        accumulated[algorithm2 + '_fr5']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr5']['stretch']
        accumulated[algorithm2 + '_fr5']['load'] = result['load'] + accumulated[algorithm2 + '_fr5']['load']
        accumulated[algorithm2 + '_fr5']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr5']['hops']
        accumulated[algorithm2 + '_fr5']['success'] = result['success'] + accumulated[algorithm2 + '_fr5']['success']
        accumulated[algorithm2 + '_fr5']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr5']['routing_computation_time']
        accumulated[algorithm2 + '_fr5']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr5']['pre_computation_time']

    if result['algorithm'] == TitleAlgo2 +" FR6":
        accumulated[algorithm2 + '_fr6']['count'] = 1 + accumulated[algorithm2 + '_fr6']['count']
        accumulated[algorithm2 + '_fr6']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr6']['stretch']
        accumulated[algorithm2 + '_fr6']['load'] = result['load'] + accumulated[algorithm2 + '_fr6']['load']
        accumulated[algorithm2 + '_fr6']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr6']['hops']
        accumulated[algorithm2 + '_fr6']['success'] = result['success'] + accumulated[algorithm2 + '_fr6']['success']
        accumulated[algorithm2 + '_fr6']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr6']['routing_computation_time']
        accumulated[algorithm2 + '_fr6']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr6']['pre_computation_time']

    if result['algorithm'] == TitleAlgo2 +" FR7":
        accumulated[algorithm2 + '_fr7']['count'] = 1 + accumulated[algorithm2 + '_fr7']['count']
        accumulated[algorithm2 + '_fr7']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr7']['stretch']
        accumulated[algorithm2 + '_fr7']['load'] = result['load'] + accumulated[algorithm2 + '_fr7']['load']
        accumulated[algorithm2 + '_fr7']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr7']['hops']
        accumulated[algorithm2 + '_fr7']['success'] = result['success'] + accumulated[algorithm2 + '_fr7']['success']
        accumulated[algorithm2 + '_fr7']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr7']['routing_computation_time']
        accumulated[algorithm2 + '_fr7']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr7']['pre_computation_time']

    if result['algorithm'] == TitleAlgo2 +" FR8":
        accumulated[algorithm2 + '_fr8']['count'] = 1 + accumulated[algorithm2 + '_fr8']['count']
        accumulated[algorithm2 + '_fr8']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr8']['stretch']
        accumulated[algorithm2 + '_fr8']['load'] = result['load'] + accumulated[algorithm2 + '_fr8']['load']
        accumulated[algorithm2 + '_fr8']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr8']['hops']
        accumulated[algorithm2 + '_fr8']['success'] = result['success'] + accumulated[algorithm2 + '_fr8']['success']
        accumulated[algorithm2 + '_fr8']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr8']['routing_computation_time']
        accumulated[algorithm2 + '_fr8']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr8']['pre_computation_time']

    if result['algorithm'] == TitleAlgo2 +" FR9":
        accumulated[algorithm2 + '_fr9']['count'] = 1 + accumulated[algorithm2 + '_fr9']['count']
        accumulated[algorithm2 + '_fr9']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr9']['stretch']
        accumulated[algorithm2 + '_fr9']['load'] = result['load'] + accumulated[algorithm2 + '_fr9']['load']
        accumulated[algorithm2 + '_fr9']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr9']['hops']
        accumulated[algorithm2 + '_fr9']['success'] = result['success'] + accumulated[algorithm2 + '_fr9']['success']
        accumulated[algorithm2 + '_fr9']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr9']['routing_computation_time']
        accumulated[algorithm2 + '_fr9']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr9']['pre_computation_time']

    if result['algorithm'] == TitleAlgo2 +" FR10":
        accumulated[algorithm2 + '_fr10']['count'] = 1 + accumulated[algorithm2 + '_fr10']['count']
        accumulated[algorithm2 + '_fr10']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr10']['stretch']
        accumulated[algorithm2 + '_fr10']['load'] = result['load'] + accumulated[algorithm2 + '_fr10']['load']
        accumulated[algorithm2 + '_fr10']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr10']['hops']
        accumulated[algorithm2 + '_fr10']['success'] = result['success'] + accumulated[algorithm2 + '_fr10']['success']
        accumulated[algorithm2 + '_fr10']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr10']['routing_computation_time']
        accumulated[algorithm2 + '_fr10']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr10']['pre_computation_time']

#ÄNDERN
print(filepath)

print(" ")
print(algorithm1 + " " + FR +  " Ergebnisse : " )
print("Count : ", accumulated[algorithm1 + FR]['count'])
print("Durchschnittliche Resilienz : ", accumulated[algorithm1 + FR ]['success'] /  accumulated[algorithm1 + FR ]['count'] )
print("Durchschnittliche Hops : ", accumulated[algorithm1 + FR ]['hops'] /  accumulated[algorithm1 + FR ]['count'] )
print("Durchschnittliche Zeit : ", (accumulated[algorithm1 + FR ]['pre_computation_time']+accumulated[algorithm1 + FR ]['routing_computation_time'])  /  accumulated[algorithm1 + FR]['count'])
print(" ")
print(algorithm2 +   " " + FR +   " Ergebnisse : " )
print("Count : ", accumulated[algorithm2 + FR]['count'])
print("Durchschnittliche Resilienz : ", accumulated[algorithm2 + FR ]['success'] /  accumulated[algorithm2 + FR]['count'] )
print("Durchschnittliche Hops : ", accumulated[algorithm2 + FR ]['hops'] /  accumulated[algorithm2 + FR ]['count'] )
print("Durchschnittliche Zeit : ", (accumulated[algorithm2 + FR ]['pre_computation_time']+accumulated[algorithm2 + FR ]['routing_computation_time'])  /  accumulated[algorithm2 + FR ]['count'])



###Graphen ####




plotfig = False
if (plotfig):

    plt.figure()

    #PLOT1

    X = [0,1,2,3,4,5,6,7,8,9,10]
    # Assign variables to the y axis part of the curve
    y = [1,1,1,1,1, 0.925 , 0.85 , 0.725 , 0.575 , 0.42 , 0.225] #OneTree
    z = [1,1,1,1,1, 0.925 , 0.874 , 0.775 , 0.575 , 0.45 , 0.25] #MultipleTrees
    # Plotting both the curves simultaneously
    plt.subplot(221)
    plt.plot(X, y, color='r', label='OneTree')
    plt.plot(X, z, color='g', label='MultipleTrees')
    # Naming the x-axis, y-axis and the whole graph
    plt.xlabel("Failure Rate")
    plt.ylabel("Resilienz")
    plt.title("Resilienz, n = 40 , k = 5 ")
    # Adding legend, which helps us recognize the curve according to it's color
    plt.legend()


    #PLOT2
    X = [0,1,2,3,4,5,6,7,8,9,10]
    y = [3.5 , 3.5 , 3.5 , 3.875 , 4.375 , 5.75 , 8.625 , 6.625 , 8.125 , 7.1 , 4] #OneTree
    z = [3.5 , 3.5 , 3.5 , 3.875 , 4.375 , 5.75 , 10.125 , 11.875 , 7.75 , 8.7 , 7]
    # Plotting both the curves simultaneously
    plt.subplot(222)
    plt.plot(X, y, color='r', label='OneTree')
    plt.plot(X, z, color='g', label='MultipleTrees')
    # Naming the x-axis, y-axis and the whole graph
    plt.xlabel("Failure Rate")
    plt.ylabel("Durschn. Hops")
    plt.title("Durschn. Hops, n = 40 , k = 5 ")
    # Adding legend, which helps us recognize the curve according to it's color
    plt.legend()

    # To load the display window
    plt.show()

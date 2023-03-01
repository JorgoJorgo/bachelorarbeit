import matplotlib.pyplot as plt
import csv
import numpy as np
import math
#liest text datei
#parse csv zu array
#plott

##################################################################################################################
#Hier müssen die algorithm1 , algorithm2 , TitleAlgo1 . TitleAlgo1 NACH JEDEM BEENDETEM PLOT geändert werden


# MultipleTrees FR2 , OneTree FR2
# Parallel and Inverse FR2 , SquareOne FR2
# MultipleTrees Mod Parallel , MultipleTrees Invert Order Mod FR2
# MultipleTrees Random Order Mod FR2s

#FÜR die neuen Real Topos :
#count = 8
# algorithm1 = 'baseMT'
# algorithm2 = 'baseOT'
# TitleAlgo1 = " MultipleTrees"
# TitleAlgo2 = " OneTree"

# algorithm1 = 'sq1'
# algorithm2 = 'parallelInverse'
# TitleAlgo1 = " SquareOne"
# TitleAlgo2 = " Parallel and Inverse"

# algorithm1 = 'mtmp'
# algorithm2 = 'mtiom'
# TitleAlgo1 = " MultipleTrees Mod Parallel"
# TitleAlgo2 = " MultipleTrees Invert Order Mod"

# algorithm1 = 'mtrom'
# TitleAlgo1 = " MultipleTrees Random Order Mod"




#FÜR die Computation Time
algorithm1 = "mt"
algorithm2 = "otbM"
TitleAlgo1 = " MultipleTrees"
TitleAlgo2 = " One Tree Breite Mod"

# algorithm1 = "mtmB"
# algorithm2 = "mtmA"
# TitleAlgo1 = " MultipleTrees Mod Breite"
# TitleAlgo2 = " MultipleTrees Mod Anzahl"

# algorithm1 = "mtmR"
# algorithm2 = "mtmP"
# TitleAlgo1 = " MultipleTrees Mod Reihenfolge"
# TitleAlgo2 = " MultipleTrees Mod Parallel"

alg1_hops = []
alg2_hops = []
alg1_resilience = [1,1]
alg2_resilience = [1,1]
alg1_real_resilience = [1,1]
alg2_real_resilience = [1,1]
alg1_time = []
alg2_time = []

for i in range(2,11):

    number = str(i)

    
    #filepath = "NewRealTopos/benchmark-zoo-RealTopos-FR"+number+"-5.txt"
    filepath = "ComputationTimeExperiments/benchmark-regular-all-multiple-trees-50-"+number+".txt"
    FR = '_fr'+number

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
        # algorithm2 + "_fr11": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        # algorithm2 + "_fr12": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},


        algorithm1 + "_fr2": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 +"_fr3": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr4": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr5": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr6": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr7": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 +"_fr8": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr9": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr10": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        # algorithm1 + "_fr11": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        # algorithm1 + "_fr12": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
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

        # if result['algorithm'] == TitleAlgo1 +" FR11":
        #     accumulated[algorithm1 + '_fr11']['count'] = 1 + accumulated[algorithm1 + '_fr11']['count']
        #     accumulated[algorithm1 + '_fr11']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr11']['stretch']
        #     accumulated[algorithm1 + '_fr11']['load'] = result['load'] + accumulated[algorithm1 + '_fr11']['load']
        #     accumulated[algorithm1 + '_fr11']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr11']['hops']
        #     accumulated[algorithm1 + '_fr11']['success'] = result['success'] + accumulated[algorithm1 + '_fr11']['success']
        #     accumulated[algorithm1 + '_fr11']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr11']['routing_computation_time']
        #     accumulated[algorithm1 + '_fr11']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr11']['pre_computation_time']


        # if result['algorithm'] == TitleAlgo1 +" FR12":
        #     accumulated[algorithm1 + '_fr12']['count'] = 1 + accumulated[algorithm1 + '_fr12']['count']
        #     accumulated[algorithm1 + '_fr12']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr12']['stretch']
        #     accumulated[algorithm1 + '_fr12']['load'] = result['load'] + accumulated[algorithm1 + '_fr12']['load']
        #     accumulated[algorithm1 + '_fr12']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr12']['hops']
        #     accumulated[algorithm1 + '_fr12']['success'] = result['success'] + accumulated[algorithm1 + '_fr12']['success']
        #     accumulated[algorithm1 + '_fr12']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr12']['routing_computation_time']
        #     accumulated[algorithm1 + '_fr12']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr12']['pre_computation_time']


        
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

        # if result['algorithm'] == TitleAlgo2 +" FR11":
        #     accumulated[algorithm2 + '_fr11']['count'] = 1 + accumulated[algorithm2 + '_fr11']['count']
        #     accumulated[algorithm2 + '_fr11']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr11']['stretch']
        #     accumulated[algorithm2 + '_fr11']['load'] = result['load'] + accumulated[algorithm2 + '_fr11']['load']
        #     accumulated[algorithm2 + '_fr11']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr11']['hops']
        #     accumulated[algorithm2 + '_fr11']['success'] = result['success'] + accumulated[algorithm2 + '_fr11']['success']
        #     accumulated[algorithm2 + '_fr11']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr11']['routing_computation_time']
        #     accumulated[algorithm2 + '_fr11']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr11']['pre_computation_time']
        
        # if result['algorithm'] == TitleAlgo2 +" FR12":
        #     accumulated[algorithm2 + '_fr12']['count'] = 1 + accumulated[algorithm2 + '_fr12']['count']
        #     accumulated[algorithm2 + '_fr12']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr12']['stretch']
        #     accumulated[algorithm2 + '_fr12']['load'] = result['load'] + accumulated[algorithm2 + '_fr12']['load']
        #     accumulated[algorithm2 + '_fr12']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr12']['hops']
        #     accumulated[algorithm2 + '_fr12']['success'] = result['success'] + accumulated[algorithm2 + '_fr12']['success']
        #     accumulated[algorithm2 + '_fr12']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr12']['routing_computation_time']
        #     accumulated[algorithm2 + '_fr12']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr12']['pre_computation_time']

    #ÄNDERN
    print(filepath)

    print(" ")
    print(algorithm1 + " " + FR +  " Ergebnisse : " )
    print("Count : ", accumulated[algorithm1 + FR]['count'])
    print("Gesamte Resilienz : " , algorithm1 , accumulated[algorithm1 + FR ]['success'] )
    print("Durchschnittliche Resilienz : ", accumulated[algorithm1 + FR ]['success'] /  accumulated[algorithm1 + FR ]['count'] )
    print("Durchschnittliche Hops : ", accumulated[algorithm1 + FR ]['hops'] /  accumulated[algorithm1 + FR ]['count'] )
    print("Durchschnittliche Zeit : ", (accumulated[algorithm1 + FR ]['pre_computation_time']+accumulated[algorithm1 + FR ]['routing_computation_time'])  /  accumulated[algorithm1 + FR]['count'])
    print(" ")
    print(algorithm2 +   " " + FR +   " Ergebnisse : " )
    print("Count : ", accumulated[algorithm2 + FR]['count'])
    print("Gesamte Resilienz : " , algorithm2 , accumulated[algorithm2 + FR ]['success'] )
    print("Durchschnittliche Resilienz : ", accumulated[algorithm2 + FR ]['success'] /  accumulated[algorithm2 + FR]['count'] )
    print("Durchschnittliche Hops : ", accumulated[algorithm2 + FR ]['hops'] /  accumulated[algorithm2 + FR ]['count'] )
    print("Durchschnittliche Zeit : ", (accumulated[algorithm2 + FR ]['pre_computation_time']+accumulated[algorithm2 + FR ]['routing_computation_time'])  /  accumulated[algorithm2 + FR ]['count'])
    print("------------------------------------------------------------------")
    print("Durchschnittliche Precomp Zeit : ", (accumulated[algorithm1 + FR ]['pre_computation_time'])  /  accumulated[algorithm1 + FR]['count'])
    print("Durchschnittliche Precomp Zeit : ", (accumulated[algorithm2 + FR ]['pre_computation_time'])  /  accumulated[algorithm2 + FR ]['count'])
    print("------------------------------------------------------------------")
    print(algorithm1 ,  " " , FR)
    print(algorithm2 ,  " " , FR)
    print("------------------------------------------------------------------")


    print("Durchschnittliche Resilienz : " , accumulated[algorithm1 + FR ]['success'] /  accumulated[algorithm1 + FR ]['count'] )
    print("Durchschnittliche Resilienz : " , accumulated[algorithm2 + FR ]['success'] /  accumulated[algorithm2 + FR]['count'] )
    alg1_resilience.append(accumulated[algorithm1 + FR ]['success'] /  accumulated[algorithm1 + FR ]['count'])
    alg2_resilience.append(accumulated[algorithm2 + FR ]['success'] /  accumulated[algorithm2 + FR ]['count'])

    alg1_real_resilience.append(accumulated[algorithm1 + FR ]['success'] /  count)
    alg2_real_resilience.append(accumulated[algorithm2 + FR ]['success'] /  count)
    print(" ")


    print("Durchschnittliche Hops : ", accumulated[algorithm1 + FR ]['hops'] /  accumulated[algorithm1 + FR ]['count'] )
    print("Durchschnittliche Hops : ", accumulated[algorithm2 + FR ]['hops'] /  accumulated[algorithm2 + FR ]['count'] )
    alg1_hops.append(accumulated[algorithm1 + FR ]['hops'] /  accumulated[algorithm1 + FR ]['count'])
    alg2_hops.append(accumulated[algorithm2 + FR ]['hops'] /  accumulated[algorithm2 + FR ]['count'])


    print(" ")
    print("Durchschnittliche Zeit : ", (accumulated[algorithm1 + FR ]['pre_computation_time']+accumulated[algorithm1 + FR ]['routing_computation_time'])  /  accumulated[algorithm1 + FR]['count'])
    print("Durchschnittliche Zeit : ", (accumulated[algorithm2 + FR ]['pre_computation_time']+accumulated[algorithm2 + FR ]['routing_computation_time'])  /  accumulated[algorithm2 + FR ]['count'])
    alg1_time.append((accumulated[algorithm1 + FR ]['pre_computation_time']+accumulated[algorithm1 + FR ]['routing_computation_time'])  /  accumulated[algorithm1 + FR]['count'])
    alg2_time.append((accumulated[algorithm2 + FR ]['pre_computation_time']+accumulated[algorithm2 + FR ]['routing_computation_time'])  /  accumulated[algorithm2 + FR ]['count'])
    print(" ")

    ###Graphen ####
    print(" ")
    #input("CLICK FOR NEXT FR ...")
    print("------------------------------------------------------------------")
#endfor
print(algorithm1 + "_Resilienz = ", alg1_resilience)
print(algorithm2 + "_Resilienz = ", alg2_resilience)
print(" ")
print(algorithm1 + "_mit_infs_Resilienz = ", alg1_real_resilience)
print(algorithm2 + "_mit_infs_Resilienz = ", alg2_real_resilience)
print(" ")
print(algorithm1 + "_Hops = ", alg1_hops)
print(algorithm2 + "_Hops = ", alg2_hops)
print(" ")
print(algorithm1 + "_hops = " + alg1_hops)
print(algorithm2 + "_hops = " + alg2_hops)
# sum1 = 0
# for number in alg1_resilience:
#     sum1 = sum1 + number

# sum2 = 0
# for number in alg2_resilience:
#     sum2 = sum2 + number

# print("Summe von Resilienz " , algorithm1 , " : ", sum1)
# print("Summe von Resilienz " , algorithm1 , " : ", sum1)




plotfig = False
if (plotfig):
    print(" ")
    ##############################'ONETREE VS MULTIPLETREES VS SQUARE ONE######################################################
    # plt.figure()
    # #PLOT1
    # X = [0,1,2,3,4,5,6,7,8,9,10]
    # # Assign variables to the y axis part of the curve
    # y = [1,1,1,1,1, 0.925 , 0.85 ,  0.725 , 0.575 , 0.42 , 0.225] #OneTree
    # z = [1,1,1,1,1, 0.925 , 0.874 , 0.775 , 0.575 , 0.45 , 0.25] #MultipleTrees
    # a = [1,1,1,1,1, 0.924 , 0.75,   0.65,   0.525,  0.35,  0.19] # SquareOne
    # # Plotting both the curves simultaneously
    # plt.subplot(221)
    # plt.plot(X, y, color='r', label='OneTree')
    # plt.plot(X, z, color='g', label='MultipleTrees')
    # plt.plot(X, a, color='b', label='SquareOne')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend()

    # #PLOT2
    # X = [0,1,2,3,4,5,6,7,8,9,10]
    # y = [3.5 , 3.5 , 3.5 , 3.875 , 4.375 , 5.75 , 8.625 , 6.625 , 8.125 , 7.1 , 4] #OneTree
    # z = [3.5 , 3.5 , 3.5 , 3.875 , 4.375 , 5.75 , 10.125 , 11.875 , 7.75 , 8.7 , 7] #multipletrees
    # a = [3.37,3.37,3.375, 3.625, 3.75, 5.875, 5.875, 5.625, 5.25, 5.571428571428571, 3.5] #squareone
    # # Plotting both the curves simultaneously
    # plt.subplot(222)
    # plt.plot(X, y, color='r', label='OneTree')
    # plt.plot(X, z, color='g', label='MultipleTrees')
    # plt.plot(X, a, color='b', label='SquareOne')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Durschn. Hops")
    # plt.title("Durschn. Hops, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend()

    # # To load the display window
    # plt.show()

    ################################### ONETREE VS ONETREE BREITE MOD #######################################################

    # plt.figure()
    # #PLOT1
    # X = [0,1,2,3,4,5,6,7,8,9,10]
    # # Assign variables to the y axis part of the curve
    # y = [1,1,1,1,1,0.92,0.85,0.725,0.575,0.4285,0.3] #OneTree
    # z = [1,1,1,1,1,0.92,0.8,0.725,0.575,0.457,0.3] #MultipleTrees
    # # Plotting both the curves simultaneously
    # plt.subplot(221)
    # plt.plot(X, y, color='r', label='OneTree')
    # plt.plot(X, z, color='g', label='OneTree Breite Mod')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend()

    # #PLOT2 
    # X = [0,1,2,3,4,5,6,7,8,9,10]
    # y = [3.5,3.5,3.5,2.875,4.375,5.75,8.6,6.625,8.125,7.1,4.0] #OneTree
    # z = [3.5,3.5,3.5,2.875,4.375,5.75,6.6,6.625,8.126,8.2,4.0]
    # # Plotting both the curves simultaneously
    # plt.subplot(222)
    # plt.plot(X, y, color='r', label='OneTree')
    # plt.plot(X, z, color='g', label='OneTree Breite Mod')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Durschn. Hops")
    # plt.title("Durschn. Hops, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend()

    
    # #PLOT3
    # X = [0,1,2,3,4,5,6,7,8,9,10]
    # y = [1.56,1.56,1.56,1.6,1.55,1.53,1.53,1.53,1.53,1.5,1.56] #OneTree
    # z = [2.3,2.3,2.3,2.6,2.28,2.26,2.25,2.25,2.27,2.27,2.3]
    # a = [1.56, 1.56 , 1.56 , 1.566 , 1.544 , 1.55 , 1.53, 1.53, 1.52 , 1.53 , 1.56  ]
    # b = [2.29,2.29 , 2.29 , 2.2955 , 2.27 , 2.28 , 2.269 , 2.254, 2.251  , 2.27 , 2.3]
    # # Plotting both the curves simultaneously
    # plt.subplot(223)

    # plt.plot(X, y, color='r', label='OneTree Gesamt')
    # plt.plot(X, a, '--', color='r', label='OneTree Pre-Comp.')
    # plt.plot(X, z, color='g', label='OneTree Breite Mod Gesamt')
    # plt.plot(X, b, '--', color='g', label='OneTree Mod Pre-Comp.')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Zeit in s")
    # plt.title("Durchschn. Ausführungszeit, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(bbox_to_anchor=(1.05, 1),loc='upper left', borderaxespad=0.)
    # # # To load the display window
    # plt.show()
    ################################### MULTIPLETREES VS MULTIPLETREES BREITE MOD #######################################################
    
    # plt.figure()
    # #PLOT1
    # X = [0,1,2,3,4,5,6,7,8,9,10]
    # # Assign variables to the y axis part of the curve

    # y = [1,1,
    # 1,1,1,0.89,0.79,0.65,0.45,0.35,0.15]

    # z = [1,1,
    # 1,1,0.975,0.92,0.59,0.45,0.4,0.15,0.05] 

    # # Plotting both the curves simultaneously
    # plt.subplot(221)
    # plt.plot(X, y, color='r', label='MultipleTrees')
    # plt.plot(X, z, color='g', label='MultipleTrees Mod')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # #PLOT2 
    # X = [2,3,4,5,6,7,8,9,10]

    # y = [7.25,7.375,9.5,10.87,14.25,11.62,12.37,12,9] 

    # z = [11,15.375,21.625,20.62,19.5,16,12.85,11,6]

    # # Plotting both the curves simultaneously
    # plt.subplot(222)
    # plt.plot(X, y, color='r', label='MultipleTrees')
    # plt.plot(X, z, color='g', label='MultipleTrees Mod')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Durschn. Hops")
    # plt.title("Durschn. Hops, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")
    # #plt.legend()

    
    # # # To load the display window
    # plt.show()

    ########################## MULTIPLETREES VS MULTIPLETREES ANZAHL MOD #################################################

    # plt.figure()
    # #PLOT1
    # X = [0,1,2,3,4,5,6,7,8,9,10]
    # # Assign variables to the y axis part of the curve

    # y = [1,1,
    # 1,1,1,0.89,0.79,0.65,0.45,0.35,0.15]

    # z = [1,1,
    # 1,1,0.92,0.89,0.625,0.55,0.3,0.325,0.125] 

    # # Plotting both the curves simultaneously
    # plt.subplot(221)
    # plt.plot(X, y, color='r', label='MultipleTrees')
    # plt.plot(X, z, color='g', label='MultipleTrees Mod')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # # # #PLOT2 
    # X = [2,3,4,5,6,7,8,9,10]

    # y = [7.25,7.375,9.5,10.87,14.25,11.62,12.37,12,9] 

    # z = [6.125,7.6,9.625,11,12,10.75,6.8,12.8,6.3]

    # # Plotting both the curves simultaneously
    # plt.subplot(222)
    # plt.plot(X, y, color='r', label='MultipleTrees')
    # plt.plot(X, z, color='g', label='MultipleTrees Mod')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Durschn. Hops")
    # plt.title("Durschn. Hops, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")
    # #plt.legend()

    
    # # To load the display window
    
    # plt.show()

    ########################## MULTIPLETREES VS MULTIPLETREES PARALLEL MOD #################################################

    # plt.figure()
    # #PLOT1
    # X = [0,1,2,3,4,5,6,7,8,9,10]
    # # Assign variables to the y axis part of the curve

    # y = [1,1,
    # 1,1,1,0.89,0.79,0.65,0.45,0.35,0.24]

    # z = [1,1,
    # 1,1,1,1,0.875,0.75,0.525,0.275,0.24] 

    # # Plotting both the curves simultaneously
    # plt.subplot(221)
    # plt.plot(X, y, color='r', label='MultipleTrees')
    # plt.plot(X, z, color='g', label='MultipleTrees Mod')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # # # #PLOT2 
    # X = [2,3,4,5,6,7,8,9,10]

    # y = [7.25,7.375,9.5,10.87,14.25,11.62,12.37,12,9] #muss man für MultipleTrees nicht ändern da es sich für gleiche Graphen identisch verhält

    # z = [8.75,8.8,11.125,14.37,14,18.5,12.25,5.4,6.6]

    # # Plotting both the curves simultaneously
    # plt.subplot(222)
    # plt.plot(X, y, color='r', label='MultipleTrees')
    # plt.plot(X, z, color='g', label='MultipleTrees Mod')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Durschn. Hops")
    # plt.title("Durschn. Hops, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")
    # #plt.legend()
    # plt.show()

    ############################################### MULTIPLETREES vs MULTIPLETREES RANDOM ORDER MOD ##################################

    # plt.figure()
    # #PLOT1
    # X = [0,1,2,3,4,5,6,7,8,9,10]
    # # Assign variables to the y axis part of the curve

    # y = [1,1,
    # 1,1, 1 , 0.899 , 0.79 , 0.65 ,  0.45, 0.39 , 0.17]

    # z = [1,1,
    # 1,1, 1 , 0.975 ,  0.8 , 0.675 , 0.45 , 0.37 ,0.14] 

    # # Plotting both the curves simultaneously
    # plt.subplot(221)
    # plt.plot(X, y, color='r', label='MultipleTrees')
    # plt.plot(X, z, color='g', label='MultipleTrees Mod')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # # # #PLOT2 
    # X = [2,3,4,5,6,7,8,9,10]

    # y = [7.25, 7.375, 9.5 , 10.875 , 14.25 , 11.625 ,  12.375, 12, 9] #muss man für MultipleTrees nicht ändern da es sich für gleiche Graphen identisch verhält

    # z = [7.625, 7.25, 10.375 ,  19.75 , 21.0 ,  18.25 ,  11.375 , 10.16, 4]

    # # Plotting both the curves simultaneously
    # plt.subplot(222)
    # plt.plot(X, y, color='r', label='MultipleTrees')
    # plt.plot(X, z, color='g', label='MultipleTrees Mod')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Durschn. Hops")
    # plt.title("Durschn. Hops, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")
    # #plt.legend()
    # plt.show()


    ############################################### MULTIPLETREES vs MULTIPLETREES INVERSE ORDER MOD ##################################

    # plt.figure()
    # #PLOT1
    # X = [0,1,2,3,4,5,6,7,8,9,10]
    # # Assign variables to the y axis part of the curve

    # y = [1, 1, 1.0, 1.0, 1.0, 0.8999999999999999, 0.7999999999999999, 0.65, 0.45000000000000007, 0.35, 0.15]

    # z = [1, 1, 1.0, 1.0, 1.0, 0.95, 0.925, 0.925, 0.6749999999999999, 0.475, 0.24000000000000005]

    # # Plotting both the curves simultaneously
    # plt.subplot(221)
    # plt.plot(X, y, color='r', label='MultipleTrees')
    # plt.plot(X, z, color='g', label='MultipleTrees Mod')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # # # #PLOT2 
    # X = [2,3,4,5,6,7,8,9,10]

    # y = alg1_hops

    # z = alg2_hops

    # # Plotting both the curves simultaneously
    # plt.subplot(222)
    # plt.plot(X, y, color='r', label='MultipleTrees')
    # plt.plot(X, z, color='g', label='MultipleTrees Mod')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Durschn. Hops")
    # plt.title("Durschn. Hops, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")
    # #plt.legend()
    # plt.show()

    ################################# KOMBINATIONEN ####################################################################

    # plt.figure()
    # #PLOT1
    # X = [4,5,6,7,8,9,10]
    # # Assign variables to the y axis part of the curve

    # # y = [1, 1, 1, 1, 1, 0.92,  0.85,  0.725, 0.575,  0.375, 0.22] # OneTree

    # # z = [1, 1, 1, 1, 1, 0.89,  0.79,  0.65,  0.450,  0.35,  0.15] # MultipleTrees

    # # b = [1, 1, 1, 1, 1, 0.975, 0.925, 0.825, 0.575, 0.3, 0.15] # p + i

    # # c = [1, 1, 1, 1, 0.925, 0.725, 0.525, 0.35, 0.2, 0.125, 0.025] # b + i

    # # d = [1, 1, 1, 1, 1, 0.975, 0.85, 0.7749999999999999, 0.5, 0.325, 0.125] # n + r

    # y = [ 1, 0.92,  0.85,  0.725, 0.575,  0.375, 0.22] # OneTree

    # z = [1,  0.925 ,0.874 ,0.775 ,0.575 , 0.45 , 0.25] #MultipleTrees

    # b = [ 1,  0.975, 0.925, 0.825, 0.575, 0.3, 0.15] # p + i

    # c = [ 0.925, 0.725, 0.525, 0.35, 0.2, 0.125, 0.025] # b + i

    # d = [ 1, 0.975, 0.85, 0.7749999999999999, 0.5, 0.325, 0.125] # n + r

    # # Plotting both the curves simultaneously
    # plt.subplot(221)
    # plt.plot(X, y, '--', color='r', label='OneTree')
    # plt.plot(X, z, '--', color='g', label='MultipleTrees')
    # plt.plot(X, b, color='c', label='Parallel & Invers')
    # plt.plot(X, c, color='m', label='Breite & Invers')
    # plt.plot(X, d, color='y', label='Anzahl & Randomisiert')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # plt.show()

    #################### KOMBINATIONEN VS ihre OG Algos #################################


    # plt.figure()
    # #PLOT1
    # X = [4,5,6,7,8,9,10]
    # # Assign variables to the y axis part of the curve

    # #RESILIENZ
    # b = [ 1,  0.975, 0.925, 0.825, 0.575, 0.3, 0.15] # p + i

    # c = [ 0.925, 0.725, 0.525, 0.35, 0.2, 0.125, 0.025] # b + i

    # d = [ 1, 0.975, 0.85, 0.7749999999999999, 0.5, 0.325, 0.125] # n + r

    # z = [1.0, 0.95, 0.925, 0.925, 0.6749999999999999, 0.475, 0.24000000000000005]#inverse order

    # a = [1 , 0.975 ,  0.8 , 0.675 , 0.45 , 0.37 ,0.14] #random order

    # e = [0.975,0.92,0.59,0.45,0.4,0.15,0.05] #breite Mod

    # f = [1,1,0.875,0.75,0.525,0.275,0.24] #parallel mod

    # g = [0.92,0.89,0.625,0.55,0.3,0.325,0.125] #anzahl mod

    # # Plotting both the curves simultaneously
    # plt.subplot(221)
    # plt.plot(X, f, '--', color='r', label='Parallel')
    # plt.plot(X, z, '--', color='c', label='Inverse Order')
    # plt.plot(X, b, color='c', label='Parallel & Invers')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # plt.subplot(222)

    # plt.plot(X, z, '--', color='c', label='Inverse Order')
    # plt.plot(X, e, '--',color='m', label='Breite')
    # plt.plot(X, c, color='m', label='Breite & Invers')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # plt.subplot(223)
    # plt.plot(X, a,'--', color='y', label='Randomisiert')
    # plt.plot(X, g,'--', color='b', label='Anzahl')
    # plt.plot(X, d, color='y', label='Anzahl & Randomisiert')
    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # plt.show()

    # #HOPS
    # X = [2,3,4,5,6,7,8,9,10]
    # plt.subplot(221)
    # z = [8.75,8.8,11.125,14.37,14,18.5,12.25,5.4,6.6] #parallel 
    # u = [7.5, 9.625, 14.75, 16.25, 19.75, 15.125, 11.5, 10.625, 8.6] #inverse
    # l = [6.625, 9.125, 9.25, 9.5, 21.0, 14.625, 10.25, 6.428571428571429, 4.6] #parallel & inverse
    
    # plt.plot(X, z, '--', color='r', label='Parallel')
    # plt.plot(X, u, '--', color='c', label='Inverse Order')
    # plt.plot(X, l, color='c', label='Parallel & Invers')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Hops")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # plt.subplot(222)

    # p = [11,15.375,21.625,20.62,19.5,16,12.85,11,6] #breite mod
    # y =[10.25, 12.625, 14.25, 14.375, 15.125, 8.0, 3.0, 3.4, 1.0] #breite & inverse

    # plt.plot(X, u, '--', color='c', label='Inverse Order')
    # plt.plot(X, p, '--',color='m', label='Breite')
    # plt.plot(X, y, color='m', label='Breite & Invers')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Hops")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # plt.subplot(223)

    # s = [7.625, 7.25, 10.375 ,  19.75 , 21.0 ,  18.25 ,  11.375 , 10.16, 4]# random
    # c = [6.125,7.6,9.625,11,12,10.75,6.8,12.8,6.3]#anzahl
    # n = [6.875, 7.125, 10.5, 11.25, 17.625, 15.125, 16.0, 12.285714285714286, 6.333333333333333] #random & anzahl

    # plt.plot(X, s,'--', color='y', label='Randomisiert')
    # plt.plot(X, c,'--', color='b', label='Anzahl')
    # plt.plot(X, n, color='y', label='Anzahl & Randomisiert')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Hops")
    # plt.title("Resilienz, n = 40 , k = 5 ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")
    # plt.show()

    ################################ REAL TOPOLOGIES #########################################################
    
    plt.figure()

    X = [2,3,4,5,6,7,8,9,10]
    
    multipletre_trees_Resilienz =            [1, 1, 0.8693333333333332, 0.808333333333333, 0.7449275362318837, 0.7014925373134325, 0.6262295081967211, 0.5962962962962963, 0.5615384615384618, 0.5173913043478262, 0.47804878048780475]
    multipletre_trees_mit_infs_Resilienz =   [1, 1, 0.8693333333333332, 0.7759999999999997, 0.685333333333333, 0.6266666666666664, 0.5093333333333332, 0.42933333333333334, 0.3893333333333335, 0.3173333333333334, 0.26133333333333325]  
    one_tree_Resilienz =                     [1, 1, 0.8773333333333331, 0.833333333333333, 0.7599999999999997, 0.7130434782608694, 0.6338461538461537, 0.606896551724138, 0.5535714285714286, 0.5058823529411764, 0.47234042553191474]
    one_tree_mit_infs_Resilienz =            [1, 1, 0.8773333333333331, 0.7999999999999997, 0.709333333333333, 0.6559999999999998, 0.5493333333333332, 0.4693333333333334, 0.4133333333333334, 0.344, 0.2959999999999999]
    parallel_inverse_Resilienz =             [1, 1, 0.8639999999999998, 0.8111111111111108, 0.742028985507246, 0.6941176470588232, 0.6196721311475408, 0.5890909090909092, 0.5615384615384618, 0.5063829787234043, 0.4558139534883719]
    parallel_inverse_mit_infs_Resilienz =    [1, 1, 0.8639999999999998, 0.7786666666666664, 0.6826666666666663, 0.629333333333333, 0.5039999999999999, 0.43200000000000005, 0.3893333333333335, 0.31733333333333336, 0.2613333333333332]
    square_one_Resilienz =                   [1, 1, 0.8506666666666661, 0.8027777777777774, 0.7428571428571425, 0.6898550724637679, 0.6, 0.5862068965517241, 0.5418181818181819, 0.4959999999999999, 0.46666666666666656]
    square_one_mit_infs_Resilienz =          [1, 1, 0.8506666666666661, 0.7706666666666663, 0.693333333333333, 0.6346666666666664, 0.512, 0.4533333333333333, 0.39733333333333337, 0.3306666666666666, 0.27999999999999997]
    parallel_Resilienz =                     [1, 1, 0.8746666666666666, 0.8194444444444441, 0.7428571428571424, 0.6898550724637678, 0.6129032258064515, 0.585714285714286, 0.5481481481481483, 0.49795918367346936, 0.4651162790697672]
    invert_Resilienz =                       [1, 1, 0.8666666666666665, 0.8055555555555552, 0.7441176470588231, 0.6823529411764703, 0.6098360655737705, 0.5709090909090909, 0.5461538461538462, 0.52, 0.4829268292682925]
    parallel_mit_infs_Resilienz =            [1, 1, 0.8746666666666666, 0.7866666666666663, 0.6933333333333329, 0.6346666666666663, 0.5066666666666666, 0.43733333333333346, 0.3946666666666668, 0.3253333333333333, 0.26666666666666655]
    invert_mit_infs_Resilienz =              [1, 1, 0.8666666666666665, 0.7733333333333331, 0.6746666666666663, 0.6186666666666664, 0.49599999999999994, 0.4186666666666667, 0.37866666666666676, 0.312, 0.2639999999999999]  
    random_Resilienz =                       [1, 1, 0.8666666666666665, 0.8028169014084504, 0.7470588235294114, 0.6895522388059697, 0.6133333333333333, 0.6000000000000001, 0.5647058823529414, 0.5227272727272727, 0.5025641025641024]
    random_mit_infs_Resilienz =              [1, 1, 0.8666666666666665, 0.7599999999999997, 0.677333333333333, 0.6159999999999997, 0.49066666666666664, 0.42400000000000004, 0.3840000000000002, 0.30666666666666664, 0.26133333333333325]
    
    
    sq1_mit_infs_Resilienz =  [1, 1, 0.975, 0.9249999999999999, 0.7250000000000001, 0.675, 0.65, 0.65, 0.625, 0.525, 0.975]
    parallelInverse_mit_infs_Resilienz =  [1, 1, 0.975, 0.95, 0.775, 0.75, 0.75, 0.7250000000000001, 0.7, 0.55, 0.975]


    plt.subplot(221)

    #print("X length : ", len(X))
    #print("multtrees length : " , len(multipletre_trees_mit_infs_Resilienz))
    #print("multtrees cut length : " , len(multipletre_trees_mit_infs_Resilienz[2:11]))
    multTreesCut = multipletre_trees_mit_infs_Resilienz[2:11]
    #print(multTreesCut)

    #erster plot
    #plt.plot(X, multTreesCut, '--', color='r', label='MultipleTrees')
    #plt.plot(X, one_tree_mit_infs_Resilienz[2:11], '--', color='g', label='OneTree')
    #plt.plot(X, square_one_mit_infs_Resilienz[2:11],'--' , color='c', label='SquareOne')
    #plt.plot(X, parallel_inverse_mit_infs_Resilienz[2:11], color='m', label='Parallel & Invers')


    #zweiter plot
    #plt.plot(X, parallel_mit_infs_Resilienz[2:11], color='y', label='Parallel')
    #plt.plot(X, invert_mit_infs_Resilienz[2:11],'--', color='m', label='Invers')
    #plt.plot(X, random_mit_infs_Resilienz[2:11], color='b', label='Randomisiert')

    # Naming the x-axis, y-axis and the whole graph
    #plt.xlabel("Failure Rate")
    #plt.ylabel("Resilienz")
    #plt.title("Resilienz, reale Topologien ")
    # Adding legend, which helps us recognize the curve according to it's color
    #plt.legend(fontsize="x-small")

    #plt.subplot(222)

    Y = [2,3,4,5,6,7,8,9,10]

    parallel_Hops =                          [16.36, 15.347222222222221, 16.12857142857143, 14.695652173913043, 12.596774193548388, 12.25, 11.907407407407407, 10.714285714285714, 9.511627906976743]
    invert_Hops =                            [11.973333333333333, 12.027777777777779, 12.338235294117647, 11.411764705882353, 9.80327868852459, 10.036363636363637, 9.153846153846153, 8.377777777777778, 7.7073170731707314]
    parallel_inverse_Hops =                  [11.133333333333333, 10.75, 11.753623188405797, 10.691176470588236, 9.639344262295081, 9.618181818181819, 9.115384615384615, 8.0, 7.093023255813954]
    square_one_Hops =                        [9.666666666666666, 9.402777777777779, 9.814285714285715, 9.043478260869565, 7.796875, 7.5, 6.9818181818181815, 6.48, 5.822222222222222]
    multipletre_trees_Hops =                 [16.253333333333334, 15.722222222222221, 16.92753623188406, 15.149253731343284, 13.163934426229508, 13.074074074074074, 12.884615384615385, 10.978260869565217, 9.292682926829269]
    one_tree_Hops =                          [10.626666666666667, 10.555555555555555, 10.542857142857143, 10.53623188405797, 9.338461538461539, 8.758620689655173, 7.732142857142857, 7.294117647058823, 7.212765957446808]
    random_Hops =                            [14.333333333333334, 13.47887323943662, 14.485294117647058, 12.701492537313433, 11.4, 11.622641509433961, 10.666666666666666, 10.090909090909092, 9.179487179487179]

    plt.plot(Y, multipletre_trees_Hops, '--', color='r', label='MultipleTrees')
    plt.plot(Y,one_tree_Hops, '--', color='g', label='OneTree')
    plt.plot(Y, square_one_Hops,'--' , color='c', label='SquareOne')
    plt.plot(Y, parallel_inverse_Hops, color='m', label='Parallel & Invers')
    plt.plot(Y, parallel_Hops, color='y', label='Parallel')
    plt.plot(Y, invert_Hops,'--', color='m', label='Invers')
    plt.plot(Y, random_Hops, color='b', label='Randomisiert')

    # Naming the x-axis, y-axis and the whole graph
    plt.xlabel("Failure Rate")
    plt.ylabel("Hops")
    plt.title("Hop-Anzahl, reale Topologien ")
    # Adding legend, which helps us recognize the curve according to it's color
    plt.legend(fontsize="x-small")

    plt.show()

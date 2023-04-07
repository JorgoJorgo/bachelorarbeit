import matplotlib.pyplot as plt
import csv
import numpy as np
import math
#liest text datei
#parse csv zu array
#plott

##################################################################################################################
#Hier müssen die algorithm1 , algorithm2 , TitleAlgo1 . TitleAlgo1 NACH JEDEM BEENDETEM PLOT geändert werden




#FÜR die neuen Real Topos :
#count = 8
# algorithm1 = 'baseMT'
#algorithm2 = 'baseOT'
# TitleAlgo1 = " MultipleTrees"
#TitleAlgo2 = " OneTree"

#algorithm1 = 'sq1'
#algorithm2 = 'parallelInverse'
#TitleAlgo1 = " SquareOne"
#TitleAlgo2 = " Parallel and Inverse"

# algorithm1 = 'mtmp'
# algorithm2 = 'mtiom'
# TitleAlgo1 = " MultipleTrees Mod Parallel"
# TitleAlgo2 = " MultipleTrees Invert Order Mod"

#algorithm1 = 'mtrom'
#TitleAlgo1 = " MultipleTrees Random Order Mod"

#count = 5


#FÜR die Computation Time
#count = 8
# algorithm1 = "mt"
# algorithm2 = "otbM"
# TitleAlgo1 = " MultipleTrees"
# TitleAlgo2 = " One Tree Breite Mod"

# algorithm1 = "mtmB"
# algorithm2 = "mtmA"
# TitleAlgo1 = " MultipleTrees Mod Breite"
# TitleAlgo2 = " MultipleTrees Mod Anzahl"

# algorithm1 = "mtmR"
# algorithm2 = "mtmP"
# TitleAlgo1 = " MultipleTrees Mod Reihenfolge"
# TitleAlgo2 = " MultipleTrees Mod Parallel"

#FÜR MT vs MTP vs MTRecycle
# count= 5
# algorithm1 = 'baseMT'
# TitleAlgo1 = " MultipleTrees"
# algorithm2 = "mtmP"
# TitleAlgo2 = " MultipleTrees Mod Parallel"
#algorithm1 = "MTRecycle"
#TitleAlgo1 = " MultipleTrees Recycle Mod"

# FÜR MT vs MTP
# algorithm1 = 'baseMT'
# TitleAlgo1 = " MultipleTrees"
# algorithm2 = "mtmP"
# TitleAlgo2 = " MultipleTrees Mod Parallel"
# count = 8 





#FÜR OT vs OTInverse
# count = 8
# #algorithm1 = 'baseMT'
# #TitleAlgo1 = " MultipleTrees"
# algorithm1 = 'baseOT'
# TitleAlgo1 = " OneTree"
# algorithm2 = 'OTInverse'
# TitleAlgo2 = " OneTree Inverse Mod"


# FÜR WEITERFÜHRENDE EXPERIMENTE

count = 7
TitleAlgo1 = " MultipleTrees"
algorithm1 = 'multipleTrees'

TitleAlgo2 = " OneTree Inverse Mod"
algorithm2 = 'oneTreeInvers'

# TitleAlgo1 = " OneTree"
# algorithm1 = 'oneTree'

# TitleAlgo2 = " MultipleTrees Invers"
# algorithm2 = 'multipleTreesInvers'


# TitleAlgo1 = " SquareOne"
# algorithm1 = 'squareOne'

# TitleAlgo2 = " MultipleTrees Parallel Invers"
# algorithm2 = ' multipleTreesParallelInvers'


alg1_hops = []
alg2_hops = []
alg1_resilience = []
alg2_resilience = []
alg1_real_resilience = []
alg2_real_resilience = []
alg1_time = []
alg2_time = []
alg1_counts = []
alg2_counts = []
alg1_sum_hops = []
alg2_sum_hops = []

for i in range(1,25):

    number = str(i)

    
    #filepath = "NewRealTopos/benchmark-zoo-RealTopos-FR"+number+"-5.txt"
    #filepath = "ComputationTimeExperiments/benchmark-regular-all-multiple-trees-50-"+number+".txt"
    #filepath = "results/benchmark-zoo-RealTopos-"+number+"-5.txt"
    #filepath = "results/benchmark-regular-all-multiple-trees-FR"+number+"-40-5.txt"
    #filepath = "ParallelNew/benchmark-regular-all-multiple-trees-FR"+number+"-40-5.txt"
    #filepath = "OneTreeInverseNew/benchmark-regular-inverseOneTree-FR"+number+"-40-5.txt"
    #filepath = "OneTreeInverse/benchmark-regular-inverseOneTree-FR"+number+"-40-5.txt"
    #filepath = "OneTreeInverse/benchmark-regular-inverseOneTree-FR"+number+"-40-5.txt"
    #filepath = "results/benchmark-regular-inverseOneTree-FR"+number+"-40-5.txt"
    #filepath = "WeiterfuhrendeExperimente/PlotMitte_nurInfZeilenRaus/benchmark-regular-weiterfuehrend-FR"+number+"-80-6.txt"
    filepath = "WeiterfuhrendeExperimente/PlotRechts_infWiederholungenRaus/benchmark-regular-weiterfuehrend-FR"+number+"-80-6.txt"
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

        algorithm2 + "_fr1": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr2": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 +"_fr3": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr4": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr5": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr6": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr7": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 +"_fr8": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr9": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr10": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr11": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr12": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},

        algorithm2 + "_fr13": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr14": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr15": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr16": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr17": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr18": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr19": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr20": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr21": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr22": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr23": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm2 + "_fr24": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},


        algorithm1 + "_fr1": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr2": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 +"_fr3": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr4": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr5": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr6": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr7": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 +"_fr8": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr9": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr10": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr11": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr12": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        
        algorithm1 + "_fr13": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr14": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr15": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr16": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr17": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr18": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr19": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr20": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr21": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr22": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr23": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
        algorithm1 + "_fr24": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},

        #... hier muss dann für jeden algorithmus den ich habe ein dict erstellt werden
    }


    # value for  multiple_tree


    for result in data:

        
        # #hier werden jetzt die daten nach algorithmen sortiert
        # if result['algorithm'] == " Multiple Trees FR8":
        #     accumulated['multiple_tree']['count'] = 1 + accumulated['multiple_tree']['count']
        #     accumulated['multiple_tree']['stretch'] = result['stretch'] + accumulated['multiple_tree']['stretch']
        #     accumulated['multiple_tree']['load'] = result['load'] + accumulated['multiple_tree']['load']
        #     accumulated['multiple_tree']['hops'] = result['hops'] + accumulated['multiple_tree']['hops']
        #     accumulated['multiple_tree']['success'] = result['success'] + accumulated['multiple_tree']['success']
        #     accumulated['multiple_tree']['routing_computation_time'] = result['routing_computation_time'] + accumulated['multiple_tree']['routing_computation_time']
        #     accumulated['multiple_tree']['pre_computation_time'] = result['pre_computation_time'] + accumulated['multiple_tree']['pre_computation_time']
    #############################################################################################################################################
        #hier müssen dann für jedes der dicts noch die daten auch aufsummiert werden
        if result['algorithm'] == TitleAlgo1 +" FR1":
            accumulated[algorithm1 + '_fr1']['count'] = 1 + accumulated[algorithm1 + '_fr1']['count']
            accumulated[algorithm1 + '_fr1']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr1']['stretch']
            accumulated[algorithm1 + '_fr1']['load'] = result['load'] + accumulated[algorithm1 + '_fr1']['load']
            accumulated[algorithm1 + '_fr1']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr1']['hops']
            accumulated[algorithm1 + '_fr1']['success'] = result['success'] + accumulated[algorithm1 + '_fr1']['success']
            accumulated[algorithm1 + '_fr1']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr1']['routing_computation_time']
            accumulated[algorithm1 + '_fr1']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr1']['pre_computation_time']
        
        
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

        if result['algorithm'] == TitleAlgo1 +" FR11":
            accumulated[algorithm1 + '_fr11']['count'] = 1 + accumulated[algorithm1 + '_fr11']['count']
            accumulated[algorithm1 + '_fr11']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr11']['stretch']
            accumulated[algorithm1 + '_fr11']['load'] = result['load'] + accumulated[algorithm1 + '_fr11']['load']
            accumulated[algorithm1 + '_fr11']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr11']['hops']
            accumulated[algorithm1 + '_fr11']['success'] = result['success'] + accumulated[algorithm1 + '_fr11']['success']
            accumulated[algorithm1 + '_fr11']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr11']['routing_computation_time']
            accumulated[algorithm1 + '_fr11']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr11']['pre_computation_time']


        if result['algorithm'] == TitleAlgo1 +" FR12":
            accumulated[algorithm1 + '_fr12']['count'] = 1 + accumulated[algorithm1 + '_fr12']['count']
            accumulated[algorithm1 + '_fr12']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr12']['stretch']
            accumulated[algorithm1 + '_fr12']['load'] = result['load'] + accumulated[algorithm1 + '_fr12']['load']
            accumulated[algorithm1 + '_fr12']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr12']['hops']
            accumulated[algorithm1 + '_fr12']['success'] = result['success'] + accumulated[algorithm1 + '_fr12']['success']
            accumulated[algorithm1 + '_fr12']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr12']['routing_computation_time']
            accumulated[algorithm1 + '_fr12']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr12']['pre_computation_time']

        if result['algorithm'] == TitleAlgo1 +" FR13":
            accumulated[algorithm1 + '_fr13']['count'] = 1 + accumulated[algorithm1 + '_fr13']['count']
            accumulated[algorithm1 + '_fr13']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr13']['stretch']
            accumulated[algorithm1 + '_fr13']['load'] = result['load'] + accumulated[algorithm1 + '_fr13']['load']
            accumulated[algorithm1 + '_fr13']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr13']['hops']
            accumulated[algorithm1 + '_fr13']['success'] = result['success'] + accumulated[algorithm1 + '_fr13']['success']
            accumulated[algorithm1 + '_fr13']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr13']['routing_computation_time']
            accumulated[algorithm1 + '_fr13']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr13']['pre_computation_time']

        if result['algorithm'] == TitleAlgo1 +" FR14":
            accumulated[algorithm1 + '_fr14']['count'] = 1 + accumulated[algorithm1 + '_fr14']['count']
            accumulated[algorithm1 + '_fr14']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr14']['stretch']
            accumulated[algorithm1 + '_fr14']['load'] = result['load'] + accumulated[algorithm1 + '_fr14']['load']
            accumulated[algorithm1 + '_fr14']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr14']['hops']
            accumulated[algorithm1 + '_fr14']['success'] = result['success'] + accumulated[algorithm1 + '_fr14']['success']
            accumulated[algorithm1 + '_fr14']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr14']['routing_computation_time']
            accumulated[algorithm1 + '_fr14']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr14']['pre_computation_time']

        if result['algorithm'] == TitleAlgo1 +" FR15":
            accumulated[algorithm1 + '_fr15']['count'] = 1 + accumulated[algorithm1 + '_fr15']['count']
            accumulated[algorithm1 + '_fr15']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr15']['stretch']
            accumulated[algorithm1 + '_fr15']['load'] = result['load'] + accumulated[algorithm1 + '_fr15']['load']
            accumulated[algorithm1 + '_fr15']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr15']['hops']
            accumulated[algorithm1 + '_fr15']['success'] = result['success'] + accumulated[algorithm1 + '_fr15']['success']
            accumulated[algorithm1 + '_fr15']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr15']['routing_computation_time']
            accumulated[algorithm1 + '_fr15']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr15']['pre_computation_time']

        if result['algorithm'] == TitleAlgo1 +" FR16":
            accumulated[algorithm1 + '_fr16']['count'] = 1 + accumulated[algorithm1 + '_fr16']['count']
            accumulated[algorithm1 + '_fr16']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr16']['stretch']
            accumulated[algorithm1 + '_fr16']['load'] = result['load'] + accumulated[algorithm1 + '_fr16']['load']
            accumulated[algorithm1 + '_fr16']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr16']['hops']
            accumulated[algorithm1 + '_fr16']['success'] = result['success'] + accumulated[algorithm1 + '_fr16']['success']
            accumulated[algorithm1 + '_fr16']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr16']['routing_computation_time']
            accumulated[algorithm1 + '_fr16']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr16']['pre_computation_time']


        if result['algorithm'] == TitleAlgo1 +" FR17":
            accumulated[algorithm1 + '_fr17']['count'] = 1 + accumulated[algorithm1 + '_fr17']['count']
            accumulated[algorithm1 + '_fr17']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr17']['stretch']
            accumulated[algorithm1 + '_fr17']['load'] = result['load'] + accumulated[algorithm1 + '_fr17']['load']
            accumulated[algorithm1 + '_fr17']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr17']['hops']
            accumulated[algorithm1 + '_fr17']['success'] = result['success'] + accumulated[algorithm1 + '_fr17']['success']
            accumulated[algorithm1 + '_fr17']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr17']['routing_computation_time']
            accumulated[algorithm1 + '_fr17']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr17']['pre_computation_time']

        if result['algorithm'] == TitleAlgo1 +" FR18":
            accumulated[algorithm1 + '_fr18']['count'] = 1 + accumulated[algorithm1 + '_fr18']['count']
            accumulated[algorithm1 + '_fr18']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr18']['stretch']
            accumulated[algorithm1 + '_fr18']['load'] = result['load'] + accumulated[algorithm1 + '_fr18']['load']
            accumulated[algorithm1 + '_fr18']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr18']['hops']
            accumulated[algorithm1 + '_fr18']['success'] = result['success'] + accumulated[algorithm1 + '_fr18']['success']
            accumulated[algorithm1 + '_fr18']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr18']['routing_computation_time']
            accumulated[algorithm1 + '_fr18']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr18']['pre_computation_time']

        if result['algorithm'] == TitleAlgo1 +" FR19":
            accumulated[algorithm1 + '_fr19']['count'] = 1 + accumulated[algorithm1 + '_fr19']['count']
            accumulated[algorithm1 + '_fr19']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr19']['stretch']
            accumulated[algorithm1 + '_fr19']['load'] = result['load'] + accumulated[algorithm1 + '_fr19']['load']
            accumulated[algorithm1 + '_fr19']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr19']['hops']
            accumulated[algorithm1 + '_fr19']['success'] = result['success'] + accumulated[algorithm1 + '_fr19']['success']
            accumulated[algorithm1 + '_fr19']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr19']['routing_computation_time']
            accumulated[algorithm1 + '_fr19']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr19']['pre_computation_time']

        if result['algorithm'] == TitleAlgo1 +" FR20":
            accumulated[algorithm1 + '_fr20']['count'] = 1 + accumulated[algorithm1 + '_fr20']['count']
            accumulated[algorithm1 + '_fr20']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr20']['stretch']
            accumulated[algorithm1 + '_fr20']['load'] = result['load'] + accumulated[algorithm1 + '_fr20']['load']
            accumulated[algorithm1 + '_fr20']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr20']['hops']
            accumulated[algorithm1 + '_fr20']['success'] = result['success'] + accumulated[algorithm1 + '_fr20']['success']
            accumulated[algorithm1 + '_fr20']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr20']['routing_computation_time']
            accumulated[algorithm1 + '_fr20']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr20']['pre_computation_time']

        if result['algorithm'] == TitleAlgo1 +" FR21":
            accumulated[algorithm1 + '_fr21']['count'] = 1 + accumulated[algorithm1 + '_fr21']['count']
            accumulated[algorithm1 + '_fr21']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr21']['stretch']
            accumulated[algorithm1 + '_fr21']['load'] = result['load'] + accumulated[algorithm1 + '_fr21']['load']
            accumulated[algorithm1 + '_fr21']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr21']['hops']
            accumulated[algorithm1 + '_fr21']['success'] = result['success'] + accumulated[algorithm1 + '_fr21']['success']
            accumulated[algorithm1 + '_fr21']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr21']['routing_computation_time']
            accumulated[algorithm1 + '_fr21']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr21']['pre_computation_time']

        if result['algorithm'] == TitleAlgo1 +" FR22":
            accumulated[algorithm1 + '_fr22']['count'] = 1 + accumulated[algorithm1 + '_fr22']['count']
            accumulated[algorithm1 + '_fr22']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr22']['stretch']
            accumulated[algorithm1 + '_fr22']['load'] = result['load'] + accumulated[algorithm1 + '_fr22']['load']
            accumulated[algorithm1 + '_fr22']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr22']['hops']
            accumulated[algorithm1 + '_fr22']['success'] = result['success'] + accumulated[algorithm1 + '_fr22']['success']
            accumulated[algorithm1 + '_fr22']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr22']['routing_computation_time']
            accumulated[algorithm1 + '_fr22']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr22']['pre_computation_time']

        if result['algorithm'] == TitleAlgo1 +" FR23":
            accumulated[algorithm1 + '_fr23']['count'] = 1 + accumulated[algorithm1 + '_fr23']['count']
            accumulated[algorithm1 + '_fr23']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr23']['stretch']
            accumulated[algorithm1 + '_fr23']['load'] = result['load'] + accumulated[algorithm1 + '_fr23']['load']
            accumulated[algorithm1 + '_fr23']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr23']['hops']
            accumulated[algorithm1 + '_fr23']['success'] = result['success'] + accumulated[algorithm1 + '_fr23']['success']
            accumulated[algorithm1 + '_fr23']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr23']['routing_computation_time']
            accumulated[algorithm1 + '_fr23']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr23']['pre_computation_time']


        if result['algorithm'] == TitleAlgo1 +" FR24":
            accumulated[algorithm1 + '_fr24']['count'] = 1 + accumulated[algorithm1 + '_fr24']['count']
            accumulated[algorithm1 + '_fr24']['stretch'] = result['stretch'] + accumulated[algorithm1 + '_fr24']['stretch']
            accumulated[algorithm1 + '_fr24']['load'] = result['load'] + accumulated[algorithm1 + '_fr24']['load']
            accumulated[algorithm1 + '_fr24']['hops'] = result['hops'] + accumulated[algorithm1 + '_fr24']['hops']
            accumulated[algorithm1 + '_fr24']['success'] = result['success'] + accumulated[algorithm1 + '_fr24']['success']
            accumulated[algorithm1 + '_fr24']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm1 + '_fr24']['routing_computation_time']
            accumulated[algorithm1 + '_fr24']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm1 + '_fr24']['pre_computation_time']

        

    ##############################################################################################################################################

        if result['algorithm'] == TitleAlgo2 +" FR1":
            accumulated[algorithm2 + '_fr1']['count'] = 1 + accumulated[algorithm2 + '_fr1']['count']
            accumulated[algorithm2 + '_fr1']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr1']['stretch']
            accumulated[algorithm2 + '_fr1']['load'] = result['load'] + accumulated[algorithm2 + '_fr1']['load']
            accumulated[algorithm2 + '_fr1']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr1']['hops']
            accumulated[algorithm2 + '_fr1']['success'] = result['success'] + accumulated[algorithm2 + '_fr1']['success']
            accumulated[algorithm2 + '_fr1']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr1']['routing_computation_time']
            accumulated[algorithm2 + '_fr1']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr1']['pre_computation_time']
        
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

        if result['algorithm'] == TitleAlgo2 +" FR11":
            accumulated[algorithm2 + '_fr11']['count'] = 1 + accumulated[algorithm2 + '_fr11']['count']
            accumulated[algorithm2 + '_fr11']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr11']['stretch']
            accumulated[algorithm2 + '_fr11']['load'] = result['load'] + accumulated[algorithm2 + '_fr11']['load']
            accumulated[algorithm2 + '_fr11']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr11']['hops']
            accumulated[algorithm2 + '_fr11']['success'] = result['success'] + accumulated[algorithm2 + '_fr11']['success']
            accumulated[algorithm2 + '_fr11']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr11']['routing_computation_time']
            accumulated[algorithm2 + '_fr11']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr11']['pre_computation_time']
        
        if result['algorithm'] == TitleAlgo2 +" FR12":
            accumulated[algorithm2 + '_fr12']['count'] = 1 + accumulated[algorithm2 + '_fr12']['count']
            accumulated[algorithm2 + '_fr12']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr12']['stretch']
            accumulated[algorithm2 + '_fr12']['load'] = result['load'] + accumulated[algorithm2 + '_fr12']['load']
            accumulated[algorithm2 + '_fr12']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr12']['hops']
            accumulated[algorithm2 + '_fr12']['success'] = result['success'] + accumulated[algorithm2 + '_fr12']['success']
            accumulated[algorithm2 + '_fr12']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr12']['routing_computation_time']
            accumulated[algorithm2 + '_fr12']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr12']['pre_computation_time']

        if result['algorithm'] == TitleAlgo2 +" FR13":
            accumulated[algorithm2 + '_fr13']['count'] = 1 + accumulated[algorithm2 + '_fr13']['count']
            accumulated[algorithm2 + '_fr13']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr13']['stretch']
            accumulated[algorithm2 + '_fr13']['load'] = result['load'] + accumulated[algorithm2 + '_fr13']['load']
            accumulated[algorithm2 + '_fr13']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr13']['hops']
            accumulated[algorithm2 + '_fr13']['success'] = result['success'] + accumulated[algorithm2 + '_fr13']['success']
            accumulated[algorithm2 + '_fr13']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr13']['routing_computation_time']
            accumulated[algorithm2 + '_fr13']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr13']['pre_computation_time']

        if result['algorithm'] == TitleAlgo2 +" FR14":
            accumulated[algorithm2 + '_fr14']['count'] = 1 + accumulated[algorithm2 + '_fr14']['count']
            accumulated[algorithm2 + '_fr14']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr14']['stretch']
            accumulated[algorithm2 + '_fr14']['load'] = result['load'] + accumulated[algorithm2 + '_fr14']['load']
            accumulated[algorithm2 + '_fr14']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr14']['hops']
            accumulated[algorithm2 + '_fr14']['success'] = result['success'] + accumulated[algorithm2 + '_fr14']['success']
            accumulated[algorithm2 + '_fr14']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr14']['routing_computation_time']
            accumulated[algorithm2 + '_fr14']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr14']['pre_computation_time']

        if result['algorithm'] == TitleAlgo2 +" FR15":
            accumulated[algorithm2 + '_fr15']['count'] = 1 + accumulated[algorithm2 + '_fr15']['count']
            accumulated[algorithm2 + '_fr15']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr15']['stretch']
            accumulated[algorithm2 + '_fr15']['load'] = result['load'] + accumulated[algorithm2 + '_fr15']['load']
            accumulated[algorithm2 + '_fr15']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr15']['hops']
            accumulated[algorithm2 + '_fr15']['success'] = result['success'] + accumulated[algorithm2 + '_fr15']['success']
            accumulated[algorithm2 + '_fr15']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr15']['routing_computation_time']
            accumulated[algorithm2 + '_fr15']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr15']['pre_computation_time']



        if result['algorithm'] == TitleAlgo2 +" FR16":
            accumulated[algorithm2 + '_fr16']['count'] = 1 + accumulated[algorithm2 + '_fr16']['count']
            accumulated[algorithm2 + '_fr16']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr16']['stretch']
            accumulated[algorithm2 + '_fr16']['load'] = result['load'] + accumulated[algorithm2 + '_fr16']['load']
            accumulated[algorithm2 + '_fr16']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr16']['hops']
            accumulated[algorithm2 + '_fr16']['success'] = result['success'] + accumulated[algorithm2 + '_fr16']['success']
            accumulated[algorithm2 + '_fr16']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr16']['routing_computation_time']
            accumulated[algorithm2 + '_fr16']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr16']['pre_computation_time']

        if result['algorithm'] == TitleAlgo2 +" FR17":
            accumulated[algorithm2 + '_fr17']['count'] = 1 + accumulated[algorithm2 + '_fr17']['count']
            accumulated[algorithm2 + '_fr17']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr17']['stretch']
            accumulated[algorithm2 + '_fr17']['load'] = result['load'] + accumulated[algorithm2 + '_fr17']['load']
            accumulated[algorithm2 + '_fr17']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr17']['hops']
            accumulated[algorithm2 + '_fr17']['success'] = result['success'] + accumulated[algorithm2 + '_fr17']['success']
            accumulated[algorithm2 + '_fr17']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr17']['routing_computation_time']
            accumulated[algorithm2 + '_fr17']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr17']['pre_computation_time']

        if result['algorithm'] == TitleAlgo2 +" FR18":
            accumulated[algorithm2 + '_fr18']['count'] = 1 + accumulated[algorithm2 + '_fr18']['count']
            accumulated[algorithm2 + '_fr18']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr18']['stretch']
            accumulated[algorithm2 + '_fr18']['load'] = result['load'] + accumulated[algorithm2 + '_fr18']['load']
            accumulated[algorithm2 + '_fr18']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr18']['hops']
            accumulated[algorithm2 + '_fr18']['success'] = result['success'] + accumulated[algorithm2 + '_fr18']['success']
            accumulated[algorithm2 + '_fr18']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr18']['routing_computation_time']
            accumulated[algorithm2 + '_fr18']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr18']['pre_computation_time']

        if result['algorithm'] == TitleAlgo2 +" FR19":
            accumulated[algorithm2 + '_fr19']['count'] = 1 + accumulated[algorithm2 + '_fr19']['count']
            accumulated[algorithm2 + '_fr19']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr19']['stretch']
            accumulated[algorithm2 + '_fr19']['load'] = result['load'] + accumulated[algorithm2 + '_fr19']['load']
            accumulated[algorithm2 + '_fr19']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr19']['hops']
            accumulated[algorithm2 + '_fr19']['success'] = result['success'] + accumulated[algorithm2 + '_fr19']['success']
            accumulated[algorithm2 + '_fr19']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr19']['routing_computation_time']
            accumulated[algorithm2 + '_fr19']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr19']['pre_computation_time']

        if result['algorithm'] == TitleAlgo2 +" FR20":
            accumulated[algorithm2 + '_fr20']['count'] = 1 + accumulated[algorithm2 + '_fr20']['count']
            accumulated[algorithm2 + '_fr20']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr20']['stretch']
            accumulated[algorithm2 + '_fr20']['load'] = result['load'] + accumulated[algorithm2 + '_fr20']['load']
            accumulated[algorithm2 + '_fr20']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr20']['hops']
            accumulated[algorithm2 + '_fr20']['success'] = result['success'] + accumulated[algorithm2 + '_fr20']['success']
            accumulated[algorithm2 + '_fr20']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr20']['routing_computation_time']
            accumulated[algorithm2 + '_fr20']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr20']['pre_computation_time']

        if result['algorithm'] == TitleAlgo2 +" FR21":
            accumulated[algorithm2 + '_fr21']['count'] = 1 + accumulated[algorithm2 + '_fr21']['count']
            accumulated[algorithm2 + '_fr21']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr21']['stretch']
            accumulated[algorithm2 + '_fr21']['load'] = result['load'] + accumulated[algorithm2 + '_fr21']['load']
            accumulated[algorithm2 + '_fr21']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr21']['hops']
            accumulated[algorithm2 + '_fr21']['success'] = result['success'] + accumulated[algorithm2 + '_fr21']['success']
            accumulated[algorithm2 + '_fr21']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr21']['routing_computation_time']
            accumulated[algorithm2 + '_fr21']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr21']['pre_computation_time']

        if result['algorithm'] == TitleAlgo2 +" FR22":
            accumulated[algorithm2 + '_fr22']['count'] = 1 + accumulated[algorithm2 + '_fr22']['count']
            accumulated[algorithm2 + '_fr22']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr22']['stretch']
            accumulated[algorithm2 + '_fr22']['load'] = result['load'] + accumulated[algorithm2 + '_fr22']['load']
            accumulated[algorithm2 + '_fr22']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr22']['hops']
            accumulated[algorithm2 + '_fr22']['success'] = result['success'] + accumulated[algorithm2 + '_fr22']['success']
            accumulated[algorithm2 + '_fr22']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr22']['routing_computation_time']
            accumulated[algorithm2 + '_fr22']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr22']['pre_computation_time']

        if result['algorithm'] == TitleAlgo2 +" FR23":
            accumulated[algorithm2 + '_fr23']['count'] = 1 + accumulated[algorithm2 + '_fr23']['count']
            accumulated[algorithm2 + '_fr23']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr23']['stretch']
            accumulated[algorithm2 + '_fr23']['load'] = result['load'] + accumulated[algorithm2 + '_fr23']['load']
            accumulated[algorithm2 + '_fr23']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr23']['hops']
            accumulated[algorithm2 + '_fr23']['success'] = result['success'] + accumulated[algorithm2 + '_fr23']['success']
            accumulated[algorithm2 + '_fr23']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr23']['routing_computation_time']
            accumulated[algorithm2 + '_fr23']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr23']['pre_computation_time']


        if result['algorithm'] == TitleAlgo2 +" FR24":
            accumulated[algorithm2 + '_fr24']['count'] = 1 + accumulated[algorithm2 + '_fr24']['count']
            accumulated[algorithm2 + '_fr24']['stretch'] = result['stretch'] + accumulated[algorithm2 + '_fr24']['stretch']
            accumulated[algorithm2 + '_fr24']['load'] = result['load'] + accumulated[algorithm2 + '_fr24']['load']
            accumulated[algorithm2 + '_fr24']['hops'] = result['hops'] + accumulated[algorithm2 + '_fr24']['hops']
            accumulated[algorithm2 + '_fr24']['success'] = result['success'] + accumulated[algorithm2 + '_fr24']['success']
            accumulated[algorithm2 + '_fr24']['routing_computation_time'] = result['routing_computation_time'] + accumulated[algorithm2 + '_fr24']['routing_computation_time']
            accumulated[algorithm2 + '_fr24']['pre_computation_time'] = result['pre_computation_time'] + accumulated[algorithm2 + '_fr24']['pre_computation_time']
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
    
    alg1_counts.append(accumulated[algorithm1 + FR ]['count'])
    alg2_counts.append(accumulated[algorithm2 + FR ]['count'])

    alg1_sum_hops.append(accumulated[algorithm1 + FR ]['hops'])
    alg2_sum_hops.append(accumulated[algorithm2 + FR ]['hops'])
    print(" ")

    ###Graphen ####
    print(" ")
    #input("CLICK FOR NEXT FR ...")
    print("------------------------------------------------------------------")
#endfor
# print(" Resilienz geteilt durch Count ohne Beachtung von Infs ")
# print(algorithm1 + "_Resilienz = ", alg1_resilience)
# print(algorithm2 + "_Resilienz = ", alg2_resilience)
# print(" ")
print(" Resilienz geteilt durch Count mit Beachtung von Infs (Summe von Resilienz geteilt durch Anzahl an Experimenten, beinhaltet auch die fehlgeschlagenen)")
print(algorithm1 + "_mit_infs_Resilienz = ", alg1_real_resilience)
print(algorithm2 + "_mit_infs_Resilienz = ", alg2_real_resilience)
print(" ")
print(algorithm1 + "_Hops = ", alg1_hops)
print(algorithm2 + "_Hops = ", alg2_hops)
print(" ")
print(algorithm1 + "_time = " , alg1_time)
print(algorithm2 + "_time = " , alg2_time)

print(" ")
# print(" NUR FÜR DEN DRITTEN PLOT WICHTIG ")
# print(algorithm1 + "_sum_hops = " , alg1_sum_hops)
# print(algorithm2 + "_sum_hops = " , alg2_sum_hops)
# print(" ")
# print(algorithm1 + "_count = " , alg1_counts)
# print(algorithm2 + "_count = " , alg2_counts)


plotfig = True
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

    ################################ COMPUTATION TIME #######################################################


    # plt.figure()

    # X = [1,2,3,4,5,6,7,8,9]

    # for i in range(0, len(X)):
    #     X[i] = X[i] * 50

    # mt_time =  [77.32267133333333, 48.845689, 81.448652, 122.17995533333333, 167.94597866666666, 229.81547299999997, 308.94882200000006, 368.6160713333333, 460.62677866666667]
    # otbM_time =  [29.739345666666665, 4.216385333333334, 6.597391333333333, 7.048780000000001, 7.8528926666666665, 8.021870666666667, 7.971387666666666, 9.272190666666667, 8.196245]
    # mtmB_time =  [29.74375533333333, 27.40294966666667, 38.087102, 62.297391000000005, 64.81008133333334, 107.90556266666668, 134.95438166666665, 141.93827766666666, 189.03758066666668]
    # mtmA_time =  [9.231850999999999, 12.291334666666666, 11.799994333333332, 14.849939, 15.638326999999999, 19.513328666666666, 20.34446766666667, 16.08910033333333, 19.533797333333336]
    # mtmR_time =  [80.51002633333333, 51.413677666666665, 75.714287, 119.014935, 165.62308499999997, 232.689798, 318.464939, 365.40515999999997, 469.14956466666666]
    # mtmP_time =  [12.541610666666669, 22.845202, 31.498940666666666, 63.022454333333336, 78.37081966666666, 108.58506433333334, 142.37752033333334, 140.24766766666667, 188.01580633333333]

    # plt.subplot(221)

    # plt.plot(X, mt_time, color='r', label='MultipleTrees')
    # plt.plot(X, otbM_time, color='g', label='OneTree Breite Mod')
    # plt.plot(X, mtmB_time, color='b', label='MultipleTrees Breite Mod')
    # plt.plot(X, mtmA_time, color='m', label='MultipleTrees Anzahl Mod')
    # plt.plot(X, mtmR_time, color='y', label='MultipleTrees Reihenfolge Mod')
    # plt.plot(X, mtmP_time, color='c', label='MultipleTrees Parallel Mod')

    # plt.xlabel("Kantenanzahl")
    # plt.ylabel("Zeit in s")
    # plt.title("Rechenzeit, n = 50, Konnektivität von 1 bis 9")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # plt.show()
    ################################ REAL TOPOLOGIES NEW #########################################################


    #DAS IST DER PLOT DEN ICH PROF. FÖRSTER AM FREITAG 3.3 zeige
    # plt.figure()

    # X = [2,3,4,5,6,7,8,9,10,11,12]

    # baseMT_mit_infs_Resilienz =           [1, 1, 0.975, 0.95, 0.775, 0.75, 0.75, 0.72, 0.7, 0.55, 0.500]
    # baseOT_mit_infs_Resilienz =           [1, 1, 0.975, 0.95, 0.775, 0.75, 0.75, 0.72, 0.7, 0.55, 0.525]
    # sq1_mit_infs_Resilienz =              [1, 1, 0.975, 0.92, 0.725, 0.67, 0.65, 0.65, 0.625, 0.525, 0.500]
    # parallelInverse_mit_infs_Resilienz =  [1, 1, 0.975, 0.95, 0.775, 0.75, 0.75, 0.72, 0.7, 0.55, 0.500]
    # mtmp_mit_infs_Resilienz =             [1, 1, 0.975, 0.95, 0.775, 0.75, 0.75, 0.72, 0.7, 0.55, 0.500]
    # mtiom_mit_infs_Resilienz =            [1, 1, 0.975, 0.95, 0.775, 0.75, 0.75, 0.721, 0.7, 0.55, 0.525]
    # mtrom_mit_infs_Resilienz =            [1, 1, 0.975, 0.95, 0.775, 0.75, 0.72, 0.725, 0.7, 0.55, 0.525]

    # plt.subplot(221)

    # plt.plot(X, baseMT_mit_infs_Resilienz, color='r', label='MultipleTrees')
    # plt.plot(X, baseOT_mit_infs_Resilienz, color='g', label='OneTree')
    # plt.plot(X, sq1_mit_infs_Resilienz, color='b', label='SquareOne')
    # plt.plot(X, parallelInverse_mit_infs_Resilienz, color='m', label='MultipleTrees parallel & invers')
    # plt.plot(X, mtmp_mit_infs_Resilienz, color='y', label='MultipleTrees parallel')
    # plt.plot(X, mtiom_mit_infs_Resilienz, color='c', label='MultipleTrees invers')
    # plt.plot(X, mtrom_mit_infs_Resilienz, '--' ,color='r', label='MultipleTrees random')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, Reale Topologien")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # plt.show()



    #plt.subplot(222)

    # Y = [2,3,4,5,6,7,8,9,10]

    # mtrom_Hops =  [12.0, 10.25, 9.5, 9.75, 10.25, 12.375, 12.125, 11.5, 10.875]
    # mtmp_Hops =  [13.125, 14.125, 11.875, 11.75, 11.625, 11.625, 11.375, 12.125, 11.25]
    # mtiom_Hops =  [8.375, 9.75, 9.75, 9.5, 9.5, 11.625, 11.375, 10.0, 9.25]
    # baseMT_Hops =  [13.125, 14.125, 11.875, 11.75, 11.625, 11.625, 11.375, 12.125, 11.25]
    # baseOT_Hops =  [8.375, 9.5, 9.625, 10.625, 10.625, 10.625, 10.375, 9.0, 9.5]
    # sq1_Hops =  [8.375, 9.25, 6.875, 6.75, 6.625, 6.625, 6.625, 7.375, 7.125]
    # parallelInverse_Hops =  [8.375, 9.75, 9.75, 9.375, 9.5, 10.875, 10.625, 9.25, 7.125]

    # plt.plot(Y, baseMT_Hops, '--', color='r', label='MultipleTrees')
    # plt.plot(Y,baseOT_Hops, '--', color='g', label='OneTree')
    # plt.plot(Y, sq1_Hops,'--' , color='c', label='SquareOne')
    # plt.plot(Y, parallelInverse_Hops, color='m', label='Parallel & Invers')
    # plt.plot(Y, mtmp_Hops, color='y', label='Parallel')
    # plt.plot(Y, mtiom_Hops,'--', color='m', label='Invers')
    # plt.plot(Y, mtrom_Hops, color='b', label='Randomisiert')

    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Hops")
    # plt.title("Hop-Anzahl, reale Topologien ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # plt.show()

    ################################ REAL TOPOLOGIES OLD #########################################################
    
    # plt.figure()

    # X = [2,3,4,5,6,7,8,9,10]
    
    # multipletre_trees_Resilienz =            [1, 1, 0.8693333333333332, 0.808333333333333, 0.7449275362318837, 0.7014925373134325, 0.6262295081967211, 0.5962962962962963, 0.5615384615384618, 0.5173913043478262, 0.47804878048780475]
    # multipletre_trees_mit_infs_Resilienz =   [1, 1, 0.8693333333333332, 0.7759999999999997, 0.685333333333333, 0.6266666666666664, 0.5093333333333332, 0.42933333333333334, 0.3893333333333335, 0.3173333333333334, 0.26133333333333325]  
    # one_tree_Resilienz =                     [1, 1, 0.8773333333333331, 0.833333333333333, 0.7599999999999997, 0.7130434782608694, 0.6338461538461537, 0.606896551724138, 0.5535714285714286, 0.5058823529411764, 0.47234042553191474]
    # one_tree_mit_infs_Resilienz =            [1, 1, 0.8773333333333331, 0.7999999999999997, 0.709333333333333, 0.6559999999999998, 0.5493333333333332, 0.4693333333333334, 0.4133333333333334, 0.344, 0.2959999999999999]
    # parallel_inverse_Resilienz =             [1, 1, 0.8639999999999998, 0.8111111111111108, 0.742028985507246, 0.6941176470588232, 0.6196721311475408, 0.5890909090909092, 0.5615384615384618, 0.5063829787234043, 0.4558139534883719]
    # parallel_inverse_mit_infs_Resilienz =    [1, 1, 0.8639999999999998, 0.7786666666666664, 0.6826666666666663, 0.629333333333333, 0.5039999999999999, 0.43200000000000005, 0.3893333333333335, 0.31733333333333336, 0.2613333333333332]
    # square_one_Resilienz =                   [1, 1, 0.8506666666666661, 0.8027777777777774, 0.7428571428571425, 0.6898550724637679, 0.6, 0.5862068965517241, 0.5418181818181819, 0.4959999999999999, 0.46666666666666656]
    # square_one_mit_infs_Resilienz =          [1, 1, 0.8506666666666661, 0.7706666666666663, 0.693333333333333, 0.6346666666666664, 0.512, 0.4533333333333333, 0.39733333333333337, 0.3306666666666666, 0.27999999999999997]
    # parallel_Resilienz =                     [1, 1, 0.8746666666666666, 0.8194444444444441, 0.7428571428571424, 0.6898550724637678, 0.6129032258064515, 0.585714285714286, 0.5481481481481483, 0.49795918367346936, 0.4651162790697672]
    # invert_Resilienz =                       [1, 1, 0.8666666666666665, 0.8055555555555552, 0.7441176470588231, 0.6823529411764703, 0.6098360655737705, 0.5709090909090909, 0.5461538461538462, 0.52, 0.4829268292682925]
    # parallel_mit_infs_Resilienz =            [1, 1, 0.8746666666666666, 0.7866666666666663, 0.6933333333333329, 0.6346666666666663, 0.5066666666666666, 0.43733333333333346, 0.3946666666666668, 0.3253333333333333, 0.26666666666666655]
    # invert_mit_infs_Resilienz =              [1, 1, 0.8666666666666665, 0.7733333333333331, 0.6746666666666663, 0.6186666666666664, 0.49599999999999994, 0.4186666666666667, 0.37866666666666676, 0.312, 0.2639999999999999]  
    # random_Resilienz =                       [1, 1, 0.8666666666666665, 0.8028169014084504, 0.7470588235294114, 0.6895522388059697, 0.6133333333333333, 0.6000000000000001, 0.5647058823529414, 0.5227272727272727, 0.5025641025641024]
    # random_mit_infs_Resilienz =              [1, 1, 0.8666666666666665, 0.7599999999999997, 0.677333333333333, 0.6159999999999997, 0.49066666666666664, 0.42400000000000004, 0.3840000000000002, 0.30666666666666664, 0.26133333333333325]
    
    
    # sq1_mit_infs_Resilienz =  [1, 1, 0.975, 0.9249999999999999, 0.7250000000000001, 0.675, 0.65, 0.65, 0.625, 0.525, 0.975]
    # parallelInverse_mit_infs_Resilienz =  [1, 1, 0.975, 0.95, 0.775, 0.75, 0.75, 0.7250000000000001, 0.7, 0.55, 0.975]


    # plt.subplot(221)

    # #print("X length : ", len(X))
    # #print("multtrees length : " , len(multipletre_trees_mit_infs_Resilienz))
    # #print("multtrees cut length : " , len(multipletre_trees_mit_infs_Resilienz[2:11]))
    # multTreesCut = multipletre_trees_mit_infs_Resilienz[2:11]
    # #print(multTreesCut)

    # #erster plot
    # #plt.plot(X, multTreesCut, '--', color='r', label='MultipleTrees')
    # #plt.plot(X, one_tree_mit_infs_Resilienz[2:11], '--', color='g', label='OneTree')
    # #plt.plot(X, square_one_mit_infs_Resilienz[2:11],'--' , color='c', label='SquareOne')
    # #plt.plot(X, parallel_inverse_mit_infs_Resilienz[2:11], color='m', label='Parallel & Invers')


    # #zweiter plot
    # #plt.plot(X, parallel_mit_infs_Resilienz[2:11], color='y', label='Parallel')
    # #plt.plot(X, invert_mit_infs_Resilienz[2:11],'--', color='m', label='Invers')
    # #plt.plot(X, random_mit_infs_Resilienz[2:11], color='b', label='Randomisiert')

    # # Naming the x-axis, y-axis and the whole graph
    # #plt.xlabel("Failure Rate")
    # #plt.ylabel("Resilienz")
    # #plt.title("Resilienz, reale Topologien ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # #plt.legend(fontsize="x-small")

    # #plt.subplot(222)

    # Y = [2,3,4,5,6,7,8,9,10]

    # parallel_Hops =                          [16.36, 15.347222222222221, 16.12857142857143, 14.695652173913043, 12.596774193548388, 12.25, 11.907407407407407, 10.714285714285714, 9.511627906976743]
    # invert_Hops =                            [11.973333333333333, 12.027777777777779, 12.338235294117647, 11.411764705882353, 9.80327868852459, 10.036363636363637, 9.153846153846153, 8.377777777777778, 7.7073170731707314]
    # parallel_inverse_Hops =                  [11.133333333333333, 10.75, 11.753623188405797, 10.691176470588236, 9.639344262295081, 9.618181818181819, 9.115384615384615, 8.0, 7.093023255813954]
    # square_one_Hops =                        [9.666666666666666, 9.402777777777779, 9.814285714285715, 9.043478260869565, 7.796875, 7.5, 6.9818181818181815, 6.48, 5.822222222222222]
    # multipletre_trees_Hops =                 [16.253333333333334, 15.722222222222221, 16.92753623188406, 15.149253731343284, 13.163934426229508, 13.074074074074074, 12.884615384615385, 10.978260869565217, 9.292682926829269]
    # one_tree_Hops =                          [10.626666666666667, 10.555555555555555, 10.542857142857143, 10.53623188405797, 9.338461538461539, 8.758620689655173, 7.732142857142857, 7.294117647058823, 7.212765957446808]
    # random_Hops =                            [14.333333333333334, 13.47887323943662, 14.485294117647058, 12.701492537313433, 11.4, 11.622641509433961, 10.666666666666666, 10.090909090909092, 9.179487179487179]

    # plt.plot(Y, multipletre_trees_Hops, '--', color='r', label='MultipleTrees')
    # plt.plot(Y,one_tree_Hops, '--', color='g', label='OneTree')
    # plt.plot(Y, square_one_Hops,'--' , color='c', label='SquareOne')
    # plt.plot(Y, parallel_inverse_Hops, color='m', label='Parallel & Invers')
    # plt.plot(Y, parallel_Hops, color='y', label='Parallel')
    # plt.plot(Y, invert_Hops,'--', color='m', label='Invers')
    # plt.plot(Y, random_Hops, color='b', label='Randomisiert')

    # # Naming the x-axis, y-axis and the whole graph
    # plt.xlabel("Failure Rate")
    # plt.ylabel("Hops")
    # plt.title("Hop-Anzahl, reale Topologien ")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # plt.show()

    ############################# REAL TOPOS WEITERE EXPERIMENTE ####################################


    # plt.figure()

    # X = [2,3,4,5,6,7,8,9,10,11,12]

    # mtmp_mit_infs_Resilienz =    [1, 1, 1.0, 0.96, 0.64, 0.64, 0.64, 0.64, 0.64, 0.44000000000000006, 0.31999999999999995]
    # mtiom_mit_infs_Resilienz =   [1, 1, 1.0, 1.0, 0.72, 0.72, 0.72, 0.72, 0.72, 0.44000000000000006, 0.31999999999999995]
    # baseMT_mit_infs_Resilienz =  [1, 1, 1.0, 1.0, 0.72, 0.72, 0.72, 0.72, 0.72, 0.44000000000000006, 0.31999999999999995]
    # baseOT_mit_infs_Resilienz =  [1, 1, 1.0, 1.0, 0.72, 0.72, 0.72, 0.72, 0.72, 0.44000000000000006, 0.31999999999999995]
    # sq1_mit_infs_Resilienz =     [1, 1, 1.0, 0.96, 0.64, 0.64, 0.64, 0.64, 0.64, 0.44000000000000006, 0.31999999999999995]
    # parallelInverse_mit_infs_Resilienz =  [1, 1, 1.0, 1.0, 0.6799999999999999, 0.6799999999999999, 0.6799999999999999, 0.6799999999999999, 0.6799999999999999, 0.44000000000000006, 0.31999999999999995]
    # mtrom_mit_infs_Resilienz =  [1, 1, 1.0, 1.0, 0.72, 0.72, 0.72, 0.72, 0.72, 0.44000000000000006, 0.31999999999999995]
 
    # mtrom_Hops =  [10.2, 14.2, 14.75, 12.5, 14.0, 13.75, 13.25, 9.0, 9.25]
    # sq1_Hops =  [9.4, 11.6, 7.25, 7.25, 7.25, 7.25, 7.25, 5.0, 5.0]
    # parallelInverse_Hops =  [9.4, 11.6, 9.5, 9.5, 9.5, 9.5, 9.5, 5.0, 5.0]
    # baseMT_Hops =  [15.2, 25.0, 18.75, 15.25, 15.25, 15.25, 14.75, 10.5, 9.75]
    # baseOT_Hops =  [9.6, 12.2, 12.5, 12.5, 12.5, 12.5, 12.0, 5.5, 5.25]
    # mtmp_Hops =  [15.2, 28.0, 16.5, 13.0, 13.0, 13.0, 12.5, 10.5, 9.75]
    # mtiom_Hops =  [9.4, 11.6, 12.0, 12.0, 12.0, 12.0, 11.5, 5.0, 5.0]

    # plt.subplot(221)

    # plt.plot(X, baseMT_mit_infs_Resilienz, color='r', label='MultipleTrees')
    # plt.plot(X, baseOT_mit_infs_Resilienz, color='g', label='OneTree')
    # plt.plot(X, sq1_mit_infs_Resilienz, color='b', label='SquareOne')
    # plt.plot(X, parallelInverse_mit_infs_Resilienz, color='m', label='MultipleTrees parallel & invers')
    # plt.plot(X, mtmp_mit_infs_Resilienz, color='y', label='MultipleTrees parallel')
    # plt.plot(X, mtiom_mit_infs_Resilienz, color='c', label='MultipleTrees invers')
    # plt.plot(X, mtrom_mit_infs_Resilienz, '--' ,color='r', label='MultipleTrees random')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, Reale Topologien")
    # # Adding legend, which helps us recognize the curve according to it's color
    # plt.legend(fontsize="x-small")

    # plt.show()

    ############################### MT vs MTP vs MTRecycle ############################

    # plt.figure()

    # X = [1,2,3,4,5,6,7,8,9,10,11,12]
    # plt.subplot(221)

    # MTRecycle_mit_infs_Resilienz =  [1, 1, 1.0, 1.0, 0.8799999999999999, 0.72, 0.56, 0.24, 0.2, 0.2, 0.12000000000000002, 0.04]
    # mtmP_mit_infs_Resilienz =  [1, 1, 1.0, 0.96, 0.8400000000000001, 0.72, 0.56, 0.24, 0.16, 0.16, 0.12000000000000002, 0.04]
    # baseMT_mit_infs_Resilienz =  [1, 1, 1.0, 1.0, 0.9199999999999999, 0.76, 0.56, 0.27999999999999997, 0.2, 0.2, 0.12000000000000002, 0.04]
    
    # plt.plot(X, baseMT_mit_infs_Resilienz, color='r', label='MultipleTrees')
    # plt.plot(X, MTRecycle_mit_infs_Resilienz, color='g', label='MultipleTrees Recycle')
    # plt.plot(X, mtmP_mit_infs_Resilienz, color='b', label='MultipleTrees Parallel')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, randomisiert, n = 40 , k = 5 ")

    # plt.legend(fontsize="x-small")

    # plt.subplot(222)
    # Y = [1,2,3,4,5,6,7,8,9,10]
    # MTRecycle_Hops =  [7.4, 10.8, 11.0, 17.8, 12.8, 10.25, 7.666666666666667, 6.0, 6.0, 2.0]
    # mtmP_Hops =  [11.4, 14.8, 14.6, 11.6, 7.2, 6.75, 5.0, 4.333333333333333, 4.0, 2.0]
    # baseMT_Hops =  [6.6, 9.6, 11.6, 14.4, 12.4, 11.0, 7.666666666666667, 6.0, 6.0, 2.0]
    # plt.plot(Y, baseMT_Hops, color='r', label='MultipleTrees')
    # plt.plot(Y, MTRecycle_Hops, color='g', label='MultipleTrees Recycle')
    # plt.plot(Y, mtmP_Hops, color='b', label='MultipleTrees Parallel')
    # plt.xlabel("Failue Rate")
    # plt.ylabel("Hops")
    # plt.title("Resilienz, randomisiert,  n = 40 , k = 5 ")
    # plt.legend(fontsize="x-small")
    # plt.show()
    ################################ MT  vs MTP NEW ##################################

    # plt.figure()

    # X = [1,2,3,4,5,6,7,8,9,10,11,12]

    # baseMT_mit_infs_Resilienz =  [1, 1, 1.0, 1.0, 0.9249999999999999, 0.85, 0.725, 0.5499999999999999, 0.39999999999999997, 0.22499999999999998, 0.175, 0.175]
    # mtmP_mit_infs_Resilienz =  [1, 1, 1.0, 0.8249999999999998, 0.8249999999999998, 0.6250000000000001, 0.5000000000000001, 0.39999999999999997, 0.24999999999999997, 0.15, 0.125, 0.125]
    
    # plt.plot(X, baseMT_mit_infs_Resilienz, color='r', label='MultipleTrees')
    # plt.plot(X, mtmP_mit_infs_Resilienz, color='b', label='MultipleTrees Parallel')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, n = 40 , k = 5 ")

    # plt.legend(fontsize="x-small")

    # plt.show()

    # baseMT_Hops =  [6.875, 6.875, 10.625, 13.75, 15.125, 11.125, 11.714285714285714, 9.428571428571429, 7.2, 6.4]
    # mtmP_Hops =  [12.25, 11.5, 12.0, 15.375, 9.25, 7.142857142857143, 4.833333333333333, 6.75, 6.25, 5.25]
 
    ####################### ONETREE VS ONETREEINVERSE ####################################

    # plt.figure()

    # X = [2,3,4,5,6,7,8,9,10]
    # plt.subplot(221)

    # OTInverse_mit_infs_Resilienz =  [1.0, 1.0, 0.9333333333333332, 0.6, 0.3333333333333333, 0.19999999999999998, 0.13333333333333333, 0.13333333333333333, 0.13333333333333333]
    # baseOT_mit_infs_Resilienz =  [1.0, 1.0, 1.0, 0.6, 0.4000000000000001, 0.26666666666666666, 0.13333333333333333, 0.13333333333333333, 0.13333333333333333]

    # OTInverse_Hops =  [5.333333333333333, 6.0, 11.333333333333334, 9.0, 7.0, 7.0, 7.0, 7.0, 7.0]
    # baseOT_Hops =  [5.333333333333333, 6.0, 14.333333333333334, 11.666666666666666, 12.5, 15.0, 7.0, 7.0, 7.0]
    
    # plt.plot(X,baseOT_mit_infs_Resilienz, color='r', label='OneTree')
    # plt.plot(X, OTInverse_mit_infs_Resilienz, color='g', label='OneTree Mod')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, randomisiert, n = 40 , k = 5 ")

    # plt.legend(fontsize="x-small")

    # plt.subplot(222)
    # Y = [2,3,4,5,6,7,8,9,10]

    # plt.plot(Y, baseOT_Hops, color='r', label='OneTree')
    # plt.plot(Y, OTInverse_Hops, color='g', label='OneTree Mod')
    # plt.xlabel("Failue Rate")
    # plt.ylabel("Hops")
    # plt.title("durchschn. Hops, randomisiert,  n = 40 , k = 5 ")
    # plt.legend(fontsize="x-small")
    # plt.show()


    ##################################### WEITERFÜHRENDE EXPERIMENTE ################################   


    X = [v for v in range(1,25)]
    

    #Linker Plot mit der Resilienz
    # plt.subplot(221)
    
    # multipleTrees_mit_infs_Resilienz =  [1.0, 1.0, 1.0, 1.0, 1.0, 0.9591837142857143, 1.0, 1.0, 1.0, 1.0, 0.9714285714285714, 0.9714285714285714, 0.9714285714285714, 0.9428571428571428, 0.9428571428571428, 1.8857142857142861, 0.857142857142857, 0.7999999999999999, 0.7999999999999999, 0.4, 0.3428571428571429, 0.3428571428571429, 0.3428571428571429, 0.2285714285714286]
    # oneTreeInvers_mit_infs_Resilienz =  [1.0, 1.0, 1.0, 1.0, 1.0, 0.9591837142857143, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9714285714285714, 0.8857142857142858, 0.8571428571428571, 0.8285714285714285, 1.4285714285714288, 0.6, 0.45714285714285713, 0.45714285714285713, 0.2571428571428571, 0.2285714285714286, 0.2285714285714286, 0.2285714285714286, 0.19999999999999998]
    # oneTree_mit_infs_Resilienz =        [1.0, 1.0, 1.0, 1.0, 1.0, 0.9591837142857143, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9714285714285714, 0.9142857142857143, 0.8571428571428571, 0.8571428571428571, 1.3142857142857143, 0.6, 0.5428571428571428,  0.5428571428571428,  0.2857142857142857, 0.19999999999999998, 0.19999999999999998, 0.19999999999999998, 0.17142857142857146]
    # multipleTreesInvers_mit_infs_Resilienz =  [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9714285714285714, 0.9142857142857143, 0.8571428571428571, 0.8571428571428571, 1.6000000000000003, 0.7714285714285714, 0.7428571428571428, 0.7142857142857142, 0.48571428571428577, 0.48571428571428577, 0.42857142857142855, 0.3428571428571429, 0.2571428571428572]
    # squareOne_mit_infs_Resilienz =  [1.0, 1.0, 1.0, 1.0, 1.0, 0.9591837142857143, 1.0, 1.0, 0.9714285714285714, 0.9714285714285714, 0.9714285714285714, 0.9142857142857143, 0.8857142857142858, 0.7999999999999999, 0.7142857142857143, 1.1999999999999997, 0.4, 0.37142857142857144, 0.37142857142857144, 0.19999999999999998, 0.19999999999999998, 0.19999999999999998, 0.19999999999999998, 0.14285714285714285]
    #multipleTreesParallelInvers_mit_infs_Resilienz =  [1.0, 1.0, 1.0, 1.0, 1.0, 0.9591837142857143, 1.0, 1.0, 1.0, 1.0, 0.9714285714285714, 0.9714285714285714, 0.8857142857142858, 0.7999999999999999, 0.7428571428571428, 1.3714285714285712, 0.5714285714285714, 0.5428571428571429, 0.5428571428571429, 0.2571428571428571, 0.2285714285714286, 0.2285714285714286, 0.2285714285714286, 0.17142857142857146]
    

    # #hier müssen die resilienzen nochmal geteilt werden weil fr16 doppelt in der liste stande
    # print(multipleTrees_mit_infs_Resilienz[15])
    # multipleTrees_mit_infs_Resilienz[15] = multipleTrees_mit_infs_Resilienz[15] /2
    # print(multipleTrees_mit_infs_Resilienz[15])
    # oneTreeInvers_mit_infs_Resilienz[15] =  oneTreeInvers_mit_infs_Resilienz[15]/2
    # oneTree_mit_infs_Resilienz[15] =  oneTree_mit_infs_Resilienz[15]/2
    # multipleTreesInvers_mit_infs_Resilienz[15] =  multipleTreesInvers_mit_infs_Resilienz[15]/2
    # squareOne_mit_infs_Resilienz[15] =  squareOne_mit_infs_Resilienz[15]/2
    #multipleTreesParallelInvers_mit_infs_Resilienz[15] =  multipleTreesParallelInvers_mit_infs_Resilienz[15]/2
    #print("MultipleTrees Parallel & Invers Resilienz : " , ( sum(multipleTreesParallelInvers_mit_infs_Resilienz)/len(multipleTreesParallelInvers_mit_infs_Resilienz)  ))
    # print(multipleTrees_mit_infs_Resilienz)
    # plt.plot(X,  multipleTrees_mit_infs_Resilienz, color='r', label='MultipleTrees')
    # plt.plot(X, oneTreeInvers_mit_infs_Resilienz , color='g', label='OneTree Invers')
    # plt.plot(X,  oneTree_mit_infs_Resilienz, color='b', label='OneTree')
    # plt.plot(X, multipleTreesInvers_mit_infs_Resilienz, color='m', label='MultipleTrees Invers')
    # plt.plot(X, squareOne_mit_infs_Resilienz , color='y', label='SquareOne')
    # plt.plot(X, multipleTreesParallelInvers_mit_infs_Resilienz, color='c', label='MultipleTrees Parallel & Invers')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Resilienz")
    # plt.title("Resilienz, randomisiert, n = 80 , k = 6 ")

    # plt.legend(fontsize="x-small")
    # plt.show()
    #Mittlerer Plot mit den Hops nur zeilen gelöscht die Inf waren


    # plt.subplot(221)
    # squareOne_Hops =  [3.857142857142857,
    #                     3.857142857142857,
    #                     4.0, 12.142857142857142,
    #                       11.857142857142858,
    #                         13.0,
    #                           4.571428571428571, 
    #                           5.714285714285714, 
    #                           5.714285714285714,
    #                             8.857142857142858,
    #                               11.142857142857142,
    #                                 10.428571428571429,
    #                                   13.714285714285714,
    #                                     13.0, 9.142857142857142,
    #                                       10.142857142857142,
    #                                         4.0,
    #                                           4.0,
    #                                             4.0, 
    #                                             3.25,
    #                                               3.25, 
    #                                               3.25, 
    #                                               3.25, 
    #                                               2.75]
    multipleTreesParallelInvers_Hops =  [3.857142857142857, 3.857142857142857, 4.0, 6.857142857142857, 6.857142857142857, 11.285714285714286, 4.0, 6.857142857142857, 7.428571428571429, 9.857142857142858, 10.857142857142858, 11.571428571428571, 15.142857142857142, 14.428571428571429, 9.714285714285714, 8.714285714285714, 8.0, 7.428571428571429, 6.857142857142857, 4.8, 4.8, 4.8, 4.8, 4.0]
    multipleTrees_Hops =  [6.285714285714286, 6.142857142857143, 6.285714285714286, 10.714285714285714, 9.428571428571429, 9.571428571428571, 6.571428571428571, 8.285714285714286, 9.428571428571429, 9.428571428571429, 11.0, 10.857142857142858, 19.0, 18.714285714285715, 18.857142857142858, 23.0, 19.857142857142858, 19.714285714285715, 18.857142857142858, 16.166666666666668, 15.0, 15.833333333333334, 15.333333333333334, 15.8]
    oneTreeInvers_Hops =  [3.857142857142857, 4.0, 4.285714285714286, 11.857142857142858, 10.714285714285714, 12.142857142857142, 4.0, 4.714285714285714, 4.714285714285714, 9.571428571428571, 12.142857142857142, 12.142857142857142, 14.142857142857142, 12.571428571428571, 12.857142857142858, 16.285714285714285, 18.142857142857142, 13.428571428571429, 13.428571428571429, 11.0, 7.8, 7.8, 7.8, 6.6]
    oneTree_Hops =  [3.857142857142857, 4.0, 4.285714285714286, 11.857142857142858, 10.714285714285714, 12.142857142857142, 4.0, 4.714285714285714, 4.714285714285714, 9.571428571428571, 12.142857142857142, 12.142857142857142, 15.0, 12.571428571428571, 16.428571428571427, 13.285714285714286, 17.857142857142858, 16.571428571428573, 16.571428571428573, 8.0, 4.0, 4.0, 4.0, 3.5]
    multipleTreesInvers_Hops =  [3.857142857142857, 3.857142857142857, 3.857142857142857, 9.428571428571429, 9.428571428571429, 9.428571428571429, 3.857142857142857, 6.857142857142857, 6.857142857142857, 7.142857142857143, 8.857142857142858, 8.0, 16.142857142857142, 16.428571428571427, 18.571428571428573, 19.0, 19.571428571428573, 15.857142857142858, 15.142857142857142, 18.571428571428573, 19.142857142857142, 14.714285714285714, 8.0, 5.333333333333333]
    
    #for i in range(0,len(oneTree_Hops)):
    #    if(oneTree_Hops[i] < oneTreeInvers_Hops[i]):
    #        print(oneTree_Hops[i])

    #print("OneTree : ", (sum(oneTree_Hops)/len(oneTree_Hops)))
    #print("OneTreeInvers : ", (sum(oneTreeInvers_Hops)/len(oneTreeInvers_Hops)))
    
    # plt.plot(X,  multipleTrees_Hops, color='r', label='MultipleTrees')
    # plt.plot(X, oneTreeInvers_Hops , color='g', label='OneTree Invers')
    # plt.plot(X,  oneTree_Hops, color='b', label='OneTree')
    # plt.plot(X, multipleTreesInvers_Hops, color='m', label='MultipleTrees Invers')
    # plt.plot(X, squareOne_Hops , color='y', label='SquareOne')
    # plt.plot(X, multipleTreesParallelInvers_Hops, color='c', label='MultipleTrees Parallel & Invers')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Hops")
    # plt.title("Hops, randomisiert, n = 80 , k = 6 ")

    # plt.legend(fontsize="x-small")
    # plt.show()

    #Für den Rechten Plot in dem die Wiederholungen entfernt wurden, bei denen SquareOne gescheitert ist

    # plt.subplot(221)
    # squareOne_sum_hops =  [27, 27, 28, 85, 83, 91, 32, 40, 40, 62, 78, 73, 96, 91, 64, 71, 24, 24, 24, 13, 13, 13, 13, 11]
    # multipleTreesParallelInvers_sum_hops =  [27, 27, 28, 48, 48, 79, 28, 48, 52, 69, 76, 81, 106, 101, 68, 61, 41, 37, 37, 13, 13, 13, 13, 11]
    # oneTree_sum_hops =  [27, 28, 30, 83, 75, 85, 28, 33, 33, 67, 85, 85, 105, 88, 115, 93, 94, 86, 86, 16, 16, 16, 16, 14]
    #multipleTreesInvers_sum_hops =  [27, 27, 27, 66, 66, 66, 27, 48, 48, 50, 62, 56, 113, 115, 130, 133, 126, 100, 98, 57, 57, 36, 19, 11]
    #multipleTrees_sum_hops =  [44, 43, 44, 75, 66, 67, 46, 58, 66, 66, 77, 76, 133, 131, 132, 161, 118, 117, 111, 66, 66, 61, 62, 58]
    # oneTreeInvers_sum_hops =  [27, 28, 30, 83, 75, 85, 28, 33, 33, 67, 85, 85, 99, 88, 90, 114, 97, 65, 65, 16, 16, 16, 16, 14]
    #print("MultipleTrees Sum : ", (sum(multipleTrees_sum_hops))/len(multipleTrees_sum_hops) )
    #print("MultipleTrees Invers Sum : ", (sum(multipleTreesInvers_sum_hops))/len(multipleTreesInvers_sum_hops) )
    # oneTree_count =                      [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 4, 4, 4, 4, 4]
    # multipleTreesInvers_count =          [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 4, 4, 4, 4, 4]
    # squareOne_count =                    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 4, 4, 4, 4, 4]
    # multipleTreesParallelInvers_count =  [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 4, 4, 4, 4, 4]
    # multipleTrees_count =                [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 4, 4, 4, 4, 4]
    # oneTreeInvers_count =                [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 4, 4, 4, 4, 4]

    # #um nochmal zu checken ob wirklich alle auch genau so oft wie sq1 ausgeführt werden, wurden alle wiederholungen gelöscht in denen sq1 fehlgeschlagen ist
    # #deswegen wird hier nochmal der durchschnitt über die addierten hops berechnet
    # for i in range(0,24):
    #     squareOne_sum_hops[i]  = squareOne_sum_hops[i] / oneTree_count[i]
    #     multipleTreesParallelInvers_sum_hops[i]  = multipleTreesParallelInvers_sum_hops[i] / oneTree_count[i]
    #     oneTree_sum_hops[i]  = oneTree_sum_hops[i] / oneTree_count[i]
    #     multipleTreesInvers_sum_hops[i]  = multipleTreesInvers_sum_hops[i] / oneTree_count[i]
    #     multipleTrees_sum_hops[i]  = multipleTrees_sum_hops[i] / oneTree_count[i]
    #     oneTreeInvers_sum_hops[i]  = oneTreeInvers_sum_hops[i] / oneTree_count[i]


    # plt.plot(X,  multipleTrees_sum_hops, color='r', label='MultipleTrees')
    # plt.plot(X, oneTreeInvers_sum_hops , color='g', label='OneTree Invers')
    # plt.plot(X,  oneTree_sum_hops, color='b', label='OneTree')
    # plt.plot(X, multipleTreesInvers_sum_hops, color='m', label='MultipleTrees Invers')
    # plt.plot(X, squareOne_sum_hops , color='y', label='SquareOne')
    # plt.plot(X, multipleTreesParallelInvers_sum_hops, color='c', label='MultipleTrees Parallel & Invers')

    # plt.xlabel("Failure Rate")
    # plt.ylabel("Hops")
    # plt.title("Hops ohne Fehlschläge SquareOne, randomisiert, n = 80 , k = 6 ")

    # plt.legend(fontsize="x-small")
    # plt.show()
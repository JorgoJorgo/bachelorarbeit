import matplotlib.pyplot as plt
import csv
#liest text datei
#parse csv zu array
#plott

filepath = "results/benchmark-custom-5.txt"
f = open(filepath, "r")
reader = csv.reader(f)
# Skip two header lines
next(reader)
next(reader)

data = []
for line in reader:
    [graph, size, connectivity, algorithm, index, stretch, load, hops, success, routing_computation_time, pre_computation_time] = line
    data.append({ "graph": graph, "size": int(size), "connectivity" : int(connectivity), "algorithm" : algorithm, "index": int(index), "stretch": int(stretch), "load": int(load), "hops": int(hops), "success": float(success), "routing_computation_time" : float(routing_computation_time), "pre_computation_time" : float(pre_computation_time)})

print(data)

accumulated = {
    "multiple_tree": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0},
    "one_tree": {"count": 0, "stretch": 0, "load": 0, "hops": 0, "success": 0, "routing_computation_time" : 0, "pre_computation_time" : 0}
    #... hier muss dann für jeden algorithmus den ich habe ein dict erstellt werden
}


# value for  multiple_tree


for result in data:

    #hier werden jetzt die daten nach algorithmen sortiert
    if result['algorithm'] == " MultipleTrees Tree":
        accumulated['multiple_tree']['count'] = 1 + accumulated['multiple_tree']['count']
        accumulated['multiple_tree']['stretch'] = result['stretch'] + accumulated['multiple_tree']['stretch']
        accumulated['multiple_tree']['load'] = result['load'] + accumulated['multiple_tree']['load']
        accumulated['multiple_tree']['hops'] = result['hops'] + accumulated['multiple_tree']['stretch']
        accumulated['multiple_tree']['success'] = result['success'] + accumulated['multiple_tree']['success']
        accumulated['multiple_tree']['routing_computation_time'] = result['routing_computation_time'] + accumulated['multiple_tree']['routing_computation_time']
        accumulated['multiple_tree']['pre_computation_time'] = result['pre_computation_time'] + accumulated['multiple_tree']['pre_computation_time']

    #hier müssen dann für jedes der dicts noch die daten auch aufsummiert werden

#hier müssen die algorithmen auskommentiert werden die nicht in der gelesenen benchmark.txt auftauchen
plt.bar("Multiple Tree", accumulated['multiple_tree']['hops'] /  accumulated['multiple_tree']['count'] )
#plt.bar("One Tree", accumulated['one_tree']['hops'] /  (accumulated['one_tree']['count']) )
plt.ylabel('some numbers')
plt.show()

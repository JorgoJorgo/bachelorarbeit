In diesem Repository befindet sich der Code zur Bachelorarbeit "Analyse, Verbesserung und Evaluation von baumbasierten Fast Failover Routingalgorithmen" von Georgios Karamoussanlis.
Es gelten die Infomationen der read.me aus dem ursprünglichen [fast failover](https://gitlab.cs.univie.ac.at/ct-papers/fast-failover) Framework auf dem dieses Repository basiert.

Die Ergebnisse, Dateien zu den Ausführungen und Log-Dateien aus den Plots der Arbeit sind in den ".._vs_.." Ordnern zu finden. 
Im Ordner Bsp. : "./MultipleTrees_vs_MultipleTrees_Anzahl_Mod/" sind die Log-Dateien mit "log_....txt", die Ergebnisse in "benchmark..."
und auszuführenden Dateien "...experiments_FR..".

## Anforderungen
Getestet wurde dieses Repository mit Ubuntu 22.04.
Weitere Module, welche installiert werden müssen sind:

```
pip install networkx numpy matplotlib pydot
```

## Überblick

* trees.py : enthält alle Algorithmen für die Baumbildung und ihre Hilfsfunktionen
* routing,.py : Routingalgorithmen
* benchmark_graphs: Ordner für genutzten Topologien
* results: Ordner für Ausgaben und Ergebnisse der Algorithmen
* ..._experiments.py : Experimente mit gesetzten Parametern für Ausführung bereit
* Die einzelnen Ergebnisse wurden zu Ordnern zusammengefasst, welche die benchmark, Experimente und log-Dateien für jede Failure-Rate beinhalten
* benchmark-....txt : Für jede Failure-Rate eines Experiments vorhanden. Diese Dateien können in den plotter.py eingesetzt werden indem man den Dateipfad  und Algorithmen Namen anpasst, passend zur Ergebnis-Datei.
* plots : Plots der Arbeit
* dot_to_svg.py : muss in Graphen Ordner liegen. Konvertiert dot Dateien von Graphen zu svg

Die Topologien sind zu finden unter [Rocketfuel](https://research.cs.washington.edu/networking/rocketfuel/) und [Internet topology zoo](http://www.topology-zoo.org/), diese müssen runtergeladen und in benchmark_graphs eingefügt werden.


Um einen Durchlauf des Experiments zu starten muss Folgendes eingegeben werden *und die auszuführende Datei muss im Hauptverzeichnis liegen*: 
```
python3 multiple_trees_experiments.py
```
Weitere Werte können der Ausführung mitgegeben werden um spezielle Durchläufe zu erhalten:
```
python3 multiple_trees_experiments.py (Zusätzliche Argumente : "regular", für randomisiert generierte Graphen / "zoo", für Topology-Zoo / "custom", für eigene Graphen)
```

Um eigene Experimente zu erstellen steht die benchmark_template.py bereit als Vorlage.

## Ausführung eigener Topologien
Um eigene Topologien zu nutzen müssen diese erst in (./objective_function_experiments.py) "create_custom_graph()" mit Hilfe von NetworkX definiert werden.
Dort erfolgt auch die Bestimmung der fehlerhaften Kanten.
Anschließend muss folgende Funktion in die Experiment Datei eingefügt und aufgerufen werden mit dem "custom" Paramater: 

```
def run_custom(out=None, seed=0, rep=5):

    original_params = [n, rep, k, samplesize, f_num, seed, name]
    graphs = []
    fails = []

    graph1, fail1 = create_custom_graph()
    graphs.append(graph1)
    fails.append(fail1) 

    for i in range(0, len(graphs)):
        random.seed(seed)
        kk = 5
        g = graphs[i]
        g.graph['k'] = kk
        nn = len(g.nodes())
        mm = len(g.edges())
        ss = min(int(nn / 2), samplesize)
        fn = min(int(mm / 2), f_num)
        fails = fails[i]
        g.graph['fails'] = fails
        set_parameters([nn, rep, kk, ss, fn, seed, name + "CUSTOM"])
        shuffle_and_run(g, out, seed, rep, graphs[i])
        set_parameters(original_params)
```


## Darstellen der Ergebnisse

Für die Darstellung der Ergebnisse ist die Datei "plotter.py" zuständig. Diese Datei iteriert über benchmark-Dateien (filepath) und sammelt die Ergebnisse der 2 vorher definierten Algorithmen (TitleAlgo1 & TitleAlgo2). Dabei müssen die TitleAlgos so bennant werden, wie sie in den benchmark-Dateien zu finden sind. Es können nur jeweils 2 Algorithmen gleichzeitig evaluiert werden. Durch Änderung an den For-Schleifen-Parametern kann auch die Anzahl an Dateien geändert werden, die für die Evaluation berücksichtigt werden sollen. Die Ausgabe findet in der Konsole statt.
Im unteren Teil dieser Datei sind auch die Plots der Arbeit zu finden, diese sind auskommentiert und mit der Variable "plotfig" ausgeblendet. Es ist [matplotlib](https://matplotlib.org/stable/users/installing/index.html#installing-an-official-release) notwendig. 


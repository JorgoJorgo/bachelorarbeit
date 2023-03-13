In diesem Repository befindet sich der Code zur Bachelorarbeit "Analyse, Verbesserung und Evaluation von baumbasierten Fast Failover Routingalgorithmen" von Georgios Karamoussanlis.
Es gelten die Infomationen der read.me aus dem ursprünglichen [fast failover](https://gitlab.cs.univie.ac.at/ct-papers/fast-failover) Framework auf dem dieses Repository basiert.

Die Ergebnisse, Dateien zu den Ausführungen und Log-Dateien aus den Plots der Arbeit sind in den ".._vs_.." Ordnern zu finden. Im Ordner Bsp. : "./MultipleTrees_vs_MultipleTrees_Anzahl_Mod/" sind die Log-Dateien mit "log_....txt", die Ergebnisse in "benchmark..." und auszuführenden Dateien "...experiments_FR..".

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
python3 multiple_trees_experiments.py (regular, für randomisiert generierte Graphen /zoo, für Topology-Zoo)
```

Um eigene Experimente zu erstellen steht die benchmark_template.py bereit als Vorlage.

## Darstellen der Ergebnisse

Für die Darstellung der Ergebnisse ist die Datei "plotter.py" zuständig. Diese Datei iteriert über benchmark-Dateien (filepath) und sammelt die Ergebnisse der 2 vorher definierten Algorithmen (TitleAlgo1 & TitleAlgo2). Dabei müssen die TitleAlgos so bennant werden, wie sie in den benchmark-Dateien zu finden sind. Es können nur jeweils 2 Algorithmen gleichzeitig evaluiert werden. Durch Änderung an den For-Schleifen-Parametern kann auch die Anzahl an Dateien geändert werden, die für die Evaluation berücksichtigt werden sollen. Die Ausgabe findet in der Konsole statt.
Im unteren Teil dieser Datei sind auch die Plots der Arbeit zu finden, diese sind auskommentiert und mit der Variable "plotfig" ausgeblendet. Es ist [matplotlib](https://matplotlib.org/stable/users/installing/index.html#installing-an-official-release) notwendig. 


In diesem Repository befindet sich der Code zur Bachelorarbeit "Analyse, Verbesserung und Evaluation von baumbasierten Fast Failover Routingalgorithmen" von Georgios Karamoussanlis.
Es gelten die Infomationen der read.me aus dem ursprünglichen [fast failover](https://gitlab.cs.univie.ac.at/ct-papers/fast-failover) Framework auf dem dieses Repository basiert.


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


Um einen Durchlauf des Experiments zu starten:
```
python3 multiple_trees_experiments.py
```
Weitere Werte können der Ausführung mitgegeben werden um spezielle Durchläufe zu erhalten:
```
python3 multiple_trees_experiments.py (regular, für randomisiert generierte Graphen /zoo, für Topology-Zoo)
```

Um eigene Experimente zu erstellen steht die benchmark_template.py bereit als Vorlage.



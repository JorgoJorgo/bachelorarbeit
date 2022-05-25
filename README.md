This repository contains the source code for the experiments in the following papers

* [SRDS 2019: Improved Fast Rerouting Using Postprocessing](https://ieeexplore.ieee.org/document/9049550) [(Journal Version)](https://ieeexplore.ieee.org/document/9102391)
* [DSN 2019: Bonsai: Efficient Fast Failover Routing Using Small Arborescences](https://ieeexplore.ieee.org/document/8809517)
* [INFOCOM 2019: CASA: Congestion and Stretch Aware Static Fast Rerouting](https://ieeexplore.ieee.org/document/8737438)
* [INFOCOM 2021: Grafting Arborescences for Extra Resilience of Fast Rerouting Schemes](https://ieeexplore.ieee.org/document/9488782)

by [Klaus-Tycho Foerster](https://ktfoerster.github.io/), [Andrzej Kamisinski](https://home.agh.edu.pl/~andrzejk/), [Yvonne-Anne Pignolet](http://yvonneanne.pignolet.ch/), [Stefan Schmid](https://www.inet.tu-berlin.de/menue/people/profs0/stefan/), [Gilles Tredan](https://homepages.laas.fr/gtredan/). 

Our individual webpages contain the Authors' Original Manuscripts in case you do not have access to the IEEE Xplore Digital Library.

We are indebted to Ilya Nikolaevskiy, Aalto University, Finland, on whose source code for [this paper](
https://ieeexplore.ieee.org/document/7728092) we based our implementation.

If you use this code, please cite the corresponding paper(s).

## Bibtex
```
@inproceedings{SRDS19-FRR,
  author    = {Klaus-Tycho Foerster and Andrzej Kamisinski and
               Yvonne-Anne Pignolet and Stefan Schmid and Gilles Tr{\'{e}}dan},
  title     = {Improved Fast Rerouting Using Postprocessing},
  booktitle = {{SRDS}},
  pages     = {173--182},
  publisher = {{IEEE}},
  year      = {2019}
}

@article{TDSC22-FRR,
  author    = {Klaus-Tycho Foerster and Andrzej Kamisinski and
               Yvonne-Anne Pignolet and Stefan Schmid and Gilles Tr{\'{e}}dan},
  title     = {Improved Fast Rerouting Using Postprocessing},
  journal   = {{IEEE} Trans. Dependable Secur. Comput.},
  volume    = {19},
  number    = {1},
  pages     = {537--550},
  year      = {2022}
}

@inproceedings{DSN19-FFR,
  author    = {Klaus-Tycho Foerster and Andrzej Kamisinski and
               Yvonne-Anne Pignolet and Stefan Schmid and Gilles Tr{\'{e}}dan},
  title     = {Bonsai: Efficient Fast Failover Routing Using Small Arborescences},
  booktitle = {{DSN}},
  pages     = {276--288},
  publisher = {{IEEE}},
  year      = {2019}
}

@inproceedings{INFOCOM19-FFR,
  author    = {Klaus-Tycho Foerster and Yvonne-Anne Pignolet and
               Stefan Schmid and Gilles Tr{\'{e}}dan},
  title     = {{CASA:} Congestion and Stretch Aware Static Fast Rerouting},
  booktitle = {{INFOCOM}},
  pages     = {469--477},
  publisher = {{IEEE}},
  year      = {2019}
}

@inproceedings{INFOCOM21-FFR,
  author    = {Klaus-Tycho Foerster and Andrzej Kamisinski and
               Yvonne-Anne Pignolet and Stefan Schmid and Gilles Tr{\'{e}}dan},
  title     = {Grafting Arborescences for Extra Resilience of Fast Rerouting Schemes},
  booktitle = {{INFOCOM}},
  pages     = {1--10},
  publisher = {{IEEE}},
  year      = {2021}
}
```
## Overview

* benchmark_graphs: directory to be filled with network topologies used in the experiments
* results: directory to which csv and other output files are written

* arborescence.py: arborescence decomposition and helper algorithms
* routing_stats.py: routing algorithms, simulation and statistic framework
* objective_function_experiments.py: objective functions, independence and SRLG experiments
* srds2019_experiments.py: experiments for SRDS 2019 paper
* dsn2019_experiments.py: experiments for DSN 2019 paper
* infocom2019_experiments.py: experiments for Infocom 2019 paper
* infocom2021_experiments.py: experiments for Infocom 2019 paper
* benchmark_template.py: template to compare algorithms

For some experiments topologies from [Rocketfuel](https://research.cs.washington.edu/networking/rocketfuel/) and the [Internet topology zoo](http://www.topology-zoo.org/) networks need to downloaded and copied into the benchmark_graphs directory.

To e.g. run the experiments for the SRDS paper, execute the corresponding python file:
```
python srds2019_experiments.py
```
With additional arguments the experiments can be customised (see main function of the python file). E.g., 
```
python srds2019_experiments.py all 6 1
```
executes 1 repetition of all SRDS experiments with seed 6. Similarly, the experiments for the other papers can be executed. 

If you want to implement and compare additional algorithms, check out benchmark_template.py. It contains examples on how to compare different algorithms and assigns them a score.

In case of questions please send an email to Yvonne-Anne Pignolet, ya at last name dot ch.

## Addendum

August 2020: Ioan Marian Dan, Diana-Alexandra Deac, Daniel Alejandro Robles, Alhamzeh Ismail provided an improved version of a randomized algorithm in RouteTryLinkToDestinationFirstPR.py.

December 2020: Paula-Elena Gheorghe added an implementation of the algorithm described in https://cpsc.yale.edu/sites/default/files/files/tr1454.pdf, see FeigenbaumAlgo.py

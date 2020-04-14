This repository contains the source code for the experiments in the following three papers

* [SRDS 2019: Improved Fast Rerouting Using Postprocessing](https://www.univie.ac.at/ct/stefan/srds19failover.pdf)
* [DSN 2019: Bonsai: Efficient Fast Failover Routing Using Small Arborescences](https://www.univie.ac.at/ct/stefan/dsn19.pdf)
* [Infocom 2019: CASA: Congestion and Stretch Aware Static Fast Rerouting](https://www.univie.ac.at/ct/stefan/infocom2019e.pdf)

by Klaus-Tycho Foerster, Andrzej Kamisinski, Yvonne-Anne Pignolet, Stefan Schmid, Gilles Tredan

We are indebted to Ilya Nikolaevskiy, Aalto University, Finland, on whose source code for [this paper](
http://www.dia.uniroma3.it/~compunet/www/docs/chiesa/Resiliency-ToN.pdf) we based our implementation.

If you use this code, please cite the corresponding paper(s).

## Bibtex
```
@INPROCEEDINGS{srds19foerster,
  author = {Klaus-Tycho Foerster and Andrzej Kamisinski and Yvonne-Anne Pignolet and Stefan Schmid and Gilles Tredan},
  title = {Improved Fast Rerouting Using Postprocessing},
  booktitle = {Proc. 38th International Symposium on Reliable Distributed Systems (SRDS)},
  year = {2019},
}

@INPROCEEDINGS{dsn19foerster,
  author = {Klaus-Tycho Foerster and Andrzej Kamisinski and
  Yvonne-Anne Pignolet and Stefan Schmid and Gilles Tredan},
  title = {Bonsai: Efficient Fast Failover Routing Using Small Arborescences},
  booktitle = {Proc. 49th IEEE/IFIP International Conference on Dependable Systems and Networks (DSN)},
  year = {2019},
}

@INPROCEEDINGS{infocom19foerster,
  author = {Klaus-Tycho Foerster and Yvonne-Anne Pignolet and Stefan Schmid and Gilles Tredan},
  title = {CASA: Congestion and Stretch Aware Static Fast Rerouting},
  booktitle = {Proc. IEEE INFOCOM},
  year = {2019},
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

For some experiments topologies from [Rocketfuel](https://research.cs.washington.edu/networking/rocketfuel/) and the [Internet topology zoo](http://www.topology-zoo.org/) networks need to downloaded and copied into the benchmark_graphs directory.

To run the experiments for the SRDS paper, execute the corresponding python file:
```
python srds2019_experiments.py
```
With additional arguments the experiments can be customised (see main function of the python file). E.g., 
```
python srds2019_experiments.py all 6 1
```
executes 1 repetition of all SRDS experiments with seed 6. Similarly, the experiments for the other papers can be executed. In case of questions please send an email to Yvonne-Anne Pignolet, ya at last name dot ch.
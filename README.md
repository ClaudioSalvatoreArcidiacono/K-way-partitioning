# K-way-partitioning
Installation
____________

The following software packages are necessary for running the program :

Networkx (Library for the creation and manipulation of graphs)
    pip install networkx
    or
    Installing with Anaconda
    conda install -c anaconda networkx=1.11

Scipy (Library that contains modules for linear algebra)
    pip install scipy

Metis (Wrapper for the METIS library for partitioning graphs)
    pip install metis


In order to simplify package management and deployment you can install Anaconda :

https://www.continuum.io/anaconda-overview

With Anaconda you can create the envirorment that we used to develop the application by simply executing the following
command :

conda env create -f environment.yml

To activate the envirorment :
source activate Advanced-Algorithms-env


Execution
____________
To execute the program :

python ./mlkp.py [-h] [-f FILE | -r DEGREE N_NODES] k

k is the number of partitions
-f and -r are exclusive, either you indicate the FILE path where to read the graph or you indicate the
DEGREE and the N_NODES (number of nodes) in order to generate a random graph with the previous criteria.

Output
____________
The program creates a file containing the partitioning dictionary (node name , partition)
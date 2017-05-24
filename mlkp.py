import networkx as nx
import argparse
import time
import metis
from coarsening import coarse
from uncoarsening import uncoarse
from utils import calculate_edge_cut
from utils import read_graph
from utils import random_graph

def k_way_partitioning(k:int,g:nx.Graph):

    # COARSENING
    start = time.time()
    print('starting coarsening phase')
    graphs_history , coarsening_history = coarse(g,k=k)
    end_coarsening = time.time()
    m, s = divmod((end_coarsening - start), 60)
    enlapsed_time = "%d minutes and %f seconds" % (m, s)
    print('finished coarsening after ', graphs_history.__len__(), ' steps in ', enlapsed_time)

    # INITIAL PARTITIONING
    edge_cut , initial_partitioning = metis.part_graph(graphs_history[-1], k, recursive=True)

    # UNCOARSENING
    start_uncoarsening = time.time()
    print('starting uncoarsening phase')
    final_partitioning = uncoarse(graphs_history,coarsening_history,initial_partitioning,k)
    end = time.time()
    m, s = divmod((end - start_uncoarsening), 60)
    enlapsed_time = "%d minutes and %f seconds" % (m, s)
    print('finished un-coarsening in', enlapsed_time)

    edge_cut = calculate_edge_cut(graphs_history[0],final_partitioning)
    print('the final edge cut is',edge_cut)

    m, s = divmod((end - start), 60)
    enlapsed_time = "%d minutes and %f seconds" % (m, s)
    print('the overall time is',enlapsed_time)

    # THE RESULT OBTAINED WITH METIS
    start_meth = time.time()
    edge_cut , metis_partitioning = metis.part_graph(graphs_history[0], k)
    end_meth = time.time()
    m, s = divmod((end_meth - start_meth), 60)
    enlapsed_time = "%d minutes and %f seconds" % (m, s)
    print('the edge cut obtained with metis is ',edge_cut)
    print('the time taken by metis was ', enlapsed_time)


parser = argparse.ArgumentParser(description='Partition the vertices of a graph in k roughly '
                                             'equal partitions such that the number of edges connecting vertices in different partitions'
                                             'is minimized')

parser.add_argument("k", help="The number of partitions", type = int)
group = parser.add_mutually_exclusive_group()
group.add_argument("-f", "--file", help="The file containing the graph to elaborate, if not specified a random graph is generated", type = str)
group.add_argument("-r", "--random", nargs = 2, metavar = ('DEGREE','N_NODES'), help="Generate a random graph with degree and number of nodes specified ",
                   type = int,default=[30,10000]) #default value for degree and number of nodes of the random generated graph

args = parser.parse_args()

if(args.file != None):
    g = read_graph(args.file)
else:
    g = random_graph(args.random[0],args.random[1])

k_way_partitioning(args.k,g)
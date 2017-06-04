import networkx as nx
import time
import metis
from coarsening import coarse
from uncoarsening import uncoarse
from utils import calculate_edge_cut
from utils import output_file
import spectral_bisection

NPARTS = 10

def read_graph (path) :
    g1 = nx.read_adjlist(path)
    g = nx.Graph()
    print('reading graph')
    for i in g1.nodes():
        g.add_node(i, {'weight': 1})
    for edge in g1.edges():
        if(edge[0]!=edge[1]):
            g.add_edge(edge[0], edge[1], {'weight': 1})
    return g

def random_graph(degree, nodes):
    print('generating a random graph')
    g1 = nx.random_regular_graph(degree,nodes)
    g = nx.Graph()
    for i in g1.nodes():
        g.add_node(i, {'weight': 1})
    for edge in g1.edges():
        if (edge[0] != edge[1]):
            g.add_edge(edge[0], edge[1], {'weight': 1})
    return g

#g = read_graph('4elt.txt')

g=random_graph(200,1000)
# COARSENING
start = time.time()
print('starting coarsening phase')
graphs_history , coarsening_history = coarse(g,k=NPARTS)
end_coarsening = time.time()
m, s = divmod((end_coarsening - start), 60)
enlapsed_time = "%d minutes and %f seconds" % (m, s)
print('finished coarsening after ', graphs_history.__len__(), ' steps in ', enlapsed_time)

# INITIAL PARTITIONING
#edge_cut , initial_partitioning = metis.part_graph(graphs_history[-1], NPARTS, recursive=True)
print('starting initial partitioning phase')
start_init_part = time.time()

initial_partitioning = spectral_bisection.initial_partitioning(graphs_history[-1],NPARTS)

end_init_part = time.time()
m, s = divmod((end_init_part - start_init_part), 60)
enlapsed_time = "%d minutes and %f seconds" % (m, s)
print('finished initial partitioning in ', enlapsed_time)

# UNCOARSENING
start_uncoarsening = time.time()
print('starting uncoarsening phase')
final_partitioning = uncoarse(graphs_history,coarsening_history,initial_partitioning,NPARTS)
end = time.time()
m, s = divmod((end - start_uncoarsening), 60)
enlapsed_time = "%d minutes and %f seconds" % (m, s)
print('finished un-coarsening in', enlapsed_time)


output_file(final_partitioning)

edge_cut = calculate_edge_cut(graphs_history[0],final_partitioning)
print('the final edge cut is',edge_cut)

m, s = divmod((end - start), 60)
enlapsed_time = "%d minutes and %f seconds" % (m, s)
print('the overall time is',enlapsed_time)

# THE RESULT OBTAINED WITH METIS
start_meth = time.time()
edge_cut , metis_partitioning = metis.part_graph(graphs_history[0], NPARTS)
end_meth = time.time()
m, s = divmod((end_meth - start_meth), 60)
enlapsed_time = "%d minutes and %f seconds" % (m, s)
print('the edge cut obtained with metis is ',edge_cut)
print('the time taken by metis was ', enlapsed_time)

import networkx as nx
import time
import metis
from Coarsening import coarse
from Uncoarsening import uncoarse
from Utils import calculate_edge_cut

NPARTS = 8

def read_graph () :
    g1 = nx.random_regular_graph(10, 2000)
    g = nx.Graph()
    print('reading graph')
    for i in g1.nodes():
        g.add_node(i, {'weight': 1})
    for edge in g1.edges():
        g.add_edge(edge[0], edge[1], {'weight': 1})

    return g


g = read_graph()
# COARSENING
start = time.time()
graphs_history , coarsening_history = coarse(g,k=NPARTS)
end = time.time()
m, s = divmod((end - start), 60)
enlapsed_time = "%d minutes and %02d seconds" % (m, s)
print('finished coarsening after ', graphs_history.__len__(), ' steps in ', enlapsed_time)

# INITIAL PARTITIONING
edge_cut , initial_partitioning = metis.part_graph(graphs_history[-1], NPARTS, recursive=True)

# UNCOARSENING
final_partitioning = uncoarse(graphs_history,coarsening_history,initial_partitioning,NPARTS)
print('finished un-coarsening')
edge_cut = calculate_edge_cut(graphs_history[0],final_partitioning)
print('the final edge cut is',edge_cut)

# THE RESULT OBTAINED WITH METIS
edge_cut , metis_partitioning = metis.part_graph(graphs_history[0], NPARTS)
print('the edge cut obtained with metis is ',edge_cut)

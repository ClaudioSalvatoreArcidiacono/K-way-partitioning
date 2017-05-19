import networkx as nx
from Matching import HEM
import time
import metis

NPARTS = 8


def contract_edge(graph: nx.Graph, edge: tuple) -> nx.Graph :
    """Returns the graph that results from contracting the specified edge.

    Edge contraction identifies the two endpoints of the edge as a single node
    incident to any edge that was incident to the original two nodes. A graph
    that results from edge contraction is called a *minor* of the original
    graph. Both the nodes and edges of the graph G must contain an attribute 'weight'
    after the contraction the weights of the nodes and the edges in the contraction is updated

    Parameters
    ----------
    G : NetworkX graph
       The graph whose edge will be contracted.

    edge : tuple
       Must be a pair of nodes in ``G``.


    Returns
    -------
    Networkx graph
        the graph that results from contracting the specified edge.

    """
    vtx1 = edge[0]
    vtx2= edge [1]
    coarsened_graph = nx.contracted_edge(graph, edge, self_loops=False)
    w = graph.node[vtx1]['weight'] + graph.node[vtx2]['weight']
    coarsened_graph.add_node(vtx1,{'weight':w})
    adj_vtx1 = graph.neighbors(vtx1)
    adj_vtx2 = graph.neighbors(vtx2)
    common_vtxs = set(adj_vtx1).intersection(adj_vtx2)

    for vtx in common_vtxs :
        w1 = graph[vtx1][vtx]['weight']
        w2 = graph[vtx2][vtx]['weight']
        coarsened_graph[vtx1][vtx]['weight'] =  w1 + w2

    return coarsened_graph





def coarse (graph: nx.Graph, k=8, min_shrink=0.8, initial_partition_size=15) :
    """Returns the graph that results from a coarsening process.



        Parameters
        ----------
        G : NetworkX graph
           The graph that will be coarsened. It is unchanged after the contraction

        k : int
           The number of partitions we intend to partition our graph.

        min_shrink : float
            If the algorithm is not able to coarse for more than min_shrink % the procedure is stopped

        initial_partition_size : int
            The procedure will stop if number of nodes <= k * initial_partition_size
            so this parameter is useful to know when to stop



        Returns
        -------
        list(Networkx graph)
            the list contains the graph at each step:
            new graph object of the same type as ``G`` (leaving ``G`` unmodified)
            resulting from the coarsening process of G, G-1 and so on

        list(list(tuple))
            a list contains the contractions that were made at each step
            G-1 -> unfolding (G) -> G

    """
    graphs_history = [graph]
    prec_step_graph = graph
    num_nodes = graph.number_of_nodes()
    coarsening_history= list()
    while num_nodes > k * initial_partition_size :

        print('current number of nodes: ',num_nodes , 'edges:',prec_step_graph.number_of_edges())
        matching = HEM(prec_step_graph)

        coarsened_graph = prec_step_graph

        for edge in matching :
            coarsened_graph = contract_edge(coarsened_graph,edge)

        graphs_history.append(coarsened_graph)
        coarsening_history.append(matching)



        prec_nodes = prec_step_graph.number_of_nodes()
        num_nodes = coarsened_graph.number_of_nodes()

        prec_step_graph = coarsened_graph

        if prec_nodes * min_shrink < num_nodes:
                break

    print('finished to coarse, num nodes: ', num_nodes, 'edges:', prec_step_graph.number_of_edges())
    return graphs_history , coarsening_history




g1 = nx.random_regular_graph(2, 500)
g = nx.Graph()
print('reading graph')
for i in g1.nodes():
    g.add_node(i, {'weight': 1})
for edge in g1.edges():
    g.add_edge(edge[0], edge[1], {'weight': 1})
start = time.time()
graphs_history , coarsening_history = coarse(g,k=NPARTS)
end = time.time()
m, s = divmod((end - start), 60)
enlapsed_time = "%d minutes and %02d seconds" % (m, s)
print('finished coarsening after ', graphs_history.__len__(), ' steps in ', enlapsed_time)




edge_cut , initial_partitioning = metis.part_graph(graphs_history[-1], NPARTS, recursive=True)





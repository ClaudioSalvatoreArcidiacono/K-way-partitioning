import networkx as nx
from matching import HEM
from itertools import chain


def contracted_nodes(G, u, v, self_loops=True):
    """Returns the graph that results from contracting ``u`` and ``v``.

    Node contraction identifies the two nodes as a single node incident to any
    edge that was incident to the original two nodes.

    Parameters
    ----------
    G : NetworkX graph
       The graph whose nodes will be contracted.

    u, v : nodes
       Must be nodes in ``G``.

    self_loops : Boolean
       If this is ``True``, any edges joining ``u`` and ``v`` in ``G`` become
       self-loops on the new node in the returned graph.

    Returns
    -------
    Networkx graph
       the graph object of the same type as ``G`` (leaving ``G`` unmodified)
       with ``u`` and ``v`` identified in a single node. The right node ``v``
       will be merged into the node ``u``, so only ``u`` will appear in the
       returned graph.

    Examples
    --------
    Contracting two nonadjacent nodes of the cycle graph on four nodes `C_4`
    yields the path graph (ignoring parallel edges)::


    See also
    --------
    contracted_edge
    quotient_graph

    Notes
    -----
    This function is also available as ``identified_nodes``.
    """
    H = G
    if H.is_directed():
        in_edges = ((w, u, d) for w, x, d in G.in_edges(v, data=True)
                    if self_loops or w != u)
        out_edges = ((u, w, d) for x, w, d in G.out_edges(v, data=True)
                     if self_loops or w != u)
        new_edges = chain(in_edges, out_edges)
    else:
        new_edges = ((u, w, d) for x, w, d in G.edges(v, data=True)
                     if self_loops or w != u)
    v_data = H.node[v]
    H.remove_node(v)
    H.add_edges_from(new_edges)
    if 'contraction' in H.node[u]:
        H.node[u]['contraction'][v] = v_data
    else:
        H.node[u]['contraction'] = {v: v_data}
    return H

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


    w = graph.node[vtx1]['weight'] + graph.node[vtx2]['weight']
    adj_vtx1 = graph.neighbors(vtx1)
    adj_vtx2 = graph.neighbors(vtx2)
    common_vtxs = set(adj_vtx1).intersection(adj_vtx2)

    common_vtxs_weight = {}
    for vtx in common_vtxs :
        w1 = graph[vtx1][vtx]['weight']
        w2 = graph[vtx2][vtx]['weight']
        common_vtxs_weight[vtx] = w1 + w2

    coarsened_graph = contracted_nodes(graph, vtx1, vtx2, self_loops=False)
    coarsened_graph.node[vtx1]['weight'] = w

    for vtx in common_vtxs :
        coarsened_graph[vtx1][vtx]['weight'] =  common_vtxs_weight[vtx]
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

        coarsened_graph = prec_step_graph.copy()

        for edge in matching :
            contract_edge(coarsened_graph, edge)

        graphs_history.append(coarsened_graph)
        coarsening_history.append(matching)



        prec_nodes = prec_step_graph.number_of_nodes()
        num_nodes = coarsened_graph.number_of_nodes()

        prec_step_graph = coarsened_graph

        if prec_nodes * min_shrink < num_nodes:
                break

    print('finished to coarse, num nodes: ', num_nodes, 'edges:', prec_step_graph.number_of_edges())
    return graphs_history , coarsening_history







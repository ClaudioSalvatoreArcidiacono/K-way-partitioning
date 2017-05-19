import networkx as nx
import random as rnd


def HEM(graph : nx.Graph):
    nodes = graph.nodes()
    rnd.shuffle(nodes)
    matched = dict([(n ,'unmatched') for n in nodes])
    max_matching = list()
    for node in nodes :

        if (matched[node] == 'matched'):
            continue

        adj_nodes = graph.neighbors(node)
        rnd.shuffle(adj_nodes)

        max_adj_node = None
        max_weight = 0
        for adj_node in adj_nodes:

            if (matched[adj_node] == 'matched'):
                continue

            adj_edge_weight = graph[node][adj_node]['weight']

            if (adj_edge_weight > max_weight) :
                max_adj_node = adj_node
                max_weight = adj_edge_weight

        if ( max_adj_node != None ) :
            max_matching.append((node,max_adj_node))
            matched[node]='matched'
            matched[max_adj_node]='matched'

    return max_matching

import networkx as nx

def calculate_edge_cut(graph:nx.Graph, partitioning:dict) :
    edge_cut = 0

    for edge in graph.edges():

        if partitioning[edge[1]] != partitioning[edge[0]]:
            edge_cut += graph[edge[0]][edge[1]]['weight']

    return edge_cut
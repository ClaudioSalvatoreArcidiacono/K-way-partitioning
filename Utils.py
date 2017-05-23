import networkx as nx

def calculate_edge_cut(graph:nx.Graph, partitioning:dict) :
    edge_cut = 0

    for edge in graph.edges():

        if partitioning[edge[1]] != partitioning[edge[0]]:
            edge_cut += 1

    return edge_cut

def parse_input_file (path) :
    input = open(path,'r')
    output= open('parsed_' + path,mode='w')
    i = 0
    for line in input.readlines()[1:]:
        output.write(str(i)+line)
        i += 1

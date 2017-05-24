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

def read_graph (path) :
    g1 = nx.read_adjlist(path)
    g = nx.Graph()
    print('reading graph in ' + path)
    for i in g1.nodes():
        g.add_node(i, {'weight': 1})
    for edge in g1.edges():
        if(edge[0]!=edge[1]):
            g.add_edge(edge[0], edge[1], {'weight': 1})
    return g

def random_graph(degree, nodes):
    print('generating a random graph: degree %d , nodes %d' %(degree,nodes))
    g1 = nx.random_regular_graph(degree,nodes)
    g = nx.Graph()
    for i in g1.nodes():
        g.add_node(i, {'weight': 1})
    for edge in g1.edges():
        if (edge[0] != edge[1]):
            g.add_edge(edge[0], edge[1], {'weight': 1})
    return g
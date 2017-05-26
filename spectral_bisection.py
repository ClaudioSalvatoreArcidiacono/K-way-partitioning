import networkx as nx
import numpy as np
from numpy import linalg as LA


def get_adj_matrix(graph : nx.Graph) -> np.array :
    shape = (graph.number_of_nodes(),graph.number_of_nodes())
    adj_matrix = np.zeros(shape=shape,dtype=np.float)
    nodes =graph.nodes()
    for i_index in range(nodes.__len__()) :
        node = nodes[i_index]
        for neighbor in graph.neighbors(nodes[i_index]):
            j_index = nodes.index(neighbor)
            adj_matrix[i_index][j_index] = graph[node][neighbor]['weight']

    return adj_matrix

def get_laplacian_matrix(graph : nx.Graph) -> np.array:

    adj_matrix = get_adj_matrix(graph)

    D = get_D_matrix(graph)

    return np.subtract(D,adj_matrix)


def get_D_matrix(graph):
    shape = (graph.number_of_nodes(), graph.number_of_nodes())
    D = np.zeros(shape, dtype=np.float)
    nodes = graph.nodes()
    for i_index in range(nodes.__len__()):
        node = nodes[i_index]
        D[i_index][i_index] = graph.node[node]['weight']
    return D


def bisect(laplacian : np.array,my_nodes,partitioning,current_partition,k):

    if(current_partition>=k):
        return
    ix=np.ix_(my_nodes,my_nodes)
    my_lap = laplacian[ix]
    eigenvalues , eigenvectors =LA.eig(my_lap)
    second_smallest_eigenvalue_index = np.argsort(eigenvalues)[1]
    bisection = eigenvectors[:,second_smallest_eigenvalue_index]
    mask = bisection >=0

    partitioning[my_nodes[mask]]+=current_partition

    bisect(laplacian,my_nodes[mask], partitioning, current_partition * 2, k)
    other_partition=np.logical_not(mask)
    bisect(laplacian, my_nodes[other_partition], partitioning, current_partition * 2, k)



def initial_partitioning(graph: nx.Graph,k=8) :
    laplacian = get_laplacian_matrix(graph)
    current_partition = 1
    num_nodes = graph.number_of_nodes()
    partitioning = np.zeros(shape=num_nodes,dtype=np.int)
    my_nodes = np.arange(laplacian.shape[0])

    bisect(laplacian,my_nodes,partitioning,current_partition,k)

    return partitioning


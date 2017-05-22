import networkx as nx
import random as rnd
import numpy as np
from Utils import calculate_edge_cut

CONVERGENCE_PERCENTAGE = 1.0


def project_back(contracted_edges:list, partitioning: dict) -> dict :

    for edge in contracted_edges:
        partitioning[edge[1]]=partitioning[edge[0]]


    return partitioning

def weight_partitions(graph : nx.Graph, partitioning : dict, k=8):
    partitions_weights = list(np.zeros(k))
    for node in graph.nodes():
        partition = partitioning[node]
        node_weight = graph.node[node]['weight']
        partitions_weights[partition] += node_weight

    return partitions_weights


def refine(graph : nx.Graph, partitioning : dict, partitions_weights : list, W_min, W_max, k=8, C=1.03) -> [dict , list ]:
    nodes = graph.nodes()
    rnd.shuffle(nodes)
    for node in nodes:

        node_partition = partitioning[node]
        partition_weight = partitions_weights[node_partition]
        node_weight = graph.node[node]['weight']

        if partition_weight - node_weight < W_min:
            # if the partition without the node doesn't respect the balancing condition don't try to swap
            continue

        # calculate internal degree (ID) and external degree (ED)
        # from the paper we have that N' = ED.keys()
        ID = 0.0
        ED = {}
        for adj in graph.neighbors(node):
            adj_partition = partitioning[adj]
            adj_part_weight = partitions_weights[adj_partition]
            if adj_partition == node_partition:
                # if the adj node is from the same partition update the internal degree
                ID += graph[node][adj]['weight']

            elif  adj_part_weight + node_weight <= W_max:
                # otherwise if is swappable to that partition update the external degree
                if adj_partition not in ED.keys():
                    ED[adj_partition] = graph[node][adj]['weight']
                else:
                    ED[adj_partition] += graph[node][adj]['weight']

        if ED.__len__() == 0:
            # if there aren't any swappable partitions
            # try another node
            continue

        max_ED = max(ED.values())
        max_partitions = []

        for e_d in ED.items():
            if max_ED == e_d[1] :
                max_partitions.append(e_d[0])

        if ID < max_ED :
            max_balance = 0
            best_partition = max_partitions[0]
            for partition in max_partitions:
                if partitions_weights[node_partition] - partitions_weights[partition] > max_balance:
                    max_balance = partitions_weights[node_partition] - partitions_weights[partition]
                    best_partition = partition

            # Swap node partition
            partitions_weights[node_partition] -= node_weight
            partitions_weights[best_partition] += node_weight
            partitioning[node] = best_partition

        elif  ID == max_ED:
            more_balanced = False
            max_balance = 0
            best_partition = max_partitions[0]
            for partition in max_partitions:
                if partitions_weights[node_partition] - partitions_weights[partition] > max_balance:
                    max_balance = partitions_weights[node_partition] - partitions_weights[partition]
                    best_partition = partition
                    more_balanced = True


            if more_balanced:
                # Swap node partition
                partitions_weights[node_partition] -= node_weight
                partitions_weights[best_partition] += node_weight
                partitioning[node] = best_partition


    return partitioning,partitions_weights


def uncoarse(graphs_history:list, coarsening_history:list, initial_partitioning:list, k=8, C=1.03)-> dict:

    total_nodes = graphs_history[0].number_of_nodes()
    W_min = 0.9 * total_nodes / k
    W_max = C * total_nodes / k
    steps = graphs_history.__len__()

    partitioning = {}
    nodes = graphs_history[-1].number_of_nodes()

    for i in range(nodes):
        node = graphs_history[-1].nodes()[i]
        partitioning[node]=initial_partitioning[i]

    partitions_weights = weight_partitions(graphs_history[-1],partitioning,k)
    for step in reversed(range(0,steps-1)) :
        print('uncoarsening at step',(steps -1 -step),'/',(steps-1))
        partitioning = project_back(coarsening_history[step],partitioning)

        prec_edge_cut = calculate_edge_cut(graphs_history[step], partitioning)
        while True:
            partitioning,partitions_weights = refine(
                                            graph=graphs_history[step],
                                            partitioning=partitioning,
                                            partitions_weights = partitions_weights,
                                            W_min = W_min,
                                            W_max = W_max)
            actual_edge_cut = calculate_edge_cut(graphs_history[step], partitioning)
            if prec_edge_cut <= actual_edge_cut * 1.02:
                # Refine until convergence, until we are not able to have a solution better than the
                # precedent from a factor Convergence percentage
                break
            prec_edge_cut = actual_edge_cut




    return partitioning

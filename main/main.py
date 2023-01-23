import networkx as nx
import copy
import random
import matplotlib.pyplot as plt
from experiments import *




"""
Social Network Updates 
by Jirmaine Tan

This program is able to perform graph network updates
"""
if __name__ == "__main__":
    # declare number of runs (how many random networks)
    runs = 50

    # initialise social networks model
    n_nodes = 50
    p_edge = 0.1
    p_behaviour = 0.2
    threshold_adopt = 0.3
    threshold_link = 0.5
    behaviours = ['A', 'B', 'C', 'D']
    links = {}
    adopters = {}

    for n in range(runs):

        # generate random graph (erdos-renyi) with n-nodes and probability p
        graph = nx.erdos_renyi_graph(n_nodes, p_edge)
        # plt.figure()
        # nx.draw(graph, with_labels=True)
        # plt.show()

        # transfer to adjacency list
        # add nodes to graph
        edges = graph.edges
        nodes = graph.nodes
        for i in nodes:
            add_node(i, links)
        for edge in edges:
            add_neighbour(edge[0], edge[1], links)

        # random initial adopters
        for behaviour in behaviours:
            adopters[behaviour] = []
            for node in nodes:
                rand = random.uniform(0.0, 1.0)
                if rand <= p_behaviour:
                    adopters[behaviour].append(node)


        # create copies to run several rules with the same starting network
        g1 = copy.deepcopy(links)
        g2 = copy.deepcopy(links)
        g3 = copy.deepcopy(links)

        a1 = copy.deepcopy(adopters)
        a2 = copy.deepcopy(adopters)
        a3 = copy.deepcopy(adopters)

        print(f'RUN: {n}')

        ### define steps here ###
        # monotonic FS + non-monotonic diffusion
        r1_a, r1_b, r1_c, r1_d = r1(g1, a1, threshold_adopt, threshold_link, n_nodes)

        # non-monotonic FS + non-monotonic diffusion
        r2_a, r2_b, r2_c, r2_d = r2(g2, a2, threshold_adopt, threshold_link, n_nodes)

        # non-monotonic diffusion
        r3_a, r3_b, r3_c, r3_d = r3(g3, a3, threshold_adopt, n_nodes)

        plot_graph_behaviour(r1_a, r2_a, r3_a, "Behaviour A")
        plot_graph_behaviour(r1_b, r2_b, r3_b, "Behaviour B")
        plot_graph_behaviour(r1_c, r2_c, r3_c, "Behaviour C")
        plot_graph_behaviour(r1_d, r2_d, r3_d, "Behaviour D")

        runs -= 1

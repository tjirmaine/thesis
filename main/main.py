import networkx as nx
import copy
import random
import matplotlib.pyplot as plt
from experiments import *
import csv


def run(n_nodes, p_edge, p_behaviour, threshold_adopt, threshold_link, behaviours, runs):

    # initialise social networks model
    links = {}
    adopters = {}

    # preparing data collection
    delta_r12 = []
    delta_r13 = []
    delta_r23 = []

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
        # monotonic FS + non-monotonic diffusion
        r1_a, r1_b, r1_c, r1_d = r1(g1, a1, threshold_adopt, threshold_link)

        # non-monotonic FS + non-monotonic diffusion
        r2_a, r2_b, r2_c, r2_d = r2(g2, a2, threshold_adopt, threshold_link)

        # non-monotonic diffusion
        r3_a, r3_b, r3_c, r3_d = r3(g3, a3, threshold_adopt)

        # writing data to csv file
        with open(f'data.csv', 'a', encoding='utf8', newline='') as f:
            writer = csv.writer(f)
            data = [
                [n_nodes, n, 1, 'A', len(r1_a), r1_a],
                [n_nodes, n, 1, 'B', len(r1_b), r1_b],
                [n_nodes, n, 1, 'C', len(r1_c), r1_c],
                [n_nodes, n, 1, 'D', len(r1_d), r1_d],
                [n_nodes, n, 2, 'A', len(r2_a), r2_a],
                [n_nodes, n, 2, 'B', len(r2_b), r2_b],
                [n_nodes, n, 2, 'C', len(r2_c), r2_c],
                [n_nodes, n, 2, 'D', len(r2_d), r2_d],
                [n_nodes, n, 3, 'A', len(r3_a), r3_a],
                [n_nodes, n, 3, 'B', len(r3_b), r3_b],
                [n_nodes, n, 3, 'C', len(r3_c), r3_c],
                [n_nodes, n, 3, 'D', len(r3_d), r3_d]
            ]
            writer.writerows(data)

        delta_r12.append(len(r1_a) - len(r2_a))
        delta_r12.append(len(r1_b) - len(r2_b))
        delta_r12.append(len(r1_c) - len(r2_c))
        delta_r12.append(len(r1_d) - len(r2_d))

        delta_r13.append(len(r1_a) - len(r3_a))
        delta_r13.append(len(r1_b) - len(r3_b))
        delta_r13.append(len(r1_c) - len(r3_c))
        delta_r13.append(len(r1_d) - len(r3_d))

        delta_r23.append(len(r2_a) - len(r3_a))
        delta_r23.append(len(r2_b) - len(r3_b))
        delta_r23.append(len(r2_c) - len(r3_c))
        delta_r23.append(len(r2_d) - len(r3_d))

        # make plots
        # plot_graph_behaviour(r1_a, r2_a, r3_a, "Behaviour A")
        # plot_graph_behaviour(r1_b, r2_b, r3_b, "Behaviour B")
        # plot_graph_behaviour(r1_c, r2_c, r3_c, "Behaviour C")
        # plot_graph_behaviour(r1_d, r2_d, r3_d, "Behaviour D")

        runs -= 1

    # at the end of all runs calculate deltas
    mean_r12 = sum(delta_r12) / len(delta_r12)
    mean_r13 = sum(delta_r13) / len(delta_r13)
    mean_r23 = sum(delta_r23) / len(delta_r23)
    values = [mean_r12, mean_r13, mean_r23]
    plot_deltas(values, n_nodes)


"""
Social Network Updates 
by Jirmaine Tan

This program performes the graph updates dor data collection for my bachelors thesis
"""
if __name__ == "__main__":

    # declare simulation criteria
    runs = 1000
    n_nodes = [10, 20, 50, 100]
    p_edge = 0.1
    p_behaviour = 0.2
    threshold_adopt = 0.3
    threshold_link = 0.5
    behaviours = ['A', 'B', 'C', 'D']

    # make csv
    header = ['n_nodes', 'run', 'rule', 'behaviour', 'steps', 'trace']
    with open(f'data.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    # run sim
    for nth in n_nodes:
        run(nth, p_edge, p_behaviour, threshold_adopt, threshold_link, behaviours, runs)


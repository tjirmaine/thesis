import networkx as nx
import matplotlib.pyplot as plt
import random


def adoption(graph, adoption, threshold):
    """Function for updating adopted nodes in a graph"""

    new_adoption = {}

    for behaviour, adopted in adoption.items():
        # new adopters list so that it doesn't effect calculations
        new_adopters = []

        # for non monotonic
        #new_nonadopters = []

        # loop all nodes
        for node in graph:

            ### MONOTONIC ###
            # if node already adopted then skip
            if node in adopted:
                continue

            # initialise count and get node's neighbours
            count = 0

            neighbours = graph[node]

            # loop over all neighbours and increment count if that neighbour is an adopter
            for neighbour in neighbours:
                if neighbour in adopted:
                    count += 1

            # calculate ratio adopters/neighbours
            if len(neighbours) == 0:
                ratio = 0
            else:
                ratio = count/len(neighbours)

            #### MONOTONIC ####
            # add node to new adopters if ratio is geq than threshold
            if ratio >= threshold:
                new_adopters.append(node)

            #### NON-MONOTONIC ####
            # remove node from adopters if ratio is less than threshold
            # elif ratio < threshold:
            #     adopted.remove(node)
        new_adoption[behaviour] = new_adopters

    return new_adoption
    # for new_adopter in new_adopters:
    #     adopted.append(new_adopter)


def full_cascade(adopted, n_nodes):
    """Function to check whether a full cascade has occurred"""
    full_cascade = []
    for behaviour, nodes in adopted.items():
        if len(nodes) == n_nodes:
            full_cascade.append(behaviour)
    return full_cascade


def stable_state(new_edges, adopters):
    """Function to check whether graph has reached a stable state"""
    for node, edges in new_edges.items():
        # if new_edges dictionary has a non-empty array then not stable
        if edges:
            return False
    for behaviour, nodes in adopters.items():
        # if new_adopters dictionary has a non-empty array then not stable
        if nodes:
            return False

    # both dictionaries were empty, therefore stable
    return True


def similarity(n1, n2, adopters):
    """Function to check the similarity between two nodes"""
    sim = []

    # loop over all behaviour sets
    for behaviour, adopted in adopters.items():

        # if both nodes are adopters add the behaviour
        if n1 in adopted and n2 in adopted:
            sim.append(behaviour)
        # else if both nodes are not adopters add the behaviour
        elif n1 not in adopted and n2 not in adopted:
            sim.append(behaviour)

    # return list of similar behaviours
    return sim


def merge(links, new_links):
    """Function to merge two dictionaries without overwriting"""

    # for all new edges append them to the original graph
    # we make the assumption that there are no duplicates
    for node, neighbours in new_links.items():
        for new_neighbour in neighbours:
            links[node].append(new_neighbour)


def friendship_selection(graph, adopters, threshold):
    """Function for updating edges in graph"""

    # making temp graph
    new_edges = {}
    for i in range(len(graph)):
        add_node(i, new_edges)

    # loop all nodes
    for node in graph:
        # retrieve the neighbours of that node
        neighbours = graph[node]

        # retrieve new neighbours (new edge may have formed during the process)
        new_neighbours = new_edges[node]

        # for each neighbour, get second neighbours
        # check if the node is neighbours with second neighbours
        # add edge if they aren't
        for neighbour in neighbours:
            second_neighbours = graph[neighbour]
            for second_neighbour in second_neighbours:
                # ignore itself
                if node == second_neighbour:
                    continue

                # potential new neighbour
                if second_neighbour not in neighbours and second_neighbour not in new_neighbours:
                    # check if node similarities
                    sim = similarity(node, second_neighbour, adopters)
                    # print(sim)

                    # sanity check
                    if len(adopters) > 0:
                        ratio = len(sim) / len(adopters)

                        # add link if ratio exceeds threshold
                        if ratio > threshold:
                            add_neighbour(node, second_neighbour, new_edges)
                    else:
                        continue
    return new_edges


def add_neighbour(n1, n2, graph):
    """Function for adding a neighbour edge between nodes"""
    graph[n1].append(n2)
    graph[n2].append(n1)


def add_node(x, graph):
    """Function for adding nodes to graph"""
    graph[x] = []

"""
Social Network Updates 
by Jirmaine Tan

This program is able to perform graph network updates
"""
if __name__ == "__main__":
    # declare number of runs (how many random networks)
    runs = 50

    # initialise social networks model
    n_nodes = 10
    p_edge = 0.3
    p_behaviour = 0.3
    threshold_adopt = 0.3
    threshold_link = 0.3
    links = {}
    adopters = {}
    behaviours = ['A', 'B', 'C', 'D']

    for n in range(runs):
        # generate random graph (erdos-renyi) with n-nodes and probability p
        graph = nx.erdos_renyi_graph(n_nodes, p_edge)
        # nx.draw(graph, with_labels=True)
        # plt.show()

        # retrieve edges and nodes
        edges = graph.edges
        nodes = graph.nodes

        # transfer to adjacency list
        # add nodes to graph
        for i in nodes:
            add_node(i, links)
        for edge in edges:
            add_neighbour(edge[0], edge[1], links)

        # initial adopters
        for behaviour in behaviours:
            adopters[behaviour] = []
            for node in nodes:
                rand = random.uniform(0.0, 1.0)
                if rand <= p_behaviour:
                    adopters[behaviour].append(node)

        print(f'RUN: {n}')

        ### define steps here ###
        # cascade = False
        stable = False
        counter = 0
        while not stable:

            # print network
            print(f'step: {counter}')
            print(links)
            print(adopters)

            # increment counter
            counter += 1

            # step updates
            new_edges = friendship_selection(links, adopters, threshold_link)
            new_adoption = adoption(links, adopters, threshold_adopt)

            stable = stable_state(new_edges, new_adoption)
            merge(links, new_edges)
            merge(adopters, new_adoption)

        print(f'stable?: {stable}')
        print(f'full cascades: {full_cascade(adopters, n_nodes)}')

        runs -= 1

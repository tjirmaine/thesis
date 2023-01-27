"""File that contains functions that imitate the behaviour of nodes in the network and the network itself"""


from network import *


def adoption(graph, adopters, threshold):
    """
    Function for updating adopted nodes in a graph (monotonic)
    :returns a list containing the nodes that adopted a new behaviour
    """

    new_adoption = {}
    for behaviour, adopted in adopters.items():
        # new adopters list so that it doesn't effect calculations
        new_adopters = []

        # loop all nodes
        for node in graph:
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

            # add node to new adopters if ratio is greater than threshold
            if ratio > threshold:
                new_adopters.append(node)

        new_adoption[behaviour] = new_adopters

    return new_adoption


def unadopt(graph, adopters, threshold):
    """
    Function for updating adopted nodes in a graph (non-monotonic)
    :returns a list containing the nodes that unadopted a new behaviour
    """

    non_adopters = {}
    for behaviour, adopted in adopters.items():
        # new adopters and deserters list so that it doesn't effect calculations
        new_deserters = []

        # loop all adopted nodes to see if they will unadopt
        for node in adopted:

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
                ratio = count / len(neighbours)

            # add node to deserters if ratio less than threshold
            if ratio <= threshold:
                new_deserters.append(node)

        non_adopters[behaviour] = new_deserters
    return non_adopters


def make_friends(graph, adopters, threshold):
    """
    Function for updating edges in graph
    :returns a list containing the edges to add to the network
    """

    # making temp graph
    new_edges = {}
    for i in range(len(graph)):
        add_node(i, new_edges)

    # loop all nodes
    for node in graph:
        # retrieve the neighbours, new neighbours (new edge may have formed during the process) of that node
        neighbours = graph[node]
        new_neighbours = new_edges[node]

        # collecting all second neighbours into a list and removing duplicates
        second_neighbours = []
        for neighbour in neighbours:
            second_neighbours.extend(graph[neighbour])
        second_neighbours = list(dict.fromkeys(second_neighbours))

        # if nodes aren't already neighbours and are similar enough then add edge
        for new in second_neighbours:
            if node == new:
                continue
            if new not in neighbours and new not in new_neighbours:
                # check node similarities
                sim = similarity(node, new, adopters)

                # sanity check
                if len(adopters) > 0:
                    ratio = len(sim) / len(adopters)
                    # add link if ratio greater threshold
                    if ratio > threshold:
                        add_neighbour(node, new, new_edges)
    return new_edges


def lose_friends(graph, adopters, threshold):
    """
    Function for updating edges in graph
    :returns a list containing the edges to add to the network
    """

    # making temp graph
    remove_edges = {}
    for i in range(len(graph)):
        add_node(i, remove_edges)

    # loop all nodes
    for node in graph:
        # retrieve the neighbours of that node
        neighbours = graph[node]

        for neighbour in neighbours:
            # skip if the edge was already removed by a previous node calculation
            if neighbour in remove_edges[node]:
                continue

            sim = similarity(node, neighbour, adopters)
            if len(adopters) > 0:
                ratio = len(sim) / len(adopters)
                if ratio <= threshold:
                    add_neighbour(node, neighbour, remove_edges)

    return remove_edges


def similarity(n1, n2, adopters):
    """
    Function to check the similarity between two nodes
    :returns a list containing the behaviours that node 1 and node 2 coincide
    """
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


def full_cascade(adopted, n_nodes):
    """Function to check whether a full cascade has occurred"""
    cascades = []
    for behaviour, nodes in adopted.items():
        if len(nodes) == n_nodes:
            cascades.append(behaviour)
    return cascades


def check_stable(d):
    for _, v in d.items():
        # if new_adopters dictionary has a non-empty array then not stable
        if v:
            return False
    return True

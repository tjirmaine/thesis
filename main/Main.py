def adoption(graph, adopted, threshold):
    """Function for updating adopted nodes in a graph"""
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
    for new_adopter in new_adopters:
        adopted.append(new_adopter)


def full_cascade(adopted, n_nodes):
    """Function to check whether a full cascade has occurred"""
    return True if n_nodes == len(adopted) else False


def merge(links, new_links):
    """Function to merge two dictionaries without overwriting"""

    # for all new edges append them to the original graph
    # we make the assumption that there are no duplicates
    for node, neighbours in new_links.items():
        for new_neighbour in neighbours:
            links[node].append(new_neighbour)


def friendship_selection(graph):
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
                if second_neighbour not in neighbours and second_neighbour not in new_neighbours:
                    add_neighbour(node, second_neighbour, new_edges)
                    # print(f'new neighbours')

    merge(graph, new_edges)


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
    # initialise number of nodes, list of nodes, threshold, edges, adopters and behaviours
    n_nodes = 4
    nodes = []
    threshold = 0.3
    links = {}
    adopters = {}
    behaviours = ['A']

    # add nodes to graph
    for i in range(n_nodes):
        nodes.append(i)
        add_node(i, links)

    # starting edges
    add_neighbour(0, 1, links)
    add_neighbour(1, 2, links)
    add_neighbour(2, 3, links)

    # initial adopters
    # 0 is an initial adopter of behaviour 'A'
    adopters[behaviours[0]] = []
    adopters[behaviours[0]].append(0)

    ### define steps here ###

    # this is
    cascade = False
    counter = 0
    while not cascade:
        counter += 1
        print(counter)
        friendship_selection(links)
        adoption(links, adopters[behaviours[0]], threshold)
        cascade = full_cascade(adopters[behaviours[0]], n_nodes)

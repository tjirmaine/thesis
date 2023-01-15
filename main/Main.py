def friendship_selection(graph):
    """Function for updating edges in graph"""

    # loop all nodes
    for node in graph:
        # retrieve the neighbours of that node
        neighbours = graph[node]

        # for each neighbour, get second neighbours
        # check if the node is neighbours with second neighbours
        # add edge if they aren't
        for neighbour in neighbours:
            second_neighbours = graph[neighbour]
            for second_neighbour in second_neighbours:
                # ignore itself
                if node == second_neighbour:
                    continue
                if second_neighbour not in neighbours:
                    add_neighbour(node, second_neighbour, graph)
                    print(f'new neighbours')



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
    # adjacency list
    links = {}
    beliefs = {}

    add_node(1, links)
    add_node(2, links)
    add_node(3, links)
    add_node(4, links)

    add_neighbour(1, 2, links)
    add_neighbour(2, 3, links)

    friendship_selection(links)

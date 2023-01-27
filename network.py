"""File that contains functions to manipulate dictionaries"""


def merge(d1, d2):
    """Function to merge two dictionaries without overwriting"""
    # for all new elements of dict2 add them to dict1
    for k, v in d2.items():
        for item in v:
            if item not in d1[k]:
                d1[k].append(item)


def remove(d1, d2):
    """Function for removing elements the elements of a second dictionary from the first"""

    # for all elements of dict 2 remove them from dict1
    for k, v in d2.items():
        for item in v:
            # sanity check
            if item in d1[k]:
                d1[k].remove(item)


def add_neighbour(n1, n2, graph):
    """Function for adding a neighbour edge between nodes"""
    graph[n1].append(n2)
    graph[n2].append(n1)


def add_node(x, graph):
    """Function for adding nodes to graph"""
    graph[x] = []

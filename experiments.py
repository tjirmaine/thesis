from behaviour import *
import matplotlib.pyplot as plt


def r1(g1, a1, threshold_adopt, threshold_link, n_nodes, max_steps=50):
    """
    Function to run monotonic FS + non-monotonic diffusion updates
    :returns 4 arrays, each showing the diffusion of a behaviour
    """
    counter = 0

    # for data collection
    y_a, y_b, y_c, y_d = [], [], [], []

    while counter < max_steps:
        # print network
        # print_step(g1, a1, counter)

        # get no. adopters at each time step
        y_a.append(len(a1['A']))
        y_b.append(len(a1['B']))
        y_c.append(len(a1['C']))
        y_d.append(len(a1['D']))

        # increment counter
        counter += 1

        # step updates
        new_edges = make_friends(g1, a1, threshold_link)
        add_adopters = adoption(g1, a1, threshold_adopt)
        remove_adopters = unadopt(g1, a1, threshold_adopt)

        merge(g1, new_edges)
        merge(a1, add_adopters)
        remove(a1, remove_adopters)

        if check_stable(new_edges) and check_stable(add_adopters) and check_stable(remove_adopters):
            # print(f'stable')
            break
    # print(f'full cascades: {full_cascade(a1, n_nodes)}')
    return y_a, y_b, y_c, y_d


def r2(g2, a2, threshold_adopt, threshold_link, n_nodes, max_steps=50):
    """
    Function to run non-monotonic FS + non-monotonic diffusion
    :returns 4 arrays, each showing the diffusion of a behaviour
    """
    # for data collection
    y_a, y_b, y_c, y_d = [], [], [], []
    counter = 0

    while counter < max_steps:
        # print network
        # print_step(g2, a2, counter)

        # get no. adopters at each time step
        y_a.append(len(a2['A']))
        y_b.append(len(a2['B']))
        y_c.append(len(a2['C']))
        y_d.append(len(a2['D']))

        # increment counter
        counter += 1

        # step updates
        new_edges = make_friends(g2, a2, threshold_link)
        remove_edges = lose_friends(g2, a2, threshold_link)
        add_adopters = adoption(g2, a2, threshold_adopt)
        remove_adopters = unadopt(g2, a2, threshold_adopt)

        merge(g2, new_edges)
        remove(g2, remove_edges)
        merge(a2, add_adopters)
        remove(a2, remove_adopters)

        if check_stable(new_edges) and check_stable(add_adopters) and check_stable(remove_adopters) \
                and check_stable(remove_edges):
            # print(f'stable')
            break
    # print(f'full cascades: {full_cascade(a2, n_nodes)}')
    return y_a, y_b, y_c, y_d


def r3(g3, a3, threshold_adopt, n_nodes, max_steps=50):
    """
    Function to run non-monotonic diffusion
    :returns 4 arrays, each showing the diffusion of a behaviour
    """
    # for data collection
    y_a, y_b, y_c, y_d = [], [], [], []
    counter = 0

    while counter < max_steps:
        # print network
        # print_step(g3, a3, counter)

        # get no. adopters at each time step
        y_a.append(len(a3['A']))
        y_b.append(len(a3['B']))
        y_c.append(len(a3['C']))
        y_d.append(len(a3['D']))

        # increment counter
        counter += 1

        # step updates
        add_adopters = adoption(g3, a3, threshold_adopt)
        remove_adopters = unadopt(g3, a3, threshold_adopt)
        merge(a3, add_adopters)
        remove(a3, remove_adopters)
        if check_stable(remove_adopters):
            # print(f'stable')
            break
    # print(f'full cascades: {full_cascade(a3, n_nodes)}')
    return y_a, y_b, y_c, y_d


def plot_graph_rule(y1, y2, y3, y4, name):
    """plot adopters over time for a rule"""
    plt.figure()
    plt.plot(y1, label='A')
    plt.plot(y2, '--', label='B')
    plt.plot(y3, '-.', label='C')
    plt.plot(y4, ':', label='D')
    plt.xlabel("Steps")
    plt.ylabel("# of adopters")
    plt.title(f'Adopters evolution {name}')
    plt.legend(loc='upper right')
    plt.show()


def plot_graph_behaviour(y1, y2, y3, name):
    """plot adopters over time for a behaviour"""
    plt.figure()
    plt.plot(y1, label="R1")
    plt.plot(y2, '--', label="R2")
    plt.plot(y3, '-.', label="R3")
    plt.xlabel("Steps")
    plt.ylabel("# of adopters")
    plt.title(f'Adopters evolution {name}')
    plt.legend(loc='upper right')
    plt.show()


def plot_deltas(values):
    rules = ['r12', 'r13', 'r23']
    plt.figure()
    plt.bar(rules, values)
    plt.xlabel("Rule comparisons")
    plt.ylabel("Step difference")
    plt.title("Performance difference rules")
    plt.show()


def print_step(g, a, i):
    """Function that prints the network graph and the adopters for a step"""
    print(f'step: {i}')
    print(g)
    print(a)

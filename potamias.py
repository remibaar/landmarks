import networkx as nx
from random import choice

def random_landmarks(g,d):
    """
    :param g: Graph
    :param d: Number of landmarks to return
    :return: d random nodes
    """
    return g.random_nodes(d)

def deg_centrality_landmarks(g,d):
    """
    :param g: Graph
    :param d: Number of landmarks to return
    :return: Return top d degree centrality nodes
    """
    dc = nx.degree_centrality()
    i = dc.items()
    s = i.sorted(reverse=True, key=lambda x: x[1])
    return map(lambda x: x[0], s[:d])

def closeness_centrality_ls(g, k, d, h=None, constrain=False):
    """
    :param g: Graph
    :param k: Number of nodes to randomly sample and solve SSSP for
    :param d: Top d landmarks to return
    :param h: Discard nodes that are at distance h from selected landmark
    :return: A sorted list in ascending order of the top d lowest
             closeness centralities of all the nodes in g, and
             all unsorted closeness centralities
    """
    v = []
    sp, closeness = {}, {}
    n = g.n()
    # Calculate shortest path lengths from random node v_i
    # to all other nodes and store in dictionary with key = v_i
    for i in range(k):
        v.append(choice(g.nodes()))
        sp[v[i]] = nx.shortest_path_length(g, source=v[i])
    # For all nodes j in g, calculate centrality estimate
    # based on Eppstein & Wang and store in closeness[j]
    for j in g.nodes():
        sum = 0
        for c in range(k):
            sum += n*sp[v[c]][j]/(k*(n-1))
        closeness[j] = sum
    # Return the top d
    sorted_cc = sorted(closeness, key=closeness.get)
    # Constrained closeness centrality
    if constrain:
        count = d
        not_a_landmark = []
        con = {}
        for i in q:
            if i not in not_a_landmark:
                con[sorted_cc[i]] = closeness[sorted_cc[i]]
                count -= 1
                not_a_landmark = list(nx.single_source_shortest_path_length(g, source=i, cutoff=h))
            if count == 0:
                return con, closeness
    return sorted_cc[:d], closeness

# Partitions
# https://github.com/valiantljk/graph-partition/blob/master/algorithms/boundary.py
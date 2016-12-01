import networkx as nx
from random import choice

def select_nodes(g, k, d, h=None, constrained=False, strategy='closeness'):
    v = []
    sp = {}
    # Calculate shortest paths from random node v_i to all other nodes and store in dictionary with key = v_i
    for i in range(k):
        v.append(choice(g.nodes()))
        sp[v[i]] = nx.shortest_path_length(g, source=v[i])
    # For all nodes j in g, calculate centrality estimate based on Eppstein & Wang and store in closeness[j]
    if strategy == 'random':
        return g.random_nodes(d)
    elif strategy == 'degree':
        node_centrality = nx.degree_centrality(g)
        sorted_c = sorted(node_centrality, reverse=True, key=node_centrality.get)
        selected = sorted_c[:d]
    elif strategy == 'closeness':
        node_centrality = approx_closeness(g, k, v, sp)
        sorted_c = sorted(node_centrality, key=node_centrality.get)
        selected = sorted_c[:d]
    # Return the top d
    if constrained:
        selected = constrain(node_centrality, sorted_c, d,h)
    return selected

def approx_closeness(g, k, v, sp):
    n = g.number_of_nodes()
    closeness = {}
    for j in g.nodes():
        sum = 0
        for c in range(k):
            sum += n*sp[v[c]][j]/(k*(n-1))
        closeness[j] = sum
    return closeness

def constrain(node_centrality, sorted_c, d, h):
    count = d
    not_a_landmark = []
    con = {}
    for i in sorted_c:
        if i not in not_a_landmark:
            con[i] = node_centrality[sorted_c[i]]
            not_a_landmark = list(nx.single_source_shortest_path_length(g, source=i, cutoff=h))
            count -= 1
        if count == 0:
            return list(con.keys())

# Partitions
# https://github.com/valiantljk/graph-partition/blob/master/algorithms/boundary.py
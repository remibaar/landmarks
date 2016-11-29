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

def closeness_centrality_landmarks(g, k, d):
    """
    :param g: Graph
    :param k: Number of nodes to randomly sample and solve SSSP for
    :param d: Top d landmarks to return
    :return: A sorted list in ascending order of the top d lowest
             closeness centralities of all the nodes in g, and
             all closeness centralities
    """
    v = []
    sp = dict()
    n = g.n()
    closeness = {}
    # Calculate shortest paths from random node v_i to all other nodes and store in dictionary with key = v_i
    for i in range(k):
        v.append(choice(g.nodes()))
        sp[v[i]] = nx.shortest_path_length(g, source=v[i])
    # For all nodes j in g, calculate centrality estimate based on Eppstein & Wang and store in closeness[j]
    for j in g.nodes():
        sum = 0
        for c in range(k):
            sum += n*sp[v[c]][j]/(k*(n-1))
        if sum == 0:
            print(sum)
        closeness[j] = sum
    # Return the top d
    q = sorted(closeness, key=closeness.get)
    return q[:d], closeness


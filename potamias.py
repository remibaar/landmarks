

def deg_centrality_landmarks(g,d):
    dc = nx.degree_centrality()
    i = dc.items()
    sorted = i.sort(reverse=True, key=lambda x: x[1])
    return map(lambda x: x[0], sorted[:d])
import networkx as nx
import csv
import metis
import logging
from random import choice
from operator import itemgetter
from common import Direction, Path, file_name, read_sketch_paths, write_sketch_paths



def precomputation(g, directory, landmark_function, landmark_kwargs):
    """
    Implements the Sketch Algorithm as Defined by Gubichev et al.

    :param g: A graph, classes are defined in graph.py
    :param k: Number of iterations
    :return:
    """

    logging.info('Start Potatmias precomputation')

    sketches = dict()

    landmarks = landmark_function(g, **landmark_kwargs)

    for l in landmarks:

        landmark = [l]

        # Forward search
        shortest_paths = g.shortest_path_nodes_to_landmark_path(landmark)
        for node, path in shortest_paths.items():
            if node not in sketches:
                sketches[node] = list()

            sketches[node].append((Direction.forward, path))

        # Backward search
        shortest_paths = g.shortest_path_nodes_from_landmark_path(landmark)
        for node, path in shortest_paths.items():
            if node not in sketches:
                sketches[node] = list()

            sketches[node].append((Direction.backward, path))


    # Write sketches to file
    logging.info('Starting to write '+str(len(sketches))+' files')
    for node, data in sketches.items():
        write_sketch_paths(file_name(node, directory), data)

    logging.info('Finished Potatmias precomputation')


def random(g, k):
    """
    Selects top d landmarks based on closeness centrality or degree centrality,
    with landmarks constrained by distance h between them or not
    :param g: graph g
    :param k: number of nodes to exact calculate closeness centrality for
    :return: list of landmark nodes
    """
    return g.random_nodes(k)


def select_nodes(g, k, d, h=None, constrained=False, strategy='closeness'):
    """
    Selects top d landmarks based on closeness centrality or degree centrality,
    with landmarks constrained by distance h between them or not
    :param g: graph g
    :param k: number of nodes to exact calculate closeness centrality for
    :param d: number of landmarks to select
    :param h: distance tolerated between two selected landmarks
    :param constrained: boolean deciding on using a constraint strategy or not
    :param strategy: use random, closeness centrality or degree centrality strategy
    :return: list of landmark nodes
    """
    if strategy == 'random':
        return g.random_nodes(d)
    elif strategy == 'degree':
        node_centrality = nx.degree_centrality(g)
        save_centralities(node_centrality, 'dc')
        sorted_c = sorted(node_centrality, reverse=True, key=node_centrality.get)
        landmarks = sorted_c[:d]
    elif strategy == 'closeness':
        node_centrality = approx_closeness(g, k)
        sorted_c = sorted(node_centrality, key=node_centrality.get)
        landmarks = sorted_c[:d]
    # Return the top d
    if constrained:
        landmarks = constrain(node_centrality, d, h)
    return landmarks


def approx_closeness(g, k):
    """
    Approximate closeness centrality (Eppstein)
    :param g: graph g
    :param k: number of nodes to calculate exact closeness centrality for
    :return: dictionary of approximated closeness for all nodes of graph g
    """
    v = []
    sp = {}
    # Calculate shortest paths from random node v_i to all other nodes and store in dictionary with key = v_i
    for i in range(k):
        v.append(choice(g.nodes()))
        sp[v[i]] = nx.shortest_path_length(g, source=v[i])
    n = g.number_of_nodes()
    closeness = {}
    for j in g.nodes():
        sum = 0
        for c in range(k):
            sum += n*sp[v[c]][j]/(k*(n-1))
        closeness[j] = sum
    save_centralities(closeness, 'cc')
    return closeness


def constrain(node_centrality, sorted_c, d, h):
    """
    Select top nodes, discarding nodes that are too close to each other
    :param node_centrality: centralities for all nodes
    :param sorted_c: sorted centralities
    :param d: top d landmarks to return based on some centrality metric
    :param h: discard nodes closer than h to each other
    :return: list of landmark nodes
    """
    count = d
    not_a_landmark = []
    con = {}
    sorted_c = sorted(node_centrality, key=node_centrality.get)
    for i in sorted_c:
        if i not in not_a_landmark:
            con[i] = node_centrality[sorted_c[i]]
            not_a_landmark = list(nx.single_source_shortest_path_length(g, source=i, cutoff=h))
            count -= 1
        if count == 0:
            return list(con.keys())


def save_centralities(c, name):
    """
    Save centralities
    :param c: centralities
    :param name: name of centrality file
    :return: None
    """
    with open('%s.csv' % name, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=' ')
        writer.writerow(["node", "centr"])
        for key, value in c.items():
            writer.writerow([key, value])
    return


def load_centralities(name):
    """
    Load centralities
    :param name: name of file with centralities to open
    :return: dictionary of centralities
    """
    centralities = {}
    with open('%s.csv' % name, 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=' ')
        for row in reader:
            centralities[int(row['node'])] = float(row['centr'])
    return centralities


def save_partitions(p):
    """
    Save partitions
    :param p: partition file
    :return: None
    """
    with open('partitions.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=' ')
        writer.writerow(["partition", "node"])
        for row in p:
            writer.writerow(row)
    return

def load_partitions():
    """
    Load partitions
    :return: dictionary of nodes and their corresponding partition
    """
    partitions = {}
    with open('partitions.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=' ')
        for row in reader:
            partitions[int(row['node'])] = int(row['partition'])
    return partitions


def partitionp(g, P, name):
    """
    Pick the nodes with the highest centrality in each partition
    :param g: graph g
    :param P: number of partitions
    :param name: partition file to save partitions in
    :return: list of landmarks
    """
    _, parts = metis.part_graph(g, P)
    centralities = load_centralities(name)
    ckeys = list(centralities.keys())
    cvalues = list(centralities.values())
    partc = list(zip(parts, cvalues, ckeys))
    part = list(zip(parts, ckeys))
    save_partitions(part)
    landmarks = []
    if name == 'cc':
        for i in range(P):
            landmarks.append((min(filter(lambda a: a[0] == i, partc), key=itemgetter(1))[2]))
    elif name == 'dc':
        for i in range(P):
            landmarks.append((max(filter(lambda a: a[0] == i, partc), key=itemgetter(1))[2]))
    return landmarks


def borderp(g):
    """
    Pick nodes close to the border of each partition
    :param g: graph g
    :return: list of landmarks
    """
    landmarks = []
    partitions = load_partitions()
    P = len(set(partitions.values()))
    bu = {}
    for node in g.nodes():
        neighbors = g.neighbors(node)
        p = partitions[node]
        dpu = 0
        diu = 0
        for n in neighbors:
            if partitions[n] == p:
                dpu += 1
            elif partitions[n] != p:
                diu += 1
        bu[node] = dpu * diu
    pbu=list(zip(partitions.keys(),partitions.values(), bu.values()))
    for i in range(P):
        landmarks.append(((max(filter(lambda a: a[1] == i, pbu), key=itemgetter(2))[0])))
    return landmarks

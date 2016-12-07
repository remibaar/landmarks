import math
import enum
import logging
import queue
import os
import networkx as nx


def _file_name(name, directory):
    return directory+'/'+str(name)+'.txt'


# Direction enum
class Direction(enum.IntEnum):
    forward = 0
    backward = 1

    def __str__(self):
        return str(self.value)


class Path(list):
    def __lt__(self, other):
        return len(self) < len(other)

    def __gt__(self, other):
        return len(self) > len(other)


def _write_sketches(filename, sketches):
    """
    Write a list of sketches to the given file
    A sketch is a tuple of (direction, path)

    :param filename:
    :param sketches:
    :return:
    """
    file = open(filename, mode='w+')
    file.writelines([str(sketch[0])+'\t'+(','.join(map(str, sketch[1])))+'\n' for sketch in sketches])
    file.close()


def _read_sketches(filename):
    """
    Reads an list of sketches from the given file
    A sketch is a tuple of (direction, path)

    :param filename:
    :return: list of sketches
    """
    if not os.path.exists(filename):
        return None

    sketches = list()
    file = open(filename, mode='r')
    for line in file:
        line = line.replace('\n', '')
        parts = line.split('\t')
        sketches.append((Direction(int(parts[0])), Path(parts[1].split(','))))
    return sketches


def precomputation(g, directory, k):
    """
    Implements the Sketch Algorithm as Defined by Gubichev et al.

    :param g: A graph, classes are defined in graph.py
    :param k: Number of iterations
    :return:
    """

    logging.info('Start Gubichev precomputation')

    sketches = dict()

    # Calculate sketches
    r = max(1, math.floor(math.log10(g.n())))
    logging.info('r = '+str(r))

    for i in range(k):
        for j in range(r + 1):
            landmarks = g.random_nodes(2**j)
            logging.info('i = ' + str(i) + ', j = ' + str(j) + ', landmarks = ' + str(landmarks))

            # Forward search
            shortest_paths = g.shortest_path_nodes_to_landmark_path(landmarks)
            for node, path in shortest_paths.items():
                if node not in sketches:
                    sketches[node] = list()

                sketches[node].append((Direction.forward, path))

            # Backward search
            shortest_paths = g.shortest_path_nodes_from_landmark_path(landmarks)
            for node, path in shortest_paths.items():
                if node not in sketches:
                    sketches[node] = list()

                sketches[node].append((Direction.backward, path))


    # Write sketches to file
    logging.info('Starting to write '+str(len(sketches))+' files')
    for node, data in sketches.items():
        _write_sketches(_file_name(node, directory), data)


    logging.info('Finished gubichev precomputation')


def convert_queue_to_length(s, d, g, directory, function):
    q = function(s, d, g, directory)
    if q.empty():
        return float('inf')
    else:
        return len(q.get()) - 1

def deg_centrality_landmarks(g,d):
    dc = nx.degree_centrality()
    i = dc.items()
    sorted = i.sort(reverse=True, key=lambda x: x[1])
    return map(lambda x: x[0], sorted[:d])

def sketch(s, d, g, directory):
    # Read sketches
    s_sketches = _read_sketches(_file_name(s, directory))
    d_sketches = _read_sketches(_file_name(d, directory))

    q = queue.PriorityQueue()

    if s_sketches is None or d_sketches is None:
        return q

    # Filter direction
    s_sketches = [sketch for sketch in s_sketches if sketch[0] == Direction.forward]
    d_sketches = [sketch for sketch in d_sketches if sketch[0] == Direction.backward]

    # Source is landmark
    for s_sketch in s_sketches:
        if d == s_sketch[1]:
            return s_sketch[2]

    # Destination is landmark
    for d_sketch in d_sketches:
        if s == d_sketch[1]:
            return d_sketch[2]


    # Approximate distance
    for s_sketch in s_sketches:
        for d_sketch in d_sketches:

            if s_sketch[1][-1] == d_sketch[1][0]:
                path = Path(s_sketch[1][:-1] + d_sketch[1])
                q.put(path)

    return q


def sketch_ce(s, d, g, directory):
    q = sketch(s, d, g, directory)

    to_be_added = list()
    for path in q.queue:

        found = False
        for i in range(len(path) - 1):

            for j in range(len(path) - 1, i):

                if path[i] == path[j]:
                    path = Path(path[0:i] + path[j+1:])
                    to_be_added.append(path)

                    found = True
                    break

            if found:
                break

    for x in to_be_added:
        q.put(x)

    return q


def sketch_cesc(s, d, g, directory):
    q = sketch_ce(s, d, g, directory)

    to_be_added = list()

    for path in q.queue:

        found = False
        for i in range(len(path)):

            for successor in g.successors(path[i]):

                for j in range(len(path) - 1, i + 1):

                    if successor == path[j]:
                        path = Path(path[0:i] + [successor] + path[j + 1:])
                        to_be_added.append(path)

                        found = True
                        break

                if found:
                    break

            if found:
                break

    for x in to_be_added:
        q.put(x)

    return q


def tree_sketch(s, d, g, directory):
    # Read sketches
    s_sketches = _read_sketches(_file_name(s, directory))
    d_sketches = _read_sketches(_file_name(d, directory))

    q = queue.PriorityQueue()

    if s_sketches is None or d_sketches is None:
        return q

    # Filter direction
    s_sketches = [sketch[1] for sketch in s_sketches if sketch[0] == Direction.forward]
    d_sketches = [list(reversed(sketch[1])) for sketch in d_sketches if sketch[0] == Direction.backward]

    index = 0

    l_shortest = float('inf')
    v_bfs = dict()
    v_rbfs = dict()

    while True:
        # Breath first search through trees
        bfs = dict()
        for i, sketch in enumerate(s_sketches):
            if len(sketch) > index and sketch not in bfs.values():
                bfs[i] = sketch[index]

        rbfs = dict()
        for i, sketch in enumerate(d_sketches):
            if len(sketch) > index and sketch not in rbfs.values():
                rbfs[i] = sketch[index]

        # Check if expansion was possible
        if len(bfs) == 0 and len(rbfs) == 0:
            break

        for s_sketches_index, u in bfs.items():
            for d_sketches_index, v in rbfs.items():

                p_v_to_d = list(reversed(d_sketches[d_sketches_index][0:index+1]))
                p_s_to_u = s_sketches[s_sketches_index][0:index+1]

                v_bfs[u] = p_s_to_u
                for x, p_s_to_x in v_bfs.items():
                    if v in g.successors(x):
                        p = Path(p_s_to_x + p_v_to_d)
                        q.put(p)
                        l_shortest = min(l_shortest, len(p))

                v_rbfs[v] = p_v_to_d
                for x, p_x_to_d in v_rbfs.items():
                    if x in g.successors(u):
                        p = Path(p_s_to_u + p_x_to_d)
                        q.put(p)
                        l_shortest = min(l_shortest, len(p))

        if min(index, len(bfs)) + min(index, len(rbfs)) >= l_shortest:
            break

        index += 1

    return q

import math
import enum
import logging
import queue
import os
import networkx as nx
import timeit
from common import Direction, Path, file_name, read_sketch_paths, write_sketch_paths


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
        write_sketch_paths(file_name(node, directory), data)

    logging.info('Finished gubichev precomputation')


def convert_queue_to_length(s, d, g, directory, function):
    q = function(s, d, g, directory)
    if q.empty():
        return float('inf')
    else:
        return len(q.get()) - 1


def sketch(s, d, g, directory):
    # Read sketches
    tic = timeit.default_timer()
    s_sketches = read_sketch_paths(file_name(s, directory))
    d_sketches = read_sketch_paths(file_name(d, directory))
    toc = timeit.default_timer()

    read_time = toc-tic

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

    q = queue.PriorityQueue()

    # the same nodes
    if s == d:
        q.put(Path([s]))
        return q

    # Read sketches
    s_sketches = read_sketch_paths(file_name(s, directory))
    d_sketches = read_sketch_paths(file_name(d, directory))

    if s_sketches is None or d_sketches is None:
        return q

    # Filter direction
    s_sketches = [sketch[1] for sketch in s_sketches if sketch[0] == Direction.forward]
    d_sketches = [list(reversed(sketch[1])) for sketch in d_sketches if sketch[0] == Direction.backward]

    # Are there common landmarks, to check if in the same component
    if len(set([sketch[-1] for sketch in s_sketches]) & set([sketch[-1] for sketch in d_sketches])) == 0:
        return q

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
            p_s_to_u = s_sketches[s_sketches_index][0:index + 1]
            v_bfs[u] = p_s_to_u

        for d_sketches_index, v in rbfs.items():
            p_v_to_d = list(reversed(d_sketches[d_sketches_index][0:index+1]))
            v_rbfs[v] = p_v_to_d

        for d_sketches_index, v in rbfs.items():
            for x, p_s_to_x in v_bfs.items():
                if v in g.successors(x):
                    p_v_to_d = v_rbfs[v]
                    p = Path(p_s_to_x + p_v_to_d)
                    q.put(p)
                    l_shortest = min(l_shortest, len(p))

        for s_sketches_index, u in bfs.items():
            for x, p_x_to_d in v_rbfs.items():
                if x in g.successors(u):
                    p_s_to_u = v_bfs[u]
                    p = Path(p_s_to_u + p_x_to_d)
                    q.put(p)
                    l_shortest = min(l_shortest, len(p))

        if index * 2 >= l_shortest:
            break

        index += 1

    return q

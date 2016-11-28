import math
import enum
import logging
import queue


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
    Write an list of sketches to the given file
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

    logging.info('Start gubichev precomputation')

    sketches = dict()

    # Calculate sketches
    r = max(1, math.floor(math.log2(g.n())))
    logging.info('r = '+str(r))

    for i in range(k):
        for j in range(r):
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


def sketch(s, d, g, directory):
    # Read sketches
    s_sketches = _read_sketches(_file_name(s, directory))
    d_sketches = _read_sketches(_file_name(d, directory))

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

    q = queue.PriorityQueue()

    # Approximate distance
    for s_sketch in s_sketches:
        for d_sketch in d_sketches:

            if s_sketch[1][-1] == d_sketch[1][0]:
                path = Path(s_sketch[1][:-1] + d_sketch[1])
                q.put(path)

    return q


def sketch_ce(s, d, g, directory):
    q = sketch(s, d, g, directory)

    for path in q.queue:

        found = False
        for i in range(len(path) - 1):

            for j in range(len(path) - 1, i):

                if path[i] == path[j]:
                    path = Path(path[0:i] + path[j+1:])
                    q.put(path)

                    found = True
                    break

            if found:
                break

    return q


def sketch_cesc(s, d, g, directory):
    q = sketch_ce(s, d, g, directory)

    for path in q.queue:

        found = False
        for i in range(len(path)):

            for successor in g.successors(path[i]):

                for j in range(len(path) - 1, i + 1):

                    if successor == path[j]:
                        path = Path(path[0:i] + [successor] +  path[j + 1:])
                        q.put(path)

                        found = True
                        break

                if found:
                    break

            if found:
                break

    return q

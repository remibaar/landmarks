import math
import enum
import logging


def _file_name(name, directory):
    return directory+'/'+str(name)+'.txt'


# Direction enum
class Direction(enum.IntEnum):
    forward = 0
    backward = 1

    def __str__(self):
        return str(self.value)


def _write_sketches(filename, sketches):
    """
    Write an list of sketches to the given file
    A sketch is a tuple of (direction, landmark, distance)

    :param filename:
    :param sketches:
    :return:
    """
    file = open(filename, mode='w+')
    file.writelines(['\t'.join(map(str, sketch))+'\n' for sketch in sketches])
    file.close()


def _read_sketches(filename):
    """
    Reads an list of sketches from the given file
    A sketch is a tuple of (direction, landmark, distance)

    :param filename:
    :return: list of sketches
    """
    sketches = list()
    file = open(filename, mode='r')
    for line in file:
        parts = line.split('\t')
        sketches.append((Direction(int(parts[0])), parts[1], int(parts[2])))
    return sketches


def precomputation(g, directory, k):
    """
    Implements the Sketch Algorithm as Defined by Das Sarma et al. http://doi.acm.org/10.1145/1718487.1718537

    :param g: A graph, classes are defined in graph.py
    :param k: Number of iterations
    :return:
    """

    logging.info('Start das_sarma precomputation')

    sketches = dict()

    # Calculate sketches
    r = max(1, math.floor(math.log2(g.n())))
    logging.info('r = '+str(r))

    for i in range(k):
        for j in range(r):
            landmarks = g.random_nodes(2**j)
            logging.info('i = ' + str(i) + ', j = ' + str(j) + ', landmarks = ' + str(landmarks))

            # Forward search
            shortest_paths = g.shortest_path_nodes_to_landmark_length(landmarks)
            for node, (landmark, distance) in shortest_paths.items():
                if node not in sketches:
                    sketches[node] = list()

                sketches[node].append((Direction.forward, landmark, distance))

            # Backward search
            shortest_paths = g.shortest_path_nodes_from_landmark_length(landmarks)
            for node, (landmark, distance) in shortest_paths.items():
                if node not in sketches:
                    sketches[node] = list()

                sketches[node].append((Direction.backward, landmark, distance))


    # Write sketches to file
    logging.info('Starting to write '+str(len(sketches))+' files')
    for node, data in sketches.items():
        _write_sketches(_file_name(node, directory), data)


    logging.info('Finished das_sarma precomputation')


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

    # Approximate distance
    best_distance = float('inf')
    for s_sketch in s_sketches:
        for d_sketch in d_sketches:

            if s_sketch[1] == d_sketch[1]:
                distance = s_sketch[2] + d_sketch[2]
                if distance < best_distance:
                    best_distance = distance

    return best_distance

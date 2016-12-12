import enum


class Path(list):
    def __lt__(self, other):
        return len(self) < len(other)

    def __gt__(self, other):
        return len(self) > len(other)


def _file_name(name, directory):
    return directory+'/'+str(name)+'.txt'


# Direction enum
class Direction(enum.IntEnum):
    forward = 0
    backward = 1

    def __str__(self):
        return str(self.value)


def _write_sketch_distances(filename, sketches):
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


def _read_sketch_distances(filename):
    """
    Reads an list of sketches from the given file
    A sketch is a tuple of (direction, landmark, distance)

    :param filename:
    :return: list of sketches
    """
    if not os.path.exists(filename):
        return None

    sketches = list()
    file = open(filename, mode='r')
    for line in file:
        parts = line.split('\t')
        sketches.append((Direction(int(parts[0])), parts[1], int(parts[2])))
    return sketches


def _write_sketch_paths(filename, sketches):
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


def _read_sketch_paths(filename):
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


def calculate_sketch_landmarks_distances(g, landmarks):
    sketches = dict()
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

    return sketches


def calculate_sketch_landmarks_paths(g, landmarks):
    sketches = dict()
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

    return sketches
from abc import ABCMeta, abstractmethod
import random
import networkx


class Graph(metaclass=ABCMeta):

    def __int__(self):
        return

    @abstractmethod
    def read_edgelist(self, filename):
        raise NotImplementedError()

    @abstractmethod
    def n(self):
        raise NotImplementedError()

    @abstractmethod
    def m(self):
        raise NotImplementedError()

    @abstractmethod
    def random_node(self):
        raise NotImplementedError()

    def random_nodes(self, n = 1):
        return [self.random_node() for i in range(n)]

    @abstractmethod
    def successors(self, node):
        raise NotImplementedError()

    @abstractmethod
    def predecessors(self, node):
        raise NotImplementedError()

    @staticmethod
    def _path_length(path):
        if path is None:
            return float('inf')
        else:
            return len(path) - 1

    @abstractmethod
    def shortest_path(self, source_node, destination_node):
        raise NotImplementedError()

    def shortest_path_length(self, source_node, destination_node):
        return self._path_length(self.shortest_path(source_node, destination_node))

    @abstractmethod
    def dijkstra_path(self, source_node, destination_node):
        raise NotImplementedError()

    def dijkstra_path_length(self, source_node, destination_node):
        return self._path_length(self.dijkstra_path(source_node, destination_node))

    @abstractmethod
    def bidirectional_shortest_path(self, source_node, destination_node):
        raise NotImplementedError()

    def bidirectional_shortest_path_length(self, source_node, destination_node):
        return self._path_length(self.bidirectional_shortest_path(source_node, destination_node))


    def _shortest_path_nodes_landmark_length(self, landmarks, expansion_function):
        shortest_paths = {l: (l, 0) for l in landmarks}

        expansion = set(landmarks)
        while expansion:
            new_expansion = set()

            for v in expansion:
                # successors that are not found before
                successors = [u for u in expansion_function(v) if u not in shortest_paths.keys()]

                for successor in successors:
                    shortest_paths[successor] = (shortest_paths[v][0], shortest_paths[v][1] + 1)
                    new_expansion.add(successor)

            expansion = new_expansion

        return shortest_paths

    def shortest_path_nodes_to_landmark_length(self, landmarks):
        return self._shortest_path_nodes_landmark_length(landmarks, self.predecessors)

    def shortest_path_nodes_from_landmark_length(self, landmarks):
        return self._shortest_path_nodes_landmark_length(landmarks, self.successors)

    def _shortest_path_nodes_landmark_path(self, landmarks, expansion_function):
        shortest_paths = {l: [l] for l in landmarks}

        expansion = set(landmarks)
        while expansion:
            new_expansion = set()

            for v in expansion:
                # successors that are not found before
                successors = [u for u in expansion_function(v) if u not in shortest_paths.keys()]

                for successor in successors:
                    shortest_paths[successor] = [successor] + shortest_paths[v]
                    new_expansion.add(successor)

            expansion = new_expansion

        return shortest_paths

    def shortest_path_nodes_to_landmark_path(self, landmarks):
        return self._shortest_path_nodes_landmark_path(landmarks, self.predecessors)

    def shortest_path_nodes_from_landmark_path(self, landmarks):
        shortest_paths = self._shortest_path_nodes_landmark_path(landmarks, self.successors)
        return {node: reversed(path) for node, path in shortest_paths.items()}

    def print_statistics(self):
        print('N: \t', self.n())
        print('M: \t', self.m())


class NetworkxGraph(Graph):
    def __init__(self):
        self.g = networkx.DiGraph()

    def read_edgelist(self, filename):
        self.g = networkx.read_edgelist(filename, create_using=networkx.DiGraph())


    def nodes(self):
        return

    def n(self):
        return self.g.number_of_nodes()

    def m(self):
        return self.g.number_of_edges()

    def random_node(self):
        return random.choice(self.g.nodes())

    def successors(self, node):
        return self.g.successors(node)

    def predecessors(self, node):
        return self.g.predecessors(node)

    def shortest_path(self, source_node, destination_node):
        try:
            return networkx.shortest_path(self.g, source_node, destination_node)
        except networkx.exception.NetworkXNoPath:
            return None

    def dijkstra_path(self, source_node, destination_node):
        try:
            return networkx.dijkstra_path(self.g, source_node, destination_node)
        except networkx.exception.NetworkXNoPath:
            return None

    def bidirectional_shortest_path(self, source_node, destination_node):
        try:
            return networkx.bidirectional_shortest_path(self.g, source_node, destination_node)
        except networkx.exception.NetworkXNoPath:
            return None


class NetworkxGraphUndirected(NetworkxGraph):
    def __init__(self):
        self.g = networkx.Graph()

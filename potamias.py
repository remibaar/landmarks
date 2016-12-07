

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
    r = max(1, math.floor(math.log10(g.n())))
    logging.info('r = '+str(r))

    for i in range(k):
        for j in range(r + 1):
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

def deg_centrality_landmarks(g,d):
    dc = nx.degree_centrality()
    i = dc.items()
    sorted = i.sort(reverse=True, key=lambda x: x[1])
    return map(lambda x: x[0], sorted[:d])
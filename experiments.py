import experiment
import das_sarma
import gubichev
import logging
import potamias
import graph

logging.basicConfig(level=logging.INFO)

data_sets = [
    #"test",
    "slashdot",
    #"google",
    #"gplus",
    "facebook",
    "twitter"
    #"roadnet_ca"
]

undirected = ["facebook"]

iterations = 10
checks = 500

experiments = dict()

for data in data_sets:
    
    if data in undirected:
        graph_processor = graph.NetworkxGraphUndirected
    else:
        graph_processor = graph.NetworkxGraph
    
    id = 'gubichev_' + data
    experiments[id] = experiment.Experiment(id=id, graph_processor=graph_processor, edgelist=data + '.txt',
                                            number_of_iterations=iterations,
                                            number_of_checks=checks,
                                            precomputation_func=gubichev.precomputation,
                                            precomputation_kwargs={'k': 1},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce}),
                                                'sketch_cesc': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_cesc}),
                                                'tree_sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.tree_sketch}),
                                            })

    id = 'random_20_' + data
    experiments[id] = experiment.Experiment(id=id, graph_processor=graph_processor, edgelist=data + '.txt',
                                            number_of_iterations=iterations,
                                            number_of_checks=checks,
                                            precomputation_func=potamias.precomputation,
                                            precomputation_kwargs={'landmark_function': potamias.select_nodes,
                                                                   'landmark_kwargs': {'k': 50, 'd': 20,
                                                                                       'strategy': 'random',
                                                                                       'dataset_name': data}},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce})
                                            })

    id = 'degree_20_' + data
    experiments[id] = experiment.Experiment(id=id, graph_processor=graph_processor, edgelist=data + '.txt',
                                            number_of_iterations=1,
                                            number_of_checks=checks,
                                            precomputation_func=potamias.precomputation,
                                            precomputation_kwargs={'landmark_function': potamias.select_nodes,
                                                                   'landmark_kwargs': {'k': 50, 'd': 20,
                                                                                       'strategy': 'closeness',
                                                                                       'dataset_name': data}},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce})
                                            })

    id = 'centrality_20_' + data
    experiments[id] = experiment.Experiment(id=id, graph_processor=graph_processor, edgelist=data + '.txt',
                                            number_of_iterations=1,
                                            number_of_checks=checks,
                                            precomputation_func=potamias.precomputation,
                                            precomputation_kwargs={'landmark_function': potamias.select_nodes,
                                                                   'landmark_kwargs': {'k': 50, 'd': 20,
                                                                                       'strategy': 'random',
                                                                                       'dataset_name': data}},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce})
                                            })

    id = 'degree_constrained_20_' + data
    experiments[id] = experiment.Experiment(id=id, graph_processor=graph_processor, edgelist=data + '.txt',
                                            number_of_iterations=1,
                                            number_of_checks=checks,
                                            precomputation_func=potamias.precomputation,
                                            precomputation_kwargs={'landmark_function': potamias.select_nodes,
                                                                   'landmark_kwargs': {'k': 50, 'd': 20, 'h': 1,
                                                                                       'constrained': True,
                                                                                       'strategy': 'closeness',
                                                                                       'dataset_name': data}},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce})
                                            })

    id = 'centrality_constrained_20_' + data
    experiments[id] = experiment.Experiment(id=id, graph_processor=graph_processor, edgelist=data + '.txt',
                                            number_of_iterations=1,
                                            number_of_checks=checks,
                                            precomputation_func=potamias.precomputation,
                                            precomputation_kwargs={'landmark_function': potamias.select_nodes,
                                                                   'landmark_kwargs': {'k': 50, 'd': 20, 'h': 1,
                                                                                       'constrained': True,
                                                                                       'strategy': 'random',
                                                                                       'dataset_name': data}},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce})
                                            })

    id = 'degree_partition_20_' + data
    experiments[id] = experiment.Experiment(id=id, graph_processor=graph_processor, edgelist=data + '.txt',
                                            number_of_iterations=1,
                                            number_of_checks=checks,
                                            precomputation_func=potamias.precomputation,
                                            precomputation_kwargs={'landmark_function': potamias.partitionp,
                                                                   'landmark_kwargs': {'type': 'dc', 'P': 20,
                                                                                       'dataset_name': data}},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce})
                                            }
                                            )

    id = 'centrality_partition_20_' + data
    experiments[id] = experiment.Experiment(id=id, graph_processor=graph_processor, edgelist=data + '.txt',
                                            number_of_iterations=1,
                                            number_of_checks=checks,
                                            precomputation_func=potamias.precomputation,
                                            precomputation_kwargs={'landmark_function': potamias.partitionp,
                                                                   'landmark_kwargs': {'type': 'cc', 'P': 20, 'k': 50,
                                                                                       'dataset_name': data}},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce})
                                            }
                                            )

    id = 'border_partition_20_' + data
    experiments[id] = experiment.Experiment(id=id, graph_processor=graph_processor, edgelist=data + '.txt',
                                            number_of_iterations=1,
                                            number_of_checks=checks,
                                            precomputation_func=potamias.precomputation,
                                            precomputation_kwargs={'landmark_function': potamias.borderp,
                                                                   'landmark_kwargs': {'P': 20, 'dataset_name': data}},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce})
                                            }
                                            )

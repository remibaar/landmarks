import experiment
import das_sarma
import gubichev
import logging
import potamias

logging.basicConfig(level=logging.INFO)

data_sets = [
    "slashdot",
    #"google",
    #"gplus",
    "facebook",
    #"roadnet_ca"
]

experiments = dict()

for data in data_sets:
    id = 'gubichev_' + data
    experiments[id] = experiment.Experiment(id=id, edgelist=data + '.txt',
                                            number_of_iterations=20,
                                            number_of_checks=1000,
                                            precomputation_func=gubichev.precomputation,
                                            precomputation_kwargs={'k': 2},
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

    id = 'random_' + data
    experiments[id] = experiment.Experiment(id=id, edgelist=data + '.txt',
                                            number_of_iterations=20,
                                            number_of_checks=1000,
                                              precomputation_func=potamias.precomputation,
                                              precomputation_kwargs={'landmark_function': potamias.random, 'landmark_kwargs': {'d': 20}},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce})
                                            })

    id = 'degree_' + data
    experiments[id] = experiment.Experiment(id=id, edgelist=data + '.txt',
                                            number_of_iterations=20,
                                            number_of_checks=1000,
                                              precomputation_func=potamias.precomputation,
                                              precomputation_kwargs={'landmark_function': potamias.random, 'landmark_kwargs': {'d': 20}},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce})
                                            })

    id = 'partition1_' + data
    experiments[id] = experiment.Experiment(id=id, edgelist=data + '.txt',
                                            number_of_iterations=20,
                                            number_of_checks=1000,
                                              precomputation_func=potamias.precomputation,
                                              precomputation_kwargs={'landmark_function': potamias.partitionp, 'landmark_kwargs': {'p': 1, 'name': '/tmp/partitions/'+id+'.csv'}},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce})
                                            })

    id = 'centrality_' + data
    experiments[id] = experiment.Experiment(id=id, edgelist=data + '.txt',
                                            number_of_iterations=20,
                                            number_of_checks=1000,
                                              precomputation_func=potamias.precomputation,
                                              precomputation_kwargs={'landmark_function': potamias.select_nodes,
                                                                     'landmark_kwargs': {'k':50, 'd':20, 'strategy':'closeness'}},
                                            computations={
                                                'sketch': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                    gubichev.convert_queue_to_length,
                                                    {'function': gubichev.sketch_ce})
                                            })


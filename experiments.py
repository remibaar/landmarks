import experiment
import das_sarma
import gubichev
import logging

logging.basicConfig(level=logging.INFO)
experiments = {
    'slashdot_k1': experiment.Experiment(id='slashdot_k1', edgelist='data/slashdot.txt', number_of_iterations=1,
                                            number_of_checks=1000,
                                            precomputation_func=gubichev.precomputation,
                                            precomputation_kwargs={'k': 1},
                                            computations={
                                                'sketch': (
                                                gubichev.convert_queue_to_length, {'function': gubichev.sketch}),
                                                'sketch_ce': (
                                                gubichev.convert_queue_to_length, {'function': gubichev.sketch_ce}),
                                                'sketch_cesc': (
                                                gubichev.convert_queue_to_length, {'function': gubichev.sketch_cesc}),
                                                'tree_sketch': (
                                                gubichev.convert_queue_to_length, {'function': gubichev.tree_sketch}),
                                            }),

    'slashdot_k2': experiment.Experiment(id='slashdot_k2', edgelist='data/slashdot.txt', number_of_iterations=1,
                                         number_of_checks=1000,
                                         precomputation_func=gubichev.precomputation,
                                         precomputation_kwargs={'k': 2},
                                         computations={
                                             'sketch': (
                                                 gubichev.convert_queue_to_length, {'function': gubichev.sketch}),
                                             'sketch_ce': (
                                                 gubichev.convert_queue_to_length, {'function': gubichev.sketch_ce}),
                                             'sketch_cesc': (
                                                 gubichev.convert_queue_to_length, {'function': gubichev.sketch_cesc}),
                                             'tree_sketch': (
                                                 gubichev.convert_queue_to_length, {'function': gubichev.tree_sketch}),
                                         }),

    'slashdot_k3': experiment.Experiment(id='slashdot_k3', edgelist='data/slashdot.txt', number_of_iterations=1,
                                         number_of_checks=1000,
                                         precomputation_func=gubichev.precomputation,
                                         precomputation_kwargs={'k': 3},
                                         computations={
                                             'sketch': (
                                                 gubichev.convert_queue_to_length, {'function': gubichev.sketch}),
                                             'sketch_ce': (
                                                 gubichev.convert_queue_to_length, {'function': gubichev.sketch_ce}),
                                             'sketch_cesc': (
                                                 gubichev.convert_queue_to_length, {'function': gubichev.sketch_cesc}),
                                             'tree_sketch': (
                                                 gubichev.convert_queue_to_length, {'function': gubichev.tree_sketch}),
                                         })

}

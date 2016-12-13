import experiment
import das_sarma
import gubichev
import logging
import potamias

logging.basicConfig(level=logging.INFO)
experiments = {
    'gubichev_k1_slashdot': experiment.Experiment(id='gubichev_k1_slashdot', edgelist='data/slashdot.txt',
                                                  number_of_iterations=20,
                                                  number_of_checks=1000,
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
                                                  }),

    'gubichev_k2_slashdot': experiment.Experiment(id='gubichev_k2_slashdot', edgelist='data/slashdot.txt',
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
                                                  }),
    'gubichev_k1_gplus': experiment.Experiment(id='gubichev_k1_gplus', edgelist='data/gplus.txt', number_of_iterations=20,
                                               number_of_checks=1000,
                                               precomputation_func=gubichev.precomputation,
                                               precomputation_kwargs={'k': 1},
                                               computations={
                                                   'sketch': (
                                                       gubichev.convert_queue_to_length, {'function': gubichev.sketch}),
                                                   'sketch_ce': (
                                                       gubichev.convert_queue_to_length,
                                                       {'function': gubichev.sketch_ce}),
                                                   'sketch_cesc': (
                                                       gubichev.convert_queue_to_length,
                                                       {'function': gubichev.sketch_cesc}),
                                                   'tree_sketch': (
                                                       gubichev.convert_queue_to_length,
                                                       {'function': gubichev.tree_sketch}),
                                               }),

    'gubichev_k2_gplus': experiment.Experiment(id='gubichev_k2_gplus', edgelist='data/gplus.txt', number_of_iterations=20,
                                               number_of_checks=1000,
                                               precomputation_func=gubichev.precomputation,
                                               precomputation_kwargs={'k': 2},
                                               computations={
                                                   'sketch': (
                                                       gubichev.convert_queue_to_length, {'function': gubichev.sketch}),
                                                   'sketch_ce': (
                                                       gubichev.convert_queue_to_length,
                                                       {'function': gubichev.sketch_ce}),
                                                   'sketch_cesc': (
                                                       gubichev.convert_queue_to_length,
                                                       {'function': gubichev.sketch_cesc}),
                                                   'tree_sketch': (
                                                       gubichev.convert_queue_to_length,
                                                       {'function': gubichev.tree_sketch}),
                                               }),
    'gubichev_k1_google': experiment.Experiment(id='gubichev_k1_google', edgelist='data/google.txt', number_of_iterations=20,
                                                number_of_checks=1000,
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
                                                }),

    'gubichev_k2_google': experiment.Experiment(id='gubichev_k2_google', edgelist='data/google.txt', number_of_iterations=20,
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
                                                 }),

}

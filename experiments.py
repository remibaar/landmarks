import experiment
import das_sarma
import gubichev
import logging

logging.basicConfig(level=logging.INFO)
experiments = {
    'das_sarma_test': experiment.Experiment(
        edgelist='data/test.txt',
        precomputation_dir='/tmp/sketches/das_sarma_test',
        precomputation=das_sarma.precomputation,
        precomputation_kwargs={'k': 1},
        number_of_checks=32,
        computation=das_sarma.sketch,
        force_precomputation=True,
        id='test'
    ),
    'gubichev_slashdot_cesc': experiment.Experiment(
        edgelist='data/slashdot.txt',
        precomputation_dir='/tmp/sketches/gubichev_slashdot_cesc',
        precomputation=gubichev.precomputation,
        precomputation_kwargs={'k': 2},
        number_of_checks=1000,
        computation=gubichev.convert_queue_to_length,
        computation_kwargs={'function': gubichev.sketch_cesc},
        force_precomputation=False,
        id='gubichev_slashdot_cesc'
    ),

    'gubichev_slashdot_ce': experiment.Experiment(
        edgelist='data/slashdot.txt',
        precomputation_dir='/tmp/sketches/gubichev_slashdot_ce',
        precomputation=gubichev.precomputation,
        precomputation_kwargs={'k': 2},
        number_of_checks=1000,
        computation=gubichev.convert_queue_to_length,
        computation_kwargs={'function': gubichev.sketch_ce},
        force_precomputation=False,
        id='gubichev_slashdot_ce'
    ),

    'gubichev_slashdot_sketch': experiment.Experiment(
        edgelist='data/slashdot.txt',
        precomputation_dir='/tmp/sketches/gubichev_slashdot_ce',
        precomputation=gubichev.precomputation,
        precomputation_kwargs={'k': 2},
        number_of_checks=1000,
        computation=gubichev.convert_queue_to_length,
        computation_kwargs={'function': gubichev.sketch},
        force_precomputation=False,
        id='gubichev_slashdot_ce'
    ),

}

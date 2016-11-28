import experiment
import das_sarma
import logging

logging.basicConfig(level=logging.INFO)
experiments = {
    'das_sarma_test': experiment.Experiment(
                edgelist='data/test.txt',
                precomputation_dir='/tmp/sketches_test',
                precomputation=das_sarma.precomputation,
                precomputation_kwargs={'k':1},
                number_of_checks=32,
                computation=das_sarma.sketch,
                force_precomputation=True,
                id='test'
            ),

}
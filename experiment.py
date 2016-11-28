import graph
import os
import logging

class Experiment:

    def __init__(
            self,
            id,
            edgelist,
            computation,
            number_of_checks,
            computation_kwargs = dict(),
            graph_processor=graph.NetworkxGraph,
            precomputation=None,
            precomputation_dir=None,
            precomputation_kwargs=dict(),
            force_precomputation=False
    ):
        self.id = id
        self.edgelist = edgelist
        self.graph_processor = graph_processor
        self.computation_func = computation
        self.precomputation_func = precomputation
        self.precomputation_kwargs = precomputation_kwargs
        self.precomputation_dir = precomputation_dir
        self.force_precomputation = force_precomputation
        self.computation_kwargs = computation_kwargs
        self.number_of_checks = number_of_checks

    def _load_graph(self):
        self.graph = self.graph_processor()
        self.graph.read_edgelist(self.edgelist)

    def precomputation(self):
        if self.precomputation is None:
            logging.info('No precomputation function is set')
            return

        if not self.force_precomputation and self.precomputation_dir is not None:
            if os.path.isdir(self.precomputation_dir):
                if os.path.exists(self.precomputation_dir+'/.precompation_completed'):
                    logging.info('Precomputation has already been processed and is not forced')
                    return

        # make dir if not exists
        if not os.path.exists(self.precomputation_dir):
            os.makedirs(self.precomputation_dir)

        logging.info('Start precomputation')
        self.precomputation_func(self.graph, self.precomputation_dir, **self.precomputation_kwargs)
        logging.info('Finished precomputation')

        # Create flag file, to indicate precomputation was completed
        open(self.precomputation_dir+'/.precompation_completed', mode='w+').close()

    def computation(self):
        good_results = list()
        for i in range(self.number_of_checks):
            s = self.graph.random_node()
            d = self.graph.random_node()
            good_results.append((s, d, self.graph.shortest_path_length(s, d)))

        for (s, d, real_distance) in good_results:
            approx_distance = self.computation_func(s, d, self.graph, self.precomputation_dir, **self.computation_kwargs)
            print(s, ' -> ', d, ' = ', approx_distance, '(real distance = ', real_distance, ')')

    def run(self):
        self._load_graph()
        self.precomputation()
        self.computation()
import graph
import os
import logging
import timeit

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
            force_precomputation=False,
            landmark_sel=None,
            landmark_sel_kwargs=dict()
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
        self.landmark_sel = landmark_sel
        self.landmark_sel_kwargs = landmark_sel_kwargs

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
        tick = timeit.default_timer()
        self.precomputation_func(self.graph, self.precomputation_dir, **self.precomputation_kwargs)
        tock = timeit.default_timer()

        logging.info('Finished precomputation in '+str(tock-tick)+'s')

        # Create flag file, to indicate precomputation was completed
        open(self.precomputation_dir+'/.precompation_completed', mode='w+').close()

    def computation(self):
        good_results = list()

        logging.info('Start selection of random nodes and distance calculation')

        tick = timeit.default_timer()
        for i in range(self.number_of_checks):
            s = self.graph.random_node()
            d = self.graph.random_node()
            good_results.append((s, d, self.graph.shortest_path_length(s, d)))
        tock = timeit.default_timer()

        logging.info('Finished selection of random nodes and distance calculation in '+str(tock-tick)+'s')

        logging.info('Start approximations')
        approximations = list()
        tick = timeit.default_timer()
        for (s, d, real_distance) in good_results:
            approximations.append(self.computation_func(s, d, self.graph, self.precomputation_dir, **self.computation_kwargs))
            #print(s, ' -> ', d, ' = ', approx_distance, '(real distance = ', real_distance, ')')
        tock = timeit.default_timer()
        logging.info('Finished approximations in '+str(tock-tick)+'s')

        logging.info('Start calculation metrics')
        total_approx_error = 0
        for i in range(self.number_of_checks):
            (s, d, real_distance) = good_results[i]
            total_approx_error += (abs(real_distance - approximations[i]) + 1) / (real_distance + 1)
        avg_approx_error = total_approx_error / self.number_of_checks

        print('Average approximation error is ' + str(avg_approx_error))
        logging.info('Finished Start calculation metrics')

    def run(self):
        self._load_graph()
        self.precomputation()
        self.computation()
import graph
import os
import logging
import timeit
import config
import pandas as pd


class Experiment:
    def __init__(self, id, edgelist, computations, precomputation_func, precomputation_kwargs={}, number_of_checks=1,
                 number_of_iterations=1, graph_processor=graph.NetworkxGraph, dijkstra=False):
        self.precomputation_results = pd.DataFrame(columns=['id', 'time', 'dir_size'])
        self.results = pd.DataFrame(columns=['s', 'd', 'dijkstra_distance', 'dijkstra_time'])

        self.number_of_iterations = number_of_iterations
        self.number_of_checks = number_of_checks

        self.precomputation_func = precomputation_func
        self.precomputation_kwargs = precomputation_kwargs
        self.id = id

        self.computations = computations

        self.edgelist = config.data_dir + edgelist
        self.graph_processor = graph_processor

        self.dijkstra = dijkstra

    def _load_graph(self):
        self.graph = self.graph_processor()
        self.graph.read_edgelist(self.edgelist)

    def precomputation(self, dir, id):

        if self.precomputation_func is None:
            return

        # make dir if not exists
        if not os.path.exists(dir):
            os.makedirs(dir)

        tick = timeit.default_timer()
        self.precomputation_func(self.graph, dir, **self.precomputation_kwargs)
        tock = timeit.default_timer()

        # Calculate results and add to data set
        time = tock - tick
        dir_size = sum([os.path.getsize(dir + '/' + f) for f in os.listdir(dir) if os.path.isfile(dir + '/' + f)])

        result = pd.DataFrame([{'id': id, 'time': time, 'dir_size': dir_size}])

        self.precomputation_results = self.precomputation_results.append(result, ignore_index=True)

    def determine_test_set(self):

        columns = ['s', 'd', 'bidirectional_distance', 'bidirectional_time']

        if self.dijkstra:
            columns.append('dijkstra_distance')
            columns.append('dijkstra_time')

        results = pd.DataFrame(
            columns=columns)

        for i in range(self.number_of_checks):
            s = self.graph.random_node()
            d = self.graph.random_node()

            tic = timeit.default_timer()
            bidirectional_distance = self.graph.bidirectional_shortest_path_length(s, d)
            toc = timeit.default_timer()
            bidirectional_time = toc - tic

            if self.dijkstra:
                tic = timeit.default_timer()
                dijkstra_distance = self.graph.dijkstra_path_length(s, d)
                toc = timeit.default_timer()
                dijkstra_time = toc - tic

            if self.dijkstra:
                results.loc[i] = [s, d, bidirectional_distance, bidirectional_time, dijkstra_distance, dijkstra_time]
            else:
                results.loc[i] = [s, d, bidirectional_distance, bidirectional_time]

        return results

    def computation(self, id, results, precomputation_dir, function, function_kwargs):

        new_results = pd.DataFrame(columns=[id + '_time', id + '_approximation'])
        for i, row in results.iterrows():
            s = row['s']
            d = row['d']

            tick = timeit.default_timer()
            approximation = function(s, d, self.graph, precomputation_dir, **function_kwargs)
            tock = timeit.default_timer()

            # Calculate results and add to data set
            time = tock - tick

            new_results.loc[i] = [time, approximation]

        return pd.concat([results, new_results], axis=1)

    def create_flag(self, dir):
        open(dir + '/.completed', mode='w+').close()

    def check_flag(self, dir):
        if os.path.isdir(dir):
            if os.path.exists(dir + '/.precompation_completed'):
                return True
        return False

    def run(self):

        results_dir = config.result_dir + '/' + str(self.id) + '/'

        if self.check_flag(results_dir):
            logging.info('Already computated', self.id, ' so skipping it!')

        # make dir if not exists
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Load graph
        self._load_graph()

        for i in range(self.number_of_iterations):
            sketch_dir = config.sketch_dir + '/' + str(self.id) + '/' + str(i) + '/'
            self.precomputation(sketch_dir, i)

            results = self.determine_test_set()
            for id, (func, kwargs) in self.computations.items():
                results = self.computation(id, results, sketch_dir, func, kwargs)

            results.to_excel(results_dir + str(i) + '.xlsx')

        self.precomputation_results.to_excel(results_dir + 'precomputation.xlsx')

        self.create_flag(results_dir)


"""
class Experiment:

    def __init__(
            self,
            id,
            edgelist,
            number_of_checks,
            computations,
            number_of_iterations=1,
            precomputation=None,
            precomputation_kwargs=dict(),
            graph_processor=graph.NetworkxGraph
    ):
        self.id = id
        self.edgelist = edgelist
        self.graph_processor = graph_processor
        self.computations = computations
        self.precomputation_func = precomputation
        self.precomputation_kwargs = precomputation_kwargs
        self.number_of_checks = number_of_checks
        self.number_of_iterations = number_of_iterations

        self.precomputation_time = list()
        self.computation_results = list()
        self.computation_time = list()

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

    def computation(self, function, function_kwargs):
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
        tock = timeit.default_timer()
        logging.info('Finished approximations in '+str(tock-tick)+'s')

        logging.info('Start calculation metrics')
        total_approx_error = 0
        for i in range(self.number_of_checks):
            (s, d, real_distance) = good_results[i]

            if (real_distance != float('inf') or approximations[i] != float('inf')) and (real_distance > 0) :
                total_approx_error += abs(real_distance - approximations[i]) / real_distance

        avg_approx_error = total_approx_error / self.number_of_checks


        print('Average approximation error is ' + str(avg_approx_error))
        logging.info('Finished Start calculation metrics')

    def run(self):
        self._load_graph()

        for i in range(self.number_of_checks):
            self.precomputation()
            self.computation() """

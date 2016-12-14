import experiments
from concurrent.futures import ProcessPoolExecutor
import time
import config

print("Running all the experiments")

# Define a function for the thread
def execute_experiment(arg):
    experiment = arg
    print('Start to run ', experiment.id)
    experiment.run()
    print('Finished', experiment.id)


executor = ProcessPoolExecutor(max_workers=config.max_workers)
schedule = list()
# Create two threads as follows
for key, exp in experiments.experiments.items():
    print('Schedule experiment', key)
    schedule.append(executor.submit(execute_experiment, exp))

print('Run the experiments')

results = [x.result() for x in schedule]



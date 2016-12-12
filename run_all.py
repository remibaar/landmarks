import experiments

for key, exp in experiments.experiments:
    print('Start experiment', key)
    exp.run()

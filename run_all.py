import experiments

for key, exp in experiments.experiments.items():
    print('Start experiment', key)
    exp.run()

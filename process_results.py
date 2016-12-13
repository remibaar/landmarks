import pandas as pd
import config
import logging

ids = [
    'gubichev_facebook', 'gubichev_google', 'gubichev_gplus', 'gubichev_roadnet_ca', 'gubichev_slashdot'
]

precomputation_results = pd.DataFrame(columns=['id', 'iterations', 'time_mean', 'time_std', 'size_mean', 'size_std'])

for index, id in enumerate(ids):
    precomputation_file = config.result_dir + id + '/precomputation.xlsx'

    try:
        df = pd.read_excel(precomputation_file)
    except Exception as e:
        logging.warning('Unable to load precomputation file: '+precomputation_file+' (' + str(e) + ')')
        continue

    precomputation_results.loc[index] = [id, df.count(), df['time'].mean(), df['time'].std(), df['dir_size'].mean(), df['dir_size'].std()]

precomputation_results.to_excel(config.final_result_dir+'precomputation.xlsx')
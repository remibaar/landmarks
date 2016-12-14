import pandas as pd
import config
import logging
import re
import os
import experiments

ids = experiments.experiments.keys()


# Precomputation results
#precomputation_results = pd.DataFrame(columns=['id', 'iterations', 'time_mean', 'size_mean'])
results = dict()
for index, id in enumerate(ids):
    precomputation_file = config.result_dir + id + '/precomputation.xlsx'

    # Get info from id
    id_parts = id.split('_')
    data_name = id_parts[-1]
    precomputation_name = ' '.join(id_parts[:-1])

    try:
        df = pd.read_excel(precomputation_file)
    except Exception as e:
        logging.warning('Unable to load precomputation file: '+precomputation_file+' (' + str(e) + ')')
        continue

    if data_name not in results:
        results[data_name] = dict()
    results[data_name].update({
        (precomputation_name, 'time_mean'): df['time'].mean(),
        (precomputation_name, 'time_median'): df['time'].median(),
        (precomputation_name, 'size'): df['dir_size'].mean()
    })

    #precomputation_results.loc[index] = [id, df['id'].count(), df['time'].mean(), df['time'].std(), df['dir_size'].mean(), df['dir_size'].std()]

#precomputation_results.to_excel(config.final_result_dir+'precomputation.xlsx')
pd.DataFrame(results).to_excel(config.final_result_dir+'precomputation.xlsx')


#############
# Gubichev
#############


# Computation results
file_re = re.compile('^[0-9]+\.xlsx$')
results_error = pd.DataFrame()
results_time = pd.DataFrame()
for index, id in enumerate([id for id in ids if id.startswith('gubichev')]):

    # Get info from id
    id_parts = id.split('_')
    data_name = id_parts[-1]

    # Read directory and load all dataframes
    dir = config.result_dir + id + '/'
    dfs = list()
    if not os.path.exists(dir):
        logging.warning('Unable to load experiments dir: ' + dir)
        continue
    for file in os.listdir(dir):
        if not file_re.match(file):
            continue

        try:
            df = pd.read_excel(dir+file)
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            logging.warning('Unable to load resulst file: '+dir+file+' (' + str(e) + ')')

    if len(dfs) > 1:
        total_df = pd.concat(dfs)
    elif len(dfs) == 1:
        total_df = dfs[0]
    else:
        logging.warning('No results found in '+dir)
        continue


    # Store result in dictionary before adding to data frame
    result_time = {('info', 'dataset'): data_name, ('info', 'tests'): total_df.shape[0]}
    result_error = {('info', 'dataset'): data_name, ('info', 'tests'): total_df.shape[0]}

    algorithms = [col.replace('_approximation', '') for col in total_df.columns.values if col.endswith('_approximation')]
    for a in algorithms:

        a_approx = a+'_approximation'
        a_time = a+'_time'

        def approx_error(x):
            if x['bidirectional_distance'] == 0:
                return float(x[a_approx] != 0)
            elif float(x['bidirectional_distance']) == float('inf'):
                return float(float(x[a_approx]) != float('inf'))
            elif float(x[a_approx]) == float('inf'):
                return 1
            else:
                return (x[a_approx] - x['bidirectional_distance']) / x['bidirectional_distance']


        error = total_df.apply(approx_error, axis=1)
        time = total_df[a_time]

        result_error[(a, 'mean')] = error.mean()
        result_error[(a, 'std')] = error.std()

        result_time[(a, 'mean')] = time.mean()
        result_time[(a, 'std')] = time.std()

    # Add bidirectional time to results
    a = 'bidirectional'
    time = total_df[a+'_time']
    result_time[(a, 'mean')] = time.mean()
    result_time[(a, 'std')] = time.std()

    # Create DF from dictionary
    df_result_error = pd.DataFrame(result_error, index=[0])
    df_result_time = pd.DataFrame(result_time, index=[0])

    # Add DF to total overview DF
    results_error = pd.concat([results_error, df_result_error])
    results_time = pd.concat([results_time, df_result_time])

results_error.to_excel(config.final_result_dir+'gubichev_error.xlsx')
results_time.to_excel(config.final_result_dir+'gubichev_time.xlsx')


#############
# Potamias
#############

file_re = re.compile('^[0-9]+\.xlsx$')
results_error = dict()
results_time = dict()
for index, id in enumerate([id for id in ids if not id.startswith('gubichev')]):

    # Get info from id
    id_parts = id.split('_')
    data_name = id_parts[-1]
    precomputation_name = ' '.join(id_parts[:-1])

    # Read directory and load all dataframes
    dir = config.result_dir + id + '/'
    dfs = list()
    if not os.path.exists(dir):
        logging.warning('Unable to load experiments dir: ' + dir)
        continue

    for file in os.listdir(dir):
        if not file_re.match(file):
            continue

        try:
            df = pd.read_excel(dir+file)
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            logging.warning('Unable to load resulst file: '+dir+file+' (' + str(e) + ')')

    if len(dfs) > 1:
        total_df = pd.concat(dfs)
    elif len(dfs) == 1:
        total_df = dfs[0]
    else:
        logging.warning('No results found in '+dir)
        continue


    # Store result in dictionary before adding to data frame
    result_time = dict() # {('info', 'dataset'): data_name, ('info', 'tests'): total_df.shape[0]}
    result_error = dict() #{('info', 'dataset'): data_name, ('info', 'tests'): total_df.shape[0]}

    algorithms = [col.replace('_approximation', '') for col in total_df.columns.values if col.endswith('_approximation')]
    for a in algorithms:

        a_approx = a+'_approximation'
        a_time = a+'_time'

        def approx_error(x):
            if x['bidirectional_distance'] == 0:
                return float(x[a_approx] != 0)
            elif float(x['bidirectional_distance']) == float('inf'):
                return float(float(x[a_approx]) != float('inf'))
            elif float(x[a_approx]) == float('inf'):
                return 1
            else:
                return (x[a_approx] - x['bidirectional_distance']) / x['bidirectional_distance']

        error = total_df.apply(approx_error, axis=1)
        time = total_df[a_time]

        result_error[(precomputation_name, a, 'mean')] = error.mean()
        result_error[(precomputation_name, a, 'std')] = error.std()

        result_time[(precomputation_name, a, 'mean')] = time.mean()
        result_time[(precomputation_name, a, 'std')] = time.std()

    # Add bidirectional time to results
    a = 'bidirectional'
    time = total_df[a+'_time']
    result_time[(precomputation_name, a, 'mean')] = time.mean()
    result_time[(precomputation_name, a, 'std')] = time.std()

    if data_name not in results_error:
        results_error[data_name] = dict()

    results_error[data_name].update(result_error)
    # Create DF from dictionary
    #df_result_error = pd.DataFrame(result_error, index=[data_name])
    #df_result_time = pd.DataFrame(result_time, index=[data_name])

    # Add DF to total overview DF
    #results_error = pd.concat([results_error, df_result_error], axis=0, join='outer')
    #results_time = pd.concat([results_time, df_result_time])

pd.DataFrame(results_error).to_excel(config.final_result_dir+'potamias_error.xlsx')
#results_time.to_excel(config.final_result_dir+'potamias_time.xlsx')
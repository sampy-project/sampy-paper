import numpy as np
import pandas as pd


def counts_to_csv(list_count_arr, graph, path_to_csv, sep=';', timesteps=None):
    """
    Take a list of numpy array generated by the count methods of the agent class, and save them as a CSV (easier for
    R users).

    :param list_count_arr: list of count arrays
    :param graph: graph object from which the count arrays have been extracted
    :param path_to_csv: full path to the final csv file
    :param sep: optional, string, default ';'. Separator in final CSV.
    :param timesteps: optional, list or array, default None. If not None, used to create a column 'timesteps' in the
                      csv.
    """
    row_stack = np.row_stack(list_count_arr)
    dict_ind_to_id = {ind: ids for ids, ind in graph.dict_cell_id_to_ind.items()}
    columns = [str(dict_ind_to_id[i]) for i in range(graph.connections.shape[0])]
    df = pd.DataFrame(row_stack, columns=columns)
    if timesteps is not None:
        df['timesteps'] = timesteps
    else:
        df['timesteps'] = np.array(range(1, row_stack.shape[0] + 1), dtype=np.int32)
    df.to_csv(path_to_csv, index=False, sep=sep)


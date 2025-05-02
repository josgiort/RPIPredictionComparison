import pandas as pd
from pathlib import Path
from collections import defaultdict

############################################################################################################################
# INITIAL VARIABLES
############################################################################################################################

counting_cols_of_interest = [f'{k}mer pair' for k in [1,3,5]] + [f'rna-{k}mer' for k in [1,3,5]] + [f'protein-{k}mer' for k in [1,3,5]]
datasets = ['RNAcompete_maxprobe', 'PDB_ground_truth', 'RNAcompete_minprobe', 'PDB_AF3_pred']

############################################################################################################################
# DATA IO AND COUNTING FUNCTIONS
############################################################################################################################

def read_csv(path):
    """
    Read a CSV file into a pandas DataFrame.

    Args:
        path (str): Path to the CSV file.

    Returns:
        pandas.DataFrame: The data from the CSV file.
    """
    return pd.read_csv(path)

def get_kmer_counts_tuples(df, column, normalize=False):
    """
    Calculate the counts of kmer pairs in a DataFrame, optionally filtering by thresholds.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        k (int): The kmer size.
        normalize (bool, optional): Whether to normalize the counts. Defaults to False.

    Returns:
        list: Sorted list of kmer pairs and their counts.
    """
    if normalize:
        return sorted([(kmer_pair, len(g) / len(df)) for kmer_pair, g in df.groupby(column)], key=lambda x: x[1], reverse=True)
    else:
        return sorted([(kmer_pair, len(g)) for kmer_pair, g in df.groupby(column)], key=lambda x: x[1], reverse=True)


def get_kmer_dict(df, column, normalize=False):
    """
    Calculate the counts of kmers in a DataFrame, optionally filtering by thresholds.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        k (int): The kmer size.
        normalize (bool, optional): Whether to normalize the counts. Defaults to False.

    Returns:
        dict: Dictionary of kmers and their counts.
    """
    if normalize:
        return {kmer: len(g) / len(df) for kmer, g in df.groupby(column)}
    else:
        return {kmer: len(g) for kmer, g in df.groupby(column)}


def get_data_dict(data_dir, which_kmer=None, pae_threshold=None, plddt_threshold=None):
    """
    Read the data from the CSV file.

    Returns:
        pandas.DataFrame: The data from the CSV file.
    """
    if which_kmer is None:
        data = {path.stem: read_csv(path) for path in Path(data_dir).rglob('*.csv')}
        if pae_threshold is not None:
            data = {k: v[v['pae'] <= pae_threshold] for k, v in data.items()}
        if plddt_threshold is not None:
            data = {k: v[v['plddt'] >= plddt_threshold] for k, v in data.items()}
    else:
        data = {path.stem: read_csv(path) for path in Path(data_dir).rglob(f'{which_kmer}mer*.csv')}
        if pae_threshold is not None:
            data = {k: v[v['pae'] <= pae_threshold] for k, v in data.items()}
        if plddt_threshold is not None:
            data = {k: v[v['plddt'] >= plddt_threshold] for k, v in data.items()}
    return data

    

def get_aggregated_data_dict(data_dir, pae_threshold=None, plddt_threshold=None):
    """
    Aggregate the data from the CSV files into a dict.
    """
    
    aggregated_data_dict = defaultdict(list)
    data_dict = get_data_dict(data_dir, pae_threshold, plddt_threshold)
    
    for key, df in data_dict.items():
        kmer = key.split('_')[0]
        aggregated_data_dict[kmer].append(df)
    
    return {kmer: pd.concat(dfs) for kmer, dfs in aggregated_data_dict.items()}

def get_all_counts(data_dir, normalize=False, pae_threshold=None, plddt_threshold=None):
    analysis_data = {}

    data = get_aggregated_data_dict(data_dir, pae_threshold=pae_threshold, plddt_threshold=plddt_threshold)

    for kmer, df in data.items():
        count_data = {}
        for col in counting_cols_of_interest:
            if not kmer in col:
                continue
            count_data[col] = {dataset: get_kmer_dict(d, col, normalize=normalize) for dataset, d in df.groupby('dataset_id1')}
            analysis_data[kmer] = count_data

    return analysis_data


def get_all_counts_df(data_dir, normalize=False, pae_threshold=None, plddt_threshold=None):
    data_dict = get_all_counts(data_dir, normalize=normalize, pae_threshold=pae_threshold, plddt_threshold=plddt_threshold)

    df_data = []

    for k, value in data_dict.items():
        for col, data in value.items():
            for dataset, counts in data.items():
                for kmer, count in counts.items():
                    df_data.append([k, col, dataset, kmer, count])
    return pd.DataFrame(df_data, columns=['k', 'kmer_type', 'dataset', 'kmer', 'count'])


def get_max_kmers(counts_dict, howmany=5):
    return {kmer: count for kmer, count in sorted(counts_dict.items(), key=lambda x: x[1], reverse=True)[:howmany]}

def get_individual_kmer_count(data_dict, kmer):
    return data_dict[kmer]

def get_kmer_counts_and_norm_tuples(df, column):
    """
    Calculate the counts of kmer pairs and their normalization percentage in a DataFrame, optionally filtering by thresholds.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        k (int): The kmer size.
        normalize (bool, optional): Whether to normalize the counts. Defaults to False.

    Returns:
        list: Sorted list of kmer pairs and their counts.
    """
    return sorted([(kmer_pair, len(g), len(g) / len(df)) for kmer_pair, g in df.groupby(column)], key=lambda x: x[1], reverse=True)



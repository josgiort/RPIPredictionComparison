import pandas as pd

from lib.utils import get_all_counts, get_all_counts_df
from lib.visualization import kmercount_comparison_barplot

data_dir = 'RNAcompete/counts'

# load all data into a dataframe
data_df = get_all_counts_df(data_dir, normalize=True, pae_threshold=None, plddt_threshold=None)
print(data_df)

# load all data into a dictionary
data_dict = get_all_counts(data_dir, normalize=True, pae_threshold=None, plddt_threshold=None)
print(data_dict)

# Plot kmers with plotly
# get the top 5 rna-3mers per dataset
max_kmers = 5
top_kmers = []
for dataset, counts in data_df[data_df['kmer_type'] == 'rna-3mer'].groupby('dataset'):
    max_kmer_data = counts.sort_values('count', ascending=False)[:max_kmers]
    top_kmers += list(max_kmer_data['kmer'])
    top_kmers = list(set(top_kmers))

# get data for all the top kmers for each dataset
plotting_data = []
for kmer in top_kmers:
    current = data_df[data_df['kmer'] == kmer]
    for dataset, group in current[current['kmer_type'] == 'rna-3mer'].groupby('dataset'):
        try:
            count = group['count'].values[0]
        except:
            count = 0

        plotting_data.append((kmer, dataset, count))

# and plot with plotly
kmercount_comparison_barplot(plotting_data)
    
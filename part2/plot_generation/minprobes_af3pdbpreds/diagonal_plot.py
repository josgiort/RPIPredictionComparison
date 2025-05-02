import pandas as pd
import plotly.express as px
from lib.utils import read_csv, get_kmer_counts_and_norm_tuples
from lib.visualization import two_dataset_diagonal_scatter_plot

path1 = "RNAcompete/counts/3mer_PDB_AF3_pred.csv"  # RNAcompete/counts/3mer_RNAcompete_maxprobe.csv" #
path2 = "RNAcompete/counts/3mer_PDB_ground_truth.csv"

path1.split("/")[-1].split(".")[0]
path2.split("/")[-1].split(".")[0]

# Read CSV files
dframe_1 = read_csv(path1)
dframe_2 = read_csv(path2)

# Get kmer counts
cnt_dframe_1 = get_kmer_counts_and_norm_tuples(dframe_1, column="3mer pair")
cnt_dframe_2 = get_kmer_counts_and_norm_tuples(dframe_2, column="3mer pair")

# Convert to DataFrames
df1 = pd.DataFrame(cnt_dframe_1, columns=["kmer", "count_" + path1.split("/")[-1].split(".")[0], "normalized_" + path1.split("/")[-1].split(".")[0]])
df2 = pd.DataFrame(cnt_dframe_2, columns=["kmer", "count_" + path2.split("/")[-1].split(".")[0], "normalized_" + path2.split("/")[-1].split(".")[0]])

opacity = 0.5

two_dataset_diagonal_scatter_plot(df1, df2, path1, path2, opacity=opacity)

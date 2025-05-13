
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from lib.utils import get_data_dict
import os

# Load your datasets
data_dir = "RNAcompete/counts/augmented"
tables_rnacmpt = get_data_dict(data_dir)

# RNACompete datasets
maxprobes = tables_rnacmpt["3mer_RNAcompete_aug_max"]
minprobes = tables_rnacmpt["3mer_RNAcompete_aug_min"]
af3_training = tables_rnacmpt["3mer_PDB_ground_truth"]

# Function to get the top 20 most frequent 3-mers
def get_top_3mers(df, column="protein_3mer", top_n=20):
    counts = Counter(df[column].dropna())  # Count occurrences, ignoring NaN
    return pd.DataFrame(counts.most_common(top_n), columns=["3-mer", "Count"])

# Compute top 3-mers separately for each dataset
df_maxprobe = get_top_3mers(maxprobes)
df_minprobe = get_top_3mers(minprobes)
df_af3 = get_top_3mers(af3_training)

os.makedirs("plots", exist_ok=True)

# Function to plot top 3-mers
def plot_top_3mers(df, dataset_name):
    plt.figure(figsize=(10, 5))
    sns.barplot(x="3-mer", y="Count", data=df, palette="coolwarm")
    plt.title(f"Top 20 Most Frequent 3-Mers in {dataset_name}")
    plt.xlabel("3-mer")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"plots/top_3mers_{dataset_name}.png")  # Save figure
    # plt.show()

# Plot the top 3-mers for each dataset
plot_top_3mers(df_maxprobe, "Maxprobe")
plot_top_3mers(df_minprobe, "Minprobe")
plot_top_3mers(df_af3, "AF3_Training")
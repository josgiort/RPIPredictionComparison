import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

from lib.utils import get_data_dict
import os

# Load data
data_dir = "RNAcompete/counts/augmented"
tables_rnacmpt = get_data_dict(data_dir)

maxprobes = tables_rnacmpt["3mer_RNAcompete_aug_max"]
minprobes = tables_rnacmpt["3mer_RNAcompete_aug_min"]

# Count 5-mer frequencies
def get_kmer_counts(df, col):
    return Counter(df[col])

maxprobes_protein_counts = get_kmer_counts(maxprobes, "protein_3mer")
minprobes_protein_counts = get_kmer_counts(minprobes, "protein_3mer")

maxprobes_rna_counts = get_kmer_counts(maxprobes, "rna_3mer")
minprobes_rna_counts = get_kmer_counts(minprobes, "rna_3mer")

# Convert to DataFrame for plotting
def prepare_plot_data(max_counts, min_counts):
    df = pd.DataFrame({
        "3-mer": list(max_counts.keys()) + list(min_counts.keys()),
        "Count": list(max_counts.values()) + list(min_counts.values()),
        "Dataset": ["Maxprobe"] * len(max_counts) + ["Minprobe"] * len(min_counts)
    })
    return df.sort_values(by="Count", ascending=False).head(20)  # Top 20

protein_df = prepare_plot_data(maxprobes_protein_counts, minprobes_protein_counts)
rna_df = prepare_plot_data(maxprobes_rna_counts, minprobes_rna_counts)

os.makedirs("plots", exist_ok=True)

# Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.barplot(data=protein_df, x="3-mer", y="Count", hue="Dataset", ax=axes[0])
axes[0].set_title("Top 3-mers in Proteins (maxprobe vs minprobe)")
axes[0].tick_params(axis='x', rotation=90)

sns.barplot(data=rna_df, x="3-mer", y="Count", hue="Dataset", ax=axes[1])
axes[1].set_title("Top 3-mers in RNA (maxprobe vs minprobe)")
axes[1].tick_params(axis='x', rotation=90)

plt.tight_layout()
plt.savefig("plots/Freq_3mers_max_min.pdf")
#plt.show()

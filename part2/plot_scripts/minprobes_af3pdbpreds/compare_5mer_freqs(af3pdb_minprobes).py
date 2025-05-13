import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os

from lib.utils import get_data_dict

# Load data
data_dir = "RNAcompete/counts/tables_pbdaf3preds_minprobes_tabpfn"
tables_alt = get_data_dict(data_dir)

positives = tables_alt["3mer_table_PDB_AF3_preds_tabpfn_max"]                                                                                                                                                                                     
negatives = tables_alt["3mer_table_nometrics_tabpfn_filled_min"]                                                                                                                                                                                   

# Count 5-mer frequencies
def get_kmer_counts(df, col):
    return Counter(df[col])

positives_protein_counts = get_kmer_counts(positives, "protein_3mer")
negatives_protein_counts = get_kmer_counts(negatives, "protein_3mer")

positives_rna_counts = get_kmer_counts(positives, "rna_3mer")
negatives_rna_counts = get_kmer_counts(negatives, "rna_3mer")

# Convert to DataFrame for plotting
def prepare_plot_data(positives_counts, negatives_counts):
    df = pd.DataFrame({
        "3-mer": list(positives_counts.keys()) + list(negatives_counts.keys()),
        "Count": list(positives_counts.values()) + list(negatives_counts.values()),
        "Dataset": ["Positives (AF3 predictions on PDB)"] * len(positives_counts) + ["Negatives (RNACompete Minprobes)"] * len(negatives_counts)
    })
    return df.sort_values(by="Count", ascending=False).head(20)  # Top 20

protein_df = prepare_plot_data(positives_protein_counts, negatives_protein_counts)
rna_df = prepare_plot_data(positives_rna_counts, negatives_rna_counts)

os.makedirs("plots_alt", exist_ok=True)

# Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.barplot(data=protein_df, x="3-mer", y="Count", hue="Dataset", ax=axes[0])
axes[0].set_title("Top 3-mers in Proteins (Positives vs Negatives)")
axes[0].tick_params(axis='x', rotation=90)

sns.barplot(data=rna_df, x="3-mer", y="Count", hue="Dataset", ax=axes[1])
axes[1].set_title("Top 3-mers in RNA (Positives vs Negatives)")
axes[1].tick_params(axis='x', rotation=90)

plt.tight_layout()
plt.savefig("plots_alt/Freq_5mers_PDBaf3Pred_minprobe.pdf")
# plt.show()

from lib.utils import get_data_dict
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Set your data directory
data_dir = "RNAcompete/counts/tables_pbdaf3preds_minprobes_tabpfn"
tables_alt = get_data_dict(data_dir)

positives = tables_alt["3mer_table_PDB_AF3_preds_tabpfn_max"]
negatives = tables_alt["3mer_table_nometrics_tabpfn_filled_min"]

# Define bins
bin_size = 0.1
bins = np.arange(min(positives['contact_prob_res_nt'].min(), negatives['contact_prob_res_nt'].min()),
                 max(positives['contact_prob_res_nt'].max(), negatives['contact_prob_res_nt'].max()) + bin_size, bin_size)

os.makedirs("plots_alt", exist_ok=True)

# Plot the histograms and density curves for both DataFrames
plt.figure(figsize=(10, 6))

# Use a more aesthetic color palette from seaborn
sns.histplot(positives['contact_prob_res_nt'], bins=bins, kde=True, stat="probability",
             color=sns.color_palette("coolwarm", as_cmap=True)(0.2), label='Positives (AF3 predictions on PDB)', linewidth=0.7)  # Cooler color for Maxprobes
sns.histplot(negatives['contact_prob_res_nt'], bins=bins, kde=True, stat="probability",
             color=sns.color_palette("coolwarm", as_cmap=True)(0.8), label='Negatives (RNACompete Minprobes)', linewidth=0.7)  # Warmer color for Minprobes

# Customizing the plot
plt.title('Probability Distribution of Residue Contacts in alternative dataset (Positives vs Negatives)', fontsize=12)
plt.xlabel('Probability of Residue Contacts', fontsize=10)
plt.ylabel('Density', fontsize=10)  # Y-axis now correctly represents probability

# Adjust x-ticks to only show larger intervals and prevent overlap
plt.xticks(bins, rotation=45, ha="right", fontsize=10)

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title='Dataset', fontsize=9)
plt.tight_layout()  # Prevents label overlap
plt.savefig("plots_alt/compare_contact_prob_res_nt_alt.pdf")
# plt.show()
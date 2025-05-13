from lib.utils import get_data_dict
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Set your data directory
data_dir = "RNAcompete/counts/tables_pbdaf3preds_minprobes_tabpfn"
tables_alt = get_data_dict(data_dir)

positives =  tables_alt["3mer_table_PDB_AF3_preds_tabpfn_max"]
negatives = tables_alt["3mer_table_nometrics_tabpfn_filled_min"]

# Define bins
bin_size = 1
bins = np.arange(min(positives['pae'].min(), negatives['pae'].min()),
                 max(positives['pae'].max(), negatives['pae'].max()) + bin_size, bin_size)

os.makedirs("plots_alt", exist_ok=True)

# Plot the histograms and density curves for both DataFrames
plt.figure(figsize=(10, 6))

sns.histplot(positives['pae'], bins=bins, kde=True, stat="density", color='#4c72b0', label='Positives (AF3 predictions on PDB)', linewidth=0.7)  # Cool Blue
sns.histplot(negatives['pae'], bins=bins, kde=True, stat="density", color='#dd8452', label='Negatives (RNACompete Minprobes)', linewidth=0.7)  # Warm Copper

# Customizing the plot
plt.title('Density Comparison of PAE in alternative dataset (Positives vs Negatives)', fontsize=10)
plt.xlabel('PAE Value', fontsize=7)
plt.ylabel('Density', fontsize=7)

# Adjust x-ticks to only show larger intervals and prevent overlap
plt.xticks(bins, rotation=45, ha="right", fontsize=7)

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title='Dataset', fontsize=7)
plt.tight_layout()  # Prevents label overlap
plt.savefig("plots_alt/compare_pae_alt.pdf")
# plt.show()

from lib.utils import get_data_dict
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set your data directory
data_dir = "/home/jose/Downloads/AI4NA_AF3_eval/RNAcompete/counts/tables_pbdaf3preds_minprobes_tabpfn"
tables_alt = get_data_dict(data_dir)

positives =  tables_alt["3mer_table_PDB_AF3_preds_tabpfn_max"]
negatives = tables_alt["3mer_table_nometrics_tabpfn_filled_min"]

# Define bins
bin_size = 3
bins = np.arange(min(positives['plddt'].min(), negatives['plddt'].min()),
                 max(positives['plddt'].max(), negatives['plddt'].max()) + bin_size, bin_size)

# Plot the histograms and density curves for both DataFrames
plt.figure(figsize=(10, 6))

sns.histplot(positives['plddt'], bins=bins, kde=True, stat="density", color='#1f77b4', label='Positives (AF3 predictions on PDB)', linewidth=0.7)  # Muted Blue
sns.histplot(negatives['plddt'], bins=bins, kde=True, stat="density", color='#ff7f0e', label='Negatives (RNACompete Minprobes)', linewidth=0.7)  # Soft Orange

# Customizing the plot
plt.title('Density Comparison of PLDDT in alternative dataset (Positives vs Negatives)', fontsize=10)
plt.xlabel('PLDDT Value', fontsize=7)
plt.ylabel('Density', fontsize=7)

# Adjust x-ticks to only show larger intervals and prevent overlap
plt.xticks(bins, rotation=45, ha="right", fontsize=7)

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title='Dataset', fontsize=7)
plt.tight_layout()  # Prevents label overlap
plt.savefig("compare_plddt_alt.pdf")
plt.show()

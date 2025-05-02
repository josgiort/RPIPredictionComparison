from lib.utils import get_data_dict
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set your data directory
data_dir = "/home/jose/Downloads/AI4NA_AF3_eval/RNAcompete/counts/augmented"
tables_rnacmpt = get_data_dict(data_dir)

maxprobes =  tables_rnacmpt["3mer_RNAcompete_aug_max"]
minprobes = tables_rnacmpt["3mer_RNAcompete_aug_min"]

# Define bins
bin_size = 3
bins = np.arange(min(maxprobes['plddt'].min(), minprobes['plddt'].min()),
                 max(maxprobes['plddt'].max(), minprobes['plddt'].max()) + bin_size, bin_size)

# Plot the histograms and density curves for both DataFrames
plt.figure(figsize=(10, 6))

sns.histplot(maxprobes['plddt'], bins=bins, kde=True, stat="density", color='#1f77b4', label='Maxprobes', linewidth=0.7)  # Muted Blue
sns.histplot(minprobes['plddt'], bins=bins, kde=True, stat="density", color='#ff7f0e', label='Minprobes', linewidth=0.7)  # Soft Orange

# Customizing the plot
plt.title('Density Comparison of PLDDT in Augmented RNACompete (Maxprobes vs Minprobes)', fontsize=10)
plt.xlabel('PLDDT Value', fontsize=7)
plt.ylabel('Density', fontsize=7)

# Adjust x-ticks to only show larger intervals and prevent overlap
plt.xticks(bins, rotation=45, ha="right", fontsize=7)

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title='Dataset', fontsize=7)
plt.tight_layout()  # Prevents label overlap
plt.savefig("compare_plddt_rnacmpt.pdf")
plt.show()

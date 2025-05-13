from lib.utils import get_data_dict
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Set your data directory
data_dir = "RNAcompete/counts/augmented"
tables_rnacmpt = get_data_dict(data_dir)

maxprobes =  tables_rnacmpt["3mer_RNAcompete_aug_max"]
minprobes = tables_rnacmpt["3mer_RNAcompete_aug_min"]

# Define bins
bin_size = 1
bins = np.arange(min(maxprobes['pae'].min(), minprobes['pae'].min()),
                 max(maxprobes['pae'].max(), minprobes['pae'].max()) + bin_size, bin_size)

# Plot the histograms and density curves for both DataFrames
plt.figure(figsize=(10, 6))

sns.histplot(maxprobes['pae'], bins=bins, kde=True, stat="density", color='#4c72b0', label='Maxprobes', linewidth=0.7)  # Cool Blue
sns.histplot(minprobes['pae'], bins=bins, kde=True, stat="density", color='#dd8452', label='Minprobes', linewidth=0.7)  # Warm Copper

# Customizing the plot
plt.title('Density Comparison of PAE in Augmented RNACompete (Maxprobes vs Minprobes)', fontsize=10)
plt.xlabel('PAE Value', fontsize=7)
plt.ylabel('Density', fontsize=7)

os.makedirs("plots", exist_ok=True)

# Adjust x-ticks to only show larger intervals and prevent overlap
plt.xticks(bins, rotation=45, ha="right", fontsize=7)

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title='Dataset', fontsize=7)
plt.tight_layout()  # Prevents label overlap
plt.savefig("plots/compare_pae_rnacmpt.pdf")
# plt.show()

from lib.utils import get_data_dict
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Set your data directory
data_dir = "RNAcompete/counts/augmented"
tables_rnacmpt = get_data_dict(data_dir)

maxprobes = tables_rnacmpt["3mer_RNAcompete_aug_max"]
minprobes = tables_rnacmpt["3mer_RNAcompete_aug_min"]

# Define bins
bin_size = 0.1
bins = np.arange(min(maxprobes['contact_prob_res_nt'].min(), minprobes['contact_prob_res_nt'].min()),
                 max(maxprobes['contact_prob_res_nt'].max(), minprobes['contact_prob_res_nt'].max()) + bin_size, bin_size)

# Plot the histograms and density curves for both DataFrames
plt.figure(figsize=(10, 6))

# Use a more aesthetic color palette from seaborn
sns.histplot(maxprobes['contact_prob_res_nt'], bins=bins, kde=True, stat="probability",
             color=sns.color_palette("coolwarm", as_cmap=True)(0.2), label='Maxprobes', linewidth=0.7)  # Cooler color for Maxprobes
sns.histplot(minprobes['contact_prob_res_nt'], bins=bins, kde=True, stat="probability",
             color=sns.color_palette("coolwarm", as_cmap=True)(0.8), label='Minprobes', linewidth=0.7)  # Warmer color for Minprobes

os.makedirs("plots", exist_ok=True)

# Customizing the plot
plt.title('Probability Distribution of Residue Contacts in Augmented RNACompete (Maxprobes vs Minprobes)', fontsize=12)
plt.xlabel('Probability of Residue Contacts', fontsize=10)
plt.ylabel('Density', fontsize=10)  # Y-axis now correctly represents probability

# Adjust x-ticks to only show larger intervals and prevent overlap
plt.xticks(bins, rotation=45, ha="right", fontsize=10)

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title='Dataset', fontsize=9)
plt.tight_layout()  # Prevents label overlap
plt.savefig("plots/compare_contact_prob_res_nt_rnacmpt.pdf")
# plt.show()

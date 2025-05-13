from lib.utils import get_data_dict
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set your data directory
data_dir = "RNAcompete/counts/augmented"
tables_rnacmpt = get_data_dict(data_dir)

maxprobes = tables_rnacmpt["3mer_RNAcompete_aug_max"]
minprobes = tables_rnacmpt["3mer_RNAcompete_aug_min"]

# Plot the density distributions for PAE(nt, res) and PAE(res, nt)
plt.figure(figsize=(10, 6))

# Maxprobes KDE plots
sns.kdeplot(maxprobes['pae(nt_res)'], label='Maxprobes PAE(nt, res)', color='#4575b4', linewidth=2)  # Deep Blue
sns.kdeplot(maxprobes['pae(res_nt)'], label='Maxprobes PAE(res, nt)', color='#91bfdb', linewidth=2, linestyle="dashed")  # Light Blue (dashed)

# Minprobes KDE plots
sns.kdeplot(minprobes['pae(nt_res)'], label='Minprobes PAE(nt, res)', color='#d73027', linewidth=2)  # Deep Red
sns.kdeplot(minprobes['pae(res_nt)'], label='Minprobes PAE(res, nt)', color='#fc8d59', linewidth=2, linestyle="dashed")  # Light Orange-Red (dashed)

os.makedirs("plots", exist_ok=True)

# Customizing the plot
plt.title('Density Comparison of PAE(nt, res) vs PAE(res, nt) in Augmented RNACompete', fontsize=10)
plt.xlabel('PAE Value', fontsize=9)
plt.ylabel('Density', fontsize=9)

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title='Dataset & PAE Type', fontsize=8)
plt.tight_layout()  # Prevents label overlap
plt.savefig("plots/compare_pae_nt_res_vs_res_nt_rnacmpt.pdf")
# plt.show()

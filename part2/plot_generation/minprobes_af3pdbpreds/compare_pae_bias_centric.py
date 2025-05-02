from lib.utils import get_data_dict
import seaborn as sns
import matplotlib.pyplot as plt

# Set your data directory
data_dir = "/home/jose/Downloads/AI4NA_AF3_eval/RNAcompete/counts/tables_pbdaf3preds_minprobes_tabpfn"
tables_alt = get_data_dict(data_dir)

positives = tables_alt["3mer_table_PDB_AF3_preds_tabpfn_max"]
negatives = tables_alt["3mer_table_nometrics_tabpfn_filled_min"]

# Plot the density distributions for PAE(nt, res) and PAE(res, nt)
plt.figure(figsize=(10, 6))

# Maxprobes KDE plots
sns.kdeplot(positives['pae(nt_res)'], label='Positives (AF3 predictions on PDB) - PAE(nt, res) ', color='#4575b4', linewidth=2)  # Deep Blue
sns.kdeplot(positives['pae(res_nt)'], label='Positives (AF3 predictions on PDB) - PAE(res, nt)', color='#91bfdb', linewidth=2, linestyle="dashed")  # Light Blue (dashed)

# Minprobes KDE plots
sns.kdeplot(negatives['pae(nt_res)'], label='Negatives (RNACompete Minprobes) - PAE(nt, res)', color='#d73027', linewidth=2)  # Deep Red
sns.kdeplot(negatives['pae(res_nt)'], label='Negatives (RNACompete Minprobes) - PAE(res, nt)', color='#fc8d59', linewidth=2, linestyle="dashed")  # Light Orange-Red (dashed)

# Customizing the plot
plt.title('Density Comparison of PAE(nt, res) vs PAE(res, nt) in alternative dataset', fontsize=10)
plt.xlabel('PAE Value', fontsize=9)
plt.ylabel('Density', fontsize=9)

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title='Dataset & PAE Type', fontsize=8)
plt.tight_layout()  # Prevents label overlap
plt.savefig("compare_pae_nt_res_vs_res_nt_alt.pdf")
plt.show()
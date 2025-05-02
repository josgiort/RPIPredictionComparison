
from lib.utils import get_data_dict
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set your data directory
data_dir = "/home/jose/Downloads/AI4NA_AF3_eval/RNAcompete/counts/tables_pbdaf3preds_minprobes_tabpfn"
tables_alt = get_data_dict(data_dir)

# Load maxprobe and minprobe datasets
positives = tables_alt["3mer_table_PDB_AF3_preds_tabpfn_max"]
negatives = tables_alt["3mer_table_nometrics_tabpfn_filled_min"]

# Create a figure with subplots for plDDT and PAE vs. distance
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Scatter plot for distance vs. plDDT (with improved visualization)
sns.scatterplot(x=positives["distance_angstroms"], y=positives["plddt"],
                label="Positives (AF3 predictions on PDB)", alpha=0.2, s=10, color="#377eb8", ax=axes[0])  # Blue
sns.scatterplot(x=negatives["distance_angstroms"], y=negatives["plddt"],
                label="Negatives (RNACompete Minprobes)", alpha=0.2, s=10, color="#e41a1c", ax=axes[0])  # Red

# Optional: Add KDE contours for density
sns.kdeplot(x=positives["distance_angstroms"], y=positives["plddt"],
            levels=5, color="blue", ax=axes[0], linewidths=1)
sns.kdeplot(x=negatives["distance_angstroms"], y=negatives["plddt"],
            levels=5, color="red", ax=axes[0], linewidths=1)

axes[0].set_xlabel("Distance (Å)")
axes[0].set_ylabel("plDDT")
axes[0].set_title("AF3 Confidence (plDDT) vs. Interaction Distance in alternative dataset")
axes[0].legend()

# Scatter plot for distance vs. PAE
sns.scatterplot(x=positives["distance_angstroms"], y=positives["pae"],
                label="Positives (AF3 predictions on PDB)", alpha=0.2, s=10, color="#377eb8", ax=axes[1])  # Blue
sns.scatterplot(x=negatives["distance_angstroms"], y=negatives["pae"],
                label="Negatives (RNACompete Minprobes)", alpha=0.2, s=10, color="#e41a1c", ax=axes[1])  # Red

# Optional: Add KDE contours
sns.kdeplot(x=positives["distance_angstroms"], y=positives["pae"],
            levels=5, color="blue", ax=axes[1], linewidths=1)
sns.kdeplot(x=negatives["distance_angstroms"], y=negatives["pae"],
            levels=5, color="red", ax=axes[1], linewidths=1)

axes[1].set_xlabel("Distance (Å)")
axes[1].set_ylabel("PAE")
axes[1].set_title("AF3 Uncertainty (PAE) vs. Interaction Distance in alternative dataset")
axes[1].legend()

plt.tight_layout()
plt.savefig("comparison_confidence_distance_alt.pdf")
plt.show()

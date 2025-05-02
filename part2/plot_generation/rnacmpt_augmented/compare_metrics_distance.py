
from lib.utils import get_data_dict
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set your data directory
data_dir = "/home/jose/Downloads/AI4NA_AF3_eval/RNAcompete/counts/augmented"
tables_rnacmpt = get_data_dict(data_dir)

# Load maxprobe and minprobe datasets
maxprobes = tables_rnacmpt["3mer_RNAcompete_aug_max"]
minprobes = tables_rnacmpt["3mer_RNAcompete_aug_min"]

# Create a figure with subplots for plDDT and PAE vs. distance
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Scatter plot for distance vs. plDDT (with improved visualization)
sns.scatterplot(x=maxprobes["distance_angstroms"], y=maxprobes["plddt"],
                label="Maxprobe", alpha=0.2, s=10, color="#377eb8", ax=axes[0])  # Blue
sns.scatterplot(x=minprobes["distance_angstroms"], y=minprobes["plddt"],
                label="Minprobe", alpha=0.2, s=10, color="#e41a1c", ax=axes[0])  # Red

# Optional: Add KDE contours for density
sns.kdeplot(x=maxprobes["distance_angstroms"], y=maxprobes["plddt"],
            levels=5, color="blue", ax=axes[0], linewidths=1)
sns.kdeplot(x=minprobes["distance_angstroms"], y=minprobes["plddt"],
            levels=5, color="red", ax=axes[0], linewidths=1)

axes[0].set_xlabel("Distance (Å)")
axes[0].set_ylabel("plDDT")
axes[0].set_title("AF3 Confidence (plDDT) vs. Interaction Distance")
axes[0].legend()

# Scatter plot for distance vs. PAE
sns.scatterplot(x=maxprobes["distance_angstroms"], y=maxprobes["pae"],
                label="Maxprobe", alpha=0.2, s=10, color="#377eb8", ax=axes[1])  # Blue
sns.scatterplot(x=minprobes["distance_angstroms"], y=minprobes["pae"],
                label="Minprobe", alpha=0.2, s=10, color="#e41a1c", ax=axes[1])  # Red

# Optional: Add KDE contours
sns.kdeplot(x=maxprobes["distance_angstroms"], y=maxprobes["pae"],
            levels=5, color="blue", ax=axes[1], linewidths=1)
sns.kdeplot(x=minprobes["distance_angstroms"], y=minprobes["pae"],
            levels=5, color="red", ax=axes[1], linewidths=1)

axes[1].set_xlabel("Distance (Å)")
axes[1].set_ylabel("PAE")
axes[1].set_title("AF3 Uncertainty (PAE) vs. Interaction Distance")
axes[1].legend()

plt.tight_layout()
plt.savefig("comparison_confidence_distance.pdf")
plt.show()

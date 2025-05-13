import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from lib.utils import get_data_dict
import os

# Load Data
data_dir = "RNAcompete/counts/augmented"
tables_rnacmpt = get_data_dict(data_dir)

maxprobes = tables_rnacmpt["3mer_RNAcompete_aug_max"]
minprobes = tables_rnacmpt["3mer_RNAcompete_aug_min"]

# Function to flatten plDDT lists
def flatten_plddt(df, column_name, label):
    """Extracts all plDDT values from the 5-mer lists and flattens them into a DataFrame."""
    flat_values = []
    for row in df[column_name]:
        flat_values.extend(eval(row))  # Convert string list to actual list
    return pd.DataFrame({"plddt": flat_values, "category": label})

# Flatten plDDT values for RNA and Protein
rna_max = flatten_plddt(maxprobes, "plddt_rna_residues", "Maxprobe RNA")
rna_min = flatten_plddt(minprobes, "plddt_rna_residues", "Minprobe RNA")

prot_max = flatten_plddt(maxprobes, "plddt_protein_residues", "Maxprobe Protein")
prot_min = flatten_plddt(minprobes, "plddt_protein_residues", "Minprobe Protein")

# Combine all data
plddt_data = pd.concat([rna_max, rna_min, prot_max, prot_min])

os.makedirs("plots", exist_ok=True)

# Violin Plot: RNA vs. Protein plDDT
plt.figure(figsize=(10, 6))
sns.violinplot(x="category", y="plddt", data=plddt_data, palette="muted")
plt.xlabel("")
plt.ylabel("plDDT Score")
plt.title("plDDT Distributions for RNA and Protein (Maxprobe vs. Minprobe) - Augmented RNACompete")
plt.xticks(rotation=20)
plt.savefig("plots/plddt_distr_rna_prot_max_min.pdf")
# plt.show()

# Aggregate lists (e.g., by taking the mean)
maxprobes["rna_plddt_mean"] = maxprobes["plddt_rna_residues"].apply(lambda x: np.mean(eval(x)))
maxprobes["prot_plddt_mean"] = maxprobes["plddt_protein_residues"].apply(lambda x: np.mean(eval(x)))

# Scatter Plot: Mean RNA plDDT vs. Mean Protein plDDT
plt.figure(figsize=(7, 7))
plt.scatter(maxprobes["prot_plddt_mean"], maxprobes["rna_plddt_mean"], alpha=0.1, s=8, color="blue")
plt.xlabel("Mean Protein plDDT")
plt.ylabel("Mean RNA plDDT")
plt.title("Mean RNA pLDDT vs Mean Protein pLDDT (Per 3mer Pair) -\nAugmented RNACompete (Maxprobes only)")
plt.axline((0, 0), slope=1, color="red", linestyle="dashed")  # y = x reference line
plt.savefig("plots/comparison_list_of_3mer_mean_plddt.png")
# plt.show()


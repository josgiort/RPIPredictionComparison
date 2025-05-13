import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from lib.utils import get_data_dict
import os

# Load Data
data_dir = "RNAcompete/counts/tables_pbdaf3preds_minprobes_tabpfn"
tables_alt = get_data_dict(data_dir)

positives = tables_alt["3mer_table_PDB_AF3_preds_tabpfn_max"]
negatives = tables_alt["3mer_table_nometrics_tabpfn_filled_min"]

# Function to flatten plDDT lists
def flatten_plddt(df, column_name, label):
    """Extracts all plDDT values from the 5-mer lists and flattens them into a DataFrame."""
    flat_values = []
    for row in df[column_name]:
        flat_values.extend(eval(row))  # Convert string list to actual list
    return pd.DataFrame({"plddt": flat_values, "category": label})

# Flatten plDDT values for RNA and Protein
rna_positives = flatten_plddt(positives, "plddt_rna_residues", "Positives (AF3 predictions"+'\n'+ "on PDB) - RNA")
rna_negatives = flatten_plddt(negatives, "plddt_rna_residues", "Negatives (RNACompete"+'\n'+ "Minprobes) - RNA")

prot_positives = flatten_plddt(positives, "plddt_protein_residues", "Positives (AF3 predictions"+'\n'+ "on PDB) - Protein")
prot_negatives = flatten_plddt(negatives, "plddt_protein_residues", "Negatives (RNACompete"+'\n'+ "Minprobes) - Protein")

# Combine all data
plddt_data = pd.concat([rna_positives, rna_negatives, prot_positives, prot_negatives])

os.makedirs("plots_alt", exist_ok=True)

# Violin Plot: RNA vs. Protein plDDT
plt.figure(figsize=(10, 6))
sns.violinplot(x="category", y="plddt", data=plddt_data, palette="muted")
plt.xlabel("")
plt.ylabel("plDDT Score")
plt.title("plDDT Distributions for RNA and Protein (Positives vs Negatives) - alternative dataset")
plt.xticks(rotation=20)
plt.xticks(fontsize=7)
plt.savefig("plots_alt/plddt_distr_rna_prot_alt.pdf")
# plt.show()

# Aggregate lists (e.g., by taking the mean)
positives["rna_plddt_mean"] = positives["plddt_rna_residues"].apply(lambda x: np.mean(eval(x)))
positives["prot_plddt_mean"] = positives["plddt_protein_residues"].apply(lambda x: np.mean(eval(x)))

# Scatter Plot: Mean RNA plDDT vs. Mean Protein plDDT
plt.figure(figsize=(7, 7))
plt.scatter(positives["prot_plddt_mean"], positives["rna_plddt_mean"], alpha=0.1, s=8, color="blue")
plt.xlabel("Mean Protein plDDT")
plt.ylabel("Mean RNA plDDT")
plt.title("Mean RNA pLDDT vs. Mean Protein pLDDT (Per 3-mer Pair) -\n Alternative Dataset (Positives only)")
plt.axline((0, 0), slope=1, color="red", linestyle="dashed")  # y = x reference line
plt.savefig("plots_alt/comparison_list_of_3mer_mean_plddt_alt.png")
# plt.show()
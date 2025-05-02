import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from lib.utils import get_data_dict

# Load your datasets
data_dir = "RNAcompete/counts"
tables_rnacmpt = get_data_dict(data_dir)

# RNACompete datasets
maxprobes = tables_rnacmpt["5mer_RNAcompete_maxprobe"]
minprobes = tables_rnacmpt["5mer_RNAcompete_minprobe"]
af3_pdb_preds = tables_rnacmpt["5mer_PDB_AF3_pred"]

# Extract relevant columns

def extract_data(df, label):
    return pd.DataFrame({
        "plddt": df["plddt"],
        "pae_res_nt": df["pae(res,nt)"],
        "pae_nt_res": df["pae(nt,res)"],
        "source": label
    })

# Combine datasets for comparison
data = pd.concat([
    extract_data(maxprobes, "Maxprobe"),
    extract_data(minprobes, "Minprobe"),
    extract_data(af3_pdb_preds, "AF3_Training")
])

# Violin plot for plDDT
plt.figure(figsize=(8, 5))
sns.violinplot(x="source", y="plddt", data=data, palette="muted")
plt.title("plDDT Distribution Across Datasets")
plt.ylabel("plDDT")
plt.xlabel("Dataset")
plt.savefig("plddt_pae_bias_plot1.pdf")
plt.show()

# Violin plot for PAE(res, nt) vs. PAE(nt, res)
plt.figure(figsize=(12, 6))
data_melted = data.melt(id_vars=["source"], value_vars=["pae_res_nt", "pae_nt_res"],
                         var_name="PAE Type", value_name="PAE Value")
sns.violinplot(x="source", y="PAE Value", hue="PAE Type", data=data_melted, palette="Set2", split=True)
plt.title("PAE(res, nt) vs. PAE(nt, res) Across Datasets")
plt.ylabel("PAE")
plt.xlabel("Dataset")
plt.legend(title="PAE Type")
plt.savefig("plddt_pae_bias_plot2.pdf")
plt.show()

# Scatter plot of 5-mer frequency vs. plDDT
plt.figure(figsize=(8, 5))
sns.scatterplot(x=data.index, y=data["plddt"], hue=data["source"], alpha=0.6)
plt.title("5-mer Frequency vs. plDDT")
plt.ylabel("plDDT")
plt.xlabel("5-mer Index")
plt.savefig("plddt_pae_bias_plot3.pdf")
plt.show()
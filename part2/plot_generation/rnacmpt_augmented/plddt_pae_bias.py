
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from lib.utils import get_data_dict

# Load your datasets
data_dir = "/home/jose/Downloads/AI4NA_AF3_eval/RNAcompete/counts/augmented"
tables_rnacmpt = get_data_dict(data_dir)

# RNACompete datasets
maxprobes = tables_rnacmpt["3mer_RNAcompete_aug_max"]
minprobes = tables_rnacmpt["3mer_RNAcompete_aug_min"]
af3_pdb_preds = tables_rnacmpt["3mer_PDB_AF3_pred"]


# Extract relevant columns
def extract_data(df, label):
    return pd.DataFrame({
        "plddt": df["plddt"],
        "pae_res_nt": df["pae(res_nt)"],
        "pae_nt_res": df["pae(nt_res)"],
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
plt.title("plDDT Distribution Across Datasets - Augmented RNACompete")
plt.ylabel("plDDT")
plt.xlabel("Dataset")
plt.savefig("plddt_pae_bias_plot1.pdf")
plt.show()

# Violin plot for PAE(res, nt) vs. PAE(nt, res)
plt.figure(figsize=(8, 5))
data_melted = data.melt(id_vars=["source"], value_vars=["pae_res_nt", "pae_nt_res"],
                        var_name="PAE Type", value_name="PAE Value")
sns.violinplot(x="source", y="PAE Value", hue="PAE Type", data=data_melted, palette="Set2", split=True, inner="box")
plt.title("PAE(res, nt) vs. PAE(nt, res) Across Datasets - Augmented RNACompete")
plt.ylabel("PAE")
plt.xlabel("Dataset")
plt.legend(title="PAE Type")
plt.savefig("plddt_pae_bias_plot2.pdf")
plt.show()

# --- Split Scatter Plot into 3 Separate Plots with Stronger Contours ---

# Create figure with three subplots and increased vertical spacing
fig, axes = plt.subplots(3, 1, figsize=(8, 18), sharex=True, sharey=True)  # Increased height

# Define dataset order and colors
datasets = ["Maxprobe", "Minprobe", "AF3_Training"]
dot_colors = ["lightblue", "lightcoral", "lightgreen"]  # Softer colors for scatter dots
contour_colors = ["darkblue", "darkred", "darkgreen"]  # Stronger contour colors

for i, dataset in enumerate(datasets):
    subset = data[data["source"] == dataset]

    # Scatter plot with lighter dots
    sns.scatterplot(x=subset.index, y=subset["plddt"], color=dot_colors[i], alpha=1, s=9, ax=axes[i])

    # KDE Contour overlay with stronger color and thicker lines
    sns.kdeplot(x=subset.index, y=subset["plddt"], levels=4, color=contour_colors[i], linewidths=0.6, ax=axes[i])

    axes[i].set_title(f"3-mer Frequency vs. plDDT - {dataset}")
    axes[i].set_ylabel("plDDT")

# Set common x-axis label
axes[-1].set_xlabel("3-mer Index")

# Adjust layout with extra spacing
plt.subplots_adjust(hspace=0.3)  # More vertical separation
# Save and show
plt.savefig("plddt_pae_bias_plot3_split_contours_enhanced.pdf")
plt.show()



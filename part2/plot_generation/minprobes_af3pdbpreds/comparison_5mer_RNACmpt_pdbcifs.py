# import pandas as pd
# import matplotlib.pyplot as plt
# from collections import Counter
#
# from lib.utils import get_data_dict
#
# # Load your datasets
# data_dir = "/home/jose/Downloads/AI4NA_AF3_eval/RNAcompete/counts/augmented"
# tables_rnacmpt = get_data_dict(data_dir)
#
# # RNACompete datasets
# maxprobes = tables_rnacmpt["3mer_RNAcompete_aug_max"]
# minprobes = tables_rnacmpt["3mer_RNAcompete_aug_min"]
# af3_training = tables_rnacmpt["3mer_PDB_ground_truth"]
#
# # Function to extract 5-mer frequencies}
# def get_3mer_frequencies(seq_column):
#     all_3mers = []
#     for seq in seq_column.dropna():  # Drop missing values
#         all_3mers.extend([seq[i:i+3] for i in range(len(seq) - 2)])  # Extract overlapping 3-mers
#     return Counter(all_3mers)
#
# # Compute 5-mer frequencies
# maxprobe_5mer_freq = get_3mer_frequencies(maxprobes["protein_3mer"])
# minprobe_5mer_freq = get_3mer_frequencies(minprobes["protein_3mer"])
# af3_5mer_freq = get_3mer_frequencies(af3_training["protein_3mer"])
#
# # Identify the top 10 most frequent 5-mers overall
# top_5mers = set(
#     [x[0] for x in maxprobe_5mer_freq.most_common(20)] +
#     [x[0] for x in minprobe_5mer_freq.most_common(20)] +
#     [x[0] for x in af3_5mer_freq.most_common(20)]
# )
#
# # Create a DataFrame with only the top 5-mers
# df_5mers = pd.DataFrame({
#     "3mer": list(top_5mers),
#     "Maxprobe": [maxprobe_5mer_freq.get(k, 0) for k in top_5mers],
#     "Minprobe": [minprobe_5mer_freq.get(k, 0) for k in top_5mers],
#     "AF3_Training": [af3_5mer_freq.get(k, 0) for k in top_5mers],
# })
# import seaborn as sns
#
# # Sort by total frequency across all datasets
# df_5mers["Total_Frequency"] = df_5mers["Maxprobe"] + df_5mers["Minprobe"] + df_5mers["AF3_Training"]
# df_5mers = df_5mers.sort_values(by="Total_Frequency", ascending=False).drop(columns=["Total_Frequency"])
#
# # Plot as a heatmap for better readability
# plt.figure(figsize=(10, 6))
# sns.heatmap(df_5mers.set_index("3mer"), cmap="coolwarm", annot=True, fmt="d", linewidths=0.5)
# plt.title("Top 10 Most Frequent 3-mers Across Datasets - Augmented RNACompete")
# plt.xlabel("Dataset")
# plt.ylabel("3-mer")
# plt.savefig("comparison_3mer_RNACmpt_pdbcifs.pdf")
# plt.show()
#













#
#
# ------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from lib.utils import get_data_dict

# Load your datasets
data_dir = "/home/jose/Downloads/AI4NA_AF3_eval/RNAcompete/counts/augmented"
tables_rnacmpt = get_data_dict(data_dir)

# RNACompete datasets
maxprobes = tables_rnacmpt["3mer_RNAcompete_aug_max"]
minprobes = tables_rnacmpt["3mer_RNAcompete_aug_min"]
af3_training = tables_rnacmpt["3mer_PDB_ground_truth"]

# Function to get the top 20 most frequent 3-mers
def get_top_3mers(df, column="protein_3mer", top_n=20):
    counts = Counter(df[column].dropna())  # Count occurrences, ignoring NaN
    return pd.DataFrame(counts.most_common(top_n), columns=["3-mer", "Count"])

# Compute top 3-mers separately for each dataset
df_maxprobe = get_top_3mers(maxprobes)
df_minprobe = get_top_3mers(minprobes)
df_af3 = get_top_3mers(af3_training)

# Function to plot top 3-mers
def plot_top_3mers(df, dataset_name):
    plt.figure(figsize=(10, 5))
    sns.barplot(x="3-mer", y="Count", data=df, palette="coolwarm")
    plt.title(f"Top 20 Most Frequent 3-Mers in {dataset_name}")
    plt.xlabel("3-mer")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"top_3mers_{dataset_name}.png")  # Save figure
    plt.show()

# Plot the top 3-mers for each dataset
plot_top_3mers(df_maxprobe, "Maxprobe")
plot_top_3mers(df_minprobe, "Minprobe")
plot_top_3mers(df_af3, "AF3_Training")



# Convert top 3-mers to sets for quick comparison
set_maxprobe = set(df_maxprobe["3-mer"])
set_minprobe = set(df_minprobe["3-mer"])
set_af3 = set(df_af3["3-mer"])

# Find common 3-mers across datasets
common_3mers = set_maxprobe & set_minprobe | set_maxprobe & set_af3 | set_minprobe & set_af3  # Union of intersections

# Create a DataFrame with counts in each dataset
common_df = pd.DataFrame({
    "3-mer": list(common_3mers),
    "Maxprobe": [df_maxprobe.set_index("3-mer")["Count"].get(k, 0) for k in common_3mers],
    "Minprobe": [df_minprobe.set_index("3-mer")["Count"].get(k, 0) for k in common_3mers],
    "AF3_Training": [df_af3.set_index("3-mer")["Count"].get(k, 0) for k in common_3mers],
})

# Sort by total occurrences across datasets
common_df["Total"] = common_df["Maxprobe"] + common_df["Minprobe"] + common_df["AF3_Training"]
common_df = common_df.sort_values(by="Total", ascending=False).drop(columns=["Total"])

# Display the common 3-mers
print("\n🔍 3-Mers that appear in multiple datasets:\n")
print(common_df)

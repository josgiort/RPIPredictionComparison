from pathlib import Path
import pandas as pd
import numpy as np

# Set parameters
N = 15  # Top N kmers
test_samples = 50  # Number of test samples

# Load datasets
min_5mer = pd.read_csv("RNAcompete/counts/5mer_RNAcompete_minprobe.added_rbd_info.tsv", sep='\t')
max_5mer = pd.read_csv("RNAcompete/counts/5mer_RNAcompete_maxprobe.added_rbd_info.tsv", sep='\t')

# Combine both dataframes for kmer frequency computation
combined_5mer = pd.concat([min_5mer, max_5mer])

# Compute the most frequent RNA 5-mers
top_rna_5mers = combined_5mer["rna-5mer"].value_counts().nlargest(N).index

# Compute the most frequent protein 5-mers
top_prot_5mers = combined_5mer["protein-5mer"].value_counts().nlargest(N).index

# Process the dataset with selected 5-mers
tabpfn_df_data = []

for df in [min_5mer, max_5mer]:
    for i, group in df.groupby("dataset_id2"):
        sample = {
            "Id": i,
            "prot_seq": group["prot_seq"].values[0],
            "rna_seq": group["rna_seq"].values[0],
            "uniprot_id": group["uniprot_id"].values[0],
            "7mer_pos": group["7mer_pos"].values[0],
            "gc": (group["rna_seq"].values[0].count("G") + group["rna_seq"].values[0].count("C")) / len(group["rna_seq"].values[0]),
            "length": len(group["rna_seq"].values[0]),
            "interpro_ids": group["interpro_ids"].values[0],
            "interaction": int(group["dataset_id1"].values[0] == 'RNAcompete_maxprobe'),
        }

        # Process only top N RNA 5-mers
        for rna_kmer, g in group.groupby("rna-5mer"):
            if rna_kmer in top_rna_5mers:
                sample[rna_kmer] = len(g)
                sample[f"{rna_kmer}_PAE_mean"] = g["pae"].mean()
                sample[f"{rna_kmer}_PAE_std"] = g["pae"].std()
                sample[f"{rna_kmer}_plddt_mean"] = g["plddt"].mean()
                sample[f"{rna_kmer}_plddt_std"] = g["plddt"].std()

        # Process only top N protein 5-mers
        for prot_kmer, g in group.groupby("protein-5mer"):
            if prot_kmer in top_prot_5mers:
                sample[prot_kmer] = len(g)
                sample[f"{prot_kmer}_PAE_mean"] = g["pae"].mean()
                sample[f"{prot_kmer}_PAE_std"] = g["pae"].std()
                sample[f"{prot_kmer}_plddt_mean"] = g["plddt"].mean()
                sample[f"{prot_kmer}_plddt_std"] = g["plddt"].std()

        tabpfn_df_data.append(sample)

# Create final DataFrame
tabpfn_df = pd.DataFrame(tabpfn_df_data)
num_features = tabpfn_df.shape[1]# Number of features

# Ensure no feature column has only NaN values
tabpfn_df = tabpfn_df.dropna(axis=1, how="all")

# --- 📌 Split 1: UniProt ID-based Split ---
uniprot_counts = tabpfn_df["uniprot_id"].value_counts()

# Select test set UniProt IDs
selected_uniprot_ids = set()
selected_rows = 0

for uniprot_id, count in uniprot_counts.items():
    selected_uniprot_ids.add(uniprot_id)
    selected_rows += count
    if selected_rows >= test_samples:
        break

# Create test and train sets
test_uniprot = tabpfn_df[tabpfn_df["uniprot_id"].isin(selected_uniprot_ids)]
train_uniprot = tabpfn_df[~tabpfn_df["uniprot_id"].isin(selected_uniprot_ids)]

# --- 📌 Split 2: Random Split ---
tabpfn_df_shuffled = tabpfn_df.sample(frac=1, random_state=42)
test_random = tabpfn_df_shuffled.iloc[:test_samples]
train_random = tabpfn_df_shuffled.iloc[test_samples:]

# --- 📌 Create Three Versions of Each Split ---

def save_splits(train_df, test_df, split_name, out_dir):
    """Save three versions of train/test splits."""
    
    # Full feature set
    train_df.to_csv(f"{out_dir}/{split_name}_{num_features}_features_train_full.csv", index=False)
    test_df.to_csv(f"{out_dir}/{split_name}_{num_features}_features_test_full.csv", index=False)

    # Only prot_seq, rna_seq, interaction
    train_df[["Id", "prot_seq", "rna_seq", "interaction"]].to_csv(f"{out_dir}/{split_name}_{num_features}_features_train_seq.csv", index=False)
    test_df[["Id", "prot_seq", "rna_seq", "interaction"]].to_csv(f"{out_dir}/{split_name}_{num_features}_features_test_seq.csv", index=False)

    # Remove k-mer features
    non_kmer_features = ["Id", "prot_seq", "rna_seq", "uniprot_id", "7mer_pos", "gc", "length", "interpro_ids", "interaction"]
    kmer_columns = [col for col in train_df.columns if col not in non_kmer_features]
    train_df.drop(columns=kmer_columns).to_csv(f"{out_dir}/{split_name}_{num_features}_features_train_no_kmer.csv", index=False)
    test_df.drop(columns=kmer_columns).to_csv(f"{out_dir}/{split_name}_{num_features}_features_test_no_kmer.csv", index=False)

# Save datasets
out_dir = Path('tabpfn_data')
out_dir.mkdir(exist_ok=True, parents=True)
save_splits(train_uniprot, test_uniprot, "split_uniprot", out_dir.resolve())
save_splits(train_random, test_random, "split_random", out_dir.resolve())

print("✅ Datasets saved successfully!")

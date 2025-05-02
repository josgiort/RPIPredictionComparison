from pathlib import Path
import pandas as pd
import numpy as np

# Set parameters
N = 15  # Top N kmers
test_samples = 50  # Number of test samples

# Load datasets
# min_5mer = pd.read_csv("RNAcompete/counts/5mer_RNAcompete_minprobe.added_rbd_info.tsv", sep='\t')
# max_5mer = pd.read_csv("RNAcompete/counts/5mer_RNAcompete_maxprobe.added_rbd_info.tsv", sep='\t')

_5mer = pd.read_csv("RNAcompete/counts/augmented2.0/5mer_RNAcompete_aug2.0.csv", sep=',')
# Combine both dataframes for kmer frequency computation
# combined_5mer = pd.concat([min_5mer, max_5mer])

# Compute the most frequent RNA 5-mers
top_rna_5mers = _5mer["rna_5mer"].value_counts().nlargest(N).index

# Compute the most frequent protein 5-mers
top_prot_5mers = _5mer["protein_5mer"].value_counts().nlargest(N).index

# Process the dataset with selected 5-mers
tabpfn_df_data = []

# for df in [min_5mer, max_5mer]:
for i, group in _5mer.groupby("dataset_id2"):
    sample = {
        "Id": i,
        "prot_seq": group["prot_seq"].values[0],
        "rna_seq": group["rna_seq"].values[0],
        "rbp_name": group["rbp_name"].values[0],
        "7mer_pos": group["7mer_pos"].values[0],
        "gc": (group["rna_seq"].values[0].count("G") + group["rna_seq"].values[0].count("C")) / len(group["rna_seq"].values[0]),
        "length": len(group["rna_seq"].values[0]),
        # "interpro_ids": group["interpro_ids"].values[0]
        "interaction": group["interaction"].values[0]
    }

    # Process only top N RNA 5-mers
    for rna_kmer, g in group.groupby("rna_5mer"):
        if rna_kmer in top_rna_5mers:
            sample[rna_kmer] = len(g)
            sample[f"{rna_kmer}_PAE_mean"] = g["pae"].mean()
            sample[f"{rna_kmer}_PAE_std"] = g["pae"].std()
            sample[f"{rna_kmer}_plddt_mean"] = g["plddt"].mean()
            sample[f"{rna_kmer}_plddt_std"] = g["plddt"].std()
            sample[f"{rna_kmer}_d_angstroms_mean"] = g["distance_angstroms"].mean()
            sample[f"{rna_kmer}_d_angstroms_std"] = g["distance_angstroms"].std()
            sample[f"{rna_kmer}_contact_prob_res_nt_mean"] = g["contact_prob_res_nt"].mean()
            sample[f"{rna_kmer}_contact_prob_res_nt_std"] = g["contact_prob_res_nt"].std()

    # Process only top N protein 5-mers
    for prot_kmer, g in group.groupby("protein_5mer"):
        if prot_kmer in top_prot_5mers:
            sample[prot_kmer] = len(g)
            sample[f"{prot_kmer}_PAE_mean"] = g["pae"].mean()
            sample[f"{prot_kmer}_PAE_std"] = g["pae"].std()
            sample[f"{prot_kmer}_plddt_mean"] = g["plddt"].mean()
            sample[f"{prot_kmer}_plddt_std"] = g["plddt"].std()
            sample[f"{prot_kmer}_d_angstroms_mean"] = g["distance_angstroms"].mean()
            sample[f"{prot_kmer}_d_angstroms_std"] = g["distance_angstroms"].std()
            sample[f"{prot_kmer}_contact_prob_res_nt_mean"] = g["contact_prob_res_nt"].mean()
            sample[f"{prot_kmer}_contact_prob_res_nt_std"] = g["contact_prob_res_nt"].std()

    tabpfn_df_data.append(sample)

# Create final DataFrame
tabpfn_df = pd.DataFrame(tabpfn_df_data)
num_features = tabpfn_df.shape[1]# Number of features





# Merge additional features from external CSVs before splitting

# Load predictions
preds_df = pd.read_csv("1mer_RNAcompete_aug_seq_info_PREDS_EMBEDOR_filtered.csv")[["dataset_id2", "RPIEmbeddor_pred"]]

# Load extra features
extra_features_cols = [
    "dataset_id2", "plddt_mean", "plddt_std", "plddt_median", "pae_mean", "pae_std", "pae_median",
    "pae(res_nt)_mean", "pae(res_nt)_std", "pae(res_nt)_median",
    "pae(nt_res)_mean", "pae(nt_res)_std", "pae(nt_res)_median",
    "distance_angstroms_mean", "distance_angstroms_std", "distance_angstroms_median",
    "contact_prob_res_nt_mean", "contact_prob_res_nt_std", "contact_prob_res_nt_median",
    "pct_ol_max_min_mer", "fraction_disordered", "has_clash", "iptm", "ptm", "ranking_score",
    "prot_rna_pae_min", "rna_prot_pae_min", "prot_rna_iptm", "rna_prot_iptm",
    "rna_mfe_value", "rna_entr", "rna_gc_skew", "rna_au_skew", "rna_au"
]
features_df = pd.read_csv("split_rbp_36_features_train_full_M.csv")[extra_features_cols]

# Merge everything into tabpfn_df
tabpfn_df = tabpfn_df.merge(preds_df, left_on="Id", right_on="dataset_id2", how="left")
tabpfn_df = tabpfn_df.merge(features_df, left_on="Id", right_on="dataset_id2", how="left")

# Remove entries with missing prediction
tabpfn_df = tabpfn_df[tabpfn_df["RPIEmbeddor_pred"].notna()]









# Ensure no feature column has only NaN values
tabpfn_df = tabpfn_df.dropna(axis=1, how="all")







# --- 📌 Split 1: RBP_name ID-based Split ---
rbp_name_counts = tabpfn_df["rbp_name"].value_counts()

# Select test set RBP_name IDs
selected_rbp_names = set()
selected_rows = 0

for rbp_name, count in rbp_name_counts.items():
    selected_rbp_names.add(rbp_name)
    selected_rows += count
    if selected_rows >= test_samples:
        break

# Create test and train sets
test_rbp_names = tabpfn_df[tabpfn_df["rbp_name"].isin(selected_rbp_names)]
train_rbp_names = tabpfn_df[~tabpfn_df["rbp_name"].isin(selected_rbp_names)]

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
    non_kmer_features = ["Id", "prot_seq", "rna_seq", "rbp_name", "7mer_pos", "gc", "length", "interaction"]
    kmer_columns = [col for col in train_df.columns if col not in non_kmer_features]
    train_df.drop(columns=kmer_columns).to_csv(f"{out_dir}/{split_name}_{num_features}_features_train_no_kmer.csv", index=False)
    test_df.drop(columns=kmer_columns).to_csv(f"{out_dir}/{split_name}_{num_features}_features_test_no_kmer.csv", index=False)

# Save datasets
out_dir = Path('tabpfn_data/augmented2.0/MERG')
out_dir.mkdir(exist_ok=True, parents=True)
save_splits(train_rbp_names, test_rbp_names, "split_rbp_name", out_dir.resolve())
save_splits(train_random, test_random, "split_random", out_dir.resolve())

print("✅ Datasets saved successfully!")

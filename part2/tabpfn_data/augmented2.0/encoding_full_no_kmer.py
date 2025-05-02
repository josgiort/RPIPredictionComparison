import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("split_rbp_name_278_features_train_no_kmer.csv")  # Replace with your actual dataset file

# --- 🔹 Drop Unnecessary Columns ---
df = df.drop(columns=["gc", "length"], errors="ignore")

# --- 🔹 Compute Sequence Lengths ---
#df["prot_length"] = df["prot_seq"].apply(len)
#df["rna_length"] = df["rna_seq"].apply(len)

# --- 🔹 Compute Amino Acid & Nucleotide Composition ---
amino_acids = "ACDEFGHIKLMNPQRSTVWY"
nucleotides = "ACGU"

for aa in amino_acids:
    df[f"aa_{aa}"] = df["prot_seq"].apply(lambda seq: seq.count(aa) / len(seq) if len(seq) > 0 else 0)

for nt in nucleotides:
    df[f"nt_{nt}"] = df["rna_seq"].apply(lambda seq: seq.count(nt) / len(seq) if len(seq) > 0 else 0)

# --- 🔹 Encode `rbp_name` as Categorical ---
encoder = LabelEncoder()
df["rbp_name"] = encoder.fit_transform(df["rbp_name"])

# --- 🔹 Split `7mer_pos` into Start & End Positions ---
df[["7mer_start", "7mer_end"]] = df["7mer_pos"].str.split("-", expand=True).astype(int)

# --- 🔹 Drop Original Columns ---
df = df.drop(columns=["prot_seq", "rna_seq", "7mer_pos"], errors="ignore")

# Save the processed dataset
df.to_csv("split_rbp_name_278_features_train_no_kmer.csv", index=False)
print("✅ Preprocessing complete. Processed dataset saved as 'processed_dataset.csv'.")

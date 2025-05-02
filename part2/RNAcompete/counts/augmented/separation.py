import pandas as pd

# Load the CSV file
input_csv = "5mer_RNAcompete_aug.csv"  # Replace with the actual filename
df = pd.read_csv(input_csv)

# Split the data based on the "dataset_id1" column
minprobe_df = df[df["dataset_id1"] == "RNAcompete_minprobe"]
maxprobe_df = df[df["dataset_id1"] == "RNAcompete_maxprobe"]

# Save to new CSV files
minprobe_df.to_csv("5mer_RNAcompete_aug_min.csv", index=False)
maxprobe_df.to_csv("5mer_RNAcompete_aug_max.csv", index=False)

print("✅ Files saved as 'RNAcompete_minprobe.csv' and 'RNAcompete_maxprobe.csv'")

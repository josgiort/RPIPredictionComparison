# import pandas as pd
#
# # Load the CSV file
# input_csv = "5mer_RNAcompete_aug.csv"  # Replace with the actual filename
# df = pd.read_csv(input_csv)
#
# # Split the data based on the "dataset_id1" column
# minprobe_df = df[df["dataset_id1"] == "RNAcompete_minprobe"]
# maxprobe_df = df[df["dataset_id1"] == "RNAcompete_maxprobe"]
#
# # Save to new CSV files
# minprobe_df.to_csv("5mer_RNAcompete_aug_min.csv", index=False)
# maxprobe_df.to_csv("5mer_RNAcompete_aug_max.csv", index=False)
#
# print("✅ Files saved as 'RNAcompete_minprobe.csv' and 'RNAcompete_maxprobe.csv'")



import pandas as pd

# Load CSV file
file_path = "1mer_RNAcompete_aug.csv"  # Change this to your actual file path
output_file = "1mer_RNAcompete_aug_seq_info.csv"  # Change this to your desired output file path

df = pd.read_csv(file_path)

# Group by 'dataset_id2' and select required columns
selected_columns = ['dataset_id2', 'prot_seq', 'rna_seq', 'rbp_name', 'uniprot_id']
df_grouped = df[selected_columns].groupby('dataset_id2').first().reset_index()

# Save the result to a new CSV file
df_grouped.to_csv(output_file, index=False)

print(f"Grouping completed! Saved to {output_file}")

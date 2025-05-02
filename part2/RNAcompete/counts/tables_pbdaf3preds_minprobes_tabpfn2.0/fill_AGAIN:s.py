# import pandas as pd
#
# # Load the CSV file
# df = pd.read_csv("file_filled.csv")  # Replace with your actual file name
#
# # Remove rows where 'uniprot_id' is empty or NaN
# df_cleaned = df.dropna(subset=["uniprot_id"])  # Drops rows with NaN in 'uniprot_id'
# df_cleaned = df_cleaned[df_cleaned["uniprot_id"].astype(str).str.strip() != ""]  # Also removes empty strings
#
# # Save the cleaned dataset
# df_cleaned.to_csv("file_filled_cleaned.csv", index=False)
#
# print("✅ Rows with empty 'uniprot_id' removed. Saved as 'file_filled_cleaned.csv'!")



import pandas as pd

# Load CSV file
file_path = "1mer_table_minprobes_pdbaf3preds_merged.csv"  # Change this to your actual file path
output_file = "1mer_table_minprobes_pdbaf3preds_merged_SEQ_INFO.csv"  # Change this to your desired output file path

df = pd.read_csv(file_path)

# Group by 'dataset_id2' and select required columns
selected_columns = ['dataset_id2', 'prot_seq', 'rna_seq', 'uniprot_id']
df_grouped = df[selected_columns].groupby('dataset_id2').first().reset_index()

# Save the result to a new CSV file
df_grouped.to_csv(output_file, index=False)

print(f"Grouping completed! Saved to {output_file}")

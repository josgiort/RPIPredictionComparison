import pandas as pd

# Path to your original CSV file
input_file = "1mer_table_minprobes_pdbaf3preds_merged_SEQ_INFO_PREDS_EMBEDOR.csv"

# Path where the cleaned CSV will be saved
output_file = "1mer_table_minprobes_pdbaf3preds_merged_SEQ_INFO_PREDS_EMBEDOR_filtered.csv"

# Read the CSV file
df = pd.read_csv(input_file)

# Filter out rows where 'RPIEmbeddor_pred' is "N/A Pred"
filtered_df = df[df["RPIEmbeddor_pred"] != "N/A Pred"]

# Save the filtered dataframe to a new CSV file
filtered_df.to_csv(output_file, index=False)

print(f"Cleaned CSV saved to: {output_file}")

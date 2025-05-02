import pandas as pd

# Paths to your CSV files
main_csv_path = "split_rbp_278_features_train_seq.csv"
predictions_csv_path = "1mer_RNAcompete_aug_seq_info_PREDS_EMBEDOR_filtered.csv"
output_csv_path = "split_rbp_278_features_train_seq.csv"

# Matching column names
main_id_column = "Id"          # <-- Change this to your actual column name in the main CSV
pred_id_column = "dataset_id2"               # This stays as is (assumed name in the predictions file)

# Read both CSV files
main_df = pd.read_csv(main_csv_path)
pred_df = pd.read_csv(predictions_csv_path)

# Merge using specified columns
merged_df = pd.merge(main_df, pred_df[[pred_id_column, 'RPIEmbeddor_pred']],
                     left_on=main_id_column, right_on=pred_id_column, how='inner')

# Drop rows where RPIEmbeddor_pred is missing or equals 'N/A Pred'
filtered_df = merged_df[merged_df['RPIEmbeddor_pred'].notna()]
filtered_df = filtered_df[filtered_df['RPIEmbeddor_pred'] != "N/A Pred"]

# Save the result
filtered_df.to_csv(output_csv_path, index=False)

print(f"Merged and filtered CSV saved to: {output_csv_path}")

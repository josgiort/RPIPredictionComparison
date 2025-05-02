# import pandas as pd
#
# # File paths
# big_csv_path = "AA_split_rbp_278_features_train_no_kmer.csv"
# small_csv_path = "AA_split_rbp_36_features_train_full.csv"
# output_path = ("MASTER_FEATURES.csv")
#
# # Read CSV files
# big_df = pd.read_csv(big_csv_path)
# small_df = pd.read_csv(small_csv_path)
#
# # Merge on different column names
# merged_df = pd.merge(
#     big_df,
#     small_df,
#     left_on="Id",
#     right_on="dataset_id2",
#     how="left"  # Change to 'inner' if you want only matches
# )
#
# # Save the merged DataFrame
# merged_df.to_csv(output_path, index=False)
#
# print(f"✅ Merged CSV saved to: {output_path}")


import pandas as pd
from sklearn.model_selection import train_test_split

# File paths
input_csv_path = "MASTER_FEATURES.csv"
train_output_path = "MASTER_FEATUREStrain_split.csv"
test_output_path = "MASTER_FEATUREStest_split.csv"

# Load the dataset
df = pd.read_csv(input_csv_path)

# Split into train (80%) and test (20%)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)

# Save the splits
train_df.to_csv(train_output_path, index=False)
test_df.to_csv(test_output_path, index=False)

print(f"✅ Train set saved to: {train_output_path}")
print(f"✅ Test set saved to: {test_output_path}")








#
# import pandas as pd
# from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
#
# # Replace this with the path to your CSV file
# csv_file = "MASTER_FEATUREStest_split.csv"
#
# # Load the CSV file
# df = pd.read_csv(csv_file)
#
# # Ensure required columns are present
# if 'RPIEmbeddor_pred' not in df.columns or 'interaction' not in df.columns:
#     raise ValueError("CSV file must contain 'RPIEmbeddor_pred' and 'interaction' columns.")
#
# # Extract predictions and ground truth
# y_pred = df['RPIEmbeddor_pred']
# y_true = df['interaction']
#
# # Calculate accuracy
# accuracy = accuracy_score(y_true, y_pred)
# print(f"Accuracy: {accuracy:.4f}")
#
# # Detailed performance metrics
# print("\nClassification Report:")
# print(classification_report(y_true, y_pred))
#
# # Confusion matrix
# print("\nConfusion Matrix:")
# print(confusion_matrix(y_true, y_pred))

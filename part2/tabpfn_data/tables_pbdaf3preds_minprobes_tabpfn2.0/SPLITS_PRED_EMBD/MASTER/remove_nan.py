import pandas as pd

# File paths
input_csv_path = "MASTER_FEATUREStest_split.csv"
output_csv_path = "MASTER_FEATUREStest_split.csv"

# Load the CSV
df = pd.read_csv(input_csv_path)

# Drop rows with any NaN values across all columns
filtered_df = df.dropna()

# Save the cleaned dataset
filtered_df.to_csv(output_csv_path, index=False)

print(f"✅ Rows with NaN values removed. Cleaned CSV saved to: {output_csv_path}")

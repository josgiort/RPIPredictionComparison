import pandas as pd

# Load the CSV file
df = pd.read_csv("file_filled.csv")  # Replace with your actual file name

# Remove rows where 'uniprot_id' is empty or NaN
df_cleaned = df.dropna(subset=["uniprot_id"])  # Drops rows with NaN in 'uniprot_id'
df_cleaned = df_cleaned[df_cleaned["uniprot_id"].astype(str).str.strip() != ""]  # Also removes empty strings

# Save the cleaned dataset
df_cleaned.to_csv("file_filled_cleaned.csv", index=False)

print("✅ Rows with empty 'uniprot_id' removed. Saved as 'file_filled_cleaned.csv'!")

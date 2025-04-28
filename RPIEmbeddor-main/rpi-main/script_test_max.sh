#!/bin/bash

# Path to your CSV file
CSV_FILE="maxprobe_seqs_extracted.csv"
# Temporary file to store results
TEMP_FILE="temp_results.csv"

# Check if the CSV file exists
if [ ! -f "$CSV_FILE" ]; then
  echo "CSV file not found: $CSV_FILE"
  exit 1
fi

# Add the new column header to the temporary file
echo -e "$(head -n 1 "$CSV_FILE")\tRPIEmbeddor_pred" > "$TEMP_FILE"

# Skip the header line and process each line
tail -n +2 "$CSV_FILE" | while IFS=$',' read -r file_id rna_seq protein_seq; do
  # Remove double quotes from the fields (if present)
  file_id=$(echo "$file_id" | tr -d '"')
  rna_seq=$(echo "$rna_seq" | tr -d '"')
  protein_seq=$(echo "$protein_seq" | tr -d '"')

  echo "Running inference for file_id: $file_id"
  echo "Protein sequence: $protein_seq"
  echo "RNA sequence: $rna_seq"

  # Use expect to simulate interactive input and capture the output
  output=$(expect <<EOF
    spawn python3 src/inference.py
    expect "Enter the protein sequence: "
    send "$protein_seq\r"
    expect "Enter the RNA sequence: "
    send "$rna_seq\r"
    expect eof
EOF
  )

  # Parse the output to determine the prediction
  if echo "$output" | grep -q "NEGATIVE"; then
    prediction=0
  elif echo "$output" | grep -q "POSITIVE"; then
    prediction=1
  else
    prediction="NA"  # In case the output format is unexpected
  fi

  echo "Prediction: $prediction"

  # Append the result to the temporary file
  echo -e "$file_id\t$rna_seq\t$protein_seq\t$prediction" >> "$TEMP_FILE"

  # Check if the Python script executed successfully
  if [ $? -eq 0 ]; then
    echo "Inference completed successfully for file_id: $file_id"
  else
    echo "Error occurred during inference for file_id: $file_id"
  fi
done

# Replace the original CSV file with the updated one
mv "$TEMP_FILE" "$CSV_FILE"

echo "All pairs processed. Results saved to $CSV_FILE."

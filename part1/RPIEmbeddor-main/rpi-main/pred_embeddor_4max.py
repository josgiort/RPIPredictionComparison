import subprocess
import csv
import os

rpi_embeddor = ["python3", "src/inference.py"]

# Step 1: Read the CSV file
input_file = os.getcwd() + '/rpiemb_rnacmpt/result_table_missing_preds.tsv'
output_file = 'result_table_missing_preds_PREDS_EMBEDOR.tsv'


def process_sequences(rna_seq, protein_seq):
    """Runs the RPIEmbeddor prediction tool for given RNA and protein sequences."""
    try:
        process = subprocess.Popen(
           rpi_embeddor, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
           stderr=subprocess.PIPE, cwd=os.getcwd(), text=True
        )

        # Send input using communicate()
        stdout, stderr = process.communicate(input=f"{protein_seq}\n{rna_seq}\n")
        
        if stdout:
            stdout = stdout.strip()
            print(stdout)  # Debugging output
            if "POSITIVE" in stdout:
                return 1
            elif "NEGATIVE" in stdout:
                return 0
            else:
                return "N/A Pred"
        elif stderr:
            return f"Error: {stderr.strip()}"
        else:
            return "Error: No output received"
    
    finally:
        if process:
            process.wait()  # Ensure subprocess is cleaned up

# Read the input CSV
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter='\t')  # Adjust delimiter if necessary
    headers = next(reader)  # Read header row
    data = list(reader)  # Read the remaining rows
    print("Read input CSV")

# Step 2: Add new column header
headers.append("RPIEmbeddor_pred")
print("Add new column header")

# Step 3: Process each row sequentially
for row in data:
    row.append(process_sequences(row[2], row[1]))
    print("Processed row")

# Step 4: Write the updated data to a new CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

    writer = csv.writer(outfile, delimiter='\t')

    #writer = csv.writer(outfile)
    writer.writerow(headers)  # Write header row
    writer.writerows(data)  # Write processed rows

print("CSV with RPIEmbeddor_pred column has been saved.")


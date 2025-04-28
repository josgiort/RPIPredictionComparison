import subprocess
import csv

# Path to your CSV file containing sequences
csv_file_path = 'sequences.csv'  # Update this path to your CSV file
inference_script_path = 'src/inference.py'  # Path to inference.py


def run_inference(prot_sequence, rna_sequence):
    # This will run the inference.py script with the given inputs
    # The 'input' function will be simulated by passing input to the script via subprocess
    try:
        # Run the inference script with the sequences as input
        result = subprocess.run(
            ['python3', inference_script_path],
            input=f'{prot_sequence}\n{rna_sequence}\n',  # Simulate user input
            text=True,  # Allow input and output to be strings
            capture_output=True  # Capture the output of the script
        )

        # Print the output of the inference script
        print(result.stdout)

        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Failed to run inference: {e}")


def process_csv_and_run_inference(csv_file_path):
    # Open the CSV file
    with open(csv_file_path, mode='r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Skip the header if present
        next(csv_reader, None)  # Uncomment if the CSV file has headers

        # Loop through each row in the CSV file
        for row in csv_reader:
            if len(row) >= 3:  # Ensure there are at least three columns (dataset_id2, prot_seq, rna_seq)
                dataset_id2 = row[0]  # The first column (identifier)
                prot_sequence = row[1]  # The second column (prot_seq)
                rna_sequence = row[2]  # The third column (rna_seq)

                print(f"Running inference for Dataset ID: {dataset_id2}")
                print(f"Prot Sequence: {prot_sequence}")
                print(f"RNA Sequence: {rna_sequence}")
                run_inference(prot_sequence, rna_sequence)


if __name__ == "__main__":
    process_csv_and_run_inference(csv_file_path)

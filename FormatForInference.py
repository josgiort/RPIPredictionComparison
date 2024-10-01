import json
import sys
import subprocess
import re
from TrimmingMode import from_left, from_right, from_middle
from Bio import SeqIO

# This file sets up the fasta file of RNA sequences to a proper text format for RPIEmbeddor to do inference
# This file has three modes of operation for handling the RNA sequences

# RNA sequences need to be specified in a fasta file 'sequences.fasta'
# Depending on the mode of operation of the script, it would be required that RNA sequences have arguments in their sequence description line, for example:
# >sequence1 | parameter_1=1234 parameter_2=1234 parameter_3=1234


# Mode 1: taking whole RNA sequence.
# Mode 2: taking substring from RNA sequence.
# Mode 3: taking substrings with gradually incrementing lengths from a starting part of the RNA sequence, these increments
# can be done from the sequence left end, from the sequence right end or from some part within the sequence,
# for this last case, the increments are done simultaneously to the left and to the right of the specified starting part (interval)
# until reaching, if possible, the half of the sequence length at each direction.

# Please specify only either 1, 2 or 3 for desired mode of operation
mode_operation = int(sys.argv[1])
# Please name this file "sequences.fasta"
input_file = sys.argv[2]
# Please name this file "dataset_inference.txt"
output_file = sys.argv[3]

sequences = list(SeqIO.parse(input_file, "fasta"))
chain_indexes = ""


# If mode is 1, sequences of fasta file are taken fully or up to the first 1022 characters
# No extra arguments needed in the fasta file
if mode_operation == 1 :
    for record in sequences :
        seq_len = min(len(record.seq), 1022)
        chain_indexes += record.id + "\t0\t" + str(seq_len) + "\n"


# if mode is 2, substrings of the sequences of fasta file are taken
# Extra arguments needed in the fasta file, in the description line of each RNA sequence:
# the interval to conserve is appended to the sequence id's in the fasta file,
# with the format " | start_index=XXX end_index=YYY"
# Note: start_index is a 0-based index while end_index is a 1-based index
# for example: from the RNA sequence "seq1", take the substring from the third character to the seventh character, both inclusive
# >seq1 | start_index=2 end_index=7
# AGCGAUCCGG
# Then the script would take the substring CGAUC from the RNA sequence

elif mode_operation == 2:
    for record in sequences:
        #interval = re.findall("\| [0-9]+ [0-9]+$", record.description)
        interval = re.findall("\| start_index=[0-9]+ end_index=[0-9]+", record.description)
        if len(interval) == 0:
            print("Not proper text format for substring intervals")
            exit(0)
        else:
            left_boundary = re.findall("start_index=[0-9]+", record.description)
            left_boundary = int(left_boundary[0].split("=")[1].strip())
            right_boundary = re.findall("end_index=[0-9]+", record.description)
            right_boundary = int(right_boundary[0].split("=")[1].strip())

            if (right_boundary - left_boundary) > 1022:
                print("Maximum length of subchain is 1022, try again with shorter subchain")
                exit(0)

            chain_indexes += record.id + "\t" + str(left_boundary) + "\t" + str(right_boundary) + "\n"

# if mode is 3, several substrings of successive varying length are taken
# it needs some parameters on the description line of the sequences in the fasta file
# the process of getting several subchains from a given starting index in a chain,
# by gradually increasing their lengths by a constant factor

elif mode_operation == 3:
    # Check correct format of input file
    for record in sequences:
        arguments = re.findall("\| varying_length_mode=[0-9] spacing=[0-9]{1,3}(?: middle_start_left=[0-9]+ middle_start_right=[0-9]+)?", record.description)
        if len(arguments) == 0:
            print("Not proper arguments for varying length substrings")
            exit(0)
        else:
            #args_varying_lengths = re.split(" ", record.description)
            varying_length_mode = re.findall("varying_length_mode=[0-9]", record.description)
            varying_length_mode = int(varying_length_mode[0].split("=")[1].strip())

            spacing = re.findall("spacing=[0-9]{1,3}", record.description)
            spacing = int(spacing[0].split("=")[1].strip())

            seq_len = len(record.seq)

            if varying_length_mode == 2:
                middle_start_left = re.findall("middle_start_left=[0-9]+", record.description)
                middle_start_left = int(middle_start_left[0].split("=")[1].strip())

                middle_start_right = re.findall("middle_start_right=[0-9]+", record.description)
                middle_start_right = int(middle_start_right[0].split("=")[1].strip())

                # Indexes for every subchain in the bed file is generated with a loop
                # Also the respective chain length is calculated for each substring for later use in the plots
            if varying_length_mode == 0:
                chain_indexes += from_left(record.id, seq_len, spacing)
            elif varying_length_mode == 1:
                chain_indexes += from_right(record.id, seq_len, spacing)
            elif varying_length_mode == 2:
                chain_indexes += from_middle(record.id, seq_len, spacing, middle_start_left, middle_start_right)
            else:
                print("Invalid argument varying_length_mode")
                exit(0)

else:
    print("Please enter a valid mode of operation")
    exit(0)

# With "w" option, it will override any existing content and create a new file if "indexes.bed" does not exist
f = open("indexes.bed", "w")
f.write(chain_indexes)
f.close()

# Call for 'bedtools getfasta' to generate the subchains into another fasta file
subprocess.run(["bash", "-c", "bedtools getfasta -fi " + input_file + " -bed indexes.bed -fo subchains.fasta"])

fasta_dict = {}
# Open the FASTA file and parse it
with open("subchains.fasta") as fasta_file:
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        # Extract the whole sequence ID or first part of the sequence ID before ':'
        sequence_id = seq_record.id.split(':')[0]
        # Check if the sequence_id already exists in the dictionary
        if sequence_id not in fasta_dict:
            fasta_dict[sequence_id] = []
        # Append the sequence to the corresponding key in the dictionary
        #fasta_dict[sequence_id].append(str(seq_record.seq))
        fasta_dict[sequence_id].append([seq_record.id.split('|')[0], seq_record.seq])

dataset_inference = ""
with open('test_set_jsonl.jsonl', 'r') as json_file:
    for (line, key_val) in zip(json_file, fasta_dict.items()):
        data_entry = json.loads(line)
        for seq in key_val[1]:
            dataset_inference += str(data_entry["Sequence_2"].upper()) + '\t' + str(data_entry["Sequence_2_len"]) + '\t' + seq[0] + '\t' + str(seq[1]) + '\t' + str(len(seq[1])) + '\t' + str(data_entry["Interaction"]) + '\n'

f = open(output_file, "w")
f.write(dataset_inference)
f.close()
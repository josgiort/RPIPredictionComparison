import json
import sys
import subprocess
import re
from TrimmingMode import from_left, from_right, from_middle
from Bio import SeqIO

# This file sets up the fasta file of sequences to a text format needed for RPIEmbeddor to do inference
# Additionally, if specified, it creates versions of the chains of varying length

# Mode 1 complete, 2 subchain, 3 iterative trimming
mode_operation = int(sys.argv[1])
# Please name this file "sequences.fasta"
input_file = sys.argv[2]
# Please name this file "dataset_inference.txt"
output_file = sys.argv[3]

sequences = list(SeqIO.parse(input_file, "fasta"))
chain_indexes = ""
# If mode is 1, sequences of fasta file are taken fully or up to the first 1022 characters, it omits the needing of an input file
if mode_operation == 1 :
    for record in sequences :
        seq_len = min(len(record.seq), 1022)
        chain_indexes += record.id + "\t0\t" + str(seq_len) + "\n"
# if mode is 2, substrings of the sequences of fasta file are taken
# the interval to conserve is appended to the sequence id's in the fasta file, with the format " | left_boundary right_boundary"
elif mode_operation == 2:
    for record in sequences:
        interval = re.findall("\| [0-9]+ [0-9]+$", record.description)
        if len(interval) == 0:
            print("Not proper text format for substring intervals")
            exit(0)
        else:
            left_boundary = re.findall(" [0-9]+ ", record.description)
            left_boundary = int(left_boundary[0].strip())
            right_boundary = re.findall(" [0-9]+$", record.description)
            right_boundary = int(right_boundary[0].strip())

            if (right_boundary - left_boundary) > 1022:
                print("Maximum length of subchain is 1022, try again with shorter subchain")
                exit(0)

            chain_indexes += record.id + "\t" + str(left_boundary) + "\t" + str(right_boundary) + "\n"

            # Pending: Specify in the documentation base of index numbers
            # intvl_bdary_l = int(input("Enter the interval left boundary (0 based index, inclusive): "))
            # intvl_bdary_r = int(input("Enter the interval right boundary (1 based index, inclusive): "))

# if mode is 3, several substrings of successive varying length are taken, it needs an input file specifying the trimmming parameters
elif mode_operation == 3:
    # Check correct format of input file
    for record in sequences:
        interval = re.findall("\| varying_length_mode=[0-9] spacing=[0-9]{1,3} (?:middle_start_left=[0-9]+ middle_start_right=[0-9]+)?$", record.description)
        if len(interval) == 0:
            print("Not proper text format for substring intervals")
            exit(0)
        else:
# TERMINAR ESTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO SOLO ES HABILITAR LOS TRES VARYING LENGTH MODE
            seq_len = min(len(record.seq), 1022)

                # Indexes for every subchain in the bed file is generated with a loop
                # Also the respective chain length is calculated for each substring for later use in the plots
            if itr_trim_mode == 0:
                chain_indexes, chain_lengths = from_left(seq_len, itr_trim_spacing)
            elif itr_trim_mode == 1:
                chain_indexes, chain_lengths = from_right(seq_len, itr_trim_spacing)
            elif itr_trim_mode == 2:
                chain_indexes, chain_lengths = from_middle(seq_len, itr_trim_spacing)

















            left_boundary = re.findall(" [0-9]+ ", record.description)
            left_boundary = int(left_boundary[0].strip())
            right_boundary = re.findall(" [0-9]+$", record.description)
            right_boundary = int(right_boundary[0].strip())

            if (right_boundary - left_boundary) > 1022:
                print("Maximum length of subchain is 1022, try again with shorter subchain")
                exit(0)

            chain_indexes += record.id + "\t" + str(left_boundary) + "\t" + str(right_boundary) + "\n"

else:
    # Print enter a valid mode of operation
    print()

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
with open('test_set_limit.jsonl', 'r') as json_file:
    for (line, key_val) in zip(json_file, fasta_dict.items()):
        data_entry = json.loads(line)
        for seq in key_val[1]:
            dataset_inference += str(data_entry["Sequence_2"].upper()) + '\t' + str(data_entry["Sequence_2_len"]) + '\t' + seq[0] + '\t' + str(seq[1]) + '\t' + str(len(seq[1])) + '\t' + str(data_entry["Interaction"]) + '\n'

f = open(output_file, "w")
f.write(dataset_inference)
f.close()





"""
#####################################################################################
# RNA chain needs to be specified previously, in a fasta file with chain id 'seq1'


#if trim_election == 1:

# Iterative trimming is just the process of getting several subchains from a given starting index in a chain,
# by just iteratively increasing their lengths by a constant factor

itr_trim_election = int(input("Iterative trimming (0 - no, 1 - yes): "))


if itr_trim_election == 1:

    itr_trim_mode = int(input("Iterative trimming mode (0 - from left, 1 - from right, 2 - from middle): "))
    itr_trim_spacing = int(input("Enter the spacing between every new trimming: "))

    chain_indexes = ""
    chain_lengths = ""
    seq_len = 1022 # With this  I am not accounting for less than 1022, later check it!
    for seq_record in SeqIO.parse("seq1.fasta", "fasta"):
        seq_len = len(seq_record)

    # Indexes for every subchain in the bed file is generated with a loop
    # Also the respective chain length is calculated for each substring for later use in the plots
    if itr_trim_mode == 0:
        chain_indexes, chain_lengths = from_left(seq_len, itr_trim_spacing)
    elif itr_trim_mode == 1:
        chain_indexes, chain_lengths = from_right(seq_len, itr_trim_spacing)
    elif itr_trim_mode == 2:
        chain_indexes, chain_lengths = from_middle(seq_len, itr_trim_spacing)

    # Once the indexes are calculated they are stored in the bed file
    f = open("indexes.bed", "w")
    f.write(chain_indexes)
    f.close()

    # Also the lengths are stored in a txt file
    f = open("lengths.txt", "w")
    f.write(chain_lengths)
    f.close()

    # Call for 'bedtools getfasta' to generate the subchains into another fasta file
    subprocess.run(["bash", "-c", "bedtools getfasta -fi seq1.fasta -bed indexes.bed -fo subchains.fasta"])

else:
    normal_mode = int(input("Enter what mode to do (0 - whole chain, 1 - subchain): "))

    if normal_mode == 0:
        for seq_record in SeqIO.parse("seq1.fasta", "fasta"):
            seq_len = min(len(seq_record), 1022)

        chain_indexes = "seq1\t0\t" + str(seq_len) + "\n"
        chain_lengths = str(seq_len) + "\n"

        f = open("indexes.bed", "w")
        f.write(chain_indexes)
        f.close()

        # Also the length is stored in txt file
        f = open("lengths.txt", "w")
        f.write(chain_lengths)
        f.close()

        # Call for 'bedtools getfasta' to generate the subchains into another fasta file
        subprocess.run(["bash", "-c", "bedtools getfasta -fi seq1.fasta -bed indexes.bed -fo subchains.fasta"])

    elif normal_mode == 1:
        intvl_bdary_l = int(input("Enter the interval left boundary (0 based index, inclusive): "))
        intvl_bdary_r = int(input("Enter the interval right boundary (1 based index, inclusive): "))

        if (intvl_bdary_r - intvl_bdary_l) > 1022:
            print("Maximum length of subchain is 1022, try again with shorter subchain")
            exit(0)

        chain_indexes = "seq1\t" + str(intvl_bdary_l) + "\t" + str(intvl_bdary_r) + "\n"
        chain_lengths = str(intvl_bdary_r - intvl_bdary_l) + "\n"

        f = open("indexes.bed", "w")
        f.write(chain_indexes)
        f.close()

        # Also the length is stored in txt file
        f = open("lengths.txt", "w")
        f.write(chain_lengths)
        f.close()

        # Call for 'bedtools getfasta' to generate the subchains into another fasta file
        subprocess.run(["bash", "-c", "bedtools getfasta -fi seq1.fasta -bed indexes.bed -fo subchains.fasta"])

"""
import sys
import subprocess
from TrimmingMode import from_left, from_right, from_middle
from Bio import SeqIO
# Mode 1 complete, 2 subchain, 3 iterative trimming
mode_operation = int(sys.argv[1])
# Please name this file "sequences.fasta"
input_file = sys.argv[2]
# Please name this file "subchains.fasta"
output_file = sys.argv[3]

sequences = list(SeqIO.parse(input_file, "fasta"))

# if mode is 1 that means we take the fasta file and use embeddor with every full chain, it omits the needing of an input file
if mode_operation == 1 :
    chain_indexes = ""
    for record in sequences :
        seq_len = min(len(record.seq), 1022)
        chain_indexes += record.id + "\t0\t" + str(seq_len) + "\n"

    # With "w" option, it will override any existing content and create anew file if "indexes.bed" does not exist
    f = open("indexes.bed", "w")
    f.write(chain_indexes)
    f.close()

    # Call for 'bedtools getfasta' to generate the subchains into another fasta file
    subprocess.run(["bash", "-c", "bedtools getfasta -fi " + input_file + " -bed indexes.bed -fo " + output_file])

"""
# if mode is 2 that means we take the fasta and take a substring for every chain, it needs an input file specifying
elif modeOperation == 2 :
    # Check correct format of input file
    print()
# if mode is 3 that means we take the fasta and do iterative trimming, it needs an input file specifying the trimmming parameters
elif modeOperation == 3 :
# Check correct format of input file
    print()
    # New step todo, make update de rna-protein pairs file to have de version with all trimmings
else:
    # Print enter a valid mode of operation
    print()







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
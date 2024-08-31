import subprocess
from TrimmingMode import from_left, from_right, from_middle
from Bio import SeqIO

# RNA chain needs to be specified previously, in a fasta file with chain id 'seq1'

# Ignore this two lines
#trim_election = int(input("Chain to trim (0 - none, 1 - prot, 2 - rna, 3 - both): "))
#if trim_election == 1:

# Iterative trimming is just the process of getting several subchains from a given starting index in a chain,
# by just iteratively increasing their lengths by a constant factor

itr_trim_election = int(input("Iterative trimming (0 - no, 1 - yes): "))
itr_trim_mode = int(input("Iterative trimming mode (0 - from left, 1 - from right, 2 - from middle): "))
itr_trim_spacing = int(input("Enter the spacing between every new trimming: "))

if itr_trim_election == 1:
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
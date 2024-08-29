import subprocess
from Bio import SeqIO
import numpy as np
from sympy.stats.sampling.sample_numpy import numpy

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
    seq_len = 1022 # With this  I am not accounting for less than 1022, check it
    for seq_record in SeqIO.parse("seq1.fasta", "fasta"):
        seq_len = len(seq_record)

    # Indexes for every subchain in the bed file is generated with a loop
    # Also the respective chain length is calculated for each substring for later use in the plots
    if itr_trim_mode == 0:
        for i in range(2, min(seq_len+1, 1023), itr_trim_spacing): # Never put start index of range() to 0, due to index definition bed format
            chain_indexes += "seq1\t0\t" + str(i) +"\n"
            chain_lengths += str(i-0)+"\n"
    elif itr_trim_mode == 1:
        for i in range(2, min(seq_len+1, 1023), itr_trim_spacing): # Never put start index of range() to 0, due to resulting chain of 0 length in legnths file but not in subchains file
            chain_indexes += "seq1\t" + str(seq_len-i) + "\t" + str(seq_len) + "\n"
            chain_lengths += str(seq_len - (seq_len-i)) + "\n"
    elif itr_trim_mode == 2:
        # Starting point to extend within the chain can be specified in interval-based (2 index required) or position-based (1 index required)
        itr_trim_mid_mode = int(input("Enter starting point type for middle trimming (0 - interval, 1- position): "))

        intvl_bdary_l = ""
        intvl_bdary_r = ""

        if itr_trim_mid_mode == 0:
            intvl_bdary_l = int(input("Enter the interval left boundary (0 based index, inclusive): "))
            intvl_bdary_r = int(input("Enter the interval right boundary (1 based index, inclusive): "))

        elif itr_trim_mid_mode == 1:
            position_conserve = int(input("Enter the specific position; (1 based index, int): "))
            # intvl_bdary_l = position_conserve - 50
            # intvl_bdary_r = position_conserve + 50

            # In practice, position based starting point is same as interval based, since two boundaries are created manually by extending two residues at each side
            intvl_bdary_l = position_conserve - 3 # Here is 1 more than right boundary due to index definition bed format
            intvl_bdary_r = position_conserve + 2

        # Trimming
        len_intvl = intvl_bdary_r - intvl_bdary_l # Finding length of interval with bed format is easier just a simple subtraction

        l_chunk = intvl_bdary_l # <- Until here the left boundary was adjusted as per the bed format
        r_chunk = seq_len - intvl_bdary_r

        half = (1022 - len_intvl) // 2

        #half = (10 - len_intvl) // 2

        if l_chunk >= half:
            if r_chunk >= half:
                # final_example_rna = trim(example_rna, intvl_bdary_l, intvl_bdary_r, half, half)
                l_chunk_itrble = half
                r_chunk_itrble = half
            else:
                # final_example_rna = trim(example_rna, intvl_bdary_l, intvl_bdary_r, half + (half - r_chunk), r_chunk)
                l_chunk_itrble =  half + (half - r_chunk)
                r_chunk_itrble =  r_chunk
        else:
            # final_example_rna = trim(example_rna, intvl_bdary_l, intvl_bdary_r, l_chunk, half + (half - l_chunk))
            l_chunk_itrble = l_chunk
            r_chunk_itrble = half + (half - l_chunk)

        for i in range(2, l_chunk_itrble, itr_trim_spacing):
            chain_indexes += ("seq1\t" + str(seq_len - i) +"\n" + str(seq_len * (flag *)) + "\n")

        splitted_str = chain_indexes


        """
        for i in range(2,  r_chunk_itrble), itr_trim_spacing):
            chain_indexes += ("seq1\t" + str((seq_len - i) * (flag *)) + "\t" + str(seq_len * (flag *)) + "\n")
            chain_indexes += ("seq1\t" +
                              str((seq_len-i) * (flag * )) +
                              "\t" + str(seq_len * (flag * )) + "\n")
            chain_lengths += str(seq_len - (seq_len-i)) + "\n"

        """
        # It misses the for loop to produce the subchains from the iterative squaring

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

# This rest of the code will be for iterative trimming mode 1 and 2, namely, from right and from middle
# This rest of the code will be for iterative trimming mode 2, namely, from middle
# Still will be tested


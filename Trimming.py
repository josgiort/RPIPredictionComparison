import subprocess

# RNA chain needs to be specified previously, in a fasta file with chain id 'seq1'
# RNA chain needs to be specified previosly, in a fasta file with chain id 'seq1'

# Ignore this two lines
#trim_election = int(input("Chain to trim (0 - none, 1 - prot, 2 - rna, 3 - both): "))
#if trim_election == 1:

# Iterative trimming is just the process of getting several subchains from a given starting index in a chain,
#  by just iteratively increasing their lengths by a constant factor

itr_trim_election = int(input("Iterative trimming (0 - no, 1 - yes): "))
itr_trim_mode = int(input("Iterative trimming mode (0 - from left, 1 - from right, 2 - from middle): "))
itr_trim_spacing = int(input("Enter the spacing between every new trimming: "))

if itr_trim_election == 1:
    chain_indices = ""
    chain_lengths = ""
    if itr_trim_mode == 0:
        # Indexes for every subchain in the bed file is generated with a loop
        for i in range(10, 1022, itr_trim_spacing):
            chain_indices += "seq1\t0\t" + str(i) +"\n"
            # Also the respective chain length is calculated for each substring for later use in the plots
            chain_lengths += str(i-0)+"\n"
    elif itr_trim_mode == 1:
        for i in range(10, 1022, itr_trim_spacing):
            chain_indices += "seq1\t" + str(1022-i) + "\t1022\n"
            # Also the respective chain length is calculated for each substring for later use in the plots
            chain_lengths += str(1022 - (1022-i)) + "\n"
    # Once the indexes are calculated they are stored in the bed file
    f = open("indexes.bed", "w")
    f.write(chain_indices)
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
"""
        if itr_trim_mode == 2:
            list_trimmings = []
            final_example_rna = example_rna


            itr_trim_mid_mode = int(input("Enter starting point for middle trimming (0 - interval, 1- position): "))

            intvl_bdary_l = ""
            intvl_bdary_r = ""

            if itr_trim_mid_mode == 0:
                intvl_bdary_l = int(input("Enter the interval left boundary (1 based index, inclusive): "))
                intvl_bdary_r = int(input("Enter the interval right boundary (1 based index, inclusive): "))

            elif itr_trim_mid_mode == 1:
                position_conserve = int(input("Enter the specific position; (1 based index, int): "))
                #intvl_bdary_l = position_conserve - 50
                #intvl_bdary_r = position_conserve + 50

                intvl_bdary_l = position_conserve - 2
                intvl_bdary_r = position_conserve + 2

            # Trimming
            len_intvl = intvl_bdary_r - intvl_bdary_l + 1

            l_chunk = intvl_bdary_l - 1
            r_chunk = len(final_example_rna) - intvl_bdary_r

            #half = (1022 - len_intvl) // 2

            half = (10 - len_intvl) // 2

            if l_chunk >= half :
                if r_chunk >= half :
                    #final_example_rna = trim(example_rna, intvl_bdary_l, intvl_bdary_r, half, half)
                else:
                    #final_example_rna = trim(example_rna, intvl_bdary_l, intvl_bdary_r, half + (half - r_chunk), r_chunk)
            else:
                #final_example_rna = trim(example_rna, intvl_bdary_l, intvl_bdary_r, l_chunk, half + (half - l_chunk))

            print(final_example_rna)
            # It misses the for loop to produce the subchains from the iterative squaring
"""


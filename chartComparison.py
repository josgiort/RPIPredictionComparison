

"""
def trim(chain, cl, cr, el, er):
    if er < 0 or el < 0:
        print("Invalid extension (can't be negative), exiting ...")
        exit(1)
    if cl > cr:
        print("Invalid conserved region indexes, exiting ...")
        exit(1)
    if (er == 0 and el == 0) and cl == cr:
        print("Invalid indexes (all indexes can't be the same), exiting ...")
        exit(1)
    index1 = (cl - el) - 1
    index2 = (cr + er) - 1 + 1
    if index1 < 0 or index2 < 0:
        # print("Invalid indexes (they cant be negative), exiting...")
        # exit(1)
        raise Exception("Invalid indexes (they cant be negative), exiting...")
    if index1 >= len(chain) or index2 > len(chain):
        raise Exception("Invalid indexes: Index out of Bounds Exception)")
    trimmed_chain = chain[index1:index2]
    return trimmed_chain


example_prot = input("Enter protein chain: ")
example_rna = input("Enter rna chain: ")

if (len(example_prot) < 2) or (len(example_rna) < 2):
    print("Invalid chain length detected (they must be at least 2 in length), exiting ...")
    exit(1)

trim_election = int(input("Chain to trim (0 - none, 1 - prot, 2 - rna, 3 - both): "))

if trim_election == 1:
    #conserved_region_left = int(input("Enter left boundary of chain region to conserve: "))
    #conserved_region_right = int(input("Enter right boundary of chain region to conserve: "))
    #extension_left = int(input("Enter left extension from conserved region: "))
    #extension_right = int(input("Enter right extension from conserved region: "))

    itr_trim_election = int(input("Iterative trimming (0 - no, 1 - yes): "))
    itr_trim_mode = int(input("Iterative trimming mode (0 - from left, 1 - from right, 2 - from middle): "))
    itr_trim_spacing = int(input("Enter the spacing between every new trimming: "))

    if itr_trim_election == 1:

        if itr_trim_mode == 0:
            list_trimmings = []
            final_example_rna = example_rna

            # Trimming
            if len(example_rna) > 1022:
                final_example_rna = trim(example_rna, 1, 1022, 0, 0)

            # It is assumed that length is 1022, not accounting for less than 1022
            # Possible exception for less than 1022 case
            temp_chain = ""
            for i in range(10, 1022, itr_trim_spacing):
                temp_chain = trim(final_example_rna, 1, i, 0, 0)
                list_trimmings.append(temp_chain)

            print(len(list_trimmings))

        if itr_trim_mode == 1:
            list_trimmings = []
            final_example_rna = example_rna

            # Trimming
            if len(example_rna) > 1022:
                final_example_rna = trim(example_rna, len(example_rna)-1022, len(example_rna), 0, 0)

            # Same assumption as above
            # Modify to account for case less than 1022
            temp_chain = ""
            for i in range(9, 1022, itr_trim_spacing):
                temp_chain = trim(final_example_rna, len(final_example_rna) - i, len(final_example_rna), 0, 0)
                list_trimmings.append(temp_chain)

            print(len(list_trimmings))


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
                    final_example_rna = trim(example_rna, intvl_bdary_l, intvl_bdary_r, half, half)
                else:
                    final_example_rna = trim(example_rna, intvl_bdary_l, intvl_bdary_r, half + (half - r_chunk), r_chunk)
            else:
                final_example_rna = trim(example_rna, intvl_bdary_l, intvl_bdary_r, l_chunk, half + (half - l_chunk))

            print(final_example_rna)"""
            # It misses the for loop to produce the subchains from the iterative squaring

#rnachain = "UUUGGGAGGCUGAGGCAGGCAGAUCACCUAAGGCCAGGAAUUCGACACCAGCCUGGCCAACGUGGCAAAACCCGUCUCUACUAAAAAUACAAAAAUUAGCCGGGCGUGGUGGUGUGCGCCUGGAAUCCCAGCUACCCAGGAGGCUGAGGCAGGAGAAAUGCUGGAACCCGGGAGGCAGAGGCUGCAGUGAGCUGAGAUCAUGCCACUACUGCACUCCAGCCUGGGUGACACAGCAAGACUCCCUCUAAAAAAAGAAAAAAAGAAAAGAAAAGAAAAGAAAAUGAUAUAUCCAUGAUGAAUUAAAAUGGAGUGGAACCCACUGAUGGGAAAGCCACAGAAGGUACCAGUUAUCCACUCACUGACUUAGGUGCCUCCACUAGAAUUCUCAGCACGUUUUUGCAGAACCUGGGCAACAAGAGCGAAACCCCAUCUCAAAACCACAACAACAACAACAGGACAACAGAGAUGGACGACGGAUCGGGAAAGCCAACCAGACAGCGUGAGGCCAGGACGGAAAGAGGCACAGGGAGCUCUGCUCAGUGUCGCUACAGGGGAUCUCUCAGGCUCACAACGGGCCACUCCUCUAGGGAAGUUCUGGUCUCAUCAUGAUCCUUGUUUGGUCUCACUCCCCAUGUCCUUCUCUGUCCCUCCUCCAACUGCCAUUUAUUUAUUUAACUGAAAAAGUACCAAUCACCCACAUAGGCAUGACAUACUCAUCCAUGUACCCAUUUCUUAAAAUUGAUCAUUGUUAACAUUUGGUGUAAUUUGCUUUAUUUAUUUUUAAUGAAAUAAAUAAAACUUUACAGAAAAUGCUUUAUUUUUCUCUUUGUUCCCUCCCCAUCCUAUAUUUUUCUCCUAAAAAACCCUAUUAUCAGAAAUAUUAGUGUGUAUUCCCAGUUUCGACUUUUUAUUUUAUUACACACACACUCCCACACAUAGCUGUGACAAUGAACUUCACAUAGUAUGGUUCUGUAUUUUCUCUUUGUUUUUCAAACUUACAUAAGUAUUUUACUAUUUCUCAUGGAAAAACUCACUUUUCCCAUCCAACGUUAUGUUUCCUUAAGAUCUCUCUAUGUUGAUAUAAAGAAAUCUAGCUCAUUCUUUUUAAUGAAAAUAAAGUAUAUUUUAUGAAUGUAACUCAUGCUAACCAUGGCAAUAAAAGCUCCAUCAAGCAUGCAUUUAGU"
#print(rnachain[0: 1022])




#print("This is your rna chain: " + example_rna)
#print("This is your chain trimmed: " +


import matplotlib.pyplot as plt
import numpy as np

#x = [0.0006067785434, 0.0004337127029, 0.004191544373, 0.0001658343681, 0.0002991639194, 0.0001573030167, 0.0005302123027]
#y = [1, -19.9, -17.3, -9.9, -6.7, -4.4, -1.6]

x=[0.0006067785434, 0.0005302123027, 0.0001573030167, 0.0002991639194, 0.0001658343681, 0.004191544373, 0.0004337127029]
y=[-1.0, -1.6, -4.4, -6.7, -9.9, -17.3, -19.9] # good one


#x1=[0.0006067785434, 0.0005302123027, 0.0001573030167, 0.0002991639194, 0.0001658343681, 0.004191544373, 0.0004337127029]
#y1=range(1,8)

#x2=[-1.0, -1.6, -4.4, -6.7, -9.9, -17.3, -19.9]
#y2=range(1,8)




plt.figure(figsize=(5, 5), layout='constrained')
plt.plot(x, y)
plt.scatter(x, y,  s=14, alpha=1.0, edgecolors="k")
plt.xticks(rotation=35)
#plt.plot(x2, y2, label='affinity score')
plt.xlabel('embeddor score (interaction probability)')
plt.ylabel('affinity score (-fold)')
plt.title("Embeddor vs Affinity score on SELEX samples")
#plt.legend()
plt.show()
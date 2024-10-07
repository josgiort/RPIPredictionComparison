import sys
import re

# Please name this file "dataset_inference.txt"
input_file = sys.argv[1]

count_line = 0

with open(input_file) as file:
    for line in file:
        count_line += 1
        prot = re.search("[A-Z]+\t", line)[0].strip()
        rna = re.search("\t[A-Z]+\t", line)[0].strip()

        max_length = 1024
        valid_letters_rna = {'A', 'C', 'G', 'U'}
        unique_letters_rna = set(rna.upper())
        invalid_letters_rna = unique_letters_rna.difference(valid_letters_rna)
        if len(invalid_letters_rna) > 0:
            print(f"Invalid characters found: {', '.join(invalid_letters_rna)}")
            print("Datapoint number: " + str(count_line))
        elif len(rna) > max_length:
            print(f"Sequence length should not exceed {max_length} characters.")
            print("Datapoint number: " + str(count_line))
        else:pass

        valid_letters_prot = {'A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W',
                         'Y', 'V'}
        unique_letters_prot = set(prot.upper())
        invalid_letters_prot = unique_letters_prot.difference(valid_letters_prot)
        if len(invalid_letters_prot) > 0:
            print(f"Invalid characters found: {', '.join(invalid_letters_prot)}")
            print("Datapoint number: " + str(count_line))
        elif len(prot) > max_length:
            print(f"Sequence length should not exceed {max_length} characters.")
            print("Datapoint number: " + str(count_line))
        else:pass



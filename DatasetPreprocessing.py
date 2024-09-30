import json

# This file works to preprocess the input files only from the test set of RPIEmbeddor

fasta = ""
cntr = 0

# Reading from a JSON Lines file
with open('test_set_jsonl.jsonl', 'r') as file:
    for line in file:
        cntr += 1
        data_entry = json.loads(line)
        fasta += ">seq" + str(cntr) + '\n' + data_entry["Sequence_1"] + '\n'

f = open("sequences.fasta", "w")
f.write(fasta)
f.close()
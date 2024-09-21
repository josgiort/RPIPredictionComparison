from Bio import SeqIO
import sys
import subprocess
import re

# Please name this file "dataset_pcsd.text"
input_file = sys.argv[1]
# Please name this file "result_table.fasta"
output_file = sys.argv[2]

#sequences = list(SeqIO.parse(input_file, "fasta"))

rpi_embeddor = ["python3", "child.py"]
result_table = ""



# ver como proveer el par protein - rna, porque con esto solo se ingresaria el rna, falta la proteina
# approach crear un archivo en Trimming llamado dataset_pcsd donde este cada par protein - rna
# esto supone procesamiento extra para el caso de iterative trimming
with open("dataset_pcsd.txt") as file:
    for line in file:
        prot = re.search("[A-Z]+\t", line)[0].strip()
        rna = re.search("\t[A-Z]+\t", line)[0].strip()

        #input_stdin = [prot, rna]
        process = subprocess.Popen(rpi_embeddor, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        process.stdin.write(prot + "\n")
        process.stdin.flush()

        process.stdin.write(rna + "\n")
        process.stdin.flush()

        stdout, stderr = process.communicate()
        print(stdout)
        print("")


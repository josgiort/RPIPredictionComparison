import sys
import subprocess
import re

# Please name this file "dataset_inference.txt"
input_file = sys.argv[1]
# Please name this file "result_table.txt"
output_file = sys.argv[2]

rpi_embeddor = ["python3", "src/inference.py"]
result_table = ""

# approach crear un archivo en Trimming llamado dataset_inference donde este cada par protein - rna
# esto supone procesamiento extra para el caso de iterative trimming

count_line = 0

with open(input_file) as file:
    for line in file:
        count_line += 1
        prot = re.search("[A-Z]+\t", line)[0].strip()
        rna = re.search("\t[A-Z]+\t", line)[0].strip()
        # Setting up call for RPIEmbeddor
        process = subprocess.Popen(rpi_embeddor, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=r'/home/jose/Desktop/RPIEmbeddor-main/rpi-main', text=True)
        # Specify first stdin
        process.stdin.write(prot + "\n")
        process.stdin.flush()
        # Specify second stdin
        process.stdin.write(rna + "\n")
        process.stdin.flush()
        # Get stdout
        stdout, stderr = process.communicate()
        print("Datapoint number: " + str(count_line))
        print(stdout)
        print(stderr)
        # Adapt prediction text to add it to result_table file
        prediction = re.search("NEGATIVE|POSITIVE", stdout)[0].strip()
        if prediction == "POSITIVE":
            prediction = "True"
        elif prediction == "NEGATIVE":
            prediction = "False"
        else:
            prediction = "something_weird_happened_with_the_prediction_check_it_out"

        result_table += line.replace("\n", "") + '\t' + prediction + '\n'

f = open(output_file, "w")
f.write(result_table)
f.close()


import subprocess
import re

input_file = "dataset3.txt"

output_file = "result_table3.txt"

rpi_embeddor = ["python3", "src/inference.py"]
result_table = ""

count_line = 0
with open(input_file) as file:
    for line in file:
        count_line += 1
        prot = re.search("[A-Z]+\t", line)[0].strip()
        rna = re.search("\t[A-Z]+\t", line)[0].strip()

        # Setting up call for RPIEmbeddor
        process = subprocess.Popen(rpi_embeddor, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=r'/home/fr/fr_fr/fr_jg590/rpi-main', text=True)
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

        # Adapt prediction text to add it to result_table file
        if stdout != None:
            # Handle the case when for any reason there was stdout but with no prediction in it
            positive_pred = stdout.find("POSITIVE")
            negative_pred = stdout.find("NEGATIVE")
            if positive_pred != -1:
                prediction = "True"
            elif negative_pred != -1:
                prediction = "False"
            # Case both variables are -1, neither positive nor negative found in any of the variables
            else:
                prediction = "N/A Pred"
        elif stderr != None:
            prediction = stderr
        result_table += line.replace("\n", "") + '\t' + prediction + '\n'
f = open(output_file, "w")
f.write(result_table)
f.close()


import sys
import subprocess
import re

# Please name this file "dataset_inference.txt"
input_file = sys.argv[1]
# Please name this file "result_table.txt"
output_file = input_file.split("_")[0] + "_result.txt"

out_dir = input_file.split("_")[0] + "_outputs"

rpi_embeddor = ["python3", "src/inference.py"]
result_table = ""

count_line = 0
with open(out_dir + "/" + input_file) as file:
    for line in file:
        count_line += 1
        prot = re.search("[A-Z]+\t", line)[0].strip()
        rna = re.search("\t[A-Z]+\t", line)[0].strip()

        # Setting up call for RPIEmbeddor
        process = subprocess.Popen(rpi_embeddor, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd="RPIEmbeddor-main/rpi-main", text=True)
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
f = open(out_dir + "/" + output_file, "w")
f.write(result_table)
f.close()


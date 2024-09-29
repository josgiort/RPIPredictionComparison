import re
import sys

# Please name this file "result_table.txt"
input_file = sys.argv[1]

correct_predictions = 0
number_datapoints = 0
with open(input_file) as file:
    for line in file:
        ground_truth = re.findall("\tTrue\t|\tFalse\t", line)[0].strip()
        prediction = re.search("\tTrue$|\tFalse$", line)[0].strip()
        if  ground_truth == prediction:
            correct_predictions += 1
        number_datapoints += 1
accuracy = correct_predictions / number_datapoints
print(accuracy)

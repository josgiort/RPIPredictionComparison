from sklearn import metrics
import re
import matplotlib.pyplot as plt


gnd_truth = []
prediction = []
with open('result_table.txt', 'r') as file:
    for line in file:
        current_gnd_truth = re.findall("\tFalse|True\t", line)
        current_prediction = re.findall("\tFalse|True$", line)

        if len(current_gnd_truth) > 0 and len(current_prediction) > 0:
            gnd_truth.append(current_gnd_truth[0].strip())
            prediction.append(current_prediction[0].strip())

correct_predictions = 0

for i in range(len(prediction)):
    if prediction[i] == gnd_truth[i]:
        correct_predictions += 1

accuracy = correct_predictions / len(prediction)

print(accuracy)

#confusion_matrix = metrics.confusion_matrix(gnd_truth, prediction)
#cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = ["False", "True"])
#cm_display.plot()
#plt.show()
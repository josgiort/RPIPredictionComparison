import re
import matplotlib.pyplot as plt
import numpy as np

file1 = open('plot_info_2.txt', 'r')
list_length = []
list_emb_score = []
while True:
    line = file1.readline()
    x = re.findall("\t[0-9]+\t", line)
    y = re.findall("\t[0-9]+,[0-9]+(?:e-[0-9][0-9])?\t", line)
    # Verify if length is exactly 1 in both regex to maintain proper correspondence between lengths and scores
    if len(x) == 1 and len(y) == 1:
        x = x[0].strip()
        list_length.append(int(x))
        y = y[0].strip()
        list_emb_score.append(float(y.replace(',', '.')))
    #else:
        # print("some strange behavior in text file, check it!")
        # exit(0)
    if not line:
        break
file1.close()

x = list_length
y = list_emb_score

coefficients = np.polyfit(x, y, 1)
regression_line = np.poly1d(coefficients)

plt.scatter(x, y,  s=14, alpha=1.0, edgecolors="k")
plt.plot(x, regression_line(x))
plt. axhline(y=0.5, color='r', linestyle='--', linewidth=1)
plt.xticks(range(0,1023,50), range(0,1023,50), rotation=35)
#plt.xticks(range(0,76,4), range(0,76,4), rotation=75)
#plt.xticks(range(0,860,30), range(0,860,30), rotation=35)

plt.xlabel('RNA length segment')
plt.ylabel('Interaction probability')
plt.title("Interaction prediction")
plt.legend()
plt.show()
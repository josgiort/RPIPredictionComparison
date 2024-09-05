import re

file1 = open('chart_info_2.txt', 'r')
count = 0
list_length = []
list_emb_score = []

while True:
    #count += 1

    line = file1.readline()
    x = re.findall("\t[0-9]+\t", line)
    y = re.findall("\t[0-9]+,[0-9]+(?:e-[0-9][0-9])?\t", line)
    # Verify if length is exactly 1 in both regex to maintain proper correspondence between lengths and scores
    if len(x) == 1 and len(y) == 1:
        x = x[0].strip()
        list_length.append(x)
        y = y[0].strip()
        list_emb_score.append(y)
    #else:
        # print("some strange behavior in text file, check it!")
        # exit(0)

    if not line:
        break
    #print("Line{}: {}".format(count, line.strip()))

file1.close()

for i in range(0, len(list_length)):
    print("length: " + list_length[i] + ", emb score: " + list_emb_score[i])


#line = "seq1:1185-1215  30  8,452065230812877e-06   negative"
#line = "seq1:1185-1215  30  8,452065230812877   negative"

#y = re.findall(" [0-9]+,[0-9]+(?:e-[0-9][0-9])? ", line)
#print(y)
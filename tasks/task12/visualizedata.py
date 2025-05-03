import csv
import numpy as np
import matplotlib.pyplot as plt

with open('tasks/task12/results.csv', mode='r', encoding='utf-8') as file:
    csvReader = csv.reader(file)
    header = next(csvReader)
    data = []
    for row in csvReader:
        row = [float(x) for x in row]
        data.append(row)

data = np.array(data)

avgVals = data[:, 1]
stdVals = data[:, 2]
over18Vals = data[:, 3]
below15Vals = data[:, 4]

# plots histogram
plt.hist(avgVals, bins=50, edgecolor='black')
plt.xlabel('Average temperature')
plt.ylabel('Frequency')
#plt.show()


avgMeanTemp = np.average(avgVals)
stdMeanTemp = np.average(stdVals)
noBuildingsOver18 = np.sum(over18Vals >= 50)
noBuildingsBelow15 = np.sum(below15Vals >= 50)

print(f"Average mean temperature = {avgMeanTemp}")
print(f"Standard deviation of mean temperatures = {stdMeanTemp}")
print(f"No buildings where >=50% of area was 18C or more = {noBuildingsOver18}")
print(f"No buildings where >=50% of area was 15C or less = {noBuildingsBelow15}")
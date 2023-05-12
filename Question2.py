import numpy as np
import matplotlib.pyplot as plt


cities = ["SuZhou", "NanJing", "NanTong", "WuXi", "ChangZhou"]

discriminantMatrix = np.array([[1, 1/5, 1/5], [5, 1, 1/2], [5, 2, 1]])
eigens = np.linalg.eig(discriminantMatrix)
maxEigenvalue = np.max(eigens[0])
rowAndColumn = np.argwhere(eigens[0] == maxEigenvalue)
maxEigenvector = eigens[1][::-1, rowAndColumn[0]]

RI_LIST = [0, 0.001, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59]
dim = discriminantMatrix.shape[0]
RI = RI_LIST[dim]
CI = (maxEigenvalue - dim) / (dim - 1)
CR = CI / RI
print("CR: " + str(CR))
print("Passed consistency test") if CR < 0.1 else print("Failed to passed consistency test")

Scores = np.array([[48.0, 126.3, 4.8],
                   [51.5, 134.3, 4.9],
                   [27, 118.7, 3.5],
                   [57.2, 97.8, 2.7],
                   [29, 71.6, 2.8]])

sums = np.sum(Scores, axis=0)
weightedScores = Scores / sums.reshape(1, -1)

# Eigenvalue average
eigenvectorWeight = maxEigenvector / sum(maxEigenvector)

# Arithmatic average
arithmaticSums = np.sum(discriminantMatrix, axis=0)
normalizedMatrix = discriminantMatrix / arithmaticSums.reshape(1, -1)
arithmaticWeight = np.sum(normalizedMatrix, axis=1)
arithmaticWeight /= dim
arithmaticWeight = arithmaticWeight[-1::-1]

# Geometric average
prodVector = np.prod(discriminantMatrix, axis=1)
prodVector = np.power(prodVector, 1/dim)
prodSums = np.sum(prodVector, axis=0)
geometricWeight = prodVector / prodSums
geometricWeight = geometricWeight[-1::-1]

weight = (arithmaticWeight + geometricWeight) / 2

finalScores = np.dot(weightedScores, weight)
for i in range(len(finalScores)):
    print('City {:}, Scores {:}'.format(cities[i], finalScores[i]))

plt.figure(figsize=(10, 6))
x = [1, 2, 3, 4, 5]
x_label = cities
plt.bar(x, finalScores, fc='g')
plt.title("Scores given by evaluation model")
plt.xticks(x, x_label)
plt.xlabel("City")
plt.ylabel("Evaluation score")

plt.show()

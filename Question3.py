import numpy as np
import matplotlib.pyplot as plt


cities = ["NanJing", "SuZhou", "WuXi", "ChangZhou", "XuZhou", "NanTong", "LianYunGang",
          "HuaiAn", "YanCheng", "YangZhou", "ZhenJiang", "TaiZhou", "SuQian"]

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

Scores = np.array([[51.5, 134.3, 4.9],
                   [48.6, 126.3, 4.8],
                   [57.2, 97.8, 2.7],
                   [29, 71.6, 2.8],
                   [30.1, 79.6, 2.91],
                   [27, 118.7, 3.5],
                   [12.4, 36.4, 1.32],
                   [13.5, 32.5, 1.34],
                   [16.7, 45.2, 1.72],
                   [20.4, 52.3, 2.01],
                   [14.01, 36.1, 1.401],
                   [14.2, 37.3, 1.412],
                   [9.27, 25.3, 0.965]])

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

sortedScores = sorted(enumerate(finalScores), key=lambda finalScores:finalScores[1], reverse=True)
finalRanking = [finalScores[0] + 1 for finalScores in sortedScores]
realRanking = [1, 2, 3, 6, 4, 5, 10, 8, 11, 12, 9, 7, 13]

plt.figure(figsize=(20, 12))
x = range(1, 14)
x_label = cities

plt.plot(x_label, finalRanking, 's-', color='r', label="Evaluated Ranking")
plt.plot(x_label, realRanking, 's-', color='g', label="Real Ranking")

plt.title("Contrast of the Evaluated Ranking and Real Ranking")
plt.xticks(x, x_label)
plt.xlabel("City")
plt.ylabel("Ranking")
plt.legend(loc="best")

plt.show()

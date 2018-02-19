import sys
sys.path.append("../Basic Functions")
import math
import numpy
import matplotlib.pyplot as plt
from LoadData import LoadDataAndLabel
#from compiler.ast import flatten
#from funcy import flatten
'''
    Let z = x1 * w1 + x2 * w2 + ... xn * wn + b
    If sigmoid(z) < 0.5, the classifition result will be 0. Otherwise, the result will be 1.
'''

def sigmod(x):
    return 1 / (1 + numpy.exp(-x))

def GradAscent(dataArray, labelList, learningRatio, times):
    # In order to calculate the bias b, add x0 = 1 for each sample
    data = [[1.0, line[0], line[1]] for line in dataArray]
    dataMatrix = numpy.mat(data)
    labelMatrix = numpy.mat(labelList).transpose()
    weights = numpy.ones((len(dataArray[0]) + 1, 1))
    for i in range(times):
        y = sigmod(dataMatrix * weights)
        error = labelMatrix - y
        weights = weights + learningRatio * dataMatrix.transpose() * error
    return weights.flatten().tolist()[0]

def ScotGradAscent(dataArray, labelList, learningRatio, times):
    weights = numpy.ones(len(dataArray[0]) + 1)
    for i in range(times):
        for index in range(len(dataArray)):
            data = [1]
            data.extend(dataArray[index])
            data = numpy.array(data)
            label = labelList[index]
            y = sigmod(sum(data * weights))
            error = label - y
            weights = weights + learningRatio * error * data
    return weights

def DrawSplitLineFor2D(dataArray, labelList, weightList, colorList):
    labelCount = len(set(labelList))
    point = [[[], []] for i in range(labelCount)]
    for index in range(len(labelList)):
        label = int(labelList[index])
        data = dataArray[index]
        point[label][0].append(data[0])
        point[label][1].append(data[1])
    
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.scatter(point[0][0], point[0][1], c='red')
    ax.scatter(point[1][0], point[1][1], c='green')

    for i in range(len(weightList)):
        # b + x1 * w1 + x2 * w2 = 0
        x11 = min([item[0] for item in dataArray])
        x21 = (-weightList[i][0] - x11 * weightList[i][1]) / weightList[i][2]
        x12 = max([item[0] for item in dataArray])
        x22 = (-weightList[i][0] - x12 * weightList[i][1]) / weightList[i][2]

        ax.plot([x11, x12], [x21, x22], c=colorList[i])

    plt.show()

def ClassifyByLogistic(inX, weights):
    y = sigmod(sum(inX * weights[1:] + weights[0]))
    if (y > 0.5):
        return 1
    else:
        return 0

if __name__ == '__main__':
    dataArray, labelList = LoadDataAndLabel("Dataset.txt")
    weights1 = GradAscent(dataArray, labelList,0.01, 3)
    weights2 = ScotGradAscent(dataArray, labelList,0.01, 300)
    print(ClassifyByLogistic(numpy.array([1, 10]), weights1))
    DrawSplitLineFor2D(dataArray, labelList, [weights1, weights2], ['yellow', 'blue'])
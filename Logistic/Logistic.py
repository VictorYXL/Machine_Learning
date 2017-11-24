import math
import numpy
import matplotlib.pyplot as plt
#from compiler.ast import flatten
from funcy import flatten
'''
    Let z = x1 * w1 + x2 * w2 + ... xn * wn + b
    If sigmoid(z) < 0.5, the classifition result will be 0. Otherwise, the result will be 1.
'''
def LoadDataset(fileName):
    f = open(fileName, "r")
    dataList = []
    labelList = []
    for line in f.readlines():
        lineArray = line.strip().split()
        numLine = []
        for num in lineArray[:-1]:
            numLine.append(float(num))
        dataList.append(numLine)
        labelList.append(float(lineArray[-1]))
    return {'data': dataList, 'label': labelList}

def sigmod(x):
    return 1 / (1 + numpy.exp(-x))

def GradAscent(dataset, learningRatio, times):
    # In order to calculate the bias b, add x0 = 1 for each sample
    data = [[1.0, line[0], line[1]] for line in dataset['data']]
    dataMatrix = numpy.mat(data)
    labelMatrix = numpy.mat(dataset['label']).transpose()
    weights = numpy.ones((len(dataset['data'][0]) + 1, 1))
    for i in range(times):
        y = sigmod(dataMatrix * weights)
        error = labelMatrix - y
        weights = weights + learningRatio * dataMatrix.transpose() * error
    return list(flatten(weights.tolist()))

def ScotGradAscent(dataset, learningRatio, times):
    weights = numpy.ones(len(dataset['data'][0]) + 1)
    for i in range(times):
        for index in range(len(dataset['data'])):
            data = [1]
            data.extend(dataset['data'][index])
            data = numpy.array(data)
            label = dataset['label'][index]
            y = sigmod(sum(data * weights))
            error = label - y
            weights = weights + learningRatio * error * data
    return weights

def DrawSplitLineFor2D(dataset, weightList, colorList):
    labelCount = len(set(dataset['label']))
    point = [[[], []] for i in range(labelCount)]
    #print numpy.shape(point)
    for index in range(len(dataset['label'])):
        label = int(dataset['label'][index])
        data = dataset['data'][index]
        point[label][0].append(data[0])
        point[label][1].append(data[1])
        #print point
        #print '-------------------------------------'
    
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.scatter(point[0][0], point[0][1], c='red')
    ax.scatter(point[1][0], point[1][1], c='green')

    for i in range(len(weightList)):
        # b + x1 * w1 + x2 * w2 = 0
        x11 = min([item[0] for item in dataset['data']])
        x21 = (-weightList[i][0] - x11 * weightList[i][1]) / weightList[i][2]
        x12 = max([item[0] for item in dataset['data']])
        x22 = (-weightList[i][0] - x12 * weightList[i][1]) / weightList[i][2]

        ax.plot([x11, x12], [x21, x22], c=colorList[i])

    plt.show()



dataset = LoadDataset("Dataset.txt")
weights1 = GradAscent(dataset,0.01, 3)
weights2 = ScotGradAscent(dataset,0.01, 300)
DrawSplitLineFor2D(dataset, [weights1, weights2], ['yellow', 'blue'])
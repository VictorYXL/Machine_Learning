import math
import numpy
import matplotlib.pyplot as plt
from compiler.ast import flatten
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

def GradAscent(dataset,learningRatio, times):
    # In order to calculate the bias b, add x0 = 1 for each sample
    data = [[1.0, line[0], line[1]] for line in dataset['data']]
    dataMatrix = numpy.mat(data)
    labelMatrix = numpy.mat(dataset['label']).transpose()
    weights = numpy.ones((len(dataset['data'][0]) + 1, 1))

    for i in range(times):
        y = sigmod(dataMatrix * weights)
        error = labelMatrix - y
        weights = weights + learningRatio * dataMatrix.transpose() * error
    return flatten(weights.tolist())

def DrawSplitLineFor2D(dataset, weights):
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

    
    # b + x1 * w1 + x2 * w2 = 0
    x11 = min([item[0] for item in dataset['data']])
    x21 = (-weights[0] - x11 * weights[1]) / weights[2]
    x12 = max([item[0] for item in dataset['data']])
    x22 = (-weights[0] - x12 * weights[1]) / weights[2]

    ax.plot([x11, x12], [x21, x22], c='blue')

    plt.show()



dataset = LoadDataset("Dataset.txt")
weights = GradAscent(dataset,0.001, 500)
DrawSplitLineFor2D(dataset, weights)
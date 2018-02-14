# -*- coding: utf-8 -*-
import sys
sys.path.append("../Basic Functions")
from numpy import *
import matplotlib
import matplotlib.pyplot as plt
from KNN import *
from LoadData import LoadData

#测试分类器
def DataClassTest(normMatrix, ranges, minValues, labelList):
    ratio = 0.1
    m = len(labelList)
    #前numToTest个数据做测试，后面的是样本集
    numToTest = int(m * ratio)
    errorCount = 0.0
    for i in range(numToTest):
        classifierResult = Classify0(normMatrix[i, :], normMatrix[numToTest:m, :], labelList[numToTest:m], 3)
        print("class result %d,real answer %d" % (classifierResult, labelList[i]))
        if (classifierResult != labelList[i]):
            errorCount += 1
    print("The error rate:%f" % (errorCount / float(numToTest)))

#绘图
def Plot(dataMatrix, labelList):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(dataMatrix[:, 1],dataMatrix[:, 2])
    ax.scatter(dataMatrix[:, 1],dataMatrix[:, 2], 15.0 * array(labelList), 15.0 * array(labelList))
    plt.show()

def ClassifyPerson(normMatrix, ranges, minValues, labelList):
    resultList = ['Not in all','In small doses','In large doses']
    percentTats = float(input("Percentage of time spent playing video game?"))
    ffMiles = float(input("Frequent flier miles earned per year?"))
    iceCream = float(input("Liters of ice cream consumed per year?"))
    inArray = [ffMiles,percentTats,iceCream]
    classifierResult = Classify0((inArray)/ranges,normMatrix,labelList,3)
    print("You will probably like this person:",resultList[int(classifierResult)-1])

if __name__ == '__main__':
    dataArray,labelList = LoadData('DatingTestSet2.txt')
    dataMatrix = array(dataArray)
    normMatrix,ranges,minValues = AutoNorm(dataMatrix)
    DataClassTest(normMatrix, ranges, minValues, labelList)
    ClassifyPerson(normMatrix, ranges, minValues, labelList)
    Plot(dataMatrix, labelList)




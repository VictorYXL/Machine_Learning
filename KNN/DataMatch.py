# -*- coding: utf-8 -*-
from numpy import *
from kNN import *
import matplotlib
import matplotlib.pyplot as plt
#从文本中读取样本数据 [数据1,数据2,数据3,所属类型]
def eadMatrixFromText(filename):
    #读文件
    fp = open(filename)
    lines = fp.readlines()
    countOfLines = len(lines)

    labels = []
    index = 0
    matrix = zeros((countOfLines,len(lines[0].split('\t'))-1))

    #从文本读取三列数据和一列分类
    for line in lines:
        line = line.strip()
        list = line.split('\t')
        matrix[index] = list[0:len(list)-1]
        labels.append (int(list[-1]))
        index = index + 1
    return matrix,labels
#测试分类器
def dataClassTest():
    ratio = 0.1
    (dataMatrix,dataLabels) = ReadMatrixFromText("datingTestSet2.txt")
    (normalMat,ranges,minValue) = AutoNorm(dataMatrix)
    m = normalMat.shape[0]
    #前numToTest个数据做测试，后面的是样本集
    numToTest = int (m * ratio)
    errorCount = 0.0
    for i in range(numToTest):
        classifierResult = Classify0(normalMat[i,:],normalMat[numToTest:m,:],dataLabels[numToTest:m],3)
        print("class result %d,real answer %d"%(classifierResult,dataLabels[i]))
        if (classifierResult != dataLabels[i]):
            errorCount += 1
    print("The error rate:%f"%(errorCount/float(numToTest)))
#(matrix,labels) = readMatrixFromText("datingTestSet2.txt")
#normMat,ranges,min = autoNorm(matrix)
#print(normMat)

def classifyPerson():
        resultList = ['not in all','in small doses','in large doses']
        percentTats = float(input("percentage of time spent playing video game?"))
        ffMiles = float(input("frequent flier miles earned per year?"))
        iceCream = float(input("liters of ice cream consumed per year?"))
        dataMatrix,dataLabels = ReadMatrixFromText('datingTestSet2.txt')
        normMatrix,ranges,minValues = AutoNorm(dataMatrix)
        inArray = ([ffMiles,percentTats,iceCream])
        classifierResult = Classify0 ((inArray)/ranges,normMatrix,dataLabels,3)
        print("You will probably like this person:",resultList[classifierResult-1])
classifyPerson()
#绘图
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.scatter(matrix[:,1],matrix[:,2])
#ax.scatter(matrix[:,1],matrix[:,2],15.0*array(labels),15.0*array(labels))
#plt.show()

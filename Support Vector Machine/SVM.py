#http://www.cnblogs.com/jerrylead/archive/2011/03/13/1982639.html
import random
import numpy
import matplotlib
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

def smoSimple(dataset, border, toler, maxIter):
    dataMatrix = numpy.mat(dataset['data'])
    labelMatrix = numpy.mat(dataset['label']).T

    dataCount = len(dataMatrix)
    vectorLen = len(dataset['data'][0])
    alphas = numpy.mat(numpy.zeros((dataCount, 1)))
    b = 0
    iter = 0

    while iter < maxIter:
        whetherChanged = False
        for i in range(dataCount):
            Ui = float(numpy.multiply(alphas, labelMatrix).T * (dataMatrix * dataMatrix[i,:].T)) + b
            Ei = Ui - float(labelMatrix[i])
            j = int(random.uniform(0,dataCount))
            while (i == j):
                j = int(random.uniform(0,dataCount))
            if ((labelMatrix[i] * Ei < -toler) and (alphas[i] < border)) or ((labelMatrix[i] * Ei > toler) and (alphas[i] > 0)):
                Uj = float(numpy.multiply(alphas, labelMatrix).T * (dataMatrix * dataMatrix[j,:].T)) + b
                Ej = Uj - float(labelMatrix[j])
                if (labelMatrix[i] == labelMatrix[j]):
                    L = max(0, alphas[j] + alphas[i] - border)
                    H = min(border, alphas[j] + alphas[i])
                else:
                    L = max(0, alphas[j] - alphas[i])
                    H = min(border, border + alphas[j] - alphas[i])
                if (L != H):
                    eta = 2.0 * dataMatrix[i,:] * dataMatrix[j,:].T - dataMatrix[i,:] * dataMatrix[i,:].T - dataMatrix[j,:] * dataMatrix[j,:].T
                    if (eta < 0):
                        newAlphaJ = alphas[j] - labelMatrix[j] * (Ei - Ej) / eta
                        newAlphaI = alphas[i] + labelMatrix[i] * labelMatrix[j] * (newAlphaJ - alphas[j])
                        b1 = b - Ei - labelMatrix[i] * (newAlphaI - alphas[i]) * dataMatrix[i,:] * dataMatrix[i,:].T - labelMatrix[j] * (newAlphaJ - alphas[j]) * dataMatrix[i,:] * dataMatrix[j,:].T
                        b2 = b - Ej - labelMatrix[i] * (newAlphaI - alphas[i]) * dataMatrix[i,:] * dataMatrix[j,:].T - labelMatrix[j] * (newAlphaJ - alphas[j]) * dataMatrix[j,:] * dataMatrix[j,:].T
                        alphas[i] = newAlphaI
                        alphas[j] = newAlphaJ
                        if (0 < alphas[i] and alphas[i] < border):
                            b = b1
                        elif (0 < alphas[j] and alphas[j] < border):
                            b = b2
                        else:
                            b = (b1 + b2) / 2.0
                        whetherChanged = True
                #print (i)
                #print (dataCount)
        if (whetherChanged == False) :
            iter = iter + 1
            print (iter)
    print (b)
    print (alphas)
    return alphas,b
    
dataset = LoadDataset("Dataset.txt")
smoSimple(dataset, 0.6, 0.0001, 100)
#http://www.cnblogs.com/jerrylead/archive/2011/03/13/1982639.html
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
    labelMatrix = numpy.mat(dataset['label'])
    dataCount = len(dataMatrix)
    vectorLen = len(dataset['data'][0])
    alphas = numpy.mat(numpy.zeros((dataCount, 1)))

    for iter in range(maxIter):
        whetherChanged = 0
        for i in range(dataCOunt):
            

    


dataset = LoadDataset("Dataset.txt")
smoSimple(dataset, 0.6, 0.0001, 1000)
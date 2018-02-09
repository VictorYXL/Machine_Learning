from numpy import *

def LoadDataset(fileName):
    file = open(fileName)
    dataArray = []
    labelList = []
    for line in file.readlines():
        data = line.strip().split('\t')
        dataArray.append([float(item) for item in data[:-1]])
        labelList.append(float(data[-1]))
    return dataArray, labelList

# w = (X.T * X)^(-1) * (X.T * Y)
def StandRegres(dataArray, labelList):
    dataMat = mat(dataArray)
    labelMat = mat(labelList)

    if linalg.det(dataMat.T * dataMat) == 0:
        print("No x^(-1)")
        return

    return (dataMat.T * dataMat).I * (dataMat.T * labelMat.T)

dataArray, labelList = LoadDataset('DataSet1.txt')
print(StandRegres(dataArray, labelList))
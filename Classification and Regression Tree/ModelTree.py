import sys
sys.path.append("../Basic Functions")
sys.path.append("../Regression")
from LoadData import LoadDataAndLabel
from Regression import StandRegres, WholeError
import numpy
from Tree import *
from RegressionTree import SplitDataset

def ChooseBestFeature(dataArray, resultList, maxDataCount, minErrorReduce):
    dataCount = len(dataArray)
    if (dataCount == 0):
        return None, None
    elif (dataCount <= maxDataCount):
        #Leaf, record the weight in leaf
        return None, StandRegres(dataArray, resultList)
    featureCount = len(dataArray[0])
    minError = numpy.inf
    bestFeature = 0
    bestValue = dataArray[0][0]
        #Loop for each feature and value to find the best match to reduce the error
    for feature in range(featureCount):
        valueList = [data[feature] for data in dataArray]
        valueSet = set(valueList)
        for value in valueSet:
            subDataArray1, subResultList1, subDataArray2, subResultList2 = SplitDataset(dataArray, resultList, feature, value)
            #Calculate the disorder
            if (len(subDataArray1) != 0):
                error1 = WholeError(subDataArray1, subResultList1)
            else:
                error1 = 0
            if (len(subDataArray2) != 0):
                error2 = WholeError(subDataArray2, subResultList2)
            else:
                error2 = 0
            if (error1 + error2 < minError):
                bestFeature = feature
                bestValue = value
                minError = error1 + error2

    currentError = WholeError(dataArray, resultList)
    if (currentError - minError <= minErrorReduce):
        return None, StandRegres(dataArray, resultList)
    return bestFeature, bestValue

def CreateModelTree(dataArray, resultList, maxDataCount, minErrorReduce):
    feature, value = ChooseBestFeature(dataArray, resultList, maxDataCount, minErrorReduce)
    if feature == None:
        #Leaf
        node = Node(0, value, None, None)
    else:
        subDataArray1, subResultList1, subDataArray2, subResultList2 = SplitDataset(dataArray, resultList, feature, value)
        leftTree = CreateModelTree(subDataArray1, subResultList1, maxDataCount, minErrorReduce)
        rightTree = CreateModelTree(subDataArray2, subResultList2, maxDataCount, minErrorReduce)
        node = Node(feature, value, leftTree, rightTree)
    return node

def ForecastByModelTree(tree, inData):
    if (tree.left == None and tree.right == None):
        return (numpy.mat(inData) * tree.value).tolist()[0][0]
    if (inData[tree.feature] > tree.value):
        return ForecastByModelTree(tree.left, inData)
    else:
        return ForecastByModelTree(tree.right, inData)

if __name__ == '__main__':
    dataArray, resultList = LoadDataAndLabel("Dataset2.txt")
    tree = CreateModelTree(dataArray, resultList, 4, 0.1)
    #ShowTree(tree)
    print(ForecastByModelTree(tree, [0.530897]))
    print(ForecastByModelTree(tree, [0.993349]))
import sys
sys.path.append("../Basic Functions")
from LoadData import LoadDataAndLabel
import numpy
from Tree import *

#Split the dataset by some feature and its value
def SplitDataset(dataArray, resultList, feature, value):
    subDataArray1 = [dataArray[index] for index in range(len(dataArray)) if dataArray[index][feature] > value]
    subResultList1 = [resultList[index] for index in range(len(dataArray)) if dataArray[index][feature] > value]
    subDataArray2 = [dataArray[index] for index in range(len(dataArray)) if dataArray[index][feature] <= value]
    subResultList2 = [resultList[index] for index in range(len(dataArray)) if dataArray[index][feature] <= value]
    return subDataArray1, subResultList1, subDataArray2, subResultList2

def ChooseBestFeature(dataArray, resultList, maxDataCount, minErrorReduce):
    dataCount = len(dataArray)
    if (dataCount == 0):
        return None, None
    elif (dataCount <= maxDataCount):
        #Leaf, use the mean of label to represent the forecast
        return None, numpy.mean(resultList)
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
            #Use variance to description the disorder
            if (len(subDataArray1) > 0):
                error1 = numpy.var(subResultList1) * len(subDataArray1)
            else:
                error1 = 0
            if (len(subDataArray2) > 0):
                error2 = numpy.var(subResultList2) * len(subDataArray2)
            else:
                error2 = 0
            if (error1 + error2 < minError):
                bestFeature = feature
                bestValue = value
                minError = error1 + error2
    if (len(dataArray) > 0):
        currentError = numpy.var(resultList) * len(dataArray)
    else:
        currentError = 0
    if (currentError - minError <= minErrorReduce):
        return None, numpy.mean(resultList)
    return bestFeature, bestValue

#Create tree
#maxDataCount: max count of each subdataset
#minErrorReduce:do not split dataset if the reducement of error is not enough
def CreateRegresTree(dataArray, resultList, maxDataCount, minErrorReduce):
    feature, value = ChooseBestFeature(dataArray, resultList, maxDataCount, minErrorReduce)
    if feature == None:
        #Leaf
        node = Node(0, value, None, None)
    else:
        subDataArray1, subResultList1, subDataArray2, subResultList2 = SplitDataset(dataArray, resultList, feature, value)
        leftTree = CreateRegresTree(subDataArray1, subResultList1, maxDataCount, minErrorReduce)
        rightTree = CreateRegresTree(subDataArray2, subResultList2, maxDataCount, minErrorReduce)
        node = Node(feature, value, leftTree, rightTree)
    return node

def ForecastByRegresTree(tree, inData):
    if (tree.left == None and tree.right == None):
        return tree.value
    if (inData[tree.feature] > tree.value):
        return ForecastByRegresTree(tree.left, inData)
    else:
        return ForecastByRegresTree(tree.right, inData)

if __name__ == '__main__':
    dataArray, resultList = LoadDataAndLabel("Dataset2.txt")
    tree = CreateRegresTree(dataArray, resultList, 4, 0.1)
    #ShowTree(tree)
    print(ForecastByRegresTree(tree, [0.530897]))
    print(ForecastByRegresTree(tree, [0.993349]))
    
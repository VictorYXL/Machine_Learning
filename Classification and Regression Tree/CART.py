import sys
sys.path.append("../Basic Functions")
from LoadData import LoadDataAndLabel
import numpy
class Node():
    def __init__(self, feature, value, left, right):
        self.feature = feature
        self.value = value
        self.left = left
        self.right = right

#Split the dataset by some feature and its value
def SplitDataset(dataArray, labelList, feature, value):
    subDataArray1 = [dataArray[index] for index in range(len(dataArray)) if dataArray[index][feature] > value]
    subLabelList1 = [labelList[index] for index in range(len(dataArray)) if dataArray[index][feature] > value]
    subDataArray2 = [dataArray[index] for index in range(len(dataArray)) if dataArray[index][feature] <= value]
    subLabelList2 = [labelList[index] for index in range(len(dataArray)) if dataArray[index][feature] <= value]
    return subDataArray1, subLabelList1, subDataArray2, subLabelList2

def ChooseBestFeature(dataArray, labelList, maxDataCount, minErrorReduce):
    dataCount = len(dataArray)
    if (dataCount == 0):
        return None, None
    elif (dataCount <= maxDataCount):
        return None, numpy.mean(labelList)
    featureCount = len(dataArray[0])
    minError = numpy.inf
    bestFeature = 0
    bestValue = dataArray[0][0]

    #Loop for each feature and value to find the best match to reduce the error
    for feature in range(featureCount):
        valueList = [data[feature] for data in dataArray]
        valueSet = set(valueList)
        for value in valueSet:
            subDataArray1, subLabelList1, subDataArray2, subLabelList2 = SplitDataset(dataArray, labelList, feature, value)
            if (len(subDataArray1) > 0):
                error1 = numpy.var(subLabelList1) * len(subDataArray1)
            else:
                error1 = 0
            if (len(subDataArray2) > 0):
                error2 = numpy.var(subLabelList2) * len(subDataArray2)
            else:
                error2 = 0
            if (error1 + error2 < minError):
                bestFeature = feature
                bestValue = value
                minError = error1 + error2
    if (len(dataArray) > 0):
        currentError = numpy.var(labelList) * len(dataArray)
    else:
        currentError = 0
    if (currentError - minError <= minErrorReduce):
        return None, numpy.mean(labelList)
    return bestFeature, bestValue

#Create tree
#maxDataCount: max count of each subdataset
#minErrorReduce:do not split dataset if the reducement of error is not enough
def CreateTree(dataArray, labelList, maxDataCount, minErrorReduce):
    feature, value = ChooseBestFeature(dataArray, labelList, maxDataCount, minErrorReduce)
    if feature == None:
        node = Node(0, value, None, None)
    else:
        subDataArray1, subLabelList1, subDataArray2, subLabelList2 = SplitDataset(dataArray, labelList, feature, value)
        leftTree = CreateTree(subDataArray1, subLabelList1, maxDataCount, minErrorReduce)
        rightTree = CreateTree(subDataArray2, subLabelList2, maxDataCount, minErrorReduce)
        node = Node(feature, value, leftTree, rightTree)
    return node



if __name__ == '__main__':
    dataArray, labelList = LoadDataAndLabel("Dataset2.txt")
    tree = CreateTree(dataArray, labelList, 4, 1)
    print(isinstance(tree, Node))
    print(tree.value)
    print(tree.left.value)
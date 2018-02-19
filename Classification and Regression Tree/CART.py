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

def ChooseBestFeature(dataArray, labelList):
    dataCount = len(dataArray)
    if (dataCount == 0):
        return None, None
    elif (dataCount == 1):
        return None, labelList[0]
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
    return bestFeature, bestValue

#Create tree
def CreateTree(dataArray, labelList):
    feature, value = ChooseBestFeature(dataArray, labelList)
    if feature == None:
        node = Node(0, value, None, None)
    else:
        subDataArray1, subLabelList1, subDataArray2, subLabelList2 = SplitDataset(dataArray, labelList, feature, value)
        leftTree = CreateTree(subDataArray1, subLabelList1)
        rightTree = CreateTree(subDataArray2, subLabelList2)
        node = Node(feature, value, leftTree, rightTree)
    return node



if __name__ == '__main__':
    dataArray, labelList = LoadDataAndLabel("Dataset2.txt")
    tree = CreateTree(dataArray, labelList)
    print(tree.value)
    print(tree.left.value)
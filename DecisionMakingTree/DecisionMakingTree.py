# -*- coding: utf-8 -*-
from math import *
import operator
import pickle
#熵是描述数据无序程度的一种度量方式
#计算香农熵，计算公式为H=-sum(p(xi)*log(p(xi))),p(xi)为某类别在总类别中所占比例(该类别概率)
def CalShannonEnt(dataSet):
    numCount = len(dataSet)
    labelCount = {}
    #统计p(xi)
    for featureVec in dataSet:
        curLabel = featureVec[-1]
        if curLabel not in labelCount.keys():
            labelCount[curLabel] = 0
        labelCount[curLabel] += 1

    #计算熵
    shannonEnt = 0.0
    for key in labelCount:
        pxi = float(labelCount[key]) / numCount
        shannonEnt -= pxi * log(pxi, 2)
    return shannonEnt

#以feature == value 划分数据集
def SplitDataset(dataset, feature, value):
    resultDataset = []
    for item in dataset:
        if (item[feature] == value):
            newItem = item.copy()
            del newItem[feature]
            resultDataset.append(newItem)
    return resultDataset

#找到熵最小的划分数据集的方式
def ChooseBestFeatureToSplit(dataset):
    #feature数，其中最后一个为label，故舍去
    featureCount = len(dataset[0]) - 1
    #Shannon初始化为最初的熵，划分后将减小
    minShannonEnt = CalShannonEnt(dataset)
    minFeature = -1
    for i in range(featureCount):
        #获取feature对应的所有value
        values = [item[i] for item in dataset]
        valueSet = set(values)
        shannonEnt = 0
        #计算该feature划分数据集的熵
        for value in valueSet:
            subDataset = SplitDataset(dataset, i, value)
            #计算feature == value 占总数的比例
            prob = 1.0 * len(subDataset) / len(dataset)
            shannonEnt += CalShannonEnt(subDataset) * prob
        if (shannonEnt < minShannonEnt):
            minShannonEnt = shannonEnt
            minFeature = i
    return minFeature

#当相同feature对应不同label时，少数服从多数
def MajorityCnt(labelList):
    labelCount = {}
    for label in labelList:
        if label not in labelCount.keys():
            labelCount[label] = 1
        else:
            labelCount[label] += 1
    #sortedLabelCount = sorted(labelCount.items(), key = operator.itemgetter(1), reverse = True)
    sortedLabelCount = sorted(labelCount.items(), key = lambda x : x[1], reverse = True)
    return sortedLabelCount[0][0]

#构造决策树，用字典存储
#tree = {'feature0': {'value0': 'label0', 'value1': {another node}}}
def CreateDecisionTreeWithFeatureName(dataset, featureName):
    #当所有样本都属于一个类，划分结束，输出该标签
    classList = [item[-1] for item in dataset]
    if (len(set(classList)) == 1):
        return classList[0]
    #当样本只剩下标签列，划分结束，输出最多标签
    if (len(dataset[0]) == 1):
        return MajorityCnt(classList)

    #选出最优特征，并以此划分数据集
    bestFeature = ChooseBestFeatureToSplit(dataset)
    bestFeatureName = featureName[bestFeature]
    decTree = {bestFeatureName:{}}
    featureName.remove(bestFeatureName)
    featureValueList = [item[bestFeature] for item in dataset]
    featureValueSet = set(featureValueList)
    for featureValue in featureValueSet:
        subDataset = SplitDataset(dataset, bestFeature, featureValue)
        decTree[bestFeatureName][featureValue] = CreateDecisionTreeWithFeatureName(subDataset, featureName)
    return decTree
def CreateDecisionTree(dataset):
    featureName = list (range(len(dataset[0]) - 1))
    return CreateDecisionTreeWithFeatureName(dataset, featureName)

#通过决策树分类
def ClassifyByDT(DecisitionTree, featureVector):
    classLabel = None
    featureIndex = 0
    currentTree = DecisitionTree
    #尝试获取标签
    for featureIndex in range(len(featureVector)):
        #获取第featureIndex个特征
        featureValue = featureVector[featureIndex]
        if (featureValue in currentTree[featureIndex].keys()):
            #找到该特征对应值，在树中的位置，如果是树则继续判断，如果是叶则结束判断返回标签
            if (type(currentTree[featureIndex][featureValue]).__name__ == 'dict'):
                currentTree = currentTree[featureIndex][featureValue]
            else:
                classLabel = currentTree[featureIndex][featureValue]
        else:
            return None
    return classLabel

#决策树的存储和读取
def StoreTree(decTree, fileName):
    fw = open(fileName, 'wb')
    #dump直接导出到文件，dumps导出到字符串
    pickle.dump(decTree, fw)
    fw.close()

def LoadTree(fileName):
    fr = open(fileName, 'rb')
    decTree = pickle.load(fr)
    fr.close()
    return decTree
if __name__ == '__main__':
    dataset = \
        [
            [1, 1, 'yes'],
            [1, 1, 'yes'],
            [1, 0, 'no'],
            [0, 1, 'no'],
            [0, 1, 'no']
        ]

    #类别越多，熵越大，如将第一个类别改为maybe，熵会增大
    #print(CalShannonEnt(dataset))
    #print(CreateDecisionTree([['yes'], ['yes'], ['no'], ['no'], ['no']]))
    decTree = CreateDecisionTree(dataset)
    print(ClassifyByDT(decTree, [1, 1]))
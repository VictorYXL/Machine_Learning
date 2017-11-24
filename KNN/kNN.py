# -*- coding: utf-8 -*-
from numpy import *
import operator
#归一化数据
def AutoNorm(dataset):
    min = dataset.min(0)
    max = dataset.max(0)
    ranges = max - min
    normDataset = zeros(shape(dataset))
    l = dataset.shape[0]
    normDataset = (dataset - tile(min,(l,1))) / tile(ranges,(l,1))
    return normDataset,ranges,min

#k邻近算法 inX 待分类向量 dataSet训练样本 labels标签 k 最邻近的k个数据
def Classify0(inX,dataSet,labels,k):
    #计算inX到样本每个点的距离 d = sqrt ((Xa0-Xb0)^2+(Xa1-Xb1)^2+ ...+(Xan-Xbn)^2)
    dataSetSize = dataSet.shape[0] # shape 维度，shape[0]第一个维度，行数
    intMat = tile (inX,(dataSetSize,1))  #tile 复制，把inX纵向复制dataSetSize次，横向复制1次
    diffMat =intMat - dataSet
    sqDiffMat = diffMat ** 2 # **乘方
    sqDistance = sqDiffMat.sum(axis=1) #横向求和
    distances = sqDistance ** 0.5 #开方求距离

    #排序
    sortedDisIndicies = distances.argsort() #升序排序，记录索引

    #选k个距离最短的点
    classCount = {} #字典，内容为   标签:次数
    for i in range (k):
        voteIlabel = labels[sortedDisIndicies[i]] #获取标签内容
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1 #当前标签次数+1

    #以次数降序排序
    #items() 以列表形式返回字典[(key1,value1),(key2,value2)..]
    #key=operator.itemgetter(1) 定义函数key，获取对象的第一个值
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True) #sorted 对副本排序

    #返回次数最多的label
    return sortedClassCount[0][0]

#测试：默认训练集四个数据，两个属性
#group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
#labels = ['A','A','B','B']
#print(classify0([0,0],group,labels,2))
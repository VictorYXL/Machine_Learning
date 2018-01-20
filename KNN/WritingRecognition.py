__author__ = 'Yang'
from numpy import *
from kNN import *
import os, sys
def img2vector (filename):
    vector = zeros((1,1024))
    fr = open (filename)
    for i in range(32):
        line = fr.readline()
        for j in range(32):
            vector [0,32*i+j] = int(line[j])
    return vector
def handwritingRecognition():
    #Read dir
    hwLabels= []
    trainingFileList = os.listdir('trainingDigits')
    trainMatrix = zeros((len(trainingFileList),1024))

    for i in range (len(trainingFileList)):
        #获取文件名与对应数字
        fileName = trainingFileList[i]
        numStr = fileName.split('_')[0]
        #添加标签
        hwLabels.append(numStr)
        #获取所有训练样本
        trainMatrix[i,:] = img2vector('trainingDigits/%s'%fileName)
    #获取测试数据
    testFileName = 'testDigits/test.txt'
    testVector = img2vector(testFileName)
    result = Classify0(testVector,trainMatrix,hwLabels,3)
    print (result)
handwritingRecognition()

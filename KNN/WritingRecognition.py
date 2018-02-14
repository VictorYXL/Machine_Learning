import os, sys
from numpy import *
from KNN import *

def Img2Vector (filename):
    vector = zeros((1,1024))
    fr = open (filename)
    for i in range(32):
        line = fr.readline()
        for j in range(32):
            vector [0,32*i+j] = int(line[j])
    return vector

def HandwritingRecognition():
    #Read dir
    hwLabels= []
    trainingFileList = os.listdir('TrainingDigits')
    trainMatrix = zeros((len(trainingFileList),1024))

    for i in range (len(trainingFileList)):
        #获取文件名与对应数字
        fileName = trainingFileList[i]
        numStr = fileName.split('_')[0]
        #添加标签
        hwLabels.append(numStr)
        #获取所有训练样本
        trainMatrix[i,:] = Img2Vector('TrainingDigits/%s'%fileName)
    #获取测试数据
    testFileName = 'TestDigits/test.txt'
    testVector = Img2Vector(testFileName)
    result = Classify0(testVector,trainMatrix,hwLabels,3)
    print (result)
    
if __name__ == '__main__':
    HandwritingRecognition()

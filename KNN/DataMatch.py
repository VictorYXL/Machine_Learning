from numpy import *
import matplotlib
import matplotlib.pyplot as plt
#从文本中读取样本数据 [数据1,数据2,数据3,所属类型]
def readMatrixFromText(filename):
    #读文件
    fp = open(filename)
    lines = fp.readlines()
    countOfLines = len(lines)

    labels = []
    index = 0
    matrix = zeros((countOfLines,len(lines[0].split('\t'))-1))

    #从文本读取三列数据和一列分类
    for line in lines:
        line = line.strip()
        list = line.split('\t')
        matrix[index] = list[0:len(list)-1]
        labels.append (list[-1])
        index = index + 1
        #print (line)
    return matrix,labels
(matrix,labels) = readMatrixFromText("datingTestSet2.txt")
#print (matrix)
#print (labels)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(matrix[:,1],matrix[:,2])
plt.show()

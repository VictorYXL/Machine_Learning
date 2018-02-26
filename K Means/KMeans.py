import sys
sys.path.append("../Basic Functions")
from LoadData import LoadData
import numpy
import matplotlib.pyplot
import random

#Calculate the distance
def Distance(vec1 ,vec2):
    return ((vec1 - vec2) * (vec1 - vec2).T)[0,0]

#Create k center points
def CreateCenter(dataArray, k):
    featureCount = len(dataArray[0])
    dataMat = numpy.mat(dataArray)
    centerPointMat = numpy.zeros((k, featureCount))

    for i in range(featureCount):
        minI = min(dataMat[:, i])
        maxI = max(dataMat[:, i])
        for j in range(k):
            centerPointMat[j, i] = random.uniform(minI, maxI)
    return centerPointMat

#K-Means cluster
def KMeans(centerPointMat, dataArray):
    dataCount = len(dataArray)
    featureCount = len(dataArray[0])
    dataMat = numpy.mat(dataArray)
    #Record the Cluster Assment and each distance as: clusterAssment[data_index] = [belonged_cluster, distance]
    clusterAssment = [[0, 0] for i in range(dataCount)]
    whetherChanged = True

    while whetherChanged:
        whetherChanged = False
        for (index, data) in enumerate(dataMat):
            DistanceList = [Distance(data, centerPoint) for centerPoint in centerPointMat]
            #Find min distance and use its index as new cluster
            newDis = min(DistanceList)
            newCluster = DistanceList.index(newDis)
            if (clusterAssment[index][0] != newCluster):
                whetherChanged = True
                #Update the assment
                clusterAssment[index][0] = newCluster
                clusterAssment[index][1] = newDis
                #Update the cluster
                dataInCluster = [dataMat[index] for index in range(dataCount) if clusterAssment[index][0] == newCluster]
                centerPointMat[newCluster] = numpy.mean(dataInCluster, 0)
    return clusterAssment

def Plot(dataArray, centerPointMat, clusterAssment):
    fig = matplotlib.pyplot.figure()
    ax = matplotlib.pyplot.subplot(111)
    color = ['blue', 'red', 'yellow', 'black', 'gray', 'green', 'gray']

    for i in range(len(centerPointMat)):
        X = [data[0] for (index, data) in enumerate(dataArray) if clusterAssment[index][0] == i]
        Y = [data[1] for (index, data) in enumerate(dataArray) if clusterAssment[index][0] == i]
        ax.scatter(X, Y, c = color[i])
        ax.scatter(centerPointMat[i, 0], centerPointMat[i, 1], c = color[i], marker = 'x')
    matplotlib.pyplot.show()




if __name__ == '__main__':
    dataArray = LoadData("Dataset.txt")
    centerPointMat = CreateCenter(dataArray, 4)
    clusterAssment = KMeans(centerPointMat, dataArray)
    print(centerPointMat)
    Plot(dataArray, centerPointMat, clusterAssment)

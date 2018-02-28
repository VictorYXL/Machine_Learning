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
def CreateCluster(dataArray, k):
    featureCount = len(dataArray[0])
    dataMat = numpy.mat(dataArray)
    clusterPointMat = numpy.zeros((k, featureCount))

    for i in range(featureCount):
        minI = min(dataMat[:, i])
        maxI = max(dataMat[:, i])
        for j in range(k):
            clusterPointMat[j, i] = random.uniform(minI, maxI)
    return clusterPointMat

#K-Means cluster
def KMeans(dataArray, clusterPointMat):
    dataCount = len(dataArray)
    featureCount = len(dataArray[0])
    dataMat = numpy.mat(dataArray)
    #Init assement
    clusterAssement = [[] for i in range(len(clusterPointMat))]
    clusterAssement[0] = [i for i in range(dataCount)]
    whetherChanged = True

    while whetherChanged:
        whetherChanged = False
        for (index, data) in enumerate(dataMat):
            DistanceList = [Distance(data, centerPoint) for centerPoint in clusterPointMat]
            #Find min distance and use its index as new cluster
            newDis = min(DistanceList)
            newCluster = DistanceList.index(newDis)

            if index not in clusterAssement[newCluster]:
                whetherChanged = True
                #Update the assment
                for assement in clusterAssement:
                    if index in assement:
                        assement.remove(index)
                        break
                clusterAssement[newCluster].append(index)
                #Update the cluster
                dataInCluster = [dataMat[index] for index in clusterAssement[newCluster]]
                clusterPointMat[newCluster] = numpy.mean(dataInCluster, 0)
    return clusterAssement

#Binary K-Means
def BinKMeans(dataArray, k):
    dataCount = len(dataArray)
    featureCount = len(dataArray[0])
    dataMat = numpy.mat(dataArray)
    #Init cluster and assement
    clusterAssement = [[] for i in range(k)]
    clusterAssement[0] = [i for i in range(dataCount)]
    clusterPointMat = numpy.zeros((k, featureCount))
    clusterPointMat[0, :] = numpy.mean(dataMat, axis = 0)
    
    
    #Split k - 1 times 
    for times in range(1, k):
        maxErrorReduce = -numpy.inf
        for clusterIndex in range(times):
            dataInCluster = [dataArray[index] for index in clusterAssement[clusterIndex]]
            if len(dataInCluster) != 0:
                newClusterPointMat = CreateCluster(dataInCluster, 2)
                newClusterAssement = KMeans(dataInCluster, newClusterPointMat)
                notSplitError = clusterError(dataInCluster, clusterPointMat, clusterAssement, clusterIndex)
                splitError1 = clusterError(dataInCluster, newClusterPointMat, newClusterAssement, 0)
                splitError2 = clusterError(dataInCluster, newClusterPointMat, newClusterAssement, 1)
                if (notSplitError - splitError1 - splitError2 > maxErrorReduce):
                    maxErrorReduce = notSplitError - splitError1 - splitError2
                    这个分裂的过程暂时没想好怎么写。
                return 





def clusterError(dataArray, clusterPointMat, clusterAssement, clusterIndex):
    dataInCluster = [dataArray[index] for index in clusterAssement[clusterIndex]]
    dataInClusterMat = numpy.mat(dataInCluster)
    distanceMat = dataInClusterMat - clusterPointMat[clusterIndex]
    errorSum = numpy.sum(numpy.multiply(distanceMat, distanceMat))
    return errorSum


def Plot(dataArray, clusterPointMat, clusterAssement):
    fig = matplotlib.pyplot.figure()
    ax = matplotlib.pyplot.subplot(111)
    color = ['blue', 'red', 'yellow', 'black', 'gray', 'green', 'gray']

    for i in range(len(clusterPointMat)):
        X = [dataArray[index][0] for index in clusterAssement[i]]
        Y = [dataArray[index][1] for index in clusterAssement[i]]
        ax.scatter(X, Y, c = color[i])
        ax.scatter(clusterPointMat[i, 0], clusterPointMat[i, 1], c = color[i], marker = 'x')
    matplotlib.pyplot.show()




if __name__ == '__main__':
    dataArray = LoadData("Dataset.txt")
    #clusterPointMat = CreateCluster(dataArray, 4)
    #clusterAssement = KMeans(dataArray, clusterPointMat)
    #Plot(dataArray, clusterPointMat, clusterAssement)
    BinKMeans(dataArray, 4)
    #print(clusterPointMat)
    #print(clusterError(dataArray, clusterPointMat, clusterAssement, 0))

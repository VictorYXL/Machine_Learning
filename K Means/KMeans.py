import sys
sys.path.append("../Basic Functions")
import numpy
import matplotlib.pyplot
import random
from LoadData import LoadData

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

    if k > dataCount:
        return None

    dataMat = numpy.mat(dataArray)
    #Init cluster and assement
    clusterAssement = [[] for i in range(k)]
    clusterAssement[0] = [i for i in range(dataCount)]
    clusterPointMat = numpy.zeros((k, featureCount))
    clusterPointMat[0, :] = numpy.mean(dataMat, axis = 0)
    
    
    #Split k - 1 times 
    for times in range(1, k):
        maxErrorReduce = 0
        #Find the best to split
        for clusterIndex in range(times):
            dataInCluster = [dataArray[index] for index in clusterAssement[clusterIndex]]
            if len(dataInCluster) >= 2:
                #Make sure split is successful
                while maxErrorReduce == 0:
                    newClusterPointMat = CreateCluster(dataInCluster, 2)
                    newClusterAssement = KMeans(dataInCluster, newClusterPointMat)
                    notSplitError = clusterError(dataArray, clusterPointMat, clusterAssement, clusterIndex)
                    splitError1 = clusterError(dataInCluster, newClusterPointMat, newClusterAssement, 0)
                    splitError2 = clusterError(dataInCluster, newClusterPointMat, newClusterAssement, 1)
                    #Choose
                    if (notSplitError - splitError1 - splitError2 > maxErrorReduce):
                        maxErrorReduce = notSplitError - splitError1 - splitError2
                        clusterToSplit = clusterIndex
                        splitPointMat = newClusterPointMat
                        bestAssement = newClusterAssement
        #Split
        clusterPointMat[clusterToSplit, :] = splitPointMat[0, :]
        clusterPointMat[times, :] = splitPointMat[1, :]
        oldAssement = clusterAssement[clusterToSplit].copy()
        clusterAssement[clusterToSplit] = [oldAssement[index] for index in bestAssement[0]]
        clusterAssement[times] = [oldAssement[index] for index in bestAssement[1]]
        print(clusterPointMat)
    return clusterPointMat, clusterAssement

def clusterError(dataArray, clusterPointMat, clusterAssement, clusterIndex):
    dataInCluster = [dataArray[index] for index in clusterAssement[clusterIndex]]
    #Make sure the result is count
    if len(dataInCluster) == 0:
        return 0
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
    clusterPointMat, clusterAssement = BinKMeans(dataArray, 4)
    print(clusterPointMat)
    print(clusterAssement)
    #print(clusterError(dataArray, clusterPointMat, clusterAssement, 0))

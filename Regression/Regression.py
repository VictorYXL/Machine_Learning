import sys
sys.path.append("../Basic Functions")
import numpy 
import matplotlib.pyplot
from LoadData import LoadData

# w = (X.T * X)^(-1) * (X.T * Y)
def StandRegres(dataArray, labelList):
    dataMat = numpy.mat(dataArray)
    labelMat = numpy.mat(labelList)
    dataMat = (dataMat - numpy.mean(dataMat, 0)) / numpy.var(dataMat, 0)
    labelMat = labelMat - numpy.mean(labelMat)

    if numpy.linalg.det(dataMat.T * dataMat) == 0:
        print("No x^(-1)")
        return
    return (dataMat.T * dataMat).I * (dataMat.T * labelMat.T)

# w = (X.T * X)^(-1) * (X.T * Y)
def LocalWeightLinearRegress(testX, dataArray, labelList, k = 1.0):
    dataMat = numpy.mat(dataArray)
    labelMat = numpy.mat(labelList)
    dataMat = (dataMat - numpy.mean(dataMat, 0)) / numpy.var(dataMat, 0)
    labelMat = labelMat - numpy.mean(labelMat)
    weight = numpy.zeros((len(dataArray), len(dataArray)))

    for i in range(len(dataArray)):
        weight[i, i] = numpy.exp((testX - dataMat[i, :]) * (testX - dataMat[i, :]).T / (-2 * k ** 2))

    if numpy.linalg.det(dataMat.T * dataMat) == 0:
        print("No x^(-1)")
        return
    return numpy.mat(testX) * (dataMat.T * (weight * dataMat)).I * (dataMat.T * (weight * labelMat.T)) 


# w = (X.T * X + lam * I)^(-1) * (X.T * Y)
def RidgeRegres(dataArray, labelList, lam = 0.2):
    dataMat = numpy.mat(dataArray)
    labelMat = numpy.mat(labelList)
    dataMat = (dataMat - numpy.mean(dataMat, 0)) / numpy.var(dataMat, 0)
    labelMat = labelMat - numpy.mean(labelMat)
    I = numpy.eye(numpy.shape(dataMat)[1])

    if numpy.linalg.det(dataMat.T * dataMat + lam * I) == 0:
        print("No x^(-1)")
        return
    return (dataMat.T * dataMat + lam * I).I * (dataMat.T * labelMat.T)

def StageWise(dataArray, labelList, esp = 0.01, numIt = 1000):
    dataMat = numpy.mat(dataArray)
    labelMat = numpy.mat(labelList)
    dataMat = (dataMat - numpy.mean(dataMat, 0)) / numpy.var(dataMat, 0)
    labelMat = labelMat - numpy.mean(labelMat)

    w = numpy.zeros((1, len(dataArray[0])))
    minError = numpy.inf

    #Iteration times
    for i in range(numIt):
        #Modify weight
        for j in range(len(dataArray[0])):
            #Add or substract
            for k in [-1, 1]:
                newW = w.copy()
                newW[0, j] += k * esp
                predLabel = dataMat * newW.T
                predError = RegError(labelList, predLabel.flatten().tolist()[0])
                #New best weight
                if (predError < minError):
                    minError = predError
                    w = newW.copy()
                    print(w, minError)
    return w

def RegError(labelList, predLabelList):
    diffList = [(labelList[i] - predLabelList[i]) ** 2 for i in range(len(labelList))]
    return sum(diffList)

#scatter: point, scatter(x array, y array)
#plot: line, plot([x0, x1, x2], [y0, y1, y2])
def Plot(X, Y, w, LWLRPredY):
    fig = matplotlib.pyplot.figure()
    ax = matplotlib.pyplot.subplot(111)
    ax.scatter(X, Y, c = 'blue')
    #ax.scatter(X, LWLRPredY, c = 'green')
    
    x1 = min(X)
    y1 = w[0] + x1 * w[1]
    x2 = max(X)
    y2 = w[0] + x2 * w[1]
    ax.plot([x1, x2], [y1, y2], 'r-')

    sortedXIndex = numpy.argsort(X)
    for index in range(len(X) - 1):
        ax.plot([X[sortedXIndex[index]], X[sortedXIndex[index + 1]]], [LWLRPredY[sortedXIndex[index]], LWLRPredY[sortedXIndex[index + 1]]], 'g--')
    matplotlib.pyplot.show()

if __name__ == '__main__':
    #dataArray, labelList = LoadData('Dataset1.txt')
    dataArray, labelList = LoadData('Dataset2.txt')

    print(StageWise(dataArray, labelList, esp = 0.001, numIt = 10000))
    print(StandRegres(dataArray, labelList))

    # w = StandRegres(dataArray, labelList)
    # StandPredY = [(w[0] + dataArray[i][1] * w[1]).tolist()[0][0] for i in range(len(dataArray))]
    # LWLRPredY = [LocalWeightLinearRegress(data, dataArray, labelList, 0.01).tolist()[0][0] for data in dataArray]
    # w1 = RidgeRegres(dataArray, labelList)
    # RidgePredY = [(w1[0] + dataArray[i][1] * w1[1]).tolist()[0][0] for i in range(len(dataArray))]
    # x = [i[1] for i in dataArray]
    # Plot(x, labelList, w.flatten().A[0], LWLRPredY)
    # print(RegError(labelList, StandPredY))
    # print(RegError(labelList, RidgePredY))
    # print(RegError(labelList, LWLRPredY))
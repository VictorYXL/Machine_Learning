import numpy 
import matplotlib.pyplot

def LoadDataset(fileName):
    file = open(fileName)
    dataArray = []
    labelList = []
    for line in file.readlines():
        data = line.strip().split('\t')
        dataArray.append([float(item) for item in data[:-1]])
        labelList.append(float(data[-1]))
    return dataArray, labelList

# w = (X.T * X)^(-1) * (X.T * Y)
def StandRegres(dataArray, labelList):
    dataMat = numpy.mat(dataArray)
    labelMat = numpy.mat(labelList)

    if numpy.linalg.det(dataMat.T * dataMat) == 0:
        print("No x^(-1)")
        return
    return (dataMat.T * dataMat).I * (dataMat.T * labelMat.T)

#scatter: point, scatter(x array, y array)
#plot: line, plot([x0, x1, x2], [y0, y1, y2])

def Plot(x, y, w):
    fig = matplotlib.pyplot.figure()
    ax = matplotlib.pyplot.subplot(111)
    ax.scatter(x, y, c = 'blue')
    
    x1 = min(x)
    y1 = w[0] + x1 * w[1]
    x2 = max(x)
    y2 = w[0] + x2 * w[1]
    ax.plot([x1, x2], [y1, y2], 'r-')

    matplotlib.pyplot.show()

dataArray, labelList = LoadDataset('DataSet1.txt')
w = StandRegres(dataArray, labelList)
x = [i[1] for i in dataArray]
Plot(x, labelList, w.flatten().A[0])
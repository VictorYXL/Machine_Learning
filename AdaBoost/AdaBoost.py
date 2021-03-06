import numpy
import matplotlib.pyplot
def LoadData():
    dataArray = \
    [
        [1.0, 2.1],
        [2.0, 1.1],
        [1.3, 1.0],
        [1.0, 1.0],
        [2.0, 1.0]
    ]
    labelList = [1.0, 1.0, -1.0, -1.0, 1.0]
    return dataArray, labelList 

#Pretict from dataArray[:][dimen] by threshVal, threshIneq
def StumpClassify(dataArray, dimen, threshVal, threshIneq):
    retArray = []
    tmplist = [dataArray[i][dimen] for i in range(len(dataArray))]
    for data in tmplist:
        if (threshIneq == 'lt'):
            if (data <= threshVal):
                retArray.append(1.0)
            else:
                retArray.append(-1.0)
        elif (threshIneq == 'gt'):
            if (data > threshVal):
                retArray.append(1.0)
            else:
                retArray.append(-1.0)
    return retArray

def BuildStump(dataArray, labelList, weight):
    dataMatrix = numpy.mat(dataArray)
    labelMatrix = numpy.mat(labelList).T
    dataCount = len(dataArray)
    featureCount = len(dataArray[0])
    numCount = 10   #Set to 10 to reduce the time for training
    bestClassifier = {}
    bestClassEst = numpy.zeros((dataCount, 1))
    minError = numpy.inf
    

    #Loop 1: Feature
    for featureIndex in range(featureCount):
        tmplist = [dataArray[i][featureIndex] for i in range(len(dataArray))]
        rangeMin = min(tmplist)
        rangeMax = max(tmplist)
        numStep = (rangeMax - rangeMin) / numCount
        #Loop 2: Thresh
        for threshVal in numpy.arange(rangeMin, rangeMax + numStep, numStep):
            #Loop 3:Operator
            for operator in ['lt', 'gt']:
                predictedValues = StumpClassify(dataArray, featureIndex, threshVal, operator)
                errorList = []
                #Error lost
                for i in range(len (labelList)):
                    if predictedValues[i] == labelList[i]:
                        errorList.append(0)
                    else:
                        errorList.append(1)
                errorSum = [errorList[i] * weight[i] for i in range(dataCount)]
                weightedError = sum(errorSum)
                
                #Find min error
                if (weightedError < minError):
                    minError = weightedError
                    bestClassEst = predictedValues.copy()
                    bestClassifier['feature'] = featureIndex
                    bestClassifier['thresh'] = threshVal
                    bestClassifier['operator'] = operator
    return bestClassifier, minError, bestClassEst

def AdaboostTrain(dataArray, labelList, maxIter):
    dataCount = len(dataArray)
    featureCount = len(dataArray[0])
    weight = [1.0 / dataCount] * dataCount
    totalPredictValue = [0] * dataCount
    classifierList = []

    for i in range(maxIter):
        #Weak stump
        classifier, error, predictValue = BuildStump(dataArray, labelList, weight)
        if (error == 0):
            error = 0.000001
        alpha = float(0.5 * numpy.log((1.0 - error) / error))
        classifier['alpha'] = alpha
        #Update stump list
        classifierList.append(classifier)

        #Update the weight
        for i in range(len(weight)):
            if (predictValue[i] == labelList[i]):
                weight[i] = weight[i] * numpy.exp(-1.0 * alpha)
            else:
                weight[i] = weight[i] * numpy.exp(alpha)
        weightSum = sum(weight)
        weight = weight / weightSum

        #Stop when classify all the dataset
        totalPredictValue = [totalPredictValue[i] + predictValue[i] * alpha for i in range(dataCount)]
        allCorrect = True
        for i in range(dataCount):
            if (numpy.sign(totalPredictValue[i]) != numpy.sign(labelList[i])):
                allCorrect = False
        if (allCorrect == True):
            break
    #print(totalPredictValue)
    return classifierList, totalPredictValue

#Draw ROC with label and predict strength (confidence)
def PlotROC(labelList, predStrengthList):
    x = 1.0
    y = 1.0
    AUC = 0.0   #Area of ROC
    posCount = sum([i for i in labelList if i == 1.0])      #TP + FN
    nagCount = sum([-i for i in labelList if i == -1.0])    #FP + TN

    sortedPredStrengthIndex = numpy.argsort(predStrengthList)

    fig = matplotlib.pyplot.figure()
    ax = matplotlib.pyplot.subplot(111)
    for index in sortedPredStrengthIndex:
        label = labelList[index]
        ox = x
        oy = y
        if (label == 1.0):
            y = y - 1.0 / posCount
        else:
            x = x - 1.0 / nagCount
            AUC = AUC + y * (1.0 / nagCount)
        ax.plot([ox, x], [oy, y], 'b--')
    matplotlib.pyplot.xlabel('FPR = FP / (FP + TN)')
    matplotlib.pyplot.ylabel('TPR = TP / (TP + FN)')
    matplotlib.pyplot.show()
    return AUC


#Classify
def AdaClassify(inputFeature, classifierList):
    totalPredict = [0] * len(inputFeature)
    for classifier in classifierList:
        predictValue = StumpClassify(inputFeature, classifier['feature'], classifier['thresh'], classifier['operator'])
        totalPredict = [totalPredict[i] + predictValue[i] * classifier['alpha'] for i in range(len(predictValue))]
    return numpy.sign(totalPredict)

if __name__ == '__main__':
    dataArray, labelList = LoadData()
    classifierList, predStrengthList = AdaboostTrain(dataArray, labelList,9)
    result = AdaClassify([[5, 5],[0, 0]], classifierList)
    print (result)
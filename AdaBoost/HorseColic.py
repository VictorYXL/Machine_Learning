import AdaBoost

def LoadDataset(fileName):
    file = open(fileName)
    dataArray = []
    labelList = []
    for line in file.readlines():
        data = line.strip().split('\t')
        dataArray.append([float(item) for item in data[:-1]])
        labelList.append(float(data[-1]))
    return dataArray, labelList

if __name__ == '__main__':
    trainingDataArray, trainingLabelList = LoadDataset("HorseColicTraining.txt")
    classifierList, totalPredictValue = AdaBoost.AdaboostTrain(trainingDataArray, trainingLabelList, 10)
    testDataArray, testLabelList = LoadDataset("HorseColicTest.txt")
    result = AdaBoost.AdaClassify(testDataArray, classifierList)
    errorList = [i for i in range(len(testLabelList)) if testLabelList[i] != result[i]]
    AdaBoost.PlotROC(trainingLabelList, totalPredictValue)
    #print (errorList)
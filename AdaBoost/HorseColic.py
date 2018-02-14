
import sys
sys.path.append("../Basic Functions")
import AdaBoost
from LoadData import LoadData

if __name__ == '__main__':
    trainingDataArray, trainingLabelList = LoadData("HorseColicTraining.txt")
    classifierList, totalPredictValue = AdaBoost.AdaboostTrain(trainingDataArray, trainingLabelList, 10)
    testDataArray, testLabelList = LoadData("HorseColicTest.txt")
    result = AdaBoost.AdaClassify(testDataArray, classifierList)
    errorList = [i for i in range(len(testLabelList)) if testLabelList[i] != result[i]]
    print (errorList) 
    
    AUC = AdaBoost.PlotROC(trainingLabelList, totalPredictValue)
    print(AUC)
    
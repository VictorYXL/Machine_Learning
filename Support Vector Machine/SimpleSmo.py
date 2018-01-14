#http://www.cnblogs.com/jerrylead/archive/2011/03/13/1982639.html
import random
import numpy
import matplotlib
import LoadData

def smoSimple(dataset, border, toler, maxIter):
    dataMatrix = numpy.mat(dataset['data'])
    labelMatrix = numpy.mat(dataset['label']).T

    dataCount = len(dataMatrix)
    vectorLen = len(dataset['data'][0])
    alphas = numpy.mat(numpy.zeros((dataCount, 1)))
    b = 0
    iter = 0

    #Outer loop
    while iter < maxIter:
        #Inner loop
        for i in range(dataCount):
            #Calculate Ui and Ei
            Ui = float(numpy.multiply(alphas, labelMatrix).T * (dataMatrix * dataMatrix[i,:].T)) + b
            Ei = Ui - float(labelMatrix[i])

            #Select j in random
            j = int(random.uniform(0,dataCount))
            while (i == j):
                j = int(random.uniform(0,dataCount))

            #Meet the requirements between i and j
            if ((labelMatrix[i] * Ei < -toler) and (alphas[i] < border)) or ((labelMatrix[i] * Ei > toler) and (alphas[i] > 0)):
                Uj = float(numpy.multiply(alphas, labelMatrix).T * (dataMatrix * dataMatrix[j,:].T)) + b
                Ej = Uj - float(labelMatrix[j])
                #Calculate the border 
                if (labelMatrix[i] == labelMatrix[j]):
                    L = max(0, alphas[j] + alphas[i] - border)
                    H = min(border, alphas[j] + alphas[i])
                else:
                    L = max(0, alphas[j] - alphas[i])
                    H = min(border, border + alphas[j] - alphas[i])
                if (L != H):
                    #Calculate the new alpha[i] and alpha[j]
                    eta = 2.0 * dataMatrix[i,:] * dataMatrix[j,:].T - dataMatrix[i,:] * dataMatrix[i,:].T - dataMatrix[j,:] * dataMatrix[j,:].T
                    if (eta < 0):
                        newAlphaJ = alphas[j] - labelMatrix[j] * (Ei - Ej) / eta
                        if (newAlphaJ > H):
                            newAlphaJ = H
                        if (newAlphaJ < L):
                            newAlphaJ = L
                        if (abs(newAlphaJ - alphas[j]) < 0.001):
                           continue
                        newAlphaI = alphas[i] - labelMatrix[i] * labelMatrix[j] * (newAlphaJ - alphas[j])

                        #Caluclate the b in two conditions
                        b1 = b - Ei - labelMatrix[i] * (newAlphaI - alphas[i]) * dataMatrix[i,:] * dataMatrix[i,:].T - labelMatrix[j] * (newAlphaJ - alphas[j]) * dataMatrix[i,:] * dataMatrix[j,:].T
                        b2 = b - Ej - labelMatrix[i] * (newAlphaI - alphas[i]) * dataMatrix[i,:] * dataMatrix[j,:].T - labelMatrix[j] * (newAlphaJ - alphas[j]) * dataMatrix[j,:] * dataMatrix[j,:].T

                        #Update the alpha[i], alpha[j] and b
                        alphas[i] = newAlphaI
                        alphas[j] = newAlphaJ
                        if (0 < alphas[i] and alphas[i] < border):
                            b = b1
                        elif (0 < alphas[j] and alphas[j] < border):
                            b = b2
                        else:
                            b = (b1 + b2) / 2.0
        iter = iter + 1
    return alphas,b


dataset = LoadData.LoadDataset("Dataset.txt")
alphas,b = smoSimple(dataset, 0.6, 0.001, 100)
print (alphas)
print (b)
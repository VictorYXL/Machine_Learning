import sys
sys.path.append("../Basic Functions")
import random
import numpy
import matplotlib
from LoadData import LoadData

#Class Operator
class Operator:
    #Init 
    def __init__(self, dataArray, labelList, border, toler):
        self.dataMatrix = numpy.mat(dataArray)
        self.labelMatrix = numpy.mat(labelList).T
        self.border = border
        self.toler = toler
        self.dataCount = len(dataArray)
        self.alphas = numpy.mat(numpy.zeros((self.dataCount, 1)))
        self.b = 0
        self.eCache = numpy.mat(numpy.zeros((self.dataCount, 2)))
    #Calculate Ei
    def CalcEi(self,i):
        Ui = float(numpy.multiply(self.alphas, self.labelMatrix).T * (self.dataMatrix * self.dataMatrix[i,:].T)) + self.b
        Ei = Ui - float(self.labelMatrix[i])
        return Ei
    #Update Ei
    def UpdateEi(self,i):
        Ei = self.CalcEi(i)
        self.eCache[i] = [1, Ei]
    #Select the second one to optimize
    def SelectJ(self,i):
        Ei = self.CalcEi(i)
        maxK = -1
        maxDeltaE = 0
        Ej = 0
        self.eCache[i] = [1, Ei]
        validList = numpy.nonzero(self.eCache[:,0].A)[0]
        #Find out the best delta between Ei and Ek
        if len(validList) > 1:
            for k in validList:
                if k != i:
                    Ek = self.CalcEi(k)
                    deltaE = abs(Ei - Ek)
                    if deltaE > maxDeltaE:
                        maxDeltaE = deltaE
                        maxK = k
                        Ej = Ek
            return maxK
        else:
            j = int(random.uniform(0,op.dataCount))
            while (i == j):
                j = int(random.uniform(0,op.dataCount))
            return j
    #Calculate w
    def CalcW(self):
        m, n = numpy.shape(self.dataMatrix)
        self.w = numpy.zeros((n, 1))
        for i in range(m):
            self.w += numpy.multiply(self.alphas[i] * self.labelMatrix[i], self.dataMatrix[i, :].T)

#Optimize once including i and j
def innerLoop(op, i):
    Ei = op.CalcEi(i)
    if ((op.labelMatrix[i] * Ei < -op.toler) and (op.alphas[i] < op.border)) or ((op.labelMatrix[i] * Ei > op.toler) and (op.alphas[i] > 0)):
        #Select j 
        j = op.SelectJ(i)
        Ej = op.CalcEi(j)
        #Define the border of new alpha
        if (op.labelMatrix[i] == op.labelMatrix[j]):
            L = max(0, op.alphas[j] + op.alphas[i] - op.border)
            H = min(op.border, op.alphas[j] + op.alphas[i])
        else:
            L = max(0, op.alphas[j] - op.alphas[i])
            H = min(op.border, op.border + op.alphas[j] - op.alphas[i])
    
        if (L != H):
            #Calculate eta
            eta = 2.0 * op.dataMatrix[i,:] * op.dataMatrix[j,:].T - op.dataMatrix[i,:] * op.dataMatrix[i,:].T - op.dataMatrix[j,:] * op.dataMatrix[j,:].T
            if (eta < 0):
                #Calculate new alpha[j]
                newAlphaJ = op.alphas[j] - op.labelMatrix[j] * (Ei - Ej) / eta
                if (newAlphaJ > H):
                    newAlphaJ = H
                if (newAlphaJ < L):
                    newAlphaJ = L
                op.UpdateEi(j)
                #Move too small
                if (abs(newAlphaJ - op.alphas[j]) < 0.001):
                    return False
                #Calculate new alpha[i]
                newAlphaI = op.alphas[i] - op.labelMatrix[i] * op.labelMatrix[j] * (newAlphaJ - op.alphas[j])
                op.UpdateEi(i)


                #calculate b in two conditions
                b1 = op.b - Ei - op.labelMatrix[i] * (newAlphaI - op.alphas[i]) * op.dataMatrix[i,:] * op.dataMatrix[i,:].T - op.labelMatrix[j] * (newAlphaJ - op.alphas[j]) * op.dataMatrix[i,:] * op.dataMatrix[j,:].T
                b2 = op.b - Ej - op.labelMatrix[i] * (newAlphaI - op.alphas[i]) * op.dataMatrix[i,:] * op.dataMatrix[j,:].T - op.labelMatrix[j] * (newAlphaJ - op.alphas[j]) * op.dataMatrix[j,:] * op.dataMatrix[j,:].T

                #Update alpha[i] and alpha[j]
                op.alphas[i] = newAlphaI
                op.alphas[j] = newAlphaJ
                #Update b
                if (0 < op.alphas[i] and op.alphas[i] < op.border):
                    op.b = b1
                elif (0 < op.alphas[j] and op.alphas[j] < op.border):
                    op.b = b2
                else:
                    op.b = (b1 + b2) / 2.0
                return True
    return False

#Use inner loop to calculate w and b
def smoPlatt(op, maxIter):
    entireSet = True
    whetherChanged = False
    iter = 0

    while (iter < maxIter) and (whetherChanged or entireSet):
        whetherChanged = False
        #Entireset or the dataset without 0
        if entireSet:
            loopRange = range(op.dataCount)
        else:
            loopRange = numpy.nonzero((op.alphas.A > 0) * (op.alphas.A < op.border))[0]
        
        #Outer loop
        for i in loopRange:
            #Inner loop
            thisChanged = innerLoop(op, i)
            #Whethe there is alpha changed in this loop
            whetherChanged = whetherChanged or thisChanged
        iter = iter + 1
        if entireSet:
            entireSet = False
        elif whetherChanged == False:
            entireSet = True
    op.CalcW()
    return op

#classify by (input * weight + bias)
def classify(input, op):
    result = input * op.w + op.b
    if result > 0:
        return 1
    else:
        return -1
if __name__ == '__main__':
    dataArray, labelList = LoadData("Dataset.txt")
    op = Operator(dataArray, labelList, 0.6, 0.001)
    op = smoPlatt(op, 100)
    print (classify(numpy.mat([1.339746, -0.291183]), op))
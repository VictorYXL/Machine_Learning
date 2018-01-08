import numpy
import matplotlib

class Operator:
    def __init__(self, dataset, border, toler):
        self.dataMatrix = dataset['data']
        self.labelMatrix = dataset['label']
        self.border = border
        self.toler = toler
        self.dataCount = len(dataset['data'])
        self.alphas = numpy.mat(numpy.zeros((dataCount, 1)))
        self.b = 0
        self.eCache = numpy.mat(numpy.zeros((dataCount, 2)))
    def CalcEi(i):
        Ui = float(numpy.multiply(self.alphas, self.labelMatrix).T * (self.dataMatrix * self.dataMatrix[i,:].T)) + self.b
        Ei = Ui - float(self.labelMatrix[i])
        return Ei
    def UpdateFi(i):
        Ei = self.calcEi(i)
        self.eCache[i] = [1, Ei]
    def SelectJ(i):
        Ei = self.CalcEi(i)
        maxK = -1
        maxDeltaE = 0
        Ej = 0
        self.eCache[i] = [1, Ei]
        validList = numpy.nonzero(self.eCache[:,0].A)[0]
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
            j = int(random.uniform(0,dataCount))
            while (i == j):
                j = int(random.uniform(0,dataCount))
            return j



import LoadData
dataset = LoadData.LoadDataset("Dataset.txt")
#alphas,b = smoSimple(dataset, 0.6, 0.001, 100)
#print (alphas)
#print (b)
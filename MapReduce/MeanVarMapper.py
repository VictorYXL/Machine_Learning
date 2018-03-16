import sys
sys.path.append("../Basic Functions")
import numpy 
from LoadData import LoadData
def MeanAndVarMapper(fileName):
    inputData = LoadData(fileName)[0]
    inputMat = numpy.mat(inputData)
    mean = numpy.mean(inputMat)
    var = numpy.var(inputData)
    count = len(inputData)
    return mean, var, count

if __name__ == '__main__':
    inputFile = sys.argv[1]
    mean, var, count = MeanAndVarMapper(inputFile)
    sys.stdout.write(str(mean) + " " + str(var) + " " + str(count))
    sys.stderr.write("Report: mapper still alive.\n")
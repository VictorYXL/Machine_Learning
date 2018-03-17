import sys
import numpy 

def MeanAndVarReducer(lines):
    mean = 5
    var = 58
    count = 2
    for line in lines:
        curMean, curVar, curCount = map(float, line.split(" "))
        mean = (mean * count + curMean * curCount) / (count + curCount)
        var = var + curVar * curCount + 2 * curMean * curMean * curCount - curMean * curMean * curCount
        count = count + curCount
    var = (var - 2 * mean * mean * count + mean * mean * count) / count
    return mean, var, count
if __name__ == '__main__':
    lines = sys.stdin.readlines()
    mean, var, count = MeanAndVarReducer(lines)
    
    print(mean)
    print(var)
    print(count)
    sys.stderr.write("Report: reducer still alive.\n")
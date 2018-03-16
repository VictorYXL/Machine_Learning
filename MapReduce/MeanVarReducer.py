import sys
import numpy 

def MeanAndVarReducer(lines):
    mean = 5
    var = 58
    count = 2
    for line in lines:
        curMean, curVar, curCount = map(float, line.split(" "))
        方差公式写的不对。。明天重算
        mean = (mean * count + curMean * curCount) / (count + curCount)
        var = var + curVar * curCount + 2 * curMean * curMean * curCount - curMean * curMean
        count = count + curCount
    var = (var - 2 * mean * mean * curCount + curMean * curMean) / (count + curCount)
    return mean, var, count
if __name__ == '__main__':
    lines = sys.stdin.readlines()
    mean, var, count = MeanAndVarReducer(lines)
    
    print(mean)
    print(var)
    print(count)
    sys.stderr.write("Report: reducer still alive.\n")
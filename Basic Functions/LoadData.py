def LoadDataAndLabel(fileName):
    file = open(fileName)
    dataArray = []
    labelList = []
    for line in file.readlines():
        data = line.strip().split('\t')
        dataArray.append(list(map(float, data[:-1])))
        labelList.append(float(data[-1]))
    return dataArray, labelList

def LoadData(fileName):
    file = open(fileName)
    dataArray = []
    labelList = []
    for line in file.readlines():
        data = line.strip().split('\t')
        dataArray.append(list(map(float, data)))
    return dataArray
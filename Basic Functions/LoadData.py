def LoadData(fileName):
    file = open(fileName)
    dataArray = []
    labelList = []
    for line in file.readlines():
        data = line.strip().split('\t')
        dataArray.append([float(item) for item in data[:-1]])
        labelList.append(float(data[-1]))
    return dataArray, labelList
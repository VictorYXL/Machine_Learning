def LoadDataset(fileName):
    f = open(fileName, "r")
    dataList = []
    labelList = []
    for line in f.readlines():
        lineArray = line.strip().split()
        numLine = []
        for num in lineArray[:-1]:
            numLine.append(float(num))
        dataList.append(numLine)
        labelList.append(float(lineArray[-1]))
    return {'data': dataList, 'label': labelList}
#Create init set that include all single item from dataset
def CreateCanSet(dataArray):
    canSet = []
    for data in dataArray:
        for item in data:
            if [item] not in canSet:
                canSet.append([item])
    canSet.sort()
    return canSet
#Return support item that frequency is higher that min support
def SuportItemList(dataArray, canSet, minSupport):
    frequencyList = [0 for i in  range(len(canSet))]
    for data in dataArray:
        for (index, item) in enumerate(canSet):
            #set(a) > set(b): a includes b
            if set(data) > set(item):
                frequencyList[index] = frequencyList[index] + 1 / len(dataArray)
    
    supportList = []
    for (index, freq) in enumerate(frequencyList):
        if freq >= minSupport:
            supportList.append(canSet[index])        
    return supportList, frequencyList


if __name__ == '__main__':
    dataArray = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    canSet = CreateCanSet(dataArray)
    supportList, frequencyList = SuportItemList(dataArray, canSet, 0.5)
    print(supportList)
    print(frequencyList)


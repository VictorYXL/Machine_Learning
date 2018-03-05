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
    tmpFreList = [0 for i in  range(len(canSet))]
    for data in dataArray:
        for (index, item) in enumerate(canSet):
            #set(a) >= set(b): a includes b
            if set(data) >= set(item):
                tmpFreList[index] = tmpFreList[index] + 1 / len(dataArray)
    
    supportList = []
    frequencyList = []
    for (index, freq) in enumerate(tmpFreList):  
        if freq >= minSupport:
            supportList.append(canSet[index])
            frequencyList.append(tmpFreList[index])
            
    return supportList, frequencyList

#From list get cartesian product
def carProduct(basicList):
    outputlist = []
    for i in range(len(basicList)):
        for j in range(i + 1, len(basicList)):
            if list(set(basicList[i] + basicList[j])) not in outputlist:
                outputlist.append(list(set(basicList[i] + basicList[j])))
    return outputlist

def Apriori(dataArray, minSupport):
    canSet = CreateCanSet(dataArray)
    currentSupportList, currentFrequencyList = SuportItemList(dataArray, canSet, minSupport)
    supportList = [currentSupportList]
    frequencyList = [currentFrequencyList]
    canListLen = 0
    while len(supportList[canListLen]) > 0:
        canSet = carProduct(currentSupportList)
        currentSupportList, currentFrequencyList = SuportItemList(dataArray, canSet, minSupport)
        if len(currentFrequencyList) <= 0:
            break
        supportList.append(currentSupportList)
        frequencyList.append(currentFrequencyList)
        canListLen = canListLen + 1
    return supportList, frequencyList



if __name__ == '__main__':
    dataArray = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    supportList, frequencyList = Apriori(dataArray, 0.5)
    print(supportList)
    print(frequencyList)

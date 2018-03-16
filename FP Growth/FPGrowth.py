import Node
def CreateTree(dataArray, minSupport):
    #Count the frequence of each item 
    headerTable = {}
    for trans in dataArray:
        for item in trans:
            if item not in headerTable.keys():
                #Create the header list and link
                headerTable[item] = [1, None]
            else:
                headerTable[item][0] += 1
    #Remove upfrequence items
    for item in headerTable.keys():
        if headerTable[item][0] < minSupport:
            del headerTable[item]
    if len(headerTable) == 0:
        return None, None
    freqItemSet = headerTable.keys()

    #Root of Tree
    rootNode = Node.Node('Root', None)
    for trans in dataArray:
        newTrans = []
        for item in trans:
            if item in freqItemSet:
                newTrans.append(item)
        if len(newTrans) != 0:
            #Sort by frequence of items
            newTrans.sort(key = lambda p: headerTable[p][0], reverse = True)
            UpdateTree(newTrans, rootNode, headerTable)
    return rootNode, headerTable

def UpdateTree(trans, root, headerTable):
    #root.show()
    #Update the tree and header list
    if trans[0] in root.children:
        root.children[trans[0]].inc()
    else:
        newNode = Node.Node(trans[0], root)
        root.children[trans[0]] = newNode
        if headerTable[trans[0]][1] == None:
            headerTable[trans[0]][1] = newNode
        else:
            node = headerTable[trans[0]][1]
            while node.next != None:
                node = node.next
            node.next = root.children[trans[0]]
    if len(trans) > 1:
        UpdateTree(trans[1:], root.children[trans[0]], headerTable)

#Find single path for one leaf
def FindPrefixPath(leafNode):
    prefixPath = []
    while leafNode.parent != None:
        prefixPath.append(leafNode.name)
        leafNode = leafNode.parent
    return prefixPath[1:]

#Find all pathes for one leaf
def FindAllPrefixPath(node):
    condPath = []
    while node != None:
        prefixPath = FindPrefixPath(node)
        for i in range(node.count):
            condPath.append(prefixPath) 
        node = node.next
    return condPath

#Create mine tree to find all frequent set
def mineTree(tree, headerTable, minSupport, prefix):
    leafList = [leaf[1] for leaf in headerTable.values()]
    tmpFreqSet = []
    for leaf in leafList:
        tmpPrefix = prefix[:]
        tmpPrefix.append(leaf)
        name = [node.name for node in tmpPrefix]
        tmpFreqSet.append(name)
        condPath = FindAllPrefixPath(leaf)
        condTree, condHeaderList = CreateTree(condPath, minSupport)
        if condHeaderList != None:
            tmpFreqSet.extend(mineTree(condTree, condHeaderList, minSupport, tmpPrefix))
    return tmpFreqSet

if __name__ == '__main__':
    dataArray = [
               ['z', 'y', 'x', 'w', 'v', 'u', 's', 't'],
               ['s', 'x', 'n', 'o', 'r'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['r', 'z', 'h', 'j', 'p'],
               ['z']]
    rootNode, headerTable = CreateTree(dataArray, 3)
    freqSet = mineTree(rootNode, headerTable, 3, [])
    print freqSet
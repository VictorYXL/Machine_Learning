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


if __name__ == '__main__':
    dataArray = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    rootNode, headerTable = CreateTree(dataArray, 1)
    rootNode.show()
    print(headerTable)
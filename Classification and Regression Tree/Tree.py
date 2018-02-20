class Node():
    def __init__(self, feature, value, left, right):
        self.feature = feature
        self.value = value
        self.left = left
        self.right = right

def ShowTree(tree):
    print(tree, tree.left, tree.right)
    print(tree.feature, tree.value)
    if (tree.left != None):
        ShowTree(tree.left)
    if (tree.right != None):
        ShowTree(tree.right)
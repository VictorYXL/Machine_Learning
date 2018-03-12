class Node:
    def __init__(self, name, parent):
        self.name = name
        self.count = 1
        self.parent = parent
        self.children = {}
        self.next = None
    def inc(self, num = 1):
        self.count += num
    def show(self, ind = 1):
        print("Deep %d: %s, %d" % (ind, self.name, self.count))
        if self.parent == None:
            print("  Parent: None")
        else:
            print("  Parent: %s" % self.parent.name)
        childList = [child.name for child in self.children.values()]
        print("  Children:%s" % str(childList))
        for child in self.children.values():
            child.show(ind + 1)
if __name__ == "__main__":
    a = Node('a', 2, None)
    b = Node('b', 1, a)
    c = Node('c', 1, a)
    d = Node('d', 0, b)
    a.children = [b, c]
    b.children = [d]
    a.show()

            
class TreeNode:
    def __init__(self, value: str, key=None):
        self.left = None
        self.right = None
        self.value = value
        self.key = key

    def smaller(self, value: str) -> bool:
        if self.key is None:
            value2 = self.value
        else:
            value = self.key(value)
            value2 = self.key(self.value)
        for i in range(min(len(value), len(value2))):
            if ord(value[i]) > ord(value2[i]):
                return False
            elif ord(value[i]) < ord(value2[i]):
                return True
        if len(value) < len(value2):
            return True
        return False

    def insert(self, value: str, key=None):
        # if value < self.value:
        if self.smaller(value):
            if self.left is None:
                self.left = TreeNode(value, key)
            else:
                self.left.insert(value, key)
        else:
            if self.right is None:
                self.right = TreeNode(value, key)
            else:
                self.right.insert(value, key)

    def append_value(self, valueList):
        if self.left is not None:
            self.left.append_value(valueList)
        valueList.append(self.value)
        if self.right is not None:
            self.right.append_value(valueList)

class BinaryTree:
    def __init__(self, root=None):
        self.root = root

    def insert(self, *values, key=None):
        for value in values:
            if self.root is None:
                self.root = TreeNode(value, key)
            else:
                self.root.insert(value, key)

    def list(self):
        valueList = list()
        if self.root is not None:
            self.root.append_value(valueList)
        return valueList

def tree_sort(e, key=None):
    tree = BinaryTree()
    tree.insert(*e, key=key)
    return tree.list()

if __name__ == "__main__":
    tree = BinaryTree()
    tree.insert("aa", "2", "ab", "n", "aaa", "a")
    print(tree.list())

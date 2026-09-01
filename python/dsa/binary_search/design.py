from typing import List


class TreeNode:
    def __init__(self, key: int, val: int, left=None, right=None):
        self.key = key
        self.val = val
        self.left = left
        self.right = right


class TreeMap:

    def __init__(self):
        self.root = None

    def insert(self, key: int, val: int) -> None:
        newNode = TreeNode(key, val)
        if not self.root:
            self.root = newNode
            return

        curr = self.root
        while True:
            if key < curr.key:
                if not curr.left:
                    curr.left = newNode
                    return
                curr = curr.left
            elif key > curr.key:
                if not curr.right:
                    curr.right = newNode
                    return
                curr = curr.right
            else:
                curr.val = val
                return

    def get(self, key: int) -> int:
        curr = self.root
        while curr:
            if key == curr.key:
                return curr.val
            elif key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
        return -1

    def getMin(self) -> int:
        curr = self.root
        if not curr:
            return -1
        while curr.left:
            curr = curr.left
        return curr.val

    def getMax(self) -> int:
        curr = self.root
        while curr.right:
            curr = curr.right
        return curr.val

    def remove(self, key: int) -> None:
        self.root = self.removeHelper(self.root, key)

    # Return the minimum value node of the BST.
    def minValueNode(self, root):
        curr = root
        while curr and curr.left:
            curr = curr.left
        return curr

    def removeHelper(self, root, key):
        if not root:
            return None

        if key > root.key:
            root.right = self.removeHelper(root.right, key)
        elif key < root.key:
            root.left = self.removeHelper(root.left, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            else:
                minNode = self.minValueNode(root.right)
                root.key = minNode.key
                root.right = self.removeHelper(root.right, minNode.key)
        return root

    def getInorderKeys(self) -> List[int]:
        res = []

        def dfs(curr):
            if not curr:
                return

            dfs(curr.left)
            res.append(curr.key)
            dfs(curr.right)

        dfs(self.root)
        return res
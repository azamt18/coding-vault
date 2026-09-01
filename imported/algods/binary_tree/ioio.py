# Definition for a binary tree node.
from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p or not q:
            return False
        stack = [(p, q)]
        while stack:
            left, right = stack.pop()
            if not left and not right:
                continue
            if left and not right:
                return False
            if right and not left:
                return False
            if left.val != right.val:
                return False

            stack.append((left.left, left.left))
            stack.append((right.right, right.right))

        return True
Solution().isSameTree([1,2,3], [1,2,3])

"""
https://leetcode.com/problems/populating-next-right-pointers-in-each-node/
"""
"""
# Definition for a Node.
class Node:
    # def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
    #     self.val = val
    #     self.left = left
    #     self.right = right
    #     self.next = next
"""
class Solution:
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        if not root:
            return None

        dq = deque([root])
        while dq:
            level_size = len(dq)
            prev_sibling_node = None
            for i in range(level_size):
                node = dq.popleft()
                if node.left:
                    dq.append(node.left)
                if node.right:
                    dq.append(node.right)

                if prev_sibling_node:
                    prev_sibling_node.next = node
                else:
                    prev_sibling_node = node

        return root

""" https://leetcode.com/problems/delete-leaves-with-a-given-value/ """
def removeLeafNodes(self, root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
    def dfs(root):
        if not root:
            return None
        root.left = dfs(root.left)
        root.right = dfs(root.right)
        if not root.left and not root.right and root.val == target:
            return None
        return root

    return dfs(root)
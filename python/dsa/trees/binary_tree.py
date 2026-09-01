# Definition for a binary tree node.
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder or not inorder:
            return None

        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])
        root.left = self.buildTree(preorder[1 : mid + 1], inorder[:mid])
        root.right = self.buildTree(preorder[mid + 1 :], inorder[mid + 1 :])
        return root

    # preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]

# call buildTree
# preorder = [3, 9, 20, 15, 7]
# inorder = [9, 3, 15, 20, 7]
# solution = Solution()
# root = solution.buildTree(preorder, inorder)


# https://leetcode.com/problems/symmetric-tree/
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        # recursive approach
        # def isMirror(leftNode, rightNode):
        #     if not leftNode and not rightNode:
        #         return True
        #     if (leftNode and not rightNode
        #         or rightNode and not leftNode):
        #         return False
        #
        #     return (leftNode.val == rightNode.val
        #             and isMirror(leftNode.left, rightNode.right)
        #             and isMirror(leftNode.right, rightNode.left)
        #     )
        #
        # return isMirror(root.left, root.right) if root else True

        # iterative approach
        # if not root.left or not root.right:
        #     return False
        if not root: return True

        queue = deque([(root.left, root.right)])
        while queue:
            leftNode, rightNode = queue.popleft()

            if not leftNode and not rightNode:
                continue
            if leftNode and not rightNode or rightNode and not leftNode:
                return False
            if leftNode.val != rightNode.val:
                return False

            queue.append((leftNode.left, rightNode.right))
            queue.append((leftNode.right, rightNode.left))

        return True

    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # perform in-order traversal with combining tree values into array
        # once traversal is done, iterate over array for non-increasing sequence

        arr = []
        def in_order(node):
            if node:
                in_order(node.left)
                arr.append(node.val)
                in_order(node.right)
            return

        in_order(root)

        L = 0
        for R in range(1, len(arr)):
            if arr[L] > arr[R]:
                return False
            L += 1
            R += 1

        return True


def buildTreeFromList(values: List[int]) -> Optional[TreeNode]:
    if not values:
        return None

    nodes = [TreeNode(val) if val is not None else None for val in values]
    for i in range(len(values)):
        if nodes[i]:
            if 2 * i + 1 < len(values):
                nodes[i].left = nodes[2 * i + 1]
            if 2 * i + 2 < len(values):
                nodes[i].right = nodes[2 * i + 2]
    return nodes[0]

# https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
def lowestCommonAncestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    cur = root
    while cur:
        if p.val > cur.val and q.val > cur.val:
            cur = cur.right
        elif p.val < cur.val and q.val < cur.val:
            cur = cur.left
        else: # means p.val == cur.val and q.val == cur.val
            return cur

# Test case
# values = [1, 2, 2, 3, 4, 4, 3]
# values = [2,1,3]
# values = [6,2,8,0,4,7,9,null,null,3,5]
# root = buildTreeFromList(values)
# solution = Solution()
# print(solution.isValidBST(root))  # Expected output: True

# https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/
"""
    Notes:
        1. LCA - deepest node that has p and q in its subtrees
        2. Unlike BST version, we can't make assumptions about node values being greater/less than parent node

    Approach: consider recursive approach that returns:
        1. LCA              if found in the current subtree
        2. One of the nodes if only one is found
        3. None             if neither node is found

    Scenarios:
        case 1: if current node is p or q or null     -> return current root
        case 2: if p and q are in the same subtree    -> return the current node as the LCA
        case 3: if p and q are in different subtrees  -> continue search on that subtree

    Time:   O(n), where n is the number of nodes in the tree.
    Space:  O(h), where h is the height of the tree (due to the recursive call stack)
"""
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # case 1: if current node is p or q or null     -> return current node
        if not root or root == p or root == q:
            return root

        # recursively call left & right subtrees
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        # case 2: if p and q are in the same subtree    -> return the current node as the LCA
        if left and right:
            return root

        # case 3: if p and q are in different subtrees  -> continue searching in that subtree
        return left if left else right


# https://leetcode.com/problems/path-sum-ii/
"""
    Approach:  
        1. run dfs(root, 0) at start
        2. keep visited nodes in path_nodes[] and update current_sum by node's value
        3. when found leaf-node [without left & right child] and target sum -> one path found
        4. continue on left and right children
        5. backtracking: pop elements from path_nodes[] at the end of each dfs

    DSs: res[] for result, path_nodes[] for keeping nodes during one path

    Time: O(n)
    Space: O(h) for res[] + O(h) for path_nodes[]
"""
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
        def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
            res = []
            path_nodes = []

            # Helper function to perform DFS and find paths
            def dfs(node, current_sum):
                if not node:
                    return

                path_nodes.append(node.val)
                current_sum += node.val

                if not node.left and not node.right and current_sum == targetSum:
                    res.append(list(path_nodes))

                if node.left:
                    dfs(node.left, current_sum)
                if node.right:
                    dfs(node.right, current_sum)

                # backtrack
                path_nodes.pop()

            dfs(root, 0)

            return res
values = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]
targetSum = 22
root = buildTreeFromList(values)
solution = Solution()
print(solution.pathSum(root, targetSum))  # Expected output: [[5, 4, 11, 2], [5, 8, 4, 5]]
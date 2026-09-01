# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque
from typing import Optional, List
from binary_tree.ioio import TreeNode


class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        # dfs recursive, tc: (n), sc: (n)
        min_depth = float("inf")
        def dfs(node, depth):
            nonlocal min_depth
            if not node:
                return 0
            if not node.left and not node.right:
                min_depth = min(min_depth, depth)
                return
            dfs(node.left, depth + 1)
            dfs(node.right, depth + 1)
        dfs(root, 1)
        return min_depth if min_depth != float("inf") else 0

        # dfs iterative, tc: (n), sc: (n)
        # if not root:
        #     return 0
        # min_depth = float("inf")
        # stack = [(root, 1)]
        # while stack:
        #     node, depth = stack.pop()
        #     if not node.left and not node.right:
        #         min_depth = min(min_depth, depth)
        #         continue
        #
        #     if node.left:
        #         stack.append((node.left, depth + 1))
        #     if node.right:
        #         stack.append((node.right, depth + 1))
        # return min_depth

        # bfs, tc: (n), sc: (n)
        # if not root:
        #     return 0
        # min_depth = 0
        # queue = deque([root])
        # while queue:
        #     n = len(queue)
        #     min_depth += 1
        #     for _ in range(n):
        #         node = queue.popleft()
        #         if not node.left and not node.right:
        #             return min_depth
        #         if node.left:
        #             queue.append(node.left)
        #         if node.right:
        #             queue.append(node.right)
        # return min_depth

    """ https://leetcode.com/problems/maximum-depth-of-n-ary-tree/ """
    """
    # Definition for a Node.
    """
    class Node:
        def __init__(self, val: Optional[int] = None, children: Optional[List['Node']] = None):
            self.val = val
            self.children = children

    def maxDepth(self, root: 'Node') -> int:
        # pure recursive, tc: (n), sc: (h)
        if not root:
            return 0
        if not root.children:
            return 1
        return 1 + max(self.maxDepth(child) for child in root.children)

        # global state dfs, tc: (n), sc: (h)
        # if not root:
        #     return 0

        # max_depth = 0
        # def dfs(node, depth):
        #     nonlocal max_depth
        #     max_depth = max(max_depth, depth)
        #     for child in node.children:
        #         dfs(child, depth + 1)
        # dfs(root, 1)
        # return max_depth

        # dfs iterative, tc: (n), sc: (h)
        # if not root:
        #     return 0
        # stack = [(root, 1)]
        # max_depth = 0
        # while stack:
        #     node, depth = stack.pop()
        #     if node:
        #         max_depth = max(max_depth, depth)
        #         for child in node.children:
        #             stack.append((child, depth + 1))
        # return max_depth

        # bfs, tc: (n), sc: (w), w = max width at any level
        # if not root:
        #     return 0
        # queue = deque([root])
        # max_depth = 0
        # while queue:
        #     n = len(queue)
        #     for _ in range(n):
        #         node = queue.popleft()
        #         for child in node.children:
        #             queue.append(child)
        #     max_depth += 1
        # return max_depth

    """ https://leetcode.com/problems/binary-tree-paths/ """
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        # backtracking optimal
        result = []
        def backtrack(node, path):
            if not node:
                return
            path.append(str(node.val))
            if not node.left and not node.right:
                result.append('->'.join(path))
            else:
                # continue exploring
                backtrack(node.left, path)
                backtrack(node.right, path)
            # backtrack
            path.pop()
        backtrack(root, [])
        return result

        # backtracking, tc: (), sc: ()
        # result = []
        # def backtrack(node, acc):
        #     if not node:
        #         return
        #     acc.append(node.val)
        #     if not node.left and not node.right:
        #         path = ""
        #         for val in acc:
        #             path += str(val)
        #             path += '->'
        #         path = path.removesuffix('->')
        #         result.append(path)
        #         # return
        #     else:
        #         backtrack(node.left, acc)
        #         backtrack(node.right, acc)
        #     acc.pop()
        # backtrack(root, [])
        # return result

    """ https://leetcode.com/problems/binary-tree-tilt/ """
    def findTilt(self, root: Optional[TreeNode]) -> int:
        # how to differentiate node values sum and tilt sum
        total_tilts = 0
        def dfs(node):
            nonlocal total_tilts
            if not node:
                return 0

            left_tilt = dfs(node.left)
            right_tilt = dfs(node.right)
            total_tilts += abs(left_tilt - right_tilt)
            return node.val + left_tilt + right_tilt

        dfs(root)
        return total_tilts

    """ https://leetcode.com/problems/maximum-binary-tree/ """
    def constructMaximumBinaryTree(self, nums: List[int]) -> Optional[TreeNode]:
        # [3,2,1,6,5,0]
        def build_tree(arr): # [32]
            if not arr:
                return None
            if len(arr) ==  1:
                return TreeNode(arr[0])

            max_val = max(arr) # 3
            max_index = arr.index(max_val) # 0

            # create node
            root = TreeNode(max_val)
            # recursively build subtrees
            root.left = build_tree(arr[ : max_index])
            root.right = build_tree(arr[max_index + 1 : ])
            return root

        return build_tree(nums)

    """ https://leetcode.com/problems/subtree-of-another-tree/ """
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        # dfs, tc: (mn), sc: max(h1, h2) for recursion stack
        # if not root: return False
        # if not subRoot: return True
        #
        # def isSameTree(s, t):
        #     if not s and not t:
        #         return True
        #     if s and t and s.val == t.val:
        #         return isSameTree(s.left, t.left) and isSameTree(s.right, t.right)
        #     return False
        #
        # return (isSameTree(root, subRoot) or
        #         self.isSubtree(root.left, subRoot) or
        #         self.isSubtree(root.right, subRoot))
        return False

    def removeLeafNodes(self, root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
        # dfs recursive
        def dfs(node):
            # base
            if not node:
                return None
            # post order
            node.left = dfs(node.left)
            node.right = dfs(node.right)
            # leaf node
            if not node.left and not node.right and node.val == target:
                return None
            return node

        return dfs(root)


        # dfs iterative is bad - use multiple pass for it
        # stack = [(root, None, "")]  # (current node, parent node, left/right)
        # while stack:
        #     node, parent, hand = stack.pop()
        #
        #     # if it is a leaf node
        #     if not node.left and not node.right:
        #         if node.val == target:
        #             if not parent:
        #                 return None  # node without parent (when target == root)
        #             if hand == "left":
        #                 parent.left = None
        #             else:
        #                 parent.right = None
        #
        #     if node.left:
        #         stack.append((node.left, node, "left"))
        #     if node.right:
        #         stack.append((node.right, node, "right"))
        #     # when node == target but not leaf yet
        #     if node.val == target:
        #         stack.append((node, parent, hand))
        #
        # return root

    """ https://leetcode.com/problems/house-robber-iii/ """
    def rob(self, root: Optional[TreeNode]) -> int:

        def dfs(node):
            if not node:
                return 0, 0
            # post order
            left_rob, left_skip = dfs(node.left)
            right_rob, right_skip = dfs(node.right)

            # states for decision: rob current, skip current
            rob_current = node.val + left_skip + right_skip
            skip_current = max(left_rob, left_skip) + max(right_rob, right_skip)

            return rob_current, skip_current

        max_rob, max_skip = dfs(root)
        return max(max_rob, max_skip)





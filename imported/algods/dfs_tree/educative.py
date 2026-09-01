from collections import deque
from typing import List, Optional


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:
    def __init__(self):
        self.marker = "M"

    def serialize_helper(self, node, stream):
        # preorder
        if not node:
            stream.append(self.marker)
            return
        stream.append(node.val)
        self.serialize_helper(node.left, stream)
        self.serialize_helper(node.right, stream)

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        stream = []
        self.serialize_helper(root, stream)
        return stream

    def deserialize_helper(self, stream):
        print(stream)
        val = stream.pop()
        if type(val) is str and val == self.marker:
            return None

        node = TreeNode(val)
        node.left = self.deserialize_helper(stream)
        node.right = self.deserialize_helper(stream)
        return node

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        data.reverse()
        node = self.deserialize_helper(data)
        return node

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))

""" https://leetcode.com/problems/binary-tree-maximum-path-sum/description/?envType=study-plan-v2&envId=top-interview-150 """
def max_path_sum(root):
    max_sum = float("-inf")

    def dfs(node):
        nonlocal max_sum
        # postorder
        if not node:
            return 0

        left_contribution = max(0, dfs(node.left))
        right_contribution = max(0, dfs(node.right))

        current_contribution = node.val + left_contribution + right_contribution
        max_sum = max(max_sum, current_contribution)

        return node.val + max(left_contribution, right_contribution)

    dfs(root)
    return max_sum

""" https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/ """
def buildTree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:

    def dfs(preorder_arr, preorder_idx, inorder_arr):  # (preorder, preorder_idx, inorder_arr)
        # base
        if preorder_idx[0] == len(preorder_arr):
            return

        pre_el = preorder_arr[preorder_idx[0]]
        preorder_idx[0] += 1
        node = TreeNode(pre_el)

        in_idx = inorder_arr.index(pre_el)

        node.left = dfs(preorder_arr, preorder_idx, inorder_arr[: in_idx])
        node.right = dfs(preorder_arr, preorder_idx, inorder_arr[in_idx + 1:])

        return node

    return dfs(preorder[:], [0], inorder[:])

""" https://leetcode.com/problems/validate-binary-search-tree/?envType=study-plan-v2&envId=top-interview-150 """
def isValidBST(root: Optional[TreeNode]) -> bool:
    def dfs(node, prev):
        # inorder dfs
        if not node:
            return True, prev

        valid_left, prev = dfs(node.left, prev)
        if not valid_left:
            return False, prev

        if node.val <= prev:
            return False, prev

        prev = node.val

        valid_right, prev = dfs(node.right, prev)
        return valid_right, prev

    valid, _ = dfs(root, float("-inf"))
    return valid


""" https://leetcode.com/problems/height-of-binary-tree-after-subtree-removal-queries/ """
class Solution:
    def treeQueries(self, root: Optional[TreeNode], queries: List[int]) -> List[int]:
        height_map = {}  # node: height
        depth_map = {}  # node: depth
        level_heights = {}  # depth: [heights of nodes at this level]

        def dfs(node, depth):
            if not node:
                return 0

            depth_map[node] = depth

            left_height = dfs(node.left, depth + 1)
            right_height = dfs(node.right, depth + 1)

            node_height = 1 + max(left_height, right_height)
            height_map[node] = node_height

            # Track heights at each level
            if depth not in level_heights:
                level_heights[depth] = []
            level_heights[depth].append(node_height)

            return node_height

        dfs(root, 0)

        # Sort heights at each level to get top 2
        for depth in level_heights:
            level_heights[depth].sort(reverse=True)

        def get_top_2_height_nodes(depth, excluded_height):
            heights = level_heights[depth]
            if len(heights) == 1:
                return 0  # Only one node, removing it leaves 0 height

            # Find the max height excluding the removed node
            for height in heights:
                if height != excluded_height:
                    return height
            return heights[1] if len(heights) > 1 else 0

        nq = len(queries)
        res = [0] * nq  # max heights after removal

        for i in range(nq):
            # bfs
            queue = deque([root])
            target_node = None
            while queue:
                node = queue.popleft()
                if node.val == queries[i]:
                    target_node = node
                    break
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

                if target_node:
                    target_depth = depth_map[target_node]
                    target_height = height_map[target_node]

                    # Get the max height after removing this node
                    remaining_height = get_top_2_height_nodes(target_depth, target_height)

                    # Result is depth + remaining height - 1 (since height includes the node itself)
                    res[i] = target_depth + remaining_height - 1 if remaining_height > 0 else target_depth - 1

                    # node_height = height_map[node]
                    # if node_height == heightest_1_node:
                    #     res[i] = heightest_2_node
                    # elif node_height == heightest_2_node:
                    #     res[i] = heightest_1_node
                    # else:
                    #

    # def max_height(self, root):
    #     def dfs(node):
    #         if not node:
    #             return 0
    #         left_d = dfs(node.left)
    #         right_d = dfs(node.right)
    #         return 1 + max(left_d, right_d)
    #
    #     return dfs(root)


def return_forest(root, delete_nodes):
    # dfs recursive
    del_set = set()
    # del_set = set(delete_nodes)
    # stack = [root]  # (node)
    # res = []
    # while stack:
    #     node = stack.pop()
    #     if not node:
    #         continue
    #
    #     if node.left:
    #         stack.append(node.left)
    #         if node.left.val in del_set:
    #             node.left = None
    #     if node.right:
    #         stack.append(node.right)
    #         if node.right.val in del_set:
    #             node.right = None
    #     if node.val in del_set:
    #         if node.left:
    #             res.append(node.left)
    #         if node.right:
    #             res.append(node.right)
    #
    #     # if node.data in del_set:
    #     #     flag = 1
    #     #
    #     # if flag:  # to be deleted
    #     #     leftchild = node.left
    #     #     rightchild = node.right
    #     #     node.left = None
    #     #     node.right = None
    #     #
    #     #     stack.append((leftchild, 0))
    #     #     stack.append((rightchild, 0))
    #     #
    #     # else:  # to be remained
    #     #     res.append(node)
    #
    # if root.val not in del_set:
    #     res.append(root)
    # return res


def kth_smallest_element(root, k):
    res = -1

    def dfs(node):
        nonlocal res
        nonlocal k
        if not node or k <= 0:
            return
        dfs(node.left)

        if k > 0:
            k -= 1
            if k == 0:
                res = node.data
                return

        if k > 0:
            dfs(node.right)

    dfs(root)
    return res
    # dfs inorder, tc: (k), sc: (k)
    # arr = []
    # def dfs(node):
    #     nonlocal arr
    #     if not node:
    #         return
    #     if len(arr) == k:
    #         return

    #     left = dfs(node.left) # 1,2
    #     arr.append(node.data)
    #     right = dfs(node.right)

    # dfs(root)
    # return arr[k-1]

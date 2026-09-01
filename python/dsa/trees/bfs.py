# Definition for a binary tree node.
import collections
from collections import deque
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        res = []
        queue = deque()
        queue.append(root)

        while len(queue) > 0:
            for _ in range(len(queue)):
                node = queue.popleft()
                res.append(node.val)
                if node.right:
                    queue.append(node.right)
        return res

    # https://leetcode.com/problems/binary-tree-level-order-traversal/
    # def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
    #     if not root:
    #         return root
    #
    #     res = []
    #     queue = deque()
    #     queue.append(root)
    #
    #     level = 0
    #     while level >= 0:
    #         if len(queue) == 0:
    #             break
    #         sublist = []
    #         cur = queue.popleft()
    #         sublist.append(cur.val)
    #         if cur.left:
    #             queue.append(cur.left)
    #         if cur.right:
    #             queue.append(cur.right)
    #
    #         level += 1
    #         res.append(sublist)
    #     return res

    """
        Approach:
            1. Use BFS (Breadth-First Search) to traverse the tree level by level
            2. For each level:
               - Keep track of all nodes at the current level using the queue size
               - Process all nodes at current level before moving to next level
               - Store values of each level in a separate array
    
        Data Structures:
            - Queue: To maintain the order of nodes to visit (FIFO principle)
            - Result array: To store the final level-by-level values
    
        Time Complexity: 
            - O(n) where n is the number of nodes in the tree
            - Each node is processed exactly once
    
        Space Complexity:
            - O(n) where n is the number of nodes in the tree
            - In worst case (complete binary tree's last level), the queue might contain n/2 nodes
    """
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        queue = deque([root])
        result = []

        while queue:
            level_size = len(queue)
            level_nodes = []

            # process all nodes at current level
            for _ in range(level_size):
                current_node = queue.popleft()
                level_nodes.append(current_node.val)

                if current_node.left:
                    queue.append(current_node.left)
                if current_node.right:
                    queue.append(current_node.right)

            # add current level to result
            result.append(level_nodes)

        return result

    def level_order_traversal(root):

        current_queue, next_queue = deque([]), deque([])

        current_queue.append(root)
        level = 0
        res, level_nodes = "", ""

        while current_queue:
            node = current_queue.popleft()
            level_nodes += str(node.data)

            if node.left:
                next_queue.append(node.left)
            if node.right:
                next_queue.append(node.right)

            if not current_queue:
                level += 1
                current_queue, next_queue = next_queue, current_queue

                if current_queue:
                    level_nodes += " : "
                    res += level_nodes
                    level_nodes = ""
                else:
                    res += level_nodes
            else:
                level_nodes += ", "
        return res

    def zigzag_level_order(root):
        if not root:
            return []

        queue = deque([(root)])
        reverse = False
        result = []

        while queue:
            children = []
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()
                children.append(node.data)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.left)

            if reverse:
                children.reverse()

            result.append(children)
            reverse = True if reverse == False else False
        return result

    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []
        dq = deque([(root)])
        reverse = False

        while dq:
            size = len(dq)
            result.insert(len(dq), [])  # will append level order nodes

            for _ in range(size):
                if not reverse:  # left-to-right direction
                    node = dq.popleft()
                    result[len(dq) - 1].append(node.val)

                    if node.left:
                        dq.append(node.left)
                    if node.right:
                        dq.append(node.right)
                    print(result)
                    print(dq)

                else:  # right-to-left direction
                    node = dq.pop()
                    result[len(dq) - 1].append(node.val)

                    if node.right:
                        dq.appendleft(node.right)
                    if node.left:
                        dq.appendleft(node.left)

                    print(result)
                    print(dq)

            reverse = not reverse

        return result

# Input: root = [1,2,3,4,5,6,7]
# Output: [[1],[2,3],[4,5,6,7]]
# Example usage of levelOrder
root = TreeNode(1)
root.right = TreeNode(2)
# root.right = TreeNode(3)
# root.left.left = TreeNode(4)
# root.left.right = TreeNode(5)
# root.right.left = TreeNode(6)
# root.right.right = TreeNode(7)

solution = Solution()
result = solution.rightSideView(root)

# Print the level order traversal
print(result)

"""
    Pattern: BFS
    Approach:
        1. traverse the tree level by level
        2. push to deque the node with its column index (node, column_index)
        3. if node has children:
            - left: push child to deque with column_index - 1 (node.left, column_index - 1)
            - right: push child to deque with column_index + 1 (node.right, column_index + 1)
        4. keep track of MIN and MAX column indexes, and populate a hash map to store nodes at column index {column_index: [nodes]}
        5. traverse from MIN to MAX column indexes appending vertical_level_nodes[] to result 
"""


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        dq = deque([(root, 0, 0)])  # (node, column_index, row_index)
        min_index, max_index = 0, 0
        index_node_pairs = collections.defaultdict(list) # {column_index: [(row, val)]}
        result = []

        while dq:
            level_nodes, level_size = [], len(dq)
            for _ in range(level_size):
                current_node, column_index, row_index = dq.popleft()

                # level_nodes.append(current_node.val)
                index_node_pairs[column_index].append((row_index, current_node.val))
                # if column_index in index_node_pairs:
                #     index_node_pairs[column_index].append(current_node)
                # else:
                #     index_node_pairs[column_index] = [current_node]

                if current_node.left:
                    dq.append((current_node.left, column_index - 1, row_index + 1))
                    min_index = min(min_index, column_index - 1)
                if current_node.right:
                    dq.append((current_node.right, column_index + 1, row_index + 1))
                    max_index = max(max_index, column_index + 1)
            # result.append(level_nodes)

        for col in range(min_index, max_index + 1):
            vertical_level_nodes = []
            index_node_pairs[col].sort() # sort by row, then by value
            for _, val in index_node_pairs[col]:
                vertical_level_nodes.append(val)
            result.append(vertical_level_nodes)

        return result


def are_neighbors(src, target):
    left, right = 0, 0
    differing_char_found = False
    while right < len(target):
        if src[left] != target[right]:  # differing_char_found not found yet
            if not differing_char_found:
                differing_char_found = True
            else:  # differing_char_found already found
                return False
        left, right = left + 1, right + 1
    return True


def word_ladder(src, dest, words):
    unique_words = set(words)
    dq = deque([src])
    counter, found = 1, False

    while dq and not found:
        level_size = len(dq)
        for _ in range(level_size):
            current_word = dq.popleft()
            if current_word == dest:
                return counter

            # find words differing by one character
            neighbor_words = []
            for unique_word in unique_words:
                if are_neighbors(current_word, unique_word):
                    neighbor_words.append(unique_word)
                    # modifying set during iteration is not possible
                    # unique_words.remove(unique_word) #TBD check if deletion is possible within iteration

            for nw in neighbor_words:
                unique_words.remove(nw)
                dq.append(nw)

        counter += 1

    return counter if found else 0
res = word_ladder("zz" , "nx" , ["nz","nx"])
print(res)
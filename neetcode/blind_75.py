from collections import defaultdict
from typing import List, Optional

from linked_lists.linked_list_generator import generate_linked_list
from trees import binary_search_tree_generator
from trees.binary_search_tree_generator import TreeNode


def groupAnagrams(strs: List[str]) -> List[List[str]]:
    if not strs:
        return [[""]]
    if len(strs) == 1:
        return [strs]

    result = []
    hash_group = defaultdict(list)

    for string in strs:
        sorted_string = ''.join(sorted(string))
        hash_group[sorted_string].append(string)

    for _, str_group in hash_group.items():
        result.append(str_group)

    return result
groupAnagrams(["act","pots","tops","cat","stop","hat"])


class Solution:
    def __init__(self):
        self.encoded_string = []

    def encode(self, strs: List[str]) -> str:
        # "neet","code","love","you"
        for s in strs:
            n = len(s)
            self.encoded_string.extend(str(n))
            self.encoded_string.extend('#')
            self.encoded_string.extend(s)

            # 4#neet4#code4#love3#you
        res = ''.join(self.encoded_string)
        print(res)
        return res

    def decode(self, s: str) -> List[str]:
        result = []
        i = 0
        while i < len(s):
            j = s.find('#', i)

            length = int(s[i:j])

            word = s[j+1 : j+1+length]

            result.append(word)
            i = j + 1 + length

        return result
sol = Solution()
sol.encode(["neet","code","love","you"])
sol.decode("4#neet4#code4#love3#you")


def productExceptSelf(nums: List[int]) -> List[int]:
    #         2*4*6=48   1*4*6=24   1*2*6=12   1*2*4=8
    #         1              2          4          6

    # left_prefix_prod
    # 1       1       2       8       48
    #         1*1=1   1*2=2   2*4=8   8*6=48
    # 1       1       2       4       6

    # right_prefix_prod
    #          48      48      24      6
    #         48*1=48 24*2=48 6*4=24 1*6=6
    #         1       2       4       6       1

    n = len(nums)
    left_prefix_prod = [1] * (n + 1)
    right_prefix_prod = [1] * (n + 1)

    left_prefix_prod[0] = nums[0]
    right_prefix_prod[-2] = nums[-1]

    for i in range(1, n):
        left_prefix_prod[i] = nums[i] * left_prefix_prod[i - 1]
    for i in range(n - 2, -1, -1):
        right_prefix_prod[i] = nums[i] * right_prefix_prod[i + 1]

    print(left_prefix_prod)  # 1 2 8 48
    print(right_prefix_prod)  # 48 48 24 6

    return []
productExceptSelf([1,2,4,6])


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reorderList(head: Optional[ListNode]) -> None:

    # 0 1 2 3 4 5 6
    # 0 6 1 5 2 4 3

    # 2 4     6 8
    #  8 6
    # 2846
    if not head or not head.next:
        return

    def middle(node):
        slow, fast = node, node
        prev = slow
        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        prev.next = None
        return slow

    def reverse(node):
        prev, current = None, node
        while current:
            tmp = current.next
            current.next = prev
            prev = current
            current = tmp
        return prev

    def merge(head, tail):
        # head -> next -> next
        # tail -> next -> next

        l1, l2 = head, tail
        while l1 and l2:
            l1_next, l2_next = l1.next, l2.next

            l1.next = l2
            if not l1_next: # for cases like l1 = 2 4 | l2 = 6 8 10
                break
            l2.next = l1_next

            l1, l2 = l1_next, l2_next

        # if there is no more in head
        # if there is no more in tail

    mid = middle(head)
    tail = reverse(mid)
    merge(head, tail)
    return

head = generate_linked_list([2,4,6,8,10])
reorderList(head)


def isValidBST(root: Optional[TreeNode]) -> bool:
    #   2
    # 1   3
    stack = [(root, float('-inf'), float('inf'))]  # node, lowest_range, highest_range
    while stack:
        node, lowest_range, highest_range = stack.pop()
        if not node:
            continue

        print(lowest_range, node.val, highest_range)
        if not lowest_range < node.val < highest_range:
            return False

        stack.append((root.left, lowest_range, node.val))
        stack.append((root.right, node.val, highest_range))

    return True
root = binary_search_tree_generator.generate_bst([2,1,3])
isValidBST(root)


def lengthOfLIS(nums: List[int]) -> int:
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if dp[i] > dp[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)
    # cache = {}
    #
    # def dfs(i, j):
    #     if i == n:
    #         return 0
    #
    #     if (i, j) in cache:
    #         return cache[(i, j)]
    #
    #     not_taken = dfs(i + 1, j)
    #
    #     taken = 0
    #     if j == -1 or nums[i] > nums[j]:
    #         taken = dfs(i + 1, i) + 1
    #
    #     cache[(i, j)] = max(taken, not_taken)
    #     return cache[(i, j)]
    #
    # return dfs(0, -1)
lengthOfLIS([9,1,4,2,3,3,7])

# https://leetcode.com/problems/spiral-matrix/
def spiralOrder(matrix: List[List[int]]) -> List[int]:
    m, n = len(matrix), len(matrix[0])

    top = (0, 0)  # [0][0]
    right = (0, n - 1)  # [0][n-1]
    bottom = (m - 1, n - 1)  # [m-1][n-1]
    left = (m - 1, 0)  # [m-1][0]

    result = []

    while left < right and top < bottom:
        # top (0,0) -> (0,n-1)
        while top[1] <= right[1]:
            result.append(matrix[top[0]][top[1]])
            top[1] += 1
        top[0] += 1

        # right (0,n-1) -> (m-1,n-1)
        while right[0] <= bottom[0]:
            result.append(matrix[right[0]][right[1]])
            right[0] += 1

        # bottom (m-1,n-1) -> (m-1,0)
        while bottom[1] >= left[1]:
            result.append(matrix[bottom[0]][bottom[1]])
            bottom[1] -= 1

        # left (m-1,0) -> (0,0)
        while left[0] > top[0]:
            result.append(matrix[left[0]][left[0]])
            left -= 1

    return result

# https://leetcode.com/problems/set-matrix-zeroes/description/
def setZeroes(matrix: List[List[int]]) -> None:

    rows, cols = len(matrix), len(matrix[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    seen = set()

    def dfs(row, col):
        if (row, col) in seen:
            return

        if (0 <= row < rows and
                0 <= col < cols):

            matrix[row][col] = 0
            seen.add((row, col))

        dfs(row, col + 1)
        dfs(row, col - 1)
        dfs(row + 1, col)
        dfs(row - 1, col)
        return

    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == 0:
                if (row, col) not in seen:
                    dfs(row, col)

    return
setZeroes([[1,2,3],[4,0,5],[6,7,8]])
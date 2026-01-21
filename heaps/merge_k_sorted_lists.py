# Definition for singly-linked list.
import heapq
from math import floor
from typing import List, Optional


def nthUglyNumber(n: int) -> int:
    min_heap = [1]  # first ugly number
    heapq.heapify(min_heap)
    prime_factors = [2, 3, 5]
    last_number = 0

    i = 0
    while i < n:
        last_number = heapq.heappop(min_heap)
        for p in prime_factors:
            new_number = last_number * p
            if new_number in min_heap:
                continue
            heapq.heappush(min_heap, new_number)
        i += 1

    return last_number
res = nthUglyNumber(10)
print(res)

# Input: nums1 = [1,1,2], nums2 = [1,2,3], k = 2
# Output: [[1,1],[1,1]]
def kSmallestPairs(nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
    # min-heap = [(nums1[i] + nums2[j], i, j)]
    min_heap = []  # len = k, every time when len > k drop the last

    for i in range(k):
        heapq.heappush(min_heap, (nums1[i] + nums2[0], i, 0))

    sums = []  # store the numbers for the output
    while min_heap and k > 0:
        _, i, j = heapq.heappop(min_heap)
        sums.append((nums1[i], nums2[j]))

        if j + 1 < len(nums2):
            heapq.heappush(min_heap, (nums1[i] + nums2[j+1], i, j + 1))

        k -= 1
    return sums
res = kSmallestPairs([1,1,2], [1,2,3], 2)
print(res)

"""
Given N bags, each bag contains Bi chocolates. There is a kid and a magician. In one unit of time, kid chooses a random bag i, eats Bi chocolates, then the magician fills the ith bag with floor(Bi/2) chocolates.

Find the maximum number of chocolates that kid can eat in A units of time.

NOTE: 

floor() function returns the largest integer less than or equal to a given number.
Return your answer modulo 109+7

# Input 2:
#  A = 5
#  B = [2, 4, 6, 8, 10]
#  Total = 10 + 8 + 6 + 5 + 4 = 33
#  MaxBag = [[2], [4], [3], [2], [2]]
"""
# @param A : integer
# @param B : list of integers
# @return an integer
def nchoc(A, B):
    max_heap = []
    total = 0

    for i, val in enumerate(B):
        heapq.heappush(max_heap, (-val, i))

    while A > 0:
        current_val, i = heapq.heappop(max_heap)
        current_val = current_val * (-1)
        total += current_val

        current_val = floor(current_val / 2)
        heapq.heappush(max_heap, (-current_val, i))

        A -= 1
    return total
res = nchoc(3, [6, 5])
print(res)

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    """
    Example 1:
        Input: lists = [[1,4,5],[1,3,4],[2,6]]
        Output: [1,1,2,3,4,4,5,6]
        Explanation: The linked-lists are:
        [
          1->4->5,
          1->3->4,
          2->6
        ]
        merging them into one sorted list:
        1->1->2->3->4->4->5->6
    """
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if len(lists) == 0:
            return None

        # initialize a min-heap
        min_heap = []
        # heapq.heapify(min_heap) # wrong

        # add the 1st node from each list to the head
        for i, node in enumerate(lists):
            if node:
                first_node = (node.val, i, node)
                heapq.heappush(min_heap, first_node)


        # dummy node to simplify result list construction
        dummy = ListNode()
        current = dummy

        while min_heap:
            val, i, node = heapq.heappop(min_heap)
            current.next = node
            current = current.next
            # res.append(smallest)
            if node.next:
                heapq.heappush(min_heap, (node.next.val, i, node.next))

        return dummy.next

    # def __lt__(self, other):



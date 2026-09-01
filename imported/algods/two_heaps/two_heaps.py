import heapq
from collections import defaultdict
from time import sleep
from typing import List


class MedianFinder2:

    def __init__(self):
        self.small = []  # max-heap
        self.large = []  # min-heap

    def addNum(self, num: int) -> None:
        # push to small by default, swap the elements if needed
        heapq.heappush(self.small, -1 * num)

        if (self.small and self.large
                and -1 * self.small[0] > self.large[0]):
            val = -1 * heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # handle uneven size
        if len(self.small) > len(self.large) + 1:
            val = -1 * heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -1 * val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -1 * self.small[0]
        elif len(self.small) < len(self.large):
            return self.large[0]

        return (-1 * self.small[0] + self.large[0]) / 2.0


class MedianFinder:
    def __init__(self, k: int):
        self.k = k  # size of the sliding window
        self.small_max_heap = []  # max heap to store the smaller half of numbers
        self.large_min_heap = []  # min heap to store the larger half of numbers
        self.delayed = defaultdict(int)  # count of delayed elements for lazy deletion
        self.small_size = 0  # size of small_max_heap (not necessarily len(small_max_heap))
        self.large_size = 0  # size of large_min_heap (not necessarily len(large_min_heap))

    def add_num(self, num: int):
        # Add a number to one of the heaps
        if not self.small_max_heap or num <= -self.small_max_heap[0]:
            heapq.heappush(self.small_max_heap, -num)
            self.small_size += 1
        else:
            heapq.heappush(self.large_min_heap, num)
            self.large_size += 1
        self.rebalance()

    def find_median(self) -> float:
        # Find the median of the current numbers
        return -self.small_max_heap[0] if self.k % 2 == 1 else (-self.small_max_heap[0] + self.large_min_heap[
            0]) / 2

    def remove_num(self, num: int):
        # Lazily remove a number (the number will be removed later during pruning)
        self.delayed[num] += 1
        if num <= -self.small_max_heap[0]:
            self.small_size -= 1
            if num == -self.small_max_heap[0]:
                self.prune(self.small_max_heap)
        else:
            self.large_size -= 1
            if num == self.large_min_heap[0]:
                self.prune(self.large_min_heap)
        self.rebalance()

    def prune(self, heap: List[int]):
        # Remove elements that have been flagged for removal
        while heap and self.delayed[heap[0]] > 0:
            self.delayed[heap[0]] -= 1
            if self.delayed[heap[0]] == 0:
                del self.delayed[heap[0]]
            heapq.heappop(heap)

    def rebalance(self):
        # Balance the two heaps to maintain the invariant small_max_heap.size() > large_min_heap.size()
        while self.small_size > self.large_size + 1:
            heapq.heappush(self.large_min_heap, -heapq.heappop(self.small_max_heap))
            self.small_size -= 1
            self.large_size += 1
            self.prune(self.small_max_heap)
        while self.small_size < self.large_size:
            heapq.heappush(self.small_max_heap, -heapq.heappop(self.large_min_heap))
            self.large_size -= 1
            self.small_size += 1
            self.prune(self.large_min_heap)

class Solution:

    def __init__(self):
        self.small = []  # max-heap (inverted min-heap)
        self.large = []  # min-heap
        self.delayed = defaultdict(int) # lazy removal map
        self.small_size = 0
        self.large_size = 0

    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        res = []

        # Add first k elements to the sliding window
        for x in nums[:k]:
            self.addNumber(x)

        # Add median of the first window
        res.append(self.findMedian())

        # Process the rest of the windows
        for i in range(k, len(nums)):
            # Add the new element coming into the window
            self.addNumber(nums[i])

            # Remove the element that is sliding out of the window
            self.removeNumber(nums[i - k])

            # Append the median of the current window
            res.append(self.findMedian())

        return res

    def addNumber(self, num: int) -> None:
        if not self.small or num <= -self.small[0]:
            heapq.heappush(self.small, -num)
            self.small_size += 1
        else:
            heapq.heappush(self.large, num)
            self.large_size += 1

        self.rebalance()

    def removeNumber(self, num: int) -> None:
        # Mark the number for delayed removal
        self.delayed[num] += 1

        if num <= -self.small[0]:
            self.small_size -= 1
            if num == -self.small[0]:
                self.prune(self.small)
        else:
            self.large_size -= 1
            if num == self.large[0]:
                self.prune(self.large)

        self.rebalance()

    def prune(self, heap: List[int]):
        # remove elements that have been flagged for removal
        while heap and self.delayed[heap[0]] > 0:
            self.delayed[heap[0]] -= 1
            if self.delayed[heap[0]] == 0:
                del self.delayed[heap[0]]
            heapq.heappop(heap)

    def rebalance(self) -> None:
        # Ensure that the heaps are either of equal size or `small` has one extra element
        while self.small_size > self.large_size + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
            self.small_size -= 1
            self.large_size += 1
            self.prune(self.small)
        while self.small_size < self.large_size:
            heapq.heappush(self.small, -heapq.heappop(self.large))
            self.small_size += 1
            self.large_size -= 1
            self.prune(self.large)

    def findMedian(self) -> float:
        # If `small` has more elements, its top is the median
        if len(self.small) > len(self.large):
            return -self.small[0]

        # If both heaps are balanced, the median is the average of the tops
        return (-self.small[0] + self.large[0]) / 2


# Example usage:
sol = Solution()
res = sol.medianSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3)  # [1.00000, -1.00000, -1.00000, 3.00000, 5.00000, 6.00000]
print(res)
res = sol.medianSlidingWindow([1,2,3,4,2,3,1,4,2], 3)  # [2.00000,3.00000,3.00000,3.00000,2.00000,3.00000,2.00000]
print(res)
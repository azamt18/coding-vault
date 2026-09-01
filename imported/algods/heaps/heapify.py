from typing import List
import heapq


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # Approach 1: Using a max heap
        # Convert nums to negative values to use min heap as max heap
        nums = [-num for num in nums]
        heapq.heapify(nums)
        # Get the kth largest element
        # Since we are using a min heap, we need to pop k-1 elements
        for _ in range(k - 1):
            heapq.heappop(nums)
        return -heapq.heappop(nums)

        max_heap = []
        heapq.heapify(max_heap)
        for num in nums:
            heapq.heappush(max_heap, -num)
            if len(max_heap) > k:
                heapq.heappop(max_heap)
        return -max_heap[k]

    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # Approach 1: Using a max heap
        # Convert points to negative values to use min heap as max heap
        points = [(-x[0], -x[1]) for x in points]
        heapq.heapify(points)
        return [[-x[0], -x[1]] for x in heapq.nsmallest(k, points)]

    def lastStoneWeight(self, stones: List[int]) -> int:
        # Approach 1: Using a max heap
        # Convert stones to negative values to use min heap as max heap
        stones = [-stone for stone in stones]
        heapq.heapify(stones)
        while len(stones) > 1:
            s1, s2 = heapq.heappop(stones), heapq.heappop(stones)
            if s1 == s2:
                continue
            else:
                heapq.heappush(stones, s1 - s2)
        return -stones[0] if stones else 0
        # arr = stones.copy()
        # while len(arr) > 1:
        #     arr.sort() # sort on the beginning of each iteration
        #     s1, s2 = arr[-1], arr[-2] # take the 2 heaviest stones
        #
        #     # smash them together
        #     if s1 == s2:
        #         arr = arr[:-2] # remove last 2 elements
        #     elif s2 < s1:
        #         arr[-2] = s1 - s2 # update the 2nd last element
        #         arr = arr[:-1] # remove last element
        # return 0 if len(arr) == 0 else arr[0]

# Example usage of lastStoneWeight
# stones = [2, 7, 4, 1, 8, 1]
stones = [2,3,6,2,4]
solution = Solution()
result = solution.findKthLargest(stones, 2)
print(result)
from collections import Counter
from typing import List


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """

        counts = [0] * (max(nums) + 1)

        for n in nums:
            counts[n] += 1

        index = 0
        for i in range(len(counts)):
            for j in range(counts[i]):
                nums[index] = i
                index += 1

        # The original list is modified in-place, so no need to return anything



    def findSmallest(self, arr):
        smallest = arr[0]
        smallest_index = 0

        for i in range(1, len(arr)):
            if smallest < arr[i]:
                smallest = arr[i]
                smallest_index = i

        return smallest_index

# Example usage of sortColors
nums = [5,6,7, 8, 9, 0, 1, 2, 3, 4, 6, 7, 7, 8, 8, 9, 0, 1, 2, 3, 4]

solution = Solution()
solution.sortColors(nums)

# Print the sorted list
print(nums)
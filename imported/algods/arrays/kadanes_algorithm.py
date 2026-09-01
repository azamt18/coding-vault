from typing import List


class Solution:
    def maxTurbulenceSize(self, arr: List[int]) -> int:
        n = len(arr)
        if n <= 2: return 1

        cur_size, max_size = 1, 1
        start, end = 0, 1
        for end in range(1, n):
            if end < n - 1 and (arr[end-1] < arr[end] > arr[end+1]) or (arr[end-1] > arr[end] < arr[end+1]):
                cur_size += 1
            else:
                cur_size = 1
            max_size = max(max_size, cur_size)

        return max_size

    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0: return 0
        if n == 1: return nums[0]

        max_sum, cur_max = nums[0], 0
        min_sum, cur_min = nums[0], 0
        total_sum = 0

        for n in nums:
            cur_max = max(cur_max + n, n)
            max_sum = max(max_sum, cur_max)

            cur_min = min(cur_min + n, n)
            min_sum = min(min_sum, cur_min)

            total_sum += n

        circular_max = total_sum - min_sum
        return max(max_sum, circular_max)

    """
    You'll want to implement the `maxSubarraySumCircular` method using a sliding window approach. For a circular array, you need to consider two cases:

    1. The maximum subarray is not circular (can be solved with standard Kadane's algorithm)
    2. The maximum subarray is circular (wraps around the array)
    
    For the second case, you can find the minimum subarray sum and subtract it from the total sum of the array, which gives you the maximum circular subarray.
    
    To implement this:
    1. Find the maximum subarray sum using Kadane's algorithm
    2. Find the minimum subarray sum using a modified Kadane's algorithm
    3. Calculate the total sum of the array
    4. The circular maximum is (total sum - minimum subarray sum)
    5. Return the maximum of the two cases (taking care of edge cases where all elements are negative)
    
    The sliding window technique will help you efficiently track both maximum and minimum subarrays in linear time complexity.
    """

    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)
        max_sum = nums[0]

        if len(nums) == 1:
            return nums[0]

        for i in range(n):
            cur_sum = 0
            for j in range(i, n):
                cur_sum += nums[j]
                max_sum = max(max_sum, cur_sum)

        return max_sum

nums = [9,4,2,10,7,8,8,1,9]
solution = Solution().maxTurbulenceSize(nums)
print(solution)
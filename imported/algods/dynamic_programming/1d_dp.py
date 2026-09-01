"""
bottom-up approach
"""
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        def dfs(i):
            if i >= len(nums):
                return 0
            if i == len(nums) - 1:
                return nums[i]
            if i == len(nums) - 2:
                return max(nums[i], nums[i + 1])
            return max(nums[i] + dfs(i + 2), dfs(i + 1))
        return dfs(0)

    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2
        dp = [0] * (n + 1)
        dp[1], dp[2] = 1, 2
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]

nums=[1,1,3,3]
solution = Solution().rob(nums)
print(solution)
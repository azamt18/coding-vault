from typing import List


class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        res = []

        # nums: [1,2,3], target: 6
        subset = []

        def dfs(i):
            if sum(subset) == target:
                res.append(subset.copy())
                return

            if i >= len(nums):
                return

            subset.append(nums[i])
            dfs(i + 1)

            subset.pop()
            dfs(i + 1)

        dfs(0)
        return res

    # def subsets(self, nums: List[int]) -> List[List[int]]:
    #     res = []
    #
    #     # [1,2,3]
    #     subset = []
    #
    #     def dfs(i):
    #         if i >= len(nums):
    #             res.append(subset.copy())
    #             return
    #
    #         # decision tree to include the number
    #         subset.append(nums[i])
    #         dfs(i + 1)
    #
    #         # decision tree to NOT include the number
    #         subset.pop()
    #         dfs(i + 1)
    #
    #     dfs(0)
    #     return res

    """
        backtracking
            - recursive approach
            - decision tree to include nums[i]
            - decision tree to not include nums[i]
    """
    def subsets(self, nums: List[int]) -> List[List[int]]:
        subsets, cur_subset = [], []
        self.helper(0, nums, subsets, cur_subset)
        return subsets

    def helper(self, i, nums, subsets, cur_subset):
        # base case
        if i >= len(nums):
            subsets.append(cur_subset.copy())
            return

        # decision to include nums[i]
        cur_subset.append(nums[i])
        self.helper(i + 1, nums, subsets, cur_subset)
        cur_subset.pop()

        # decision to not include nums[i]
        self.helper(i + 1, nums, subsets, cur_subset)

nums = [1,2,3]
solution = Solution()
res = solution.subsets(nums)
print(res)




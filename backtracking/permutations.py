from typing import List


class Solution:
    def permute_iter(self, nums: List[int]) -> List[List[int]]:
        perms = [[]]

        for n in nums:
            next_perm = []
            for p in perms:
                for i in range(len(p) + 1):
                    p_copy = p.copy()
                    p_copy.insert(i, n)
                    next_perm.append(p_copy)
            perms = next_perm

        return perms

    def permute_recur(self, nums: List[int]) -> List[List[int]]:
        def helper(curr_perm: List[int], available_elements: List[int]):
            # base case
            if len(available_elements) == 0:
                res.append(curr_perm.copy())
                return

            # recursive case
            for i in range(len(available_elements)):
                # choose
                curr_el = available_elements[i]
                curr_perm.append(curr_el)

                # explore
                helper(curr_perm, available_elements[:i] + available_elements[i+1:])

                # unchoose (backtrack)
                curr_perm.pop()

        res = []

        helper([], nums)
        return res

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        visited = set()

        def helper(i, nums):
            if i == len(nums):
                return [[]]

            perms = []
            curr_perms = helper(i + 1, nums)
            for p in curr_perms:
                for j in range(len(p) + 1):
                    p_copy = p.copy()
                    p_copy.insert(j, nums[i])
                    p_tuple = tuple(p_copy)
                    if p_tuple not in visited:
                        perms.append(p_copy)
                        visited.add(p_tuple)

            return perms

        return helper(0, nums)
sol = Solution()
sol.permuteUnique([1,2,3])
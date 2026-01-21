from typing import List


def permute(nums: List[int]) -> List[List[int]]:
    result = []

    def backtrack(acc, used):
        if len(acc) == len(nums):
            result.append(acc[:])
            return

        for n in nums:
            if n not in used:
                acc.append(n)
                used.add(n)
                backtrack(acc, used)

                acc.pop()
                used.remove(n)

    backtrack([], set())

    return result
permute([1,2,3])


# combinations
# ( n )          n!
# ( - ) =  -------------
# ( k )    k! * (n - k)!
def combine(self, n: int, k: int) -> List[List[int]]:
    result = []

    def backtrack(acc, start):
        # base
        if len(acc) == k:
            result.append(acc[:])
            return

        for num in range(start, n + 1):
            acc.append(num)

            backtrack(acc, num + 1)

            acc.pop()

    backtrack([], 1)

    return result

def subsets(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    result = []

    def backtrack(acc, start):
        # base
        if start >= n:
            return

        result.append(acc[:])

        for i in range(start, n):
            acc.append(nums[i])
            backtrack(acc, i + 1)
            acc.pop()

    backtrack([], 0)

    return result
subsets([1,2,3])

# https://leetcode.com/problems/combination-sum/
def combinationSum(candidates: List[int], target: int) -> List[List[int]]:
    result = []

    def backtracking(start, acc, path_sum):
        if path_sum == target:
            result.append(acc[:])
            return

        if path_sum > target:
            return

        while start < len(candidates):
            num = candidates[start]

            acc.append(num)
            backtracking(start, acc, path_sum + num)
            acc.pop()

            start += 1

    backtracking(0, [], 0)

    return result

# https://leetcode.com/problems/combination-sum-ii/
def combinationSum2(candidates: List[int], target: int) -> List[List[int]]:
    candidates.sort()
    result = []

    def bt(start, acc, path_sum):
        if path_sum == target:
            result.append(acc[:])
        if path_sum > target:
            return

        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i-1]:
                continue

            acc.append(candidates[i])
            bt(start + 1, acc, path_sum + candidates[i])
            acc.pop()

    bt(0, [], 0)

    return result
from typing import List


def productExceptSelf(nums: List[int]) -> List[int]:
    prefix = [0] * len(nums)
    product = 1
    for i in range(len(nums)):
        product *= nums[i]
        prefix[i] = product

    postfix = [0] * len(nums)
    product = 1
    for i in range(len(nums) - 1, -1, -1):
        product *= nums[i]
        postfix[i] = product

    output = [0] * len(nums)
    for i in range(len(nums)):
        left = prefix[i - 1] if i > 0 else 1
        right = postfix[i + 1] if i < len(nums) - 1 else 1
        output[i] = left * right

    return output


nums=[-1,0,1,2,3]
res = productExceptSelf(nums)
print(res)

def subarraySum(nums: List[int], k: int) -> int:
    sum = 0
    count = 0
    L = 0
    for R in range(len(nums)):
        if nums[R] == k or sum == k:
            sum = 0
            count += 1
            continue
        sum += nums[R]
    return count

nums = [1,1,1]
res = subarraySum(nums, 2)
print(res)

class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        self.prefix_sum = []

        ROWS, COLS = len(matrix), len(matrix[0])
        for r in range(ROWS):
            total = 0
            row = []
            for c in range(COLS):
                total += matrix[r][c]
                row.append(total)
            self.prefix_sum.append(row)

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        total_sum = 0
        for r in range(row1, row2 + 1):
            pre_right = self.prefix_sum[r][col2]
            pre_left = self.prefix_sum[r][col1 - 1] if col1 > 0 else 0
            total_sum += pre_right - pre_left
        return total_sum
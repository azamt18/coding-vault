from typing import List


def applyOperations(nums: List[int]) -> List[int]:
    for i in range(len(nums)):
        if i + 1 < len(nums) and nums[i] == nums[i + 1]:
            nums[i] = nums[i] * 2
            nums[i + 1] = 0

    # LR
    # [1694,    399,    0,  0,  0,  832,    1758,   0,  412,    0,  206,    0,  272,    0]
    # L = LEFT = empty slot = [0]
    # R = RIGHT = non zero slot = [1], [2], [1]
    L, R = 0, 0
    while R < len(nums):
        if nums[R] != 0 and nums[L] == 0 and L != R:
            nums[L] = nums[R]
            nums[R] = 0
            L += 1
        # else:
        #     L = R
        # L += 1

        if nums[L] != 0 and nums[R] == 0:
            L = R

        R += 1

    return nums
nums = [847,847,0,0,0,399,416,416,879,879,206,206,206,272]
res = applyOperations(nums)
print(res)

def maxArea(heights: List[int]) -> int:
    arr = heights
    left, right = 0, len(arr) - 1
    res = 0
    while left < right:
        area = min(arr[left], arr[right]) * (right - left)
        res = max(res, area)
        if arr[left] <= arr[right]:
            left += 1
        else:
            right -= 1

    return res

height=[1,7,2,5,4,7,3,6]
res = maxArea(height)
print(res)
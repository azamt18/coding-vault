from typing import List

# 153. Find Minimum in Rotated Sorted Array
def findMin(nums: List[int]) -> int:
    left, right = 0, len(nums) - 1

    while left < right:
        pivot = left + (right - left) // 2

        if nums[pivot] > nums[right]:
            left = pivot + 1
        else:
            right = pivot

    return right

# [1,2,1,3,5,6,4]
def findPeakElement(nums: List[int]) -> int:
    left, right = 0, len(nums) - 1

    while left < right: # 5 < 6
        mid = left + (right - left) // 2  #  5

        # upward slope
        if nums[mid] < nums[mid + 1]:
            left = mid + 1 # 6
        # downward slope
        elif nums[mid] > nums[mid + 1]:
            right = mid # 6

    return right

def arrangeCoins(n: int) -> int:
    left, right = 0, n
    while left < right:
        mid = left + (right - left) // 2 # middle

        coins_needed = mid * (mid + 1) // 2 # based on the k * (k + 1) / 2

        if coins_needed == n:
            return mid
        elif coins_needed < n:
            left = mid + 1
        else:
            right = mid - 1

    return right

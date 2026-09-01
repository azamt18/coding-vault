from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) >> 1 # bitwise right shift
            # mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid
            elif target > nums[mid]:
                left = mid + 1
            elif target < nums[mid]:
                right = mid - 1
        return - 1


# Example usage of sortColors
nums=[-1,0,2,4,6,8]
target=4

solution = Solution()
res = solution.search(nums, target)

# Print the sorted list
print(res)
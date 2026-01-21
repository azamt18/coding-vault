from typing import List


def isMonotonic(nums: List[int]) -> bool:
    if len(nums) <= 1:
        return False

    # find first 2 different values
    L, R = 0, 1
    if nums[L] == nums[R]:
        while R < len(nums) - 1 and nums[L] == nums[R]:
            L += 1
            R += 1

    is_increasing_monotonic = nums[L] <= nums[R]

    while R in range(1, len(nums)):
        if is_increasing_monotonic:
            if not nums[L] <= nums[R]:
                return False
        else:
            if not nums[L] >= nums[R]:
                return False
        L += 1
        R += 1

    return True
nums = [1,1,0]
res = isMonotonic(nums)
print(res)


# heights = [2, 1, 5, 6, 2, 3]
def largestRectangleArea(self, heights: List[int]) -> int:
    stack = [] # monotonic stack to store indices
    max_area = 0 # variable to track the maximum area

    for i, h in enumerate(heights):
        # process bars in the stack if the current bar is shorter
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()] # height of the rectangle
            width = i - stack[-1] - 1 if stack else i # width of the rectangle
            max_area = max(max_area, height * width)

        stack.append(i) # push the current index onto the stack

    # process remaining bars in the stack
    n = len(heights)
    while stack:
        height = heights[stack.pop()]
        width = n - stack[-1] if stack else n
        max_area = max(max_area, height * width)

    return max_area

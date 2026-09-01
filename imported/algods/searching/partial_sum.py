from typing import List


def maxSubArray(nums: List[int]) -> int:
    # init the max subarray with the first element
    max_sum = cur_sum = nums[0]
    for num in nums[1:]:
        # update cur_sum by max of cur_sum + num and num
        # or reset to the current number if current sum is negative
        cur_sum = max(cur_sum + num, num)

        # update max subarray sum if current sum is greater
        max_sum = max(max_sum, cur_sum)
    return max_sum
# res = maxSubArray([-2,1,-3,4,-1,2,1,-5,4])
# print(res)

class NumArray:
    def __init__(self, nums: List[int]):
        self.total = 0
        self.prefix_sums = [0] * len(nums)
        self.prefix_sums[0] = nums[0]
        for i in range(1, len(nums)):
            self.prefix_sums[i] = nums[i] + self.prefix_sums[i-1]

    # prefix_sums:  [-2,-2, 1,-4,-2,-3]
    # nums:         [-2, 0, 3,-5, 2,-1]
    #                 0, 1, 2, 3, 4, 5
    def sumRange(self, left: int, right: int) -> int:
        prefix_sum_right = self.prefix_sums[right]
        prefix_sum_left = self.prefix_sums[left - 1] if left >= 1 else 0
        return prefix_sum_right - prefix_sum_left

# numArray = NumArray([-2, 0, 3, -5, 2, -1])
# numArray.sumRange(0, 2) #  return (-2) + 0 + 3 = 1
# numArray.sumRange(2, 5) #  return 3 + (-5) + 2 + (-1) = -1
# numArray.sumRange(0, 5) #  return (-2) + 0 + 3 + (-5) + 2 + (-1) = -3
# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)

class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        ROWS, COLS = len(matrix), len(matrix[0])
        self.prefix_matrix = []
        for row in range(ROWS):
            row_sum = 0
            prefix_row = []
            for col in range(COLS):
                row_sum += matrix[row][col]
                prefix_row.append(row_sum)
            self.prefix_matrix.append(prefix_row)

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        region_sum = 0
        for row in range(row1, row2 + 1):
            # get the prefix sum of this row within given columns
            prefix_row = self.prefix_matrix[row]
            prefix_col2 = prefix_row[col2]
            prefix_col1 = prefix_row[col1 - 1] if col1 > 0 else 0
            region_sum += prefix_col2 - prefix_col1
        return region_sum
# numMatrix = NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]);
# numMatrix.sumRegion(2, 1, 4, 3) #  return 8 (i.e sum of the red rectangle)
# numMatrix.sumRegion(1, 1, 2, 2) #  return 11 (i.e sum of the green rectangle)
# numMatrix.sumRegion(1, 2, 2, 4) #  return 12 (i.e sum of the blue rectangle)
# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# param_1 = obj.sumRegion(row1,col1,row2,col2)


def subarraySum(nums: List[int], k: int) -> int:
    prefix_sums = {0: 1}
    count = running_sum = 0
    for num in nums:
        running_sum += num  # 3
        complement = running_sum - k  # 3 - 2 = 1
        if complement in prefix_sums:
            count += prefix_sums[complement]  # 1
        prefix_sums[running_sum] = prefix_sums.get(running_sum, 0) + 1

    return count
res = subarraySum([1,1,1], 1)
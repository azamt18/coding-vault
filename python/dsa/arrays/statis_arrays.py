# Insert n into index i after shifting elements to the right.
# Assuming i is a valid index and arr is not full.
def insertMiddle(arr, i, n, length):
    # Shift starting from the end to i.
    for index in range(length - 1, i - 1, -1):
        arr[index + 1] = arr[index]
    
    # Insert at i
    arr[i] = n


from typing import List # used to add type hint for List

def count_x(nums: List[int], x: int) -> int:
    count = 0
    for i in nums:
        if i == x: 
            count += 1 
    return count



# do not modify below this line
print(count_x([1, 2, 5, 6, 5], 5))
print(count_x([4, 3, 6, 1, 6], 5))
print(count_x([4, 7, 7, 6, 7, 6], 7))


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        tmp = [num == val for num in nums]
        for i in range(len(tmp)):
            nums[i] = tmp[i]
        return len(tmp)

class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [0] * (2 * n)  # Initialize result with the correct size
        for i in range(len(nums)):
            result[i], result[i+n] = nums[i], nums[i]
        return result




# https://leetcode.com/problems/circular-array-loop/description/
from typing import List


def circularArrayLoop(nums: List[int]) -> bool:
    n = len(nums)

    def next_index(i):
        return (i + nums[i]) % n

    for i in range(n):
        if nums[i] == 0:
            continue

        slow, fast = i, next_index(i)
        while nums[slow] * nums[fast] > 0 and  nums[slow] * nums[next_index(fast)] > 0:
            if slow == fast:
                if slow == next_index(slow):
                    break
                return True

            slow = next_index(slow)
            fast = next_index(next_index(fast))

        slow = i
        while nums[slow] * nums[next_index(slow)] > 0:
            next_i = next_index(slow)
            nums[slow] = 0
            slow = next_i

    return False
print(circularArrayLoop([2,-1,1,2,2]))
print(circularArrayLoop([1,1,1,1,1,1,1,1,1,-5])) # expected False
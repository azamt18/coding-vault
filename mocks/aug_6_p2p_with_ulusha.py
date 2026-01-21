from collections import Counter
from typing import List


def minIncrementForUnique(nums: List[int]) -> int:
    # nums.sort()
    # steps = 0
    #
    # for i in range(1, len(nums)):
    #     if nums[i] <= nums[i - 1]:
    #         increment = nums[i - 1] - nums[i] + 1
    #         nums[i] += increment
    #         steps += increment
    #
    # return steps

    freq = Counter(nums)
    steps = 0

    # [3,2,1,2,1,7]
    # 3: 2
    # 2: 1
    # 1: 2
    # 7: 1

    # steps: 0 + 1

    for num in sorted(freq):
        while freq[num] > 1:
            next_num = num + 1
            freq[num] -= 1

            while next_num in freq:
                next_num += 1

            freq[next_num] += 1
            steps += next_num - num

    return steps
minIncrementForUnique([3,2,1,2,1,7])


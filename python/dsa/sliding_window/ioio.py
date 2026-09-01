from typing import List


def longestOnes(nums: List[int], k: int) -> int:
    begin = 0
    window_state = 0  # how many zeros in window
    result = 0

    for end in range(len(nums)):
        if nums[end] == 0:
            window_state += 1

        while window_state > k:  # window condition 0? > k
            if nums[begin] == 0:
                window_state -= 1
            begin += 1  # shrink window

        result = max(result, end - begin + 1)

    return result
longestOnes([1,1,1,0,0,0,1,1,1,1,0], 2)
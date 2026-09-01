from typing import List


def jump_game_two(nums):
    farthest_jump, current_jump, jumps = 0, 0, 0
    for i in range(len(nums) - 1):
        farthest_jump = max(farthest_jump, i + nums[i])

        if i == current_jump:
            jumps += 1
            current_jump = farthest_jump

    return jumps
jump_game_two([2,3,1,1,9])

# https://leetcode.com/problems/jump-game-ii/
# bfs approach
def jump(nums: List[int]) -> int:
    left, right, jumps = 0, 0, 0

    while right < len(nums) - 1:
        farthest_jump = 0

        for i in range(left, right + 1):
            farthest_jump = max(farthest_jump, i + nums[i])

        jumps += 1

        if farthest_jump >= len(nums):
            # we reach or pass the end
            return jumps

        left = right + 1
        right = farthest_jump

    return jumps
jump([2,1])

""" https://leetcode.com/problems/gas-station/ """
def canCompleteCircuit(gas: List[int], cost: List[int]) -> int:
    return 0
from typing import List


class Solution:
    """
    You are given two arrays, instructions and values, both of size n.
    You need to simulate a process based on the following rules:

    You start at the first instruction at index i = 0 with an initial score of 0.
    If instructions[i] is "add":
    Add values[i] to your score.
    Move to the next instruction (i + 1).
    If instructions[i] is "jump":
    Move to the instruction at index (i + values[i]) without modifying your score.
    The process ends when you either:

    Go out of bounds (i.e., i < 0 or i >= n), or
    Attempt to revisit an instruction that has been previously executed. The revisited instruction is not executed.
    Return your score at the end of the process.©leetcode
    """
    def calculateScore(self, instructions: List[str], values: List[int]) -> int:
        score = 0
        cur_index = 0
        n = len(values)
        visited = set()
        while 0 <= cur_index < n:
            if cur_index in visited:
                break
            visited.add(cur_index)
            if instructions[cur_index] == "add":
                score += values[cur_index]
                cur_index += 1
            elif instructions[cur_index] == "jump":
                cur_index += values[cur_index]
        return score
#// call calculateScore with ["jump","add","add","jump","add","jump"] and [2,1,3,1,-2,-3]
solution = Solution()
instructions = ["jump", "add", "add", "jump", "add", "jump"]
values = [2,1,3,1,-2,-3]
res = solution.calculateScore(instructions, values)
print(res)
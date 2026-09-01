from typing import List

# https://leetcode.com/problems/insert-interval/?envType=problem-list-v2&envId=assbvovv
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        if len(intervals) == 0:
            return [newInterval]
        merged = []
        n = len(intervals)
        i = 0

        # 1 2 3 4 5 6 7 8 9 10 11
        # # 1
        # [. .]
        #         [.   .]
        # # 2
        #                    [. .]
        #         [.   .]
        # # 3
        #     [.  .]
        #         [.   .]
        # # 4
        #           [..]
        #         [.    .]
        # # 5
        #            [.  .]
        #         [.   .]

        while i < n and newInterval[0] > intervals[i][1]:
            merged.append(intervals[i])
            i += 1

        while i < n and ((newInterval[0] <= intervals[i][0] <= newInterval[1]) or
                         (newInterval[0] >= intervals[i][0] and newInterval[1] <= intervals[i][1]) or
                         (intervals[i][0] <= newInterval[0] <= intervals[i][1] <= newInterval[1])):
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        merged.append(newInterval)

        while i < n:
            merged.append(intervals[i])
            i += 1

        return merged




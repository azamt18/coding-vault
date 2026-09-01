from collections import defaultdict
from typing import List


def merge(intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort(key=lambda x : x[0])
    # print(intervals) # [[1, 9], [2, 7], [3, 5], [4, 5], [5, 18], [8, 9]]
    result = [intervals[0]] # [1,9]
    for i in range(1, len(intervals)):
        # get last added interval
        last_start, last_end = result[-1] # [1,9]
        current_start, current_end = intervals[i][0], intervals[i][1] # [2,7]
        if last_end >= current_start:
            final_start, final_end = last_start, current_end if current_end > last_end else last_end
            result[-1] = [final_start, final_end]
        else:
            result.append([current_start, current_end])

    return result
# res = merge([[8,9],[4,5],[1,9],[2,7],[3,5],[5,18]])
# res = merge([[1,3],[2,6],[8,10],[15,18]])
# print(res)

def merge(intervals: List[List[int]]) -> List[List[int]]:
    mp = defaultdict(int)
    for start, end in intervals:
        mp[start] += 1
        mp[end] -= 1

    result = []
    have = 0
    interval = []

    for i in sorted(mp):
        if not interval:
            interval.append(i)

        have += mp[i]
        if have == 0:
            interval.append(i)
            result.append(interval)
            interval = []

    return result
# res = merge([[8,9],[4,5],[1,9],[2,7],[3,5],[5,18]])
# res = merge([[1,3],[2,6],[8,10],[15,18]])
# print(res)


def insert(intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
    result = []
    i, n = 0, len(intervals)

    # intervals = [[1,2],[3,5],[9,10]], newInterval = [6,7]
    # intervals = [[1,3],[4,6]], newInterval = [2,5]
    #             [[1,3],[2,5],[4,6]]
    # case 1: no overlapping before merging intervals
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1

    # case 2: overlapping and merging intervals
    #             [[1,3],[2,5],[4,6]]
    #             [[1,5],[4,6]]
    #             [[1,6]]
    while i < n and newInterval[1] >= intervals[i][0]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)

    # case 3: no overlapping after merging intervals
    while i < n:
        result.append(intervals[i])
        i += 1

    return result

    # case 1: we've appended all intervals
    # case 2: reached intervals[i][0] > newInterval[1]
    # case 3: find overlapping interval
# res = insert([[1,3],[4,6]], [2,5])
# print(res)


# input = [[1,2],[2,4],[1,4]]
# sorted = [[1,2],[1,4],[2,4]]
# prevEnd = 1
# intervals = [[1,2],[1,1],[2,4]]
def eraseOverlapIntervals(intervals: List[List[int]]) -> int:
    if len(intervals) == 1:
        return 0

    count = 0
    intervals.sort(key=lambda x: x[0])
    prevEnd = intervals[0][1]

    for start, end in intervals[1:]:
        # check for overlapping
        if prevEnd > start:
            prevEnd = min(prevEnd, end)  # 1
            count += 1  # 1
        else:
            prevEnd = end

    print(intervals)

    return count
# res = eraseOverlapIntervals([[1,2],[2,4],[1,4]])
# print(res)

# https://leetcode.com/problems/the-skyline-problem/
def getSkyline(buildings: List[List[int]]) -> List[List[int]]:
    max_x = max(b[1] for b in buildings)
    skyline = [0] * (max_x + 1)

    for x, y, height in buildings:
        for i in range(x, y):
            skyline[i] = max(skyline[i], height)

    result = []
    prev_height = 0
    for i, height in enumerate(skyline):
        if height != prev_height:
            result.append([i, height])
            prev_height = height

    return result


print(getSkyline([[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]])) # expected [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]
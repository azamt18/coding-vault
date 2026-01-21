import heapq
from collections import defaultdict
from typing import List


def dfs_recursive_adj_list(graph, node, visited):
    if not visited[node]:
        print(node, end=' ')
        visited[node] = True

        for neighbor in graph[node]:
            dfs_recursive_adj_list(graph, neighbor, visited)


# Example Usage:
graph_adj_list = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 5],
    3: [1],
    4: [1],
    5: [2]
}
visited = [False] * len(graph_adj_list)
dfs_recursive_adj_list(graph_adj_list, 0, visited)

def dfs_recursive_adj_matrix(graph, node, visited):
    if not visited[node]:
        print(node, end=' ')
        visited[node] = True
        for neighbor in range(len(graph[node])):
            if graph[node][neighbor] == 1:
                dfs_recursive_adj_matrix(graph, neighbor, visited)

# Example Usage:
graph_adj_matrix = [
    [0, 1, 1, 0, 0, 0],  # Node 0 connections
    [1, 0, 0, 1, 1, 0],  # Node 1 connections
    [1, 0, 0, 0, 0, 1],  # Node 2 connections
    [0, 1, 0, 0, 0, 0],  # Node 3 connections
    [0, 1, 0, 0, 0, 0],  # Node 4 connections
    [0, 0, 1, 0, 0, 0],  # Node 5 connections
]
visited = [False] * len(graph_adj_matrix)
dfs_recursive_adj_matrix(graph_adj_matrix, 0, visited)

# https://leetcode.com/problems/number-of-islands/
"""
    Approach: 
        1. iterate through each cell. When 'land' and unvisited cell is found -> start dfs from that point, increment islands count
        2. in dfs:
            2.1. make boundary checks + water cell + already visited cell
            2.2. mark cell as visited
            2.3. explore cell in 4 directions -> continue dfs(r + dr, c + dc)
    DS: visited() set 
    
    Time: O(V) for processing all vertices, O(V^2) for checking all edges --> O(V^2)  
    Space: O(V) for visited set, O(V) for call stack
"""
def numIslands(grid: List[List[str]]) -> int:
    if not grid:
        return 0

    # grid dimensions
    ROWS, COLS = len(grid), len(grid[0])

    # directions
    DIRECTIONS = [
        [-1, 0], # up
        [0, 1],# right
        [1, 0], # down
        [0, -1], # left
    ]

    # visited set
    visited = set()

    # count islands
    islands = 0

    # iterative DFS function
    def dfs(r, c):
        stack = [(r, c)]

        visited.add((r, c))

        while stack:
            current_row, current_col = stack.pop()

            for dr, dc in DIRECTIONS:
                new_row, new_col = current_row + dr, current_col + dc

                if (0 <= new_row < ROWS and
                    0 <= new_col < COLS and
                    grid[new_row][new_col] == '1' and
                    (new_row, new_col) not in visited):

                    visited.add((new_row, new_col))

                    # add to stack for further explorations
                    stack.append((new_row, new_col))

    # recursive DFS function
    # def dfs(r, c):
    #     # base cases:
    #     # 1. out of bounds
    #     if (r < 0 or r >= ROWS
    #         or c < 0 or c >= COLS):
    #         return
    #     # 2. water cell ('0')
    #     elif grid[r][c] == '0':
    #         return
    #     # 3. already visited cell
    #     elif (r, c) in visited:
    #         return
    #
    #     # mark cell as visited
    #     visited.add((r, c))
    #
    #     # explore in all four directions
    #     for dr, dc in DIRECTIONS:
    #         dfs(r + dr, c + dc)

    # main loop to iterate through the entire grid
    for i in range(ROWS):
        for j in range(COLS):
            # for each not visited cell:
            if grid[i][j] == '1' and (i ,j) not in visited:
                # 1. start dfs from the cell
                dfs(i, j)
                # 2. increment islands count
                islands += 1

    return islands

# https://leetcode.com/problems/reconstruct-itinerary/
class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        # build adjacency list
        graph = defaultdict(list)
        for source, destination in tickets:
            graph[source].append(destination)

        for airport in graph:
            graph[airport].sort()
        print(graph)

        res = []
        def dfs(airport):
            # while there are destinations from the current airport
            while graph[airport]:
                # get next destination
                next_dst = graph[airport].pop(0)
                dfs(next_dst)

            res.append(airport)

        dfs("JFK")

        res.reverse()
        return res

        # return res[::-1]

        # return list(reversed(res))

        # reversed_list = []
        # for item in res:
        #     reversed_list.insert(0, item)
        # return reversed_list

        # reversed_list = [res[i] for i in range(len(res) - 1, -1, -1)]
        # return reversed_list

        # from functools import reduce
        # reversed_list = reduce(lambda acc, x: [x] + acc, res, [])
        # return reversed_list

print('\n--------\n')
sol = Solution().findItinerary([["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]])
print(sol)

# https://leetcode.com/problems/course-schedule-ii/
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # visited statuses
        # 0 = not visited, 1 = currently visited [in stack], 2 = completely visited
        visited = [0 for _ in range(numCourses)]

        graph = defaultdict(list)
        for a, b in prerequisites:
            graph[b].append(a)

        res = []

        # to detect cycle: cycle found -> false, not found -> true
        def dfs(course):
            if visited[course] == 1: # if currently in stack
                return False # found cycle

            # already visited and processed -> skip
            if visited[course] == 2:
                return True

            visited[course] = 1 # mark as being visited

            # check neighbors
            for next_course in graph[course]:
                if not dfs(next_course): # if cycle detected in neighbor
                    return False

            visited[course] = 2 # mark as completely visited

            res.append(course)

            return True # course can be taken

        # dfs from each course
        for course in range(numCourses):
            # only start dfs from unvisited nodes
            if visited[course] == 0:
                if not dfs(course): # if cycle detected
                    return []

        return res[::-1]
print('\n--------\n')
sol = Solution().findOrder(4, [[1,0],[2,0],[3,1],[3,2]])
print(sol)

"""
    Notes: finish all courses means no cycle detected
    Approach: detect cycle using dfs from each course
        1. build necessary structures to use them further
            1.1. collect graph of courses [adj list] where graph[course] contains all courses requiring 'course' as prerequisite 
            1.2. generate stack of courses with unvisited status
            1.3. define visiting statuses: 0 = not visited, 1 = currently visiting (in stack), 2 = already visited

        2. define dfs as:
            2.1. check for visiting statuses, continue only on unvisited(0)
            2.2. call dsf on every neighbor to detect if it has a cycle
                    if found -> false
            2.3. mark current course as already visited(2), append to result

        3. call dfs on each course
"""


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:

        graph = defaultdict(list)
        for a, b in prerequisites:
            graph[b].append(a)

        visited = [0 for _ in range(numCourses)]
        # visited statuses
        # 0 = not visited, 1 = currently visiting (in stack), 2 = already visited

        res = []

        # to detect cycle, if cycle found -> false, not found -> true
        def dfs(course):
            if visited[course] == 1:  # if currently in stack
                return False

            if visited[course] == 2:  # if already completed[visited]
                return True

            visited[course] = 1 # mark as being visited [in recursion stack]

            # check every neighbor (next_course)
            for next_course in graph[course]:
                if not dfs(next_course):  # cycle found in neighbor
                    return False

            # mark as visited
            visited[course] = 2

            # append course to result
            res.append(course)

            return True  # course can be taken

        # dfs from each course
        for course in range(numCourses):
            if visited[course] == 0:
                if not dfs(course):
                    return []

        return res[::-1]  # reversing in necessary because courses were appended from end
print('\n--------\n')
sol = Solution().findOrder(2, [[0,1],[1,0]])
print(sol)

"""
Definition of Interval:
class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
"""
class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


# Example 1:
# Input: intervals = [[0,30],[5,10],[15,20]]   ///   0 - 30 ,  5  - 10 , 10 - 20 ,
# Output: 2

# // 0  — 10   5 — 15   20 - 30 	  25 - 35
# max = 0
# // PQ:
# [(end, idx)]
# 10
# size = max(max, len(pq)) -> 1
# 10, 15
# 30

# 5 & 10 -> overlapping -> put to PQ
# size = max(size, len(pq)) -> 2

# 15 & 20 -> non-overlapping ->
# while 20 & top PQ -> <compare start>
# (20 & 10 ) ::  if non-overlapping -> pop top [10]
# (20 & 15) ::  if non-overlapping -> pop top [15]
# <push end> 30 to PQ
# size = max(size, len(pq)) -> 2

# 	30 & 25 -> overlapping -> push to PQ
# size = max(size, len(pq)) -> 2

# return size

class Solution:
    def minMeetingRooms(self, intervals: List[int]) -> int:
        if len(intervals) <= 1:
            return 1

        intervals.sort(key=lambda interval: interval[0])

        size = 0
        queue = []
        heapq.heappush(queue, intervals[0][1])
        size = max(size, len(queue))

        for i in range(1, len(intervals)):
            curr_start, curr_end = intervals[i]
            while queue and curr_start >= queue[0]:  # non-overlapping
                heapq.heappop(queue)
            heapq.heappush(queue, curr_end)
            size = max(size, len(queue))

        return size
print('\n--------\n')
sol = Solution().minMeetingRooms([(0,10),(5,15),(20,30),(25,35)])
print(sol)


class Solution:
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        adjList = {}
        for s, d in connections:
            if s in adjList:
                adjList[s].append(d)
            else:
                adjList[s] = [d]
            if d in adjList:
                adjList[d].append(s)
            else:
                adjList[d] = [s]

        globalVisited = set()
        criticalConnections = []

        def tryTraverseWithoutConnection(graph, startNode, candidate):
            def dfs(node):
                visited = set()
                stack = [node]

                while stack:
                    node = stack.pop()

                    # if node not in visited:
                    #     visited.add(node)

                    for neighbor in graph[node]:
                        if (node == startNode and neighbor == candidate) or (neighbor in visited):
                            continue

                        visited.add(neighbor)
                        stack.append(neighbor)

                return len(visited)

            visitedNodes = dfs(startNode)
            if visitedNodes != n and (
                    (startNode, candidate) not in globalVisited or (candidate, startNode) not in globalVisited):
                criticalConnections.append([startNode, candidate])
                globalVisited.add((startNode, candidate))
                globalVisited.add((candidate, startNode))

            return

        for node in adjList:
            for neighbor in adjList[node]:
                tryTraverseWithoutConnection(adjList, node, neighbor)

        return criticalConnections
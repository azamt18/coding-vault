from collections import deque
from typing import List



class Solution:

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        q = deque()
        visited = set()
        max_area = 0

        def bfs(r, c) -> int:
            q.append((r, c))
            visited.add((r, c))
            area = 1

            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            while q:
                for i in range(len(q)):
                    r, c = q.popleft()
                    for dr, dc in directions:
                        row, col = r + dr, c + dc
                        if (row < 0 or row == ROWS or
                                col < 0 or col == COLS or
                                (row, col) in visited or
                                grid[row][col] == 0):
                            continue
                        q.append((row, col))
                        visited.add((row, col))
                        area += 1
            return area

        ROWS, COLS = len(grid), len(grid[0])
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 1 and (r, c) not in visited:
                    area = bfs(r, c)
                    max_area = max(max_area, area)

        return max_area

    def orangesRotting(self, grid: List[List[int]]) -> int:
        q = deque()
        time, fresh = 0, 0
        ROWS, COLS = len(grid), len(grid[0])

        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 1:
                    fresh += 1
                elif grid[r][c] == 2:
                    q.append((r, c))

        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        while q and fresh > 0:
            for i in range(len(q)):
                r, c = q.popleft()
                for dr, dc in directions:
                    row, col = r + dr, c + dc
                    if (row < 0 or row == ROWS or
                            col < 0 or col == COLS or
                            grid[row][col] != 1):
                        continue

                    grid[row][col] = 2
                    q.append((row, col))
                    fresh -= 1
            time += 1
        return time if fresh == 0 else -1
# grid=[[2,1,1],[1,1,0],[0,1,1]]
# grid = [[1, 1, 0], [0, 1, 1], [0, 1, 2]]
# solution = Solution()
# result = solution.orangesRotting(grid)
# print(result)

    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        ROWS, COLS = len(grid), len(grid[0])
        if grid[0][0] == 1 or grid[ROWS - 1][COLS - 1] == 1:
            return -1

        visited = {0, 0}
        queue = deque([(0, 0)])
        length = 0

        while queue:
            length += 1
            for i in range(len(queue)):
                r, c = queue.popleft()
                if r == ROWS - 1 and c == COLS - 1:
                    return length

                directions = [
                    [0, 1], [0, -1], [1, 0], [-1, 0],
                    [-1, -1], [-1, 1], [1, 1], [1, -1]
                ]
                for dr, dc in directions:
                    if (min(r + dr, c + dc) < 0 or
                            r + dr == ROWS or c + dc == COLS or
                            (r + dr, c + dc) in visited or
                            grid[r + dr][c + dc] == 1):
                        continue

                    visited.add((r + dr, c + dc))
                    queue.append((r + dr, c + dc))

        return -1

grid = [[0, 1, 1, 0, 1], [1, 0, 1, 0, 1], [0, 1, 1, 0, 1], [0, 1, 0, 0, 1]]
solution = Solution()
result = solution.maxAreaOfIsland(grid)
print(result)

# grid = [[0,0,0],[1,1,0],[1,1,0]]
# solution = Solution()
# result = solution.shortestPathBinaryMatrix(grid)
# print(result)

class Solution:
    def shortestPath(self, grid: List[List[int]]) -> int:
        ROWS, COLS = len(grid), len(grid[0])

        def bfs(grid) -> int:
            visited = set()
            queue = deque()
            visited.add((0, 0))
            queue.append((0, 0))

            length = 0
            while queue:
                for i in range(len(queue)):
                    r, c = queue.popleft()
                    if r == ROWS - 1 and c == COLS - 1:
                        return length

                    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
                    for dr, dc in directions:
                        if (min(r + dr, c + dc) < 0 or
                                r + dr == ROWS or c + dc == COLS or
                                grid[r + dr][c + dc] == 1 or
                                (r + dr, c + dc) in visited):
                            continue
                        visited.add((r + dr, c + dc))
                        queue.append((r + dr, c + dc))
                length += 1
            return length

        return bfs(grid)

# grid = [
#         [0, 0, 0, 0],
#         [1, 1, 0, 0],
#         [0, 0, 0, 1],
#         [0, 1, 0, 0]
#         ]
# grid = [[1, 1, 1],[1, 0, 1],[1, 1, 1]]
# solution = Solution()
# result = solution.shortestPath(grid)
# print(result)


class Solution:
    def islandsAndTreasure(self, grid: List[List[int]]) -> None:
        rows = len(grid)
        cols = len(grid[0])
        directions = [[0, 1], [1, 0], [-1, 0], [0, -1]]

        def isValid(r, c, visited):
            if r >= 0 and r < rows and c >= 0 and c < cols and (r, c) not in visited and grid[r][c] != -1 and grid[r][
                c] != 0:
                return True
            return False

        def helper(r, c):
            q = deque([(r, c, 0)])
            visited = set()

            while q:
                node = q.popleft()
                row, col, dist = node

                visited.add((r, c))

                # update the value of the cell
                if grid[row][col] > dist:
                    grid[row][col] = dist

                for dR, dC in directions:
                    nR = row + dR
                    nC = col + dC
                    if isValid(nR, nC, visited):
                        q.append((nR, nC, dist + 1))

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 0:
                    helper(r, c)

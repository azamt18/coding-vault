import heapq
from collections import deque
from typing import List


class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        if not image:
            return []

        ROWS, COLS = len(image), len(image[0])
        DIRECTIONS = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        visited = set()
        target_color = image[sr][sc]

        # def recursive_dfs(r, c):
        #     # checks
        #     # 1. out of bound
        #     if r < 0 or c < 0 or r > ROWS - 1 or c > COLS - 1:
        #         return
        #     # 2. target cell
        #     elif image[r][c] != target_color:
        #         return
        #     # 3. already visited
        #     elif (r, c) in visited:
        #         return
        #
        #     # mark as visited
        #     visited.add((r, c))
        #
        #     # explore neighbors
        #     for dr, dc in DIRECTIONS:
        #         recursive_dfs(r + dr, c + dc)
        #
        #     # update cell
        #     image[r][c] = color
        # start dfs
        # recursive_dfs(sr, sc)

        def iterative_dfs(r, c):
            visited.add((r, c))
            image[r][c] = color
            stack = [(r, c)]

            while stack:
                current_row, current_col = stack.pop()

                for dr, dc in DIRECTIONS:
                    new_row, new_col = dr + current_row, dc + current_col

                    # checks
                    # 1. out of bound
                    if new_row < 0 or new_col < 0 or new_row > ROWS - 1 or new_col > COLS - 1:
                        continue
                    # 2. target cell
                    elif image[new_row][new_col] != target_color:
                        continue
                    # 3. already visited
                    elif (new_row, new_col) in visited:
                        continue

                    # mark as visited
                    visited.add((new_row, new_col))

                    # update cell
                    image[new_row][new_col] = color

                    # push to stack for further explorations
                    stack.append((new_row, new_col))

        iterative_dfs(sr, sc)

        return image
sol = Solution().floodFill([[1,1,1],[1,1,0],[1,0,1]], 1, 1, 2)
print(sol)


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        if not grid:
            return -1

        if grid[0][0] == -1:
            return -1

        ROWS, COLS = len(grid), len(grid[0])
        DIRECTIONS = [
            [0, 1], [0, -1], [1, 0], [-1, 0],  # horizontally & vertically
            [1, 1], [1, -1], [-1, 1], [-1, -1]  # diagonally
        ]
        visited = {0, 0}
        queue = deque([(0, 0)])
        length = 0

        while queue:
            length += 1
            for i in range(len(queue)):
                current_row, current_col = queue.popleft()

                # check if we are at the end
                if current_row == ROWS - 1 and current_col == COLS - 1:
                    return length

                for dr, dc in DIRECTIONS:
                    new_row, new_col = dr + current_row, dc + current_col

                    # checks
                    # 1. out of bound
                    if new_row < 0 or new_col < 0 or new_row >= ROWS or new_col >= COLS:
                        continue
                    # 2. "clear" cell (equal to 0)
                    elif grid[new_row][new_col] != 0:
                        continue
                    # 3. not visited
                    elif (new_row, new_col) in visited:
                        continue

                    # mark as visited
                    visited.add((new_row, new_col))
                    # update counter
                    # push to stack for further exploration
                    queue.append((new_row, new_col))

        return -1
# sol = Solution().shortestPathBinaryMatrix([[0,0,0],[1,1,0],[1,1,0]]) # 4
# print(sol)
sol = Solution().shortestPathBinaryMatrix([[1,0,0],[1,1,0],[1,1,0]]) # -1
print(sol)



# https://leetcode.com/problems/path-with-minimum-effort/
class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        ROWS, COLS = len(heights), len(heights[0])
        DIRECTIONS = [[0, 1],[0, -1],[1, 0],[-1, 0]]

        # priority queue to store (effort, row, col) to use effort as priority
        pq = [(0, 0, 0)]

        # visited cells with their min effort
        efforts = {(0, 0): 0}

        while pq:
            current_effort, row, col = heapq.heappop(pq)

            # check if we are at the destination
            if row == ROWS - 1 and col == COLS - 1:
                return current_effort

            # if we've already found a better path, skip it
            if efforts[(row, col)] < current_effort and (row, col) in efforts:
                continue

            # explore neighbors
            for dr, dc in DIRECTIONS:
                nr, nc = dr + row, dc + col

                # check if neighbor is within boundaries
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    # calculate effort to move neighbor
                    new_effort = max(current_effort, abs(heights[row][col] - heights[nr][nc]))

                    # if we found better path
                    if (nr, nc) not in efforts or ((nr, nc) in efforts and new_effort < efforts[(nr, nc)]):
                        # update min effort
                        efforts[(nr, nc)] = new_effort

                        # add to pq for further exploration
                        heapq.heappush(pq, (new_effort, nr, nc))


        return -1
sol = Solution().minimumEffortPath([[1,2,2],[3,8,2],[5,3,5]])
print(sol)


# https://leetcode.com/problems/01-matrix/
class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        if not mat:
            return []

        ROWS, COLS = len(mat), len(mat[0])
        DIRECTIONS = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        # step 1: init result matrix and queue
        result = [[float('inf')] * COLS for _ in range(ROWS)]
        queue = deque()

        # step 2: find all 0s and add them to queue as starting points
        for i in range(ROWS):
            for j in range(COLS):
                if mat[i][j] == 0:
                    queue.append((i, j))
                    result[i][j] = 0

        # step 3: perform BFS from all 0s simultaneously
        while queue:
            row, col = queue.popleft()

            # check neighbors
            for dr, dc in DIRECTIONS:
                nr, nc = dr + row, dc + col

                # checks bounds
                if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLS:
                    continue

                # check distance
                if result[nr][nc] > result[row][col] + 1:
                    # update with shorter distance
                    result[nr][nc] = result[row][col] + 1

                    # add to queue for further exploration
                    queue.append((nr, nc))

        return result
sol = Solution().updateMatrix([[0,0,0],[0,1,0],[1,1,1]])
print(sol)


class Solution:
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        ROWS, COLS = len(grid), len(grid[0])
        DIRECTIONS = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        queue = deque([(0, 0, 0, 0)])   # (row, col, obstacles_removed, steps)
        visited = {(0, 0, 0)}           # (row, col, obstacles_removed)

        while queue:
            row, col, obstacles, steps = queue.popleft()

            if row == ROWS - 1 and col == COLS - 1:
                return steps

            for dr, dc in DIRECTIONS:
                nr, nc = dr + row, dc + col

                # check boundaries
                if nr < 0 or nc < 0 or nr >= ROWS or nc >= COLS:
                    continue

                # step 3: check if obstacle and if we can eliminate it
                if grid[nr][nc] == 1:
                    if obstacles >= k:
                        continue
                    new_obstacles = obstacles + 1
                else:
                    new_obstacles = obstacles

                # step 4: add to queue if state not visited before
                new_state = (nr, nc, new_obstacles)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((nr, nc, new_obstacles, steps + 1))


        return -1
sol = Solution().shortestPath([[0,1,1],[1,1,1],[1,0,0]], 1)
print(sol)

# https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/
"""
    Approach:
        1. Dijkstra: using PQ to process cells in order of increasing cost
        2. Cost calculation: 
            - if the sign matches with the direction we're going -> cost doesn't change
            - otherwise -> add 1 to cost
        3. Visited tracking: track visited cells with min cost
        4. Direction mapping

    DS: 
        1. priority queue to store (cost, row, col); we use cost as priority
        2. visited cells dict {(row, col): cost} with their min cost

    Time: O(m x n x log(m x n))
    Space: O(m x n) for PQ, O(m x n) for dict

    Q/A:
    How much time have I spent, end-to-end?
    - 4 h 55 minutes:
        1. https://leetcode.com/problems/flood-fill
            - [ Time taken: 16 m 32 s ] recursive dfs
            - [ Time taken: 11 m 54 s ] iterative dfs
        2. https://leetcode.com/problems/shortest-path-in-binary-matrix
            - [ Time taken: 25 m 6 s ] bfs
        3. https://leetcode.com/problems/path-with-minimum-effort
            - [ Time taken: 27 m 30 s ] modified dijkstra's, priority queue approach
        4. https://leetcode.com/problems/01-matrix/
            - [ Time taken: 20 m 1 s ] multi-source BFS
        5. https://leetcode.com/problems/shortest-path-in-a-grid-with-obstacles-elimination
            - ~[ Time taken: 1 h ] BFS with state
        6. https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/
            - [ Time taken: 42 m 25 s ] modified Dijkstra, Priority queue

    What were the trickiest aspects? Where did you lose the most time?
    - most tracking aspects - understanding how tracking min cost; lost time mostly on completing the "prerequisite" problems

    What are some lessons/insights I gained from this problem?
    - I applied the "Eat an elephant" technique: if problem seems hard, go and try a problem with a lower-level to gain a baseground skills/understanding, then combine those here

    What would I do differently if I had extra time? What’s remaining to improve?
    - I'd go to try similar or lower-level problems mostly <by my own>

    What did I do well?
    - "divide-and-conquer" as mentioned before

    Did you use any hints, if yes, what? (please do not give up and look up the hints quickly. if you do need to look up the hints, only use the ones given on the problem page one by one, and DON'T look at youtube videos or full solutions, until you try really hard)
    - Prompted to Claude to suggest a learning plan for problem. Prompt was: "I want to solve it by my own as much as possible. But I'm struggling now. Give a 1-2 hour plan to revise its prerequisite-problems so that after which it would be easier. Start from Easy level problem. Go harder step-by-step."

    How difficult was the problem (1 super trivial, 10 extremely difficult) (answer this question three times separately for a) implementing quickly b) finding the right approach c) overall)
    - 
        a) 5, took ~5 h with revising 5 "prerequisite" problems
        b) 3 before solving 5 problems, then became 7 after
        c) 9 before solving 5 problems, then became 7 after

    What's the time & space complexity?
    -   Time: O(m x n x log(m x n))
        Space: O(m x n) for PQ, O(m x n) for dict => O(m x n)
"""


class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        if not grid:
            return -1

        ROWS, COLS = len(grid), len(grid[0])
        # directions: right=1   left=2   down=3  up=4
        DIRECTIONS = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        # priority queue to store (cost, row, col); we use cost as priority
        pq = [(0, 0, 0)]

        # visited cells dict {(row, col): cost} with their min cost
        costs = {(0, 0): 0}

        while pq:
            cost, row, col = heapq.heappop(pq)

            # check if we are at the destination
            if row == ROWS - 1 and col == COLS - 1:
                return cost

            # skip we've already found a better way
            if (row, col) in costs and costs[(row, col)] < cost:
                continue

            # explore neighbors
            for i, (dr, dc) in enumerate(DIRECTIONS):
                nr, nc = dr + row, dc + col

                # check boundaries
                if nr < 0 or nc < 0 or nr >= ROWS or nc >= COLS:
                    continue

                # calculate new cost
                new_cost = cost
                if grid[row][col] != i + 1:
                    new_cost += 1

                # update cost if better path found
                if (nr, nc) not in costs or ((nr, nc) in costs and new_cost < costs[(nr, nc)]):
                    # update new min cost
                    costs[(nr, nc)] = new_cost

                    # push to queue for further explorations
                    heapq.heappush(pq, (new_cost, nr, nc))

        return -1

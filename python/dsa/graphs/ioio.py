import heapq
from collections import deque, defaultdict
from typing import List


def maxAreaOfIsland(grid: List[List[int]]) -> int:
    if not grid:
        return 0

    n = len(grid)
    m = len(grid[0])

    def is_valid(r, c):
        return (0 <= r < n and
                0 <= c < m and
                grid[r][c] == 1)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    seen = set()
    queue = deque()
    max_area = 0

    def bfs(i, j) -> int:
        queue.append((i,j))
        seen.add((i,j))
        current_area = 1
        while queue:
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if is_valid(nr, nc) and (nr, nc) not in seen:
                    current_area += 1

                    seen.add((nr, nc))
                    queue.append((nr, nc))

        return current_area

    for i in range(n):
        for j in range(m):
            if is_valid(i,j) and (i,j) not in seen:
                area = bfs(i,j)
                max_area = max(max_area, area)

    return max_area
maxAreaOfIsland([[0,0,1,0,0,0,0,1,0,0,0,0,0],
                 [0,0,0,0,0,0,0,1,1,1,0,0,0],
                 [0,1,1,0,1,0,0,0,0,0,0,0,0],
                 [0,1,0,0,1,1,0,0,1,0,1,0,0],
                 [0,1,0,0,1,1,0,0,1,1,1,0,0],
                 [0,0,0,0,0,0,0,0,0,0,1,0,0],
                 [0,0,0,0,0,0,0,1,1,1,0,0,0],
                 [0,0,0,0,0,0,0,1,1,0,0,0,0]])


def updateMatrix(mat: List[List[int]]) -> List[List[int]]:
    n = len(mat)
    m = len(mat[0])

    queue = deque()
    seen = set()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def is_valid(r, c):
        return (0 <= r < n and
                0 <= c < n and
                mat[r][c] == 1)

    for i in range(n):
        for j in range(m):
            if mat[i][j] == 0:
                queue.append((i, j, 1))
                seen.add((i, j))

    while queue:
        r, c, d = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and (nr, nc) not in seen:
                mat[nr][nc] = d
                seen.add((nr, nc))
                queue.append((nr, nc, d + 1))

    return mat
updateMatrix([[0,0,0],
              [0,1,0],
              [1,1,1]])


def nearestExit(maze: List[List[str]], entrance: List[int]) -> int:
    if not maze:
        return 0

    n = len(maze)
    m = len(maze[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def is_valid(r, c):
        return (0 <= r < n and
                0 <= c < m and
                maze[r][c] == ".")

    def is_exit(r, c):
        return r == 0 or r == n - 1 or c == 0 or c == m - 1

    e_r, e_c = entrance[0], entrance[1]
    queue = deque([(e_r, e_c, 0)])  # row, col, step
    # seen = {(entrance[0], entrance[1])}
    maze[e_r][e_c] = "+"

    while queue:
        row, col, step = queue.popleft()

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if is_valid(nr, nc):
                if is_exit(nr, nc):
                    return step + 1

                queue.append((nr, nc, step + 1))
                maze[nr][nc] = "+"

    return -1

nearestExit([["+","+","+"],[".",".","."],["+","+","+"]],[1,0])


def openLock(deadends: List[str], target: str) -> int:
    # 0201 0101 0102 1212 2002

    # 0000

    # 1000
    # 1100
    # 1200
    # 1201
    # 1202

    # 0202

    if "0000" in deadends:
        return -1

    queue = deque([("0000", 0)])
    seen = set(deadends)

    def neighbours(current_comb):
        result = []
        for i in range(4):
            num = int(current_comb[i])
            x = (num + 1) % 10
            result.append(current_comb[:i] + str(x) + current_comb[i + 1:])
            x = (num - 1) % 10
            result.append(current_comb[:i] + str(x) + current_comb[i + 1:])
        return result

    while queue:
        current_comb, steps = queue.popleft()
        if current_comb == target:
            return steps

        for n in neighbours(current_comb):
            if n not in seen:
                queue.append((n, steps + 1))
                seen.add(n)

    return -1

openLock(["0201","0101","0102","1212","2002"], "0202")


def networkDelayTime(times: List[List[int]], n: int, k: int) -> int:
    graph = defaultdict(list)
    for a, b, w in times:
        graph[a].append((b, w))

    distances = {k: 0}

    min_heap = []
    heapq.heappush(min_heap, (0, k))  # weight, node

    while min_heap:
        weight, node = heapq.heappop(min_heap)
        if weight > distances.get(node, float('inf')):
            continue

        for neighbor_node, neighbor_weight in graph[node]:
            next_weight = weight + neighbor_weight
            if next_weight < distances.get(neighbor_node, float('inf')):
                distances[neighbor_node] = next_weight
                heapq.heappush(min_heap, (next_weight, neighbor_node))

    if len(distances) != n:
        return -1

    return distances[max(distances, key=lambda x: distances[x])]
networkDelayTime([[1,2,1],[2,1,3]], 2, 2)
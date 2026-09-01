from typing import List


# https://leetcode.com/problems/surrounded-regions/
def solve(board: List[List[str]]) -> None:
    """
    Do not return anything, modify board in-place instead.
    """

    # 1. mark all border-connected 'O' cells
    # 2. flip interior 'O' cells to 'X'
    # 3. restore safe cells

    rows, cols = len(board), len(board[0])
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    def mark_safe(r, c):
        if (0 <= r < rows and
            0 <= c < cols and
            board[r][c] == 'O'):

            board[r][c] = '#'
            for dr, dc in directions:
                new_row, new_col = r + dr, c + dc
                mark_safe(new_row, new_col)

    # 1
    for col in range(cols):
        if board[0][col] == 'O':
            # board[0][col] = '#'
            mark_safe(0, col)
        if board[rows-1][col] == 'O':
            # board[rows-1][col] = '#'
            mark_safe(rows-1, col)
    for row in range(rows):
        if board[row][0] == 'O':
            # board[row][0] = '#'
            mark_safe(row, 0)
        if board[row][cols-1] == 'O':
            # board[row][cols-1] = '#'
            mark_safe(row, cols-1)

    # 2
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 'O':
                board[i][j] = 'X'

    # 3
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == '#':
                board[row][col] = 'O'

    print(board)


solve(board = [
  ["X","X","X","X"],
  ["X","O","O","X"],
  ["X","O","O","X"],
  ["X","X","X","O"]
])


def minCostClimbingStairs(cost: List[int]) -> int:
    n = len(cost)
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = cost[0]

    for i in range(2, n + 1):
        dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])

    return dp[n]




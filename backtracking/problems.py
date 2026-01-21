from typing import List


def word_search(grid, word):
    # Replace this placeholder return statement with your code
    ROWS, COLS = len(grid), len(grid[0])
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    path = set()

    def helper(row, col, i):
        # base case
        if i == len(word):
            return True

        # out of bounds or cell doesn't match current char or already visited
        if (row < 0 or col < 0 or row >= ROWS or col >= COLS or
            grid[row][col] != word[i] or
            (row, col) in path):
            return  False

        # mark as visited
        path.add((row, col))

        for dr, dc in DIRECTIONS:
            if helper(row + dr, col + dc, i + 1):
                return True

        # backtrack - remove from path if no match found
        path.remove((row, col))
        return False

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == word[0] and helper(r, c, 0):
                return True

    return False


"""
    design
        - dfs function(curr_comb, curr_el_pos)
            - base case: sum(curr_comb) == target: add curr_comb to res
            - boundary check: sum(curr_comb) > target: return
            - add curr_el to curr_comb
            - call dfs on the next el: dfs(curr_comb, curr_el_pos + 1)
            - backtrack: remove curr_el from curr_com
        - call dfs with ([], 0)
        - return res
    timeline
        - start-finish [11:20 - ]
        - design [11:20 - 11:26]
        - coding [11:26 - 11:28]
        - debugging [11:28 - ]
"""
# candidates = [1,2,2,3], target = 3
def combinationSum2(candidates: List[int], target: int) -> List[List[int]]:
    res = []

    def helper(curr_comb, i):  # [1, 3], 3
        # base case
        if sum(curr_comb) == target:
            res.append(curr_comb.copy())  # [ [1,2], [1,2] ]
            return

        # boundary check
        if sum(curr_comb) > target or i >= len(candidates):
            return

        curr_comb.append(candidates[i])  # [1, 3]
        helper(curr_comb, i + 1)  #
        curr_comb.pop()  # [1]

        # handle duplicates in current combinations
        while i + 1 < len(candidates) and candidates[i] == candidates[i + 1]:
            i += 1
        helper(curr_comb, i + 1)

        return

    helper([], 0)
    return res
combinationSum2([1,2,2,3], 3)

"""
    design
        - palindrome checker function
            - left and right pointer at both ends of the string
        - backtracking helper function
            - receives (curr_str, idx)
            - base case: if curr_str is palindrome -> add to final result
            - boundary check: if idx > s.length or curr_str is not palindrome -> return
            - add current char, s[idx], to curr_str
            - call dfs helper on the next char (curr_str, idx + 1)
            - remove current char
        - start call from helper("", 0)
    timeline
        - start-finish [11:50]
        - design [11:53 - 11:57]
        - coding [11:58 - 12:02]
"""
def partition(s: str) -> List[List[str]]:
    res = []

    def is_palindrome(substr):
        if len(substr) < 1:
            return False

        left, right = 0, len(substr) - 1
        while left < right:
            if substr[left] != substr[right]:
                return False
            left += 1
            right -= 1
        return True

    def helper(curr_part, idx):
        # boundary check
        if idx > len(s):
            return

        # base case
        if idx == len(s):
            res.append(curr_part.copy())
            return

        # try all possible substrings
        for end in range(idx, len(s) + 1):
            substr = s[idx : end]

            if is_palindrome(substr):
                curr_part.append(substr)

                # backtrack
                helper(curr_part, end)

                curr_part.pop()

        return

    helper([], 0)
    return res


partition("aab")
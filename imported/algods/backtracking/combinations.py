from collections import defaultdict
from typing import List


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        combs, cur_comb = [], []
        self.helper(1, combs, cur_comb, n, k)
        return combs

    def helper(self, i, combs, cur_comb, n, k):
        # base case
        if len(cur_comb) == k:
            combs.append(cur_comb.copy())
            return
        if i > n:
            return

        # decision to include i
        cur_comb.append(i)
        self.helper(i + 1, combs, cur_comb, n, k)
        cur_comb.pop()

        # decision to not include i
        self.helper(i + 1, combs, cur_comb, n, k)

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []

        def dfs(i, combs):
            current_sum = sum(combs)
            # explicit check for boundaries
            if i == len(candidates) or current_sum > target:
                return

            # base case
            if current_sum == target:
                res.append(combs.copy())
                return

            # adding element to current comb
            combs.append(candidates[i])
            dfs(i, combs)
            combs.pop()

            dfs(i + 1, combs) # move to next candidate


        dfs(0, [])
        return res

    """
        design
            - iterate over digits to cover input_letters[], e.g. [["d","e","f"], ["g", "h", "i"]]
                - current_letters[] = for each digit get corresponding letters, e.g. func(2) returns ["a","b","c"], func(3) returns ["d","e","f"]
                - put current_letters[] into input_letters[] 
    
            - 3 letters/digit 
                => define func(digit)-> return letters
    
            - as input_letters[] are prepared, we can try combinations size of input_letters (meaning equal to len(input_letters))
                input_letters[] = [["d","e","f"], ["g", "h", "i"]]
                k = len(input_letters) = 2
    
            - now, think about how to make combination taking one element from each set
                - tracks current combination and current digit
                - base case is when all digits have been used
                - recursive case is try each letter for the current digit, then move to the next digit
                
    """
    # https://leetcode.com/problems/letter-combinations-of-a-phone-number/
    def letterCombinations(self, digits: str) -> List[str]:
        # empty case
        if not digits:
            return []

        digit_to_letters = self.digit_to_letters(digits)
        res = []

        # backtracking function that adds one char at a time from each digit's letter
        def dfs(i, curr_comb):
            # base case: used all digits
            if i == len(digits):
                res.append(curr_comb)
                return

            # recursive case: try each letter for the current digit, then move to the next digit
            letters = digit_to_letters[digits[i]]
            for letter in letters:
                curr_comb += letter
                dfs(i + 1, curr_comb)
                curr_comb = curr_comb[:i]


        dfs(0, "")

        return res

    def digit_to_letters(self, digits: str):
        digit_to_letters_map = {}
        for d in digits:
            match d:
                case '2':
                    digit_to_letters_map['2'] = ["a", "b", "c"]
                case '3':
                    digit_to_letters_map['3'] = ["d", "e", "f"]
                case '4':
                    digit_to_letters_map['4'] = ["g", "h", "i"]
                case '5':
                    digit_to_letters_map['5'] = ["j", "k", "l"]
                case '6':
                    digit_to_letters_map['6'] = ["m", "n", "o"]
                case '7':
                    digit_to_letters_map['7'] = ["p", "q", "r", "s"]
                case '8':
                    digit_to_letters_map['8'] = ["t", "u", "v"]
                case '9':
                    digit_to_letters_map['9'] = ["w", "x", "y", "z"]
        return digit_to_letters_map


sol = Solution()
sol.letterCombinations("34")
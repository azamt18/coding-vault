

class Solution:
    """
    At each recursion step, we have two choices: if the characters at the current indices of both strings match, we move both indices forward and extend the subsequence. Otherwise, we explore two paths by advancing one index at a time and recursively finding the longest subsequence. We return the maximum length between these two choices. This approach is exponential.
    """
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        if m == 0 or n == 0:
            return 0
        # init 2d table with zeros
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # fill the dp table iteratively
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i-1] == text2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        # result is in the bottom-right cell
        return dp[m][n]

    def visualizeLCS(self, text1: str, text2: str):
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        print("Initial DP Table:")
        for row in dp:
            print(row)
        print()

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

                # Print the DP table after updating each cell
                print(f"After processing text1[{i - 1}]='{text1[i - 1]}' and text2[{j - 1}]='{text2[j - 1]}':")
                for row in dp:
                    print(row)
                print()

        print("Final DP Table:")
        for row in dp:
            print(row)
        print(f"LCS Length: {dp[m][n]}")

# Example usage
text1 = "abcde"
text2 = "ace"
solution = Solution()
solution.visualizeLCS(text1, text2)
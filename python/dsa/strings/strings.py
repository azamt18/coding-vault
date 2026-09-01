class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        left, right = 0, 0  # right is for haystack, left for needle
        h, n = len(haystack), len(needle)
        idx = -1
        for right in range(h):
            if haystack[right] == needle[left]:
                idx = right
                while haystack[right] == needle[left] and left < n - 1:
                    left += 1
                    right += 1

                if haystack[right] == needle[left]:  # last chars
                    return idx
                else:
                    left = 0
                    idx = -1

        return idx if idx != -1 else -1

    def is_palindrome(self, s, j, k):
        count = 0
        while j >= 0 and k < len(s):
            if s[j] != s[k]:
                break

            count += 1
            j -= 1
            k += 1
        return count
    # https://leetcode.com/problems/palindromic-substrings/
    def countSubstrings(self, s: str) -> int:
        count = len(s) # each char is palindrome itself
        for i in range(len(s)):
            # odd length palindromes (centered at i)
            count += self.is_palindrome(s, i - 1, i + 1)

            # even length palindromes (centered between i and i + 1)
            count += self.is_palindrome(s, i, i + 1)

        return count

    """
        Design:
            1. expand-around-center approach
                - receives left (moves to left) and right (moves to right) pointers, check until substring is palindrome
                - returns substring s[left + 1:right], here "+1" is to adjust the boundaries
            2. iterate through each character in string
                - treats it as the center of a potential palindrome
                - checks for both odd- and even-length palindromes
                - keeps track of the longest found

    """
    # https://leetcode.com/problems/longest-palindromic-substring/
    def longestPalindrome(self, s: str) -> str:
        def expand_around_center(left, right) -> str:
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return s[left + 1: right]

        longest = ""
        for i in range(len(s)):
            # odd-length palindromes
            odd_length_palindrome = expand_around_center(i, i)
            if len(odd_length_palindrome) > len(longest):
                longest = odd_length_palindrome

            # even-length palindromes
            even_length_palindrome = expand_around_center(i, i + 1)
            if len(even_length_palindrome) > len(longest):
                longest = even_length_palindrome

        return longest

    """
        Approach 1: naive
        1. find the longest palindrome starting from index 0
        2. add the reverse of the remaining chars to the beginning
        Time: O(n^2)
            
    """
    # https://leetcode.com/problems/shortest-palindrome/
    def shortestPalindrome(self, s: str) -> str:
        if not s:
            return ""

        rev = s[::-1]
        for i in range(len(s)):
            a = s[:len(s) - i]
            b = rev[i:]
            if a == b:
                return rev[:i] + s
        return rev + s[1:]

    """
        Approach 1: search for duplicates within s length of l, where l is controlled by binary search
        Components:
            - binary search on s, passing the mid to check(mid) function
            - check(l) function: 
                - contains visited set() to store already seen substrings
                - 
    """
    # https://leetcode.com/problems/longest-duplicate-substring/
    def longestDupSubstring(self, s: str) -> str:
        return ""



sol = Solution()
res = sol.shortestPalindrome("abcd")
print(res)

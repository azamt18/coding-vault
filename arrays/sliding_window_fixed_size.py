from collections import Counter
from typing import List


def lengthOfLongestSubstring(s: str) -> int:
    window = {}
    max_length = 0
    L = 0

    for R in range(len(s)):
        # If character exists in window, move left pointer to position after the duplicate
        if s[R] in window:
            L = max(window[s[R]] + 1, L)

        # Update max_length
        max_length = max(max_length, R - L + 1)

        # Store character position
        window[s[R]] = R

    return max_length
# res = lengthOfLongestSubstring("pwwkew")
# print(res)

def numOfSubarrays(arr: List[int], k: int, threshold: int) -> int:
    target_sum = k * threshold
    current_sum = sum(arr[:k])
    count = 0

    for i in range(k, len(arr)):
        current_sum += arr[i] - arr[i-k]
        if current_sum >= target_sum:
            count += 1
    return count

# res = numOfSubarrays([2,2,2,2,5,5,5,8], 3, 4)
# print(res)

def containsNearbyDuplicate(nums: List[int], k: int) -> bool:
    window = set()
    L, R = 0, 0

    for R in range(len(nums)):
        if R - L + 1 > k + 1:
            window.remove(nums[L])
            L += 1
        if nums[R] in window:
            return True
        window.add(nums[R])
    return False

# nums = [1,2,3,1]
# print(containsNearbyDuplicate(nums, 3))

def checkInclusion(s1: str, s2: str) -> bool:
    freq_s1 = Counter(s1)
    freq_s2 = {}
    L = R = 0
    while R < len(s2):
        # R - L + 1 = current length
        if R - L + 1 > len(s1):
            # shrink window :: move one from left
            freq_s2[s2[L]] -= 1
            L += 1

        freq_s2[s2[R]] = freq_s2.get(s2[R], 0) + 1

        # running inner loop to compare freq count
        valid = False
        for char, count in freq_s1.items():
            if char in freq_s2 and count == freq_s2[char]:
                valid = True
            else:
                valid = False
                break

        if valid:
            return True

        R += 1

    return False
s1="ab"
s2="lecabee"
res = checkInclusion(s1, s2)
print(res)
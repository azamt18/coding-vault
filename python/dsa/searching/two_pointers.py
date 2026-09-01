# p w w k e w
#   l r
# p w
# 1 2
import heapq
from collections import Counter
from typing import List


def lengthOfLongestSubstring(s: str) -> int:
    window = set()
    L = R = 0
    max_length = 0

    while R in len(s):
        while s[R] in window:  # move L to R to start the new window & pop elements from window
            window.remove(s[L])
            L += 1

        window.add(s[R])
        max_length = max(max_length, len(window))
        R += 1

    return max_length
# res = lengthOfLongestSubstring("pwwkew")
# print(res)


# 1  0  1  1
#    l     r
# 0  1  2  3
def containsNearbyDuplicate(nums: List[int], k: int) -> bool:
    # iterate through nums, at each step check if there is already such num exists before adding
    # when length of set exceeds k, remove element

    window = set()  # maintain a set size of k + 1
    # L, R = 0, 0  # control length of window using k = R - L + 1
    for i, n in enumerate(nums):  # 3
        if len(window) > k:
            window.remove(nums[i-k-1])  # 1 2

        if n in window:
            return True

        window.add(n)  # 1 4 2
    return False
# res = containsNearbyDuplicate([1,0,1,1], 1) # true
# print(res)
# res = containsNearbyDuplicate([1,2,3,1,2,3], 2) # false
# print(res)
# res = containsNearbyDuplicate([1,4,2,3,1,2], 3) # true
# print(res)


def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    result = []
    heap = []

    for i, num in enumerate(nums):
        heapq.heappush(heap, (-num, i))

        if i >= k - 1:
            while heap and heap[0][1] <= i - k: # to leave the last element = top element
                heapq.heappop(heap)

            result.append(-heap[0][0]) # retrieve the top element from the heap without removing it
    return result
# res = maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3)
# print(res)
# res = maxSlidingWindow([1], 1)
# print(res)

def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    result = []
    heap = []

    L = R = 0
    while R < len(nums):
        heapq.heappush(heap, (-nums[R], R))

        if R - L + 1 == k:
            result.append(-heap[0][0])
            L += 1

            while heap and heap[0][1] < L:
                heapq.heappop(heap)

        R += 1

    return result
# res = maxSlidingWindow([1,2,1,0,4,2,6], 3)
# print(res)


def characterReplacement(s: str, k: int) -> int:
    L = R = 0
    max_length = 0
    freq_count = {}
    while R < len(s):
        freq_count[s[R]] = freq_count.get(s[R], 0) + 1

        max_freq = max(freq_count.values()) if freq_count else 0

        current_length = R - L + 1
        replacements_needed = current_length - max_freq

        if replacements_needed > k:
            freq_count[s[L]] -= 1
            L += 1
        else:
            max_length = max(max_length, current_length)

        R += 1
    return max_length

# https://leetcode.com/problems/contains-duplicate-iii/
def containsNearbyAlmostDuplicate(nums: List[int], indexDiff: int, valueDiff: int) -> bool:
    # buckets
    if valueDiff < 0 or indexDiff <= 0:
        return False

    buckets = {}
    bucket_size = valueDiff + 1  # Bucket size is valueDiff + 1 to ensure proper range

    for i, num in enumerate(nums):
        # Calculate bucket ID
        bucket_id = (num + 1 * valueDiff) // bucket_size
        # bucket_id = num // bucket_size if num >= 0 else (num // bucket_size) - 1

        # Check if the current bucket already contains a number
        if bucket_id in buckets:
            return True

        # Check adjacent buckets
        if bucket_id - 1 in buckets and abs(num - buckets[bucket_id - 1]) <= valueDiff:
            return True
        if bucket_id + 1 in buckets and abs(num - buckets[bucket_id + 1]) <= valueDiff:
            return True

        # Add the current number to its bucket
        buckets[bucket_id] = num

        # Maintain the sliding window size
        if i >= indexDiff:
            leftmost = nums[i - indexDiff]
            oldest_bucket_id = (leftmost + 1 * valueDiff) // bucket_size
            # oldest_bucket_id = leftmost // bucket_size if leftmost >= 0 else (leftmost // bucket_size) - 1
            del buckets[oldest_bucket_id]

    return False

    # buckets (simple)
    # if valueDiff < 0: return False
    # seen = {}
    # for i, num in enumerate(nums):
    #     bucket = num
    #     if bucket in seen and i - seen[bucket][0] <= indexDiff:
    #         return True
    #     if bucket - 1 in seen and i - seen[bucket - 1][0] <= indexDiff and abs(num - seen[bucket - 1][1]) <= valueDiff:
    #         return True
    #     if bucket + 1 in seen and i - seen[bucket + 1][0] <= indexDiff and abs(num - seen[bucket + 1][1]) <= valueDiff:
    #         return True
    #
    #     seen[bucket] = (i, num)
    # return False

    # sliding window
    # L = R = 0
    # while R < len(nums):
    #     # shrink window if it exceeds window size
    #     while R - L > indexDiff:
    #         L += 1
    #
    #     # check all elements in the current window
    #     for i in range(L, R):
    #         diff = abs(nums[R] - nums[i])
    #         if diff <= valueDiff:
    #             return True
    #
    #     R += 1
    #
    # return False

    # brute force
    # n = len(nums)
    # for i in range(n):
    #     for j in range(i + 1, min(i + indexDiff + 1, n)):
    #         if abs(i - j) <= indexDiff and abs(nums[i] - nums[j]) <= valueDiff:
    #             return True
    # return False

print(containsNearbyAlmostDuplicate([-2,3], 2, 5)) # true
print(containsNearbyAlmostDuplicate([-3,3], 2, 4)) # false
print(containsNearbyAlmostDuplicate([1,2,2,3,4,5], 3, 0)) # true
print(containsNearbyAlmostDuplicate([1,5,9,1,5,9], 2, 3)) # false
print(containsNearbyAlmostDuplicate([8,7,15,1,6,1,9,15], 1, 3)) # true



def minWindow(s: str, t: str) -> str:
    min_length = float("inf")
    result = ""
    freq_t, freq_s = {}, {}
    for char in t:
        freq_t[char] = freq_t.get(char, 0) + 1

    L = R = 0
    required_chars = len(freq_t) # unique chars needed
    formed_chars = 0 # satisfied chars requirements

    while R < len(s):
        # expand window
        char = s[R]
        freq_s[char] = freq_s.get(char, 0) + 1

        # check if satisfied char req
        if char in freq_t and freq_s[char] == freq_t[char]:
            formed_chars += 1

        # contract window while valid
        while L <= R and formed_chars == required_chars:
            # update result if smaller window found
            current_length = R - L + 1
            if current_length < min_length:
                min_length = current_length
                result = s[L : R + 1]

            # move left pointer forward (contract window)
            left_char = s[L]
            freq_s[left_char] -= 1
            L += 1

            # check if window becomes invalid after removing left char
            if left_char in freq_t and freq_s[left_char] < freq_t[left_char]:
                formed_chars -= 1

        R += 1

    return result
    # for i in range(len(s)):
    #     freq_s = {}
    #     for j in range(i, len(s)):
    #         freq_s[s[j]] = freq_s.get(s[j], 0) + 1
    #
    #         found = True
    #         for key, val in freq_t.items():
    #             if key not in freq_s or freq_s[key] < val:
    #                 found = False
    #                 break
    #
    #         if found:
    #             current_length = j - i + 1
    #             if current_length < min_length:
    #                 min_length = current_length
    #                 substring = s[i : j + 1]
    #             break
    # return substring
# res = minWindow("ADOBECODEBANC", "ABC")
# print(res)

def minWindow(s: str, t: str) -> str:
    if len(s) < len(t):
        return ""
    elif len(s) == len(t) == 1:
        if t[0] in s:
            return t[0]
        else:
            ""

    count_s, count_t = {}, Counter(t)
    min_length = float("inf")
    required_chars, formed_chars = len(t), 0
    result = ""

    L = R = 0
    while R < len(s):
        # count char frequencies
        count_s[s[R]] = count_s.get(s[R], 0) + 1

        # count formed substring chars
        if s[R] in count_t and count_s[s[R]] <= count_t[s[R]]:
            formed_chars += 1

        while L <= R and required_chars == formed_chars:
            current_length = R - L + 1
            if current_length < min_length:
                min_length = min(min_length, current_length)
                result = s[L : R + 1]

            # check if window may become invalid after shrinking
            if s[L] in count_t and count_s[s[L]] == count_t[s[L]]:
                formed_chars -= 1

            # shrink the window
            count_s[s[L]] -= 1
            L += 1

        R += 1

    return result
# res = minWindow("aa", "aa")
# res = minWindow("ADOBECODEBANC", "ABC")
# print(res)



def threeSum(nums: List[int]) -> List[List[int]]:
    res = []
    seen = set()
    for i, num in enumerate(nums):
        left_arr = nums[:i]
        right_arr = nums[i+1:] if i + 1 < len(nums) - 1 else []
        opposite_sum = twoSum(left_arr + right_arr, -num)
        if opposite_sum:
            triplet = tuple(sorted([num, opposite_sum[0], opposite_sum[1]]))
            if triplet not in seen:
                seen.add(triplet)
                res.append([num, opposite_sum[0], opposite_sum[1]])

    return res


def twoSum(nums, target) -> List[int]:
    hash_map = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in hash_map:
            return [diff, num]
        hash_map[num] = i
    return []
# res = threeSum([-1,0,1,2,-1,-4])
# print(res)

def threeSum(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    result = []
    nums.sort()

    for i in range(n):
        # skip duplicate for i
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])

                # skip duplicates for left pointer
                while left < right and nums[left] == nums[left + 1]:
                    left += 1

                # skip duplicates for right pointer
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                left += 1
                right -= 1

    return result
# res = threeSum([-1,0,1,2,-1,-4])
# print(res)

def trap(height: List[int]) -> int:
    if len(height) < 3:
        return 0

    area = 0
    left, i, right = 0, 1, 2
    while right < len(height):
        trapped = height[i] - min(height[left], height[right])
        if trapped > 0:
            area += trapped

        left += 1
        i += 1
        right += 1

    return area
# height=[0,2,0,3,1,0,1,3,2,1]
# res = trap(height)
# print(res)
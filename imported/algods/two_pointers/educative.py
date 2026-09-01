from itertools import count
from typing import List


def sort_colors(colors):
    # 0, 1, 2, 2, 1, 0
    next_red, next_white, next_blue = 0, 0, len(colors)

    for i in range(len(colors) - 1):
        if colors[i] == 0:  # red
            colors[i], colors[i + 1] = colors[i + 1], colors[i]  # 1, 2, 0, 2, 1, 0
        elif colors[i] == 1:  # white
            continue
        elif colors[i] == 2:  # blue
            colors[i], colors[i + 1] = colors[i + 1], colors[i]
    return colors


def reverse_words(sentence):
    # Replace this placeholder return statement with your code
    res = sentence.strip().split()
    left, right = 0, len(res) - 1

    while left <= right:
        res[left], res[right] = res[right], res[left]
        left += 1
        right -= 1

    return " ".join(res)

# https://leetcode.com/problems/valid-word-abbreviation/
def valid_word_abbreviation(word, abbr):
    # Replace the following return statement with your code
    word_ptr, abbr_ptr = 0, 0

    while word_ptr < len(word) and abbr_ptr < len(abbr):
        # if letter
        if abbr[abbr_ptr].isalpha():
            if abbr[abbr_ptr] != word[word_ptr]:
                return False
            word_ptr += 1
            abbr_ptr += 1

        # if digit
        elif abbr[abbr_ptr].isdigit():
            if abbr[abbr_ptr] == "0":
                return False

            # parse number
            count = 0
            while abbr_ptr < len(abbr) and abbr[abbr_ptr].isdigit():
                count = count * 10 + int(abbr[abbr_ptr])
                abbr_ptr += 1

            # skip count chars
            word_ptr += count


    return word_ptr == len(word) and abbr_ptr == len(abbr)


# https://leetcode.com/problems/strobogrammatic-number/
def is_strobogrammatic(num):
    # Replace this placeholder return statement with your code
    if len(num) == 0:
        return True

    dic = {"0": "0", "1": "1", "6": "9", "8": "8", "9": "6"}
    left, right = 0, len(num) - 1
    while left <= right: # check mid element in odd-length string
        if num[left] in dic:
            if dic[num[left]] != num[right]:
                return False
            left += 1
            right -= 1
        else:
            return False
    return True
is_strobogrammatic("962")

# https://leetcode.com/problems/minimum-number-of-moves-to-make-palindrome/
def min_moves_to_make_palindrome(s):
    s = list(s)
    moves = 0
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] == s[j]: # already match
            i += 1
            j -= 1
            continue

        # find matching char from right side
        k = j - 1
        while k > i and s[i] != s[k]:
            k -= 1

        # if found matching char on right side
        if s[i] == s[k]:
            # shift chars from right to left
            while k < j:
                s[k], s[k + 1] = s[k + 1], s[k]
                moves += 1
                k += 1
        else:
            # no match found, char must be the center of palindrome
            # Use temp variable to avoid variable shadowing with k
            temp = i
            while temp < j:
                s[temp], s[temp + 1] = s[temp + 1], s[temp]
                moves += 1
                temp += 1
            j -= 1
            continue

        i += 1
        j -= 1

    return moves
min_moves_to_make_palindrome("ccxx")

# https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii/
# Definition for a binary tree node
# class EduTreeNode:
#     def __init__(self, data):
#         self.data = data
#         self.left = None
#         self.right = None
#         self.parent = None
# from EduTreeNode import *
def lowest_common_ancestor(p, q):
    # Replace this placeholder return statement with your code
    left, right = p, q
    while left != right:
        if left is None:
            left = q
            continue
        elif right is None:
            right = p
            continue

        left = left.parent
        right = right.parent
    return left

# https://leetcode.com/problems/count-pairs-whose-sum-is-less-than-target/
def countPairs(nums: List[int], target: int) -> int:
    nums.sort()

    low, high = 0, len(nums) - 1
    count = 0

    while low < high:
        sum = nums[low] + nums[high]
        if sum < target:
            # count pairs btw high and low
            count += high - low
            low += 1

        elif sum >= target:
            high -= 1

    return count
countPairs([1,3,2,4,5], 6)
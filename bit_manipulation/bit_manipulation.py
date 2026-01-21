from collections import Counter
from typing import List


def reverseBits(n: int) -> int:
    result = 0

def countBits(n: int) -> List[int]:
    ans = [0] * (n + 1)
    for i in range(n + 1):
        count = bitsCountHelper(i)
        ans[i] = count
    return ans
def bitsCountHelper(num):
    count = 0
    while num > 0:
        if num & 1:
            count += 1
        num = num >> 1
    return count

def singleNumber(nums: List[int]) -> int:
    res = 0
    for n in nums:
        print(n, n ^ 1, 1 ^ n)
        print(n, n ^ 0, 0 ^ n)
        print(res, n, res ^ n, n ^ res)
        res = res ^ n
        print(res)
        print("================")

    return res
# singleNumber([4,1,2,1,2])


def duplicateNumbersXOR(nums: List[int]) -> int:
    twins = []
    counter = Counter(nums)
    for key, val in counter.items():
        if val == 2:
            twins.append(key)

    print(twins)
    res = 0
    for n in twins:
        res = res ^ n
    return res
# duplicateNumbersXOR([1,2,3])

# https://leetcode.com/problems/single-number-ii/
def singleNumber(nums: List[int]) -> int:
    ones, twos = 0, 0
    for n in nums:
        ones = ones ^ n & ~twos
        twos = twos ^ n & ~ones
    return ones

# https://leetcode.com/problems/single-number-iii/
def singleNumber(nums: List[int]) -> List[int]:
    if len(nums) <= 2: return nums

    xor_sum = 0
    for n in nums:
        xor_sum = xor_sum ^ n

    # rightmost set bit
    set_bit = xor_sum & -xor_sum

    # partition numbers into 2 groups
    num1, num2 = 0, 0
    for n in nums:
        if n & set_bit: # numbers with the set bit = 1
            num1 = num1 ^ n
        else:           #  numbers with the set bit = 0
            num2 = num2 ^ n

    return [num1, num2]
# print(singleNumber([1,2,1,3,2,5]))

# https://leetcode.com/problems/bitwise-and-of-numbers-range/
def rangeBitwiseAnd(left: int, right: int) -> int:
    shift = 0
    while left < right:
        left >>= 1
        right >>= 1
        shift += 1
    res = left << shift
    return res
# print(rangeBitwiseAnd(5, 7))


def hammingDistance(x: int, y: int) -> int:
    # 1 = 0 0 0 1
    # 4 = 0 1 0 0
    # 2 = 0 0 1 0
    res = 0

    while x > 0 if x > y else y > 0:
        if (x & 1) != (y & 1):
            res += 1
        x >>= 1
        y >>= 1

    return res
# print(hammingDistance(4, 2))

# https://leetcode.com/problems/total-hamming-distance/
def totalHammingDistance(nums: List[int]) -> int:
    # 4  = 0100
    # 14 = 1110
    total = 0
    n = len(nums)
    for i in range(32):
        bit_count = 0
        for num in nums:
            num >>= i
            bit_count += num & 1
        total += bit_count * (n - bit_count)
    return total
print(totalHammingDistance([4,14,2]))


def reverse(x: int) -> int:

    # negative sign
    is_negative = x < 0

    if is_negative:
        x = x * (-1)

    x_str = str(x)
    x_str = x_str[::-1]

    res = int(x_str)

    if is_negative:
        res = res * (-1)

    # if type(x) != int:
    #     return 0
    # 32-bit range
    if x.bit_length() >= 31:
        return 0

    return res
reverse(1234236467)


def getSum(a: int, b: int) -> int:
    carry = 0
    res = 0
    mask = 0xFFFFFFFF

    while b != 0:
        # sum without carry
        tmp = (a ^ b) & mask

        # carry
        b = ((a & b) << 1) & mask

        a = tmp

    if a > 0x7FFFFFFF:
        a = ~(a ^ mask)
    return a
getSum(9, -2)










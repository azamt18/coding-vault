from typing import List


class Solution:
    def kthCharacter(self, k: int) -> str:
        str_list = ['a']

        while len(str_list) <= k:
            temp_str = []
            for c in str_list:
                next_char = chr(ord(c) + 1)
                temp_str.append(next_char)
            str_list.extend(temp_str)

        return str_list[k]

sol = Solution()
sol.kthCharacter(5)


def isOneBitCharacter(bits: List[int]) -> bool:
    """ daily
        appr 1: sliding window on array
    """

    # 0 1 2
    # 1 0 0
    n = len(bits)
    i = 0
    last_bit = None
    digits = [bits[i]]
    one_bit = {0}
    two_bit = {10, 11}
    while i < n:
        current = int("".join(map(str, digits)))
        if not digits:
            i += 1
            continue
        print(digits, current, last_bit)
        if current in one_bit or current in two_bit:
            last_bit = current
            digits = []
            i += 1
        else:
            i += 1
            digits.append(bits[i])

    return last_bit in one_bit
isOneBitCharacter([1,0,0])
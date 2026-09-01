# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num: int) -> int:

class Solution:
    def guessNumber(self, n: int) -> int:
        l, r = 1, n
        while True:
            m1 = l + (r - l) // 3
            m2 = r - (r - l) // 3
            if self.guess(m1) == 0:
                return m1
            if self.guess(m2) == 0:
                return m2
            if self.guess(m1) + self.guess(m2) == 0:
                l = m1 + 1
                r = m2 - 1
            elif self.guess(m1) == -1:
                r = m1 - 1
            else:
                l = m2 + 1

    def guess(self, num):
        if num > 10:
            return 1
        elif num < 10:
            return -1
        else:
            return 0
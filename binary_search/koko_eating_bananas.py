import math
from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        m = max(piles)
        for speed in range(1, m + 1):
            total_hours = 0
            for pile in piles:
                total_hours += math.ceil(pile / speed)
            if total_hours <= h:
                return speed

        return m

        # Consider m to be the largest pile and n to be the number of piles. A brute force solution would be to linearly check all values from 1 to m and find the minimum possible value at which Koko can complete the task. This approach would take O(n * m) time. Can you think of a more efficient method? Perhaps an efficient searching algorithm could help.
        # speed = 1
        # while True:
        #     total = 0
        #     for pile in piles:
        #         total += (pile + speed - 1) // speed  # This is equivalent to math.ceil(pile / speed)
        #     if total <= h:
        #         return speed
        #     speed += 1
        # return speed








# Example usage of sortColors
piles = [1,4,3,2]
h = 9

solution = Solution()
res = solution.minEatingSpeed(piles, h)

# Print the sorted list
print(res)

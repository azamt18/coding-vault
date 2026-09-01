# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

def isBadVersion(num):
    if num >= 1:
        return True
    return False


class Solution:
    def firstBadVersion(self, n: int) -> int:
        left, right = 1, n
        while left <= right:
            mid = (left + right) >> 1
            if isBadVersion(mid):
                result = mid
                right = mid - 1
            else:
                left = mid + 1

        return result

# Example usage of sortColors
nums=[0,1,2,4,5,6,7,8]
target=4

solution = Solution()
res = solution.firstBadVersion(3)

# Print the sorted list
print(res)
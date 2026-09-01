# https://leetcode.com/problems/find-k-closest-elements/
def find_closest_elements(nums, k, target):

    n = len(nums)
    if n == k:
        return nums
    if target <= nums[0]:
        return nums[:k]
    elif target >= nums[-1]:
        return nums[n - k:]

    # nums = [1, 3, 5, 7, 9, 11]
    # k = 4
    # target = -7
    mid_window = 0
    left, right = 0, n - 1
    while left <= right:
        mid = left + (right - left) // 2
        # if target == nums[mid]:
        #     # expand window from mid index until k
        #     mid_window = mid
        #     break
        if target > nums[mid]:
            left = mid + 1
        elif target < nums[mid]:
            right = mid - 1

    # first_closest = mid_window if mid_window else left
    window_left, window_right = left - 1, left
    while (window_right - window_left - 1) < k:
        if window_left < 0:
            window_right += 1
        elif window_right >= n:
            window_left -= 1
        else:
            # choose the closer element
            if abs(nums[window_left] - target) <= abs(nums[window_right] - target):
                window_left -= 1
            elif abs(nums[window_right] - target) < abs(nums[window_left] - target):
                window_right += 1

    print(window_left, window_right)
    return nums[window_left + 1: window_right]

# https://leetcode.com/problems/maximum-value-at-a-given-index-in-a-bounded-array/description/
def max_value(n, index, max_sum):
    def calculate_sum(value, length):
        if value >= length:
            return (value + (value - length + 1)) * length // 2
        else:
            return (value * (value + 1)) // 2 + (length - value)

    left, right = 1, max_sum
    while left < right:
        mid = left + (right - left) // 2

        left_sum = calculate_sum(mid - 1, index)
        right_sum = calculate_sum(mid - 1, n - index - 1)
        total_sum = left_sum + right_sum
        if total_sum <= max_sum:
            left = mid
        else:
            right = mid - 1

    return left

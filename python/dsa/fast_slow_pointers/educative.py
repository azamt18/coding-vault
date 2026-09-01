def is_happy_number(n): # 28
    if n == 1:
        return True

    slow, fast = n, get_sum_of_squared_digits(n) # sum of squared digits
    while fast != 1 and slow != fast:
        slow = get_sum_of_squared_digits(slow)
        fast = get_sum_of_squared_digits(get_sum_of_squared_digits(fast))
        if fast == 1:
            return True
    return False

def get_sum_of_squared_digits(n):
    digits = get_digits(n)
    sum = 0
    for d in digits:
        sum += d * d
    return sum

def get_digits(n): # 19
    digits = []
    while n > 0: # 19
        remain = n % 10 # 1 % 10 = 1
        digits.append(remain)
        n = n // 10 # 1 / 10 = 0
    # digits.append(n)
    return digits
is_happy_number(10)

# https://leetcode.com/problems/circular-array-loop/description/
def circular_array_loop(nums):
    size = len(nums)
    for i, num in enumerate(nums):
        slow, fast = i, i
        forward = nums[i] > 0
        while True:
            slow = next_move(slow, nums[slow], size)
            if not is_cycle_formed(nums, forward, slow):
                break

            fast = next_move(fast, nums[fast], size)
            if not is_cycle_formed(nums, forward, fast):
                break

            fast = next_move(fast, nums[fast], size)
            if not is_cycle_formed(nums, forward, fast):
                break

            if slow == fast:
                return True

    return False

def next_move(pointer, value, size):
    return (pointer + value) % size

def is_cycle_formed(nums, prev_direction, index):
    curr_direction = nums[index] > 0

    if curr_direction == prev_direction and nums[index] % len(nums) != 0:
        # cycle is possible
        return True
    else:
        return False

# https://leetcode.com/problems/find-the-duplicate-number/description/
def find_duplicate(nums):
    slow, fast = 0, 0
    while True:
        slow = nums[slow]
        fast = nums[fast]
        fast = nums[fast]
        if slow == fast:
            break

    slow = 0
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow
find_duplicate([3,4,4,4,2])

# https://leetcode.com/problems/palindrome-linked-list/
def palindrome(head):
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # reverse the 2nd half
    second_half_head = reverse_linked_list_2(slow)

    # Store the head of second half to restore later
    second_half_start = second_half_head

    first, second = head, second_half_start
    while second:
        if first.val != second.val:
            return False
        first = first.next
        second = second.next

    # reverse the 2nd half to restore the original
    reverse_linked_list_2(second_half_head)

    return True

def reverse_linked_list_2(node):
    prev, next = None, None
    curr = node
    while curr is not None:
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    return prev

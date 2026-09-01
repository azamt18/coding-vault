import heapq

nums = [4, -2, 3, -5]
heap = []

for num in nums:
    pair = (abs(num), num)
    heapq.heappush(heap, pair)

while heap:
    pair = heapq.heappop(heap)
    original_num = pair[1]
    print(original_num)
# Output: -2, 3, 4, -5
# The output is the original numbers sorted by their absolute values.
# The negative numbers are printed in the order of their absolute values.
# The positive numbers are printed in the order of their absolute values.
# The absolute values are sorted in ascending order.

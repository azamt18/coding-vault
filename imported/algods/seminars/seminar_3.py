import heapq


def smallest_range(nums):
    # step 1: Initialize a min heap (priority queue) to store the current smallest elements from each list, along with their indexes.
    smallest_elements = []

    # step 2: Track the maximum value among the elements currently in the heap to help calculate the range.
    max_element = nums[0][0]

    # step 3: Push the first element from each of the k lists into the heap and update the maximum value.
    for rng_idx in range(len(nums)):
        min_element = nums[rng_idx][0]
        heapq.heappush(smallest_elements, (min_element, rng_idx, 0))  # (number, range index, element index)
        max_element = max(max_element, min_element)

    # step 4: While the heap contains one element from each list, pop the smallest element (min) from the heap.
    best_range = [smallest_elements[0][0], max_element]  # [min, max]
    while smallest_elements:
        min_element, rng_idx, element_idx = heapq.heappop(smallest_elements)

        # step 5: Compare and update the current best range [min,max] if it is smaller than the previously recorded one
        if max_element - min_element < best_range[1] - best_range[0]:
            best_range = [min_element, max_element]

        # step 6: If the popped element’s list has more elements, push the next element from that list into the heap and update the max value if needed.
        if element_idx < len(nums[rng_idx]) - 1:
            next_min_element_idx = element_idx + 1
            next_min_element = nums[rng_idx][next_min_element_idx]
            heapq.heappush(smallest_elements, (next_min_element, rng_idx, next_min_element_idx))
            max_element = max(max_element, next_min_element)

        # step 7: should stop the loop as soon as any list runs out of elements, ensuring the range always covers all lists
        if element_idx == len(nums[rng_idx]) - 1:
            break

    return best_range
res = smallest_range([[1,5],[3,7],[4,6]])
print(res)
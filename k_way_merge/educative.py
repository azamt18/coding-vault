import heapq


def merge_sorted(nums1, m, nums2, n):
    p1, p2 = m - 1, n - 1  # p1 = 6, p2 = 1
    p = (m + n) - 1  # 5

    # 1, 2, 7, 92, 0, 0, 5
    while p >= 0:
        if p2 < 0:
            break
        if p1 >= 0 and nums1[p1] > nums2[p2]:  #
            nums1[p] = nums1[p1]
            p = p - 1
            p1 = p1 - 1
        else:
            nums1[p] = nums2[p2]  #
            p = p - 1  #
            p2 = p2 - 1

    return nums1
merge_sorted([6,7,8,9,10,0,0,0,0,0] , 5 , [1,2,3,4,5] , 5)


def k_smallest_number(lists, k):
    pq = []
    for index, l in enumerate(lists):
        if l:
            heapq.heappush(pq, (l[0], 0, index))  # [value, i-th element in list, i-th list]

    last_popped_element = 0
    while pq and k > 0:
        element_value, element_index, list_index = heapq.heappop(pq)
        current_list = lists[list_index]
        if element_index < len(current_list) - 1:
            heapq.heappush(pq, (current_list[element_index + 1], element_index + 1, list_index))

        last_popped_element = element_value
        k -= 1

    return last_popped_element

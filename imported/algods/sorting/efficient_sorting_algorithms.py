import heapq
import random
from typing import List


def merge_sort(arr):
    n = len(arr)
    if n == 1:
        return arr

    arr_left = arr[ : n//2 ]
    arr_right = arr[ (n//2) : ]

    arr_left = merge_sort(arr_left)
    arr_right = merge_sort(arr_right)

    return merge(arr_left, arr_right)

def merge(arr_left: List[int], arr_right: List[int]):
    arr_tmp = []
    i = j = 0

    while i < len(arr_left) and j < len(arr_right):
        if arr_left[i] < arr_right[j]:
            arr_tmp.append(arr_left[i])
            i += 1
        else:
            arr_tmp.append(arr_right[j])
            j += 1

    # add remaining elements
    arr_tmp.extend(arr_left[i:])
    arr_tmp.extend(arr_right[j:])

    return arr_tmp

# res = merge_sort([5,2,3,1])
# print(res)

def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # check if left child exists and is greater than root
        if left < n and arr[left] > arr[largest]:
            largest = left
        # check if right child exists and is greater the largest so far
        if right < n and arr[right] > arr[largest]:
            largest = right

        # if the largest is not the root, swap and continue swapping
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)
    # build max-heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # extract elements from the heap one by one
    for i in range(n - 1, 0, -1):
        # move the current root to the end
        arr[0], arr[i] = arr[i], arr[0]
        # call heapify on the reduced heap
        heapify(arr, i, 0)

    return arr

# res = heap_sort([-2,3,-5])
# res = heap_sort([3, 1, 4, 1, 5, 9, 2, 6])
# print(res)


# [3,2,1,5,6,4], k = 2
def findKthLargest(nums: List[int], k: int) -> int:
    k = len(nums) - k  # 6 - 2 = 4

    def quickSelect(l, r):
        p, pivot = l, nums[r]  # 0, 4
        for i in range(l, r):
            if nums[i] <= pivot:  # 2 < 4
                nums[p], nums[i] = nums[i], nums[p]  # 2, 3 = 3, 2
                p += 1  # 1
        nums[p], nums[r] = nums[r], nums[p]

        if p > k:
            return quickSelect(l, p - 1)
        elif p < k:
            return quickSelect(p + 1, r)
        else:
            return nums[p]

    return quickSelect(0, len(nums) - 1)
# res = findKthLargest([3,2,1,5,6,4], 2)
# print(res)


def kClosest(points: List[List[int]], k: int) -> List[List[int]]:
    # calculate distance
    distance = lambda x: x[0]**2 + x[1]**2

    def partition(left, right, pivot_idx):
        pivot_distance = distance(points[pivot_idx])
        # move pivot to the end
        points[pivot_idx], points[right] = points[right], points[pivot_idx]
        store_idx = left
        # move all points with smaller distance to the left
        for i in range(left, right):
            if distance(points[i]) < pivot_distance:
                points[store_idx], points[i] = points[i], points[store_idx]
                store_idx += 1
        # move pivot to its final place
        points[store_idx], points[right] = points[right], points[store_idx]
        return store_idx

    def quickSelect(left, right, k):
        if left <= right:
            # random pivot
            pivot_idx = random.randint(left, right)
            # partition the array
            pivot_idx = partition(left, right, pivot_idx)
            # check the position of the pivot
            if pivot_idx == k:
                return
            elif pivot_idx < k:
                quickSelect(pivot_idx + 1, right, k)
            else:
                quickSelect(left, pivot_idx - 1, k)

    quickSelect(0, len(points) - 1, k)
    return points[:k]
# res = kClosest([[1, 3], [-2, 2], [5, 8], [0, 1]], 2)
# print(res)  # Output: [[-2, 2], [0, 1]]


def topKFrequent(nums: List[int], k: int) -> List[int]:
    # 1. count the freq of each element
    freq_map = {}
    for num in nums:
        freq_map[num] = freq_map.get(num, 0) + 1

    # 2. create buckets
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in freq_map.items():
        buckets[freq].append(num)

    # 3. collect the top k freq elements
    res = []
    for i in range(len(buckets) - 1, 0, -1):
        for num in buckets[i]:
            res.append(num)
            if len(res) == k:
                return res
    return res
res = topKFrequent([4,1,-1,2,-1,2,3, 7,7,7], 3)
print(res) # expected [2,-1]
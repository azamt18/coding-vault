# Definition for a pair.
from typing import List

class Pair:
    def __init__(self, key: int, value: str):
        self.key = key
        self.value = value

class Solution:
    def quickSort(self, pairs: List[Pair]) -> List[Pair]:
        self.quickSortHelper(pairs, 0, len(pairs) - 1)
        return pairs

    def quickSortHelper(self, arr, s, e):
        # base case
        if e - s <= 1:
            return arr

        pivot = arr[e]  # pivot
        left = s  # left pointer

        # partition: elements less than pivot on left side
        for i in range(s, e):
            if arr[i].key < pivot.key:
                # swap arr[i] with the left element
                arr[i], arr[left] = arr[left], arr[i]
                left += 1

        # swap pivot with the left pointer
        arr[left], arr[e] = arr[e], arr[left]

        # call sorting for left side
        self.quickSortHelper(arr, s, left - 1)
        self.quickSortHelper(arr, left + 1, e)

        return

# Example usage of quickSort
pairs = [Pair(3, "three"), Pair(1, "one"), Pair(2, "two")]

solution = Solution()
sorted_pairs = solution.quickSort(pairs)

# Print the sorted pairs
for pair in sorted_pairs:
    print(f"Key: {pair.key}, Value: {pair.value}")
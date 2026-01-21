from typing import Optional


def bubble_sort(arr):
    n = len(arr)
    flag = False
    for i in range(n):
        if flag:
            print('sorted')
            break

        for j in range(1, n):
            flag = True
            if arr[j] < arr[j - 1]:
                # swap the elements
                arr[j-1], arr[j] = arr[j], arr[j-1]
                flag = False
    return arr

# res = bubble_sort([5,2,3,1])
# print(res)

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        current_element_idx = i # 0
        min_el_idx = i # 0

        while current_element_idx < n - 1:
            if arr[current_element_idx] < arr[min_el_idx]: # 2
                min_el_idx = current_element_idx # 4
            current_element_idx += 1

        if arr[min_el_idx] < arr[i]: # 2 < 4
            arr[i], arr[min_el_idx] = arr[min_el_idx], arr[i]

    return arr

#                     0, 1, 2, 3, 4, 5, 6,  7,  8,  9
# res = selection_sort([4, 7, 1, 4, 2, 8, 10, 43, 32, 55])
# res = selection_sort([1, 2, 2, 3, 4, 5, 6, 7, 8])
# print(res)

def insertion_sort(arr):
    for i in range(0, len(arr)):
        j = i
        while (0 <= j < len(arr) - 1  # left and right bounds
               and arr[j] > arr[j + 1]):
            arr[j + 1], arr[j] = arr[j], arr[j + 1]
            j -= 1
    return arr
#                     0, 1, 2, 3, 4, 5, 6,
res = insertion_sort([7, 4, 1, 4, 2, 8, 10, 43, 32, 55])
print(res)

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# dummy -> 4        -> 2        -> 1        -> 3
#          cur, pre
def insertionSortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head

    dummy = ListNode(-1, head)
    prev, cur = head, head.next
    while cur:
        if prev.val <= cur.val:
            prev, cur = cur, cur.next
            continue

        tmp = dummy
        while cur.val >= tmp.next.val:
            tmp = tmp.next

        prev.next = cur.next
        cur.next = tmp.next
        tmp.next = cur
        cur = prev.next

    return dummy.next

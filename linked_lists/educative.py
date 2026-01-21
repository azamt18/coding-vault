# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# https://leetcode.com/problems/reverse-linked-list-ii/
def reverseBetween(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    if left == right:
        return head

    left_prev = None
    right_next = None
    position = 0
    dummy = ListNode(next=head)

    cur = dummy
    # d, 3  5
    #    c
    #       p
    # lp
    while cur:
        if cur.next and position + 1 == left:
            left_prev = cur
            cur = cur.next
            position += 1
            break
        cur = cur.next
        position += 1

    stack = []
    while cur:
        stack.append(cur)  # 3 5
        if position == right:
            right_next = cur.next  # null
            break
        cur = cur.next
        position += 1

    right_next = cur
    while stack:
        left_prev.next = stack.pop()
        left_prev = left_prev.next

    left_prev.next = right_next
    return dummy.next

    # cur = left_prev  # dummy
    # if left_prev == dummy:
    #     cur = head

    # reversed_nodes = []
    # while stack:
    #     reversed_nodes.append(stack.pop())
    #
    # for node in reversed_nodes:
    #     cur.next = node
    #     cur = cur.next

    # while stack and cur:
    #     cur.next = stack.pop()  # 5
    #     cur = cur.next

    # if cur:
    #     cur.next = right_next

    # return head

# https://leetcode.com/problems/reorder-list/
def reorderList(self, head: Optional[ListNode]) -> None:
    """
    Do not return anything, modify head in-place instead.
    """
    if not head or not head.next:
        return

    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # reverse the second half
    prev, curr = None, slow.next
    slow.next = None # break the link to avoid cycles
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp

    # merge 1st and 2nd half
    first, second = head, prev
    while second:
        temp1, temp2 = first.next, second.next

        first.next = second
        second.next = temp1

        first, second = temp1, temp2
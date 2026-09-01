from collections import Counter
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def isPalindrome(self, head: Optional[ListNode]) -> bool:
    res = []
    current = head

    while current:
        res.append(current.val)
        current = current.next

    if res == res[::-1]:
        return True
    return False

def deleteDuplicates(head: Optional[ListNode]) -> Optional[ListNode]:
    current = head
    while current:
        if current.next and current.next.val == current.val:
            if current.next.next:
                current.next = current.next.next
            else:
                current.next = None

        current = current.next
    return head

def findDuplicate(nums: List[int]) -> int:
    counter = Counter(nums)
    for key, count in counter.items():
        if count > 1:
            return key
    return 0

nums = [1,2,3,2,2]
res = findDuplicate(nums)
print(res)


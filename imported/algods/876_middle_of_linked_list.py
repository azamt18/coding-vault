# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def middleNode(self, head):
        length = self.getLength(head)
        print(length)

    def getLength(self, linkedList):
        length = 0
        while linkedList.next is not None:
            length = length + 1

        return length
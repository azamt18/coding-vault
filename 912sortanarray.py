class Solution:
    def sortColors(self, nums) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        newArr = []
        copiedArr = list(nums)

        for i in range(len(nums)):
            smallest = self.findSmallest(copiedArr)
            newArr.append(copiedArr.pop(smallest))

        print(newArr)
        print(copiedArr)
        print(nums)

    def findSmallest(self, arr):
        smallest = arr[0]
        smallest_index = 0

        for i in range(1, len(arr)):
            if smallest < arr[i]:
                smallest = arr[i]
                smallest_index = i

        return smallest_index

    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        new_list = None
        current = head

        while current is not None:
            next_node = current.next
            current.next = new_list
            new_list = current
            current = next_node

        return new_list